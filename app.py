import requests
import logging
import os
from flask import Flask, render_template, jsonify, abort, request, redirect, url_for
from database import get_services_db, get_service_db, save_order_to_db, get_reviews
from flask_mail import Mail, Message
from dotenv import load_dotenv
from email_templates import admin_email_template, user_email_template
from logging_config import setup_logging
from validation import validate_order_form  

# Configuring logging
setup_logging()
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Gain access to .env file
load_dotenv()

# Checking environment variables
project_id = os.environ.get('GCP_PROJECT_ID')
recaptcha_site_key = os.environ.get('RECAPTCHA_SITE_KEY')
recaptcha_secret_key = os.environ.get('RECAPTCHA_SECRET_KEY')

if not project_id:
    raise ValueError("GCP_PROJECT_ID environment variable is not set")
if not recaptcha_site_key:
    raise ValueError("RECAPTCHA_SITE_KEY environment variable is not set")
if not recaptcha_secret_key:
    raise ValueError("RECAPTCHA_SECRET_KEY environment variable is not set")

# Config settings for Flask-Mail
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)

def verify_recaptcha(token):
    secret_key = os.environ.get('RECAPTCHA_SECRET_KEY')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    params = {
        'secret': secret_key,
        'response': token
    }
    response = requests.post(url, data=params)
    result = response.json()
    return result.get('success', False)

def send_email(to, subject, template):
    try:
        msg = Message(
            subject,
            recipients=[to],
            html=template,
            sender=app.config['MAIL_DEFAULT_SENDER']
        )
        mail.send(msg)
        logger.info(f"Email sent to {to} with subject '{subject}'")
    except Exception as e:
        logger.error(f"Failed to send email to {to} with subject '{subject}'. Error: {e}")

@app.route("/")
def power_wash():
    services = get_services_db()
    recaptcha_site_key = os.environ.get('RECAPTCHA_SITE_KEY')
    logger.info("Rendering homepage with services")
    return render_template('homepage.html', services=services, recaptcha_site_key=recaptcha_site_key)

@app.route("/about")
def about_us():
    recaptcha_site_key = os.environ.get('RECAPTCHA_SITE_KEY')
    logger.info("Rendering About Us page")
    return render_template('about.html', recaptcha_site_key=recaptcha_site_key)

@app.route("/faqs")
def faqs():
    recaptcha_site_key = os.environ.get('RECAPTCHA_SITE_KEY')
    logger.info("Rendering FAQs page")
    return render_template('faqs.html', recaptcha_site_key=recaptcha_site_key)

@app.route("/reviews")
def reviews():
    recaptcha_site_key = os.environ.get('RECAPTCHA_SITE_KEY')
    reviews = get_reviews()
    logger.info("Rendering Reviews page")
    return render_template('reviews.html', reviews=reviews, recaptcha_site_key=recaptcha_site_key)

@app.route("/api/services")
def list_services():
    services = get_services_db()
    logger.info("Listing services through API")
    return jsonify(services)

@app.route("/service/<int:service_id>")
def service_detail(service_id):
    recaptcha_site_key = os.environ.get('RECAPTCHA_SITE_KEY')
    service = get_service_db(service_id)
    if service:
        logger.info(f"Rendering details for service ID: {service_id}")
        return render_template('service_details.html', service=service, recaptcha_site_key=recaptcha_site_key)
    else:
        logger.warning(f"Service ID: {service_id} not found")
        abort(404)

@app.route("/service/<int:service_id>/order", methods=["POST"])
def order_service(service_id):
    token = request.form.get('g-recaptcha-response')
    if not token:
        abort(400, description="reCAPTCHA token is missing. Please try again.")

    if not verify_recaptcha(token):
        abort(400, description="Invalid reCAPTCHA. Please try again.")

    order_data = request.form.to_dict()

    is_valid, error_message = validate_order_form(order_data)  # Validate order form data
    if not is_valid:
        abort(400, description=error_message)

    save_order_to_db(order_data['fullName'], order_data['email'],
                     order_data.get('tel'), order_data['serviceType'],
                     order_data['workObjectDetails'], order_data.get('remark'))

    # Sending email to admin
    send_email(os.environ.get('ADMIN_EMAIL'), 'New Order Received', admin_email_template(order_data))

    # Sending submit approval email to customer
    send_email(order_data['email'], 'Order Confirmation', user_email_template(order_data))

    logger.info(f"Order received and emails sent for service ID: {service_id}")
    return redirect(url_for('order_success'))

@app.route("/order_success")
def order_success():
    recaptcha_site_key = os.environ.get('RECAPTCHA_SITE_KEY')
    logger.info("Rendering order success page")
    return render_template('order_success.html', recaptcha_site_key=recaptcha_site_key)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
