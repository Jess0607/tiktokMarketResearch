# Importing the necessary modules and libraries
from flask import Flask
from flask_migrate import Migrate
from routes.mainblueprint import blueprint as blueprint
from routes.homepageblueprint import blueprint as homepage_blueprint
from routes.dashboardblueprint import blueprint as dashboard_blueprint
from models.mysqlmodel import db


def create_app():
    app = Flask(__name__)  # flask app object
    app.config.from_object('config')  # Configuring from Python Files

    db.init_app(app)  # Initializing the database
    return app


app = create_app()  # Creating the app
# Registering the blueprint
app.register_blueprint(homepage_blueprint, url_prefix='/', name='homepage')
app.register_blueprint(blueprint, url_prefix='/looker')
app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard', name='dashboard')

migrate = Migrate(app, db)  # Initializing the migration


if __name__ == '__main__':  # Running the app
    app.run(host='127.0.0.1', port=5000, debug=True)