from flask import Flask
app = Flask(__name__, static_url_path='')

@app.route('/')
def splash():
    return app.send_static_file('index.html')

@app.route('/about')
def about():
    return app.send_static_file('about.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')