from flask import Flask

app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:8080'


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/api/v1/hello-world-8')
def variant():
    return 'Hello, World! {8}'


if __name__ == '__main__':
    from waitress import serve

    serve(app, host="0.0.0.0", port=8080)
    # app.run(debug=True)                   #for debugging
