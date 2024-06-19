from flask import Flask, render_template, jsonify  #from moduel importing Flask class

app = Flask(__name__)  #creating Flusk App

SERVICES = [{
    'id': 1,
    'title': 'Roof Pressure Washing',
    'description':
    ' We provide expert roof cleaning services using high-pressure washers designed for both residential and commercial properties. Our process not only rejuvenates your roof´s appearance but also prevents long-term damage by removing build-ups of moss, dirt, and debris',
    'price': ' From $250'
}, {
    'id': 2,
    'title': 'Driveway and Pathway Cleaning',
    'description':
    ' Our high-pressure cleaning effectively removes dirt, grime, and stains from your driveways and pathways, ensuring a pristine entrance to your home.',
    'price': ' From $100'
}, {
    'id': 3,
    'title': 'House Walls and Windows Cleaning',
    'description':
    ' We offer professional roof cleaning services for residential and commercial properties, effectively removing moss, dirt, and debris to enhance appearance and prevent damage.',
    'price': ' From $150'
}, {
    'id': 4,
    'title': 'Lawn Care Service',
    'description':
    ' Available only during the summer and autumn seasons, our lawn care service ensures your grass remains healthy and visually appealing, complementing our main pressure washing services.',
    'price': ' From $100'
}]


@app.route("/")
def power_wash():
    return render_template('homepage.html', services=SERVICES)


@app.route("/about")
def about_us():
    return render_template('about.html')


@app.route("/faqs")
def faqs():
    return render_template('faqs.html')


@app.route("/api/services")
def list_servises():
    return jsonify(SERVICES)  #abruf der webseite in json format (json API)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)  #debug= True to update changes live
