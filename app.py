from flask import Flask



app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Server running on port 5000"



if __name__ == '__main__':
    app.run(debug=True,port=5000)