from flask import Flask

app = Flask(__name__)

@app.route('/app/<variable>')
def hello(variable):
    return f"Hello {variable}!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
