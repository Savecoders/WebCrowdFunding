from flask import Blueprint, request, render_template, url_for, session

# Create the donation blueprint
bp = Blueprint('donation', __name__, url_prefix='/donation')

# create a route for the donation blueprint


@bp.route('/', methods=['GET'])
def index():
    return 'show all donation in projects'


@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        return 'Create donation'
    return render_template('donation/create.html')
