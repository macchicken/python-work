from flask import Flask
app = Flask(__name__)

@app.route('/helloWorld')
def helloWorld():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=20000,debug=True)