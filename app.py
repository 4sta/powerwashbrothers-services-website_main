from flask import Flask, render_template, jsonify, abort
from database import get_services_db, get_service_db

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


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
