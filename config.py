import os
from flask import Flask, render_template
from dotenv import load_dotenv

from src.routes import user, projects, group, donation

# Load the environment variables from the .env file
load_dotenv()


def create_app():
    # Create the flask app
    # search for templates and static in the templates folder
    app = Flask(__name__, template_folder='./public/templates',
                static_folder='./public/static')

    # Set up the app configuration

    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', default='dev'),
        DATABASE_HOST=os.getenv('DATABASE_HOST'),
        DATABASE_PASSWORD=os.getenv('DATABASE_PASSWORD'),
        DATABASE_USER=os.getenv('DATABASE_USER'),
        DATABASE_PORT=os.getenv('DATABASE_PORT'),
        DATABASE_NAME=os.getenv('DATABASE_NAME'),
        DATABASE_DSN=os.getenv('DATABASE_DSN'),
        DATABASE_URL=os.getenv('DATABASE_URL'),
    )
    # Create the database object
    from src.db.database import init_app

    init_app(app)

    # Register the blueprints
    app.register_blueprint(user.bp)
    app.register_blueprint(projects.bp)
    app.register_blueprint(group.bp)
    app.register_blueprint(donation.bp)

    # app / route

    @app.route('/')
    def index():
        # use template
        return render_template('index.html', title='Home', message='Hello World!')

    # 404 error handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template(
            'notFindPage.html',
            title='404 CrowdFunding',
            message='Page not found'
        ), 404

    return app
