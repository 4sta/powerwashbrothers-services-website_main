from flask import Flask  #from moduel importing Flask class

app = Flask(__name__)  #creating a Flusk App


@app.route("/")   
def power_wash():
  return "Power Wash Website."


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)  #debug to update changes
