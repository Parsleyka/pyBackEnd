from flask import Flask
from flask_jwt_extended import JWTManager

from API.config import Config

from API.EventAPI import evquery
from API.TicketAPI import tiquery
from API.UserAPI import uquery

app = Flask(__name__)
app.config.from_object(Config)
#app.config['SERVER_NAME'] = 'localhost:8080'

jwt = JWTManager(app)

app.register_blueprint(uquery)
app.register_blueprint(evquery)
app.register_blueprint(tiquery)


if __name__ == '__main__':
    app.run(debug=True)
