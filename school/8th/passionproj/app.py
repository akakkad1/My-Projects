from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/batteries")
def batteries():
    return render_template("batteries.html")

@app.route("/electronics")
def electronics():
    return render_template("electronics.html")

@app.route("/plastics")
def plastics():
    return render_template("plastics.html")

@app.route("/chemicals")
def chemicals():
    return render_template("chemicals.html")

if __name__ == "__main__":
    app.run(debug=True)
