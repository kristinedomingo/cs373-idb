from flask import Flask
app = Flask(__name__, static_url_path='')

@app.route('/')
def splash():
    return app.send_static_file('template1.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')