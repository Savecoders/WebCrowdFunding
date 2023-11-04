from flask import Blueprint, request, render_template, url_for, session

# Create the projects blueprint
bp = Blueprint('projects', __name__, url_prefix='/projects')

# create a route for the projects blueprint


@bp.route('/', methods=['GET'])
def index():
    return 'show all projects'


@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        return 'Create project'
    return render_template('projects/create.html')
