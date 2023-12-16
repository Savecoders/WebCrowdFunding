from flask import Blueprint, request, render_template, url_for, session

# login_required
from .user import login_required

from src.models import Proyecto

from src.schema import ProyectoDao
from src.models import GruposColaboradores
from src.schema import GruposColaboradoresDao
# Create the projects blueprint
bp = Blueprint('projects', __name__, url_prefix='/projects')

# create a route for the projects blueprint


@bp.route('/', methods=['GET'])
def index():
    return 'show all projects'


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        proyecto = Proyecto()
        proyecto.nombre = request.form["nameProject"]
        grupo = request.form["nameGroup"]
        proyecto.idea = request.form["ideaProject"]
        proyecto.presentacion = request.form["image_present"]

        return 'Create project'
    return render_template('projects/create.html')
