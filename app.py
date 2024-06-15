from flask import Flask, render_template   #from moduel importing Flask class

app = Flask(__name__)  #creating Flusk App


@app.route("/")   
def power_wash():
  return render_template('homepage.html')


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)  #debug= True to update changes live
