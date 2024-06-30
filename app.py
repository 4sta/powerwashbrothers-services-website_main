import logging
import os
from flask import Flask, render_template, jsonify, abort, request, redirect, url_for
from database import get_services_db, get_service_db, save_order_to_db, get_reviews
from flask_mail import Mail, Message
from dotenv import load_dotenv
from email_templates import admin_email_template, user_email_template
from logging_config import setup_logging

# Configuring logging
setup_logging()
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Gain access to .env file
load_dotenv()

# Config settings for Flask-Mail
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)

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
    logger.info("Rendering homepage with services")
    return render_template('homepage.html', services=services)

@app.route("/about")
def about_us():
    logger.info("Rendering About Us page")
    return render_template('about.html')

@app.route("/faqs")
def faqs():
    logger.info("Rendering FAQs page")
    return render_template('faqs.html')

@app.route("/reviews")
def reviews():
    reviews = get_reviews()
    logger.info("Rendering Reviews page")
    return render_template('reviews.html', reviews=reviews)

@app.route("/api/services")
def list_services():
    services = get_services_db()
    logger.info("Listing services through API")
    return jsonify(services)

@app.route("/service/<int:service_id>")
def service_detail(service_id):
    service = get_service_db(service_id)
    if service:
        logger.info(f"Rendering details for service ID: {service_id}")
        return render_template('service_details.html', service=service)
    else:
        logger.warning(f"Service ID: {service_id} not found")
        abort(404)

@app.route("/service/<int:service_id>/order", methods=["POST"])
def order_service(service_id):
    order_data = request.form.to_dict()
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
    logger.info("Rendering order success page")
    return render_template('order_success.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
