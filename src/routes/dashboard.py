from flask import Blueprint, request, render_template, url_for, session
# Create the projects blueprint
bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# create a route for the projects blueprint


@bp.route('/', methods=['GET'])
def index():
    return 'Show info acount'
