from flask import Flask, render_template, jsonify  #from moduel importing Flask class

app = Flask(__name__)  #creating Flusk App


SERVICES = [{
    'id': 1,
    'title': 'Roof Pressure Washing',
    'description':
    ' We provide roof pressure washing services for residential and commercial properties.',
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
    ' We provide thorough cleaning for your home’s exterior walls and windows, enhancing your property’s curb appeal and maintaining its condition.',
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


@app.route("/api/services")
def list_servises():
  return jsonify(SERVICES)  #abruf der webseite in json format (json API)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)  #debug= True to update changes live
