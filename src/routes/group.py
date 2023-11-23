from flask import Blueprint, request, render_template, url_for, session

# Create the group blueprint
bp = Blueprint('group', __name__, url_prefix='/group')

# create a route for the group blueprint


@bp.route('/', methods=['GET'])
def index():
    return 'show all groups'


@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        return 'Create group'
    return render_template('group/create.html')
