from flask import Flask, render_template, jsonify, abort, request, redirect, url_for
from database import get_services_db, get_service_db, save_order_to_db

app = Flask(__name__)


@app.route("/")
def power_wash():
    services = get_services_db()
    return render_template('homepage.html', services=services)


@app.route("/about")
def about_us():
    return render_template('about.html')


@app.route("/faqs")
def faqs():
    return render_template('faqs.html')


@app.route("/api/services")
def list_services():
    services = get_services_db()
    return jsonify(services)


@app.route("/service/<int:service_id>")
def service_detail(service_id):
    service = get_service_db(service_id)
    if service:
        return render_template('service_details.html', service=service)
    else:
        abort(404)


@app.route("/service/<int:service_id>/order", methods=["POST"])
def order_service(service_id):
    order_data = request.form.to_dict()
    save_order_to_db(order_data['fullName'], order_data['email'],
                     order_data.get('tel'), order_data['serviceType'],
                     order_data['workObjectDetails'], order_data.get('remark'))
    return redirect(url_for('order_success'))


@app.route("/order_success")
def order_success():
    return render_template('order_success.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
