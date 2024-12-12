# Database: src/db/__init__.py
from src.db.database import DataBase, get_db, close_db

# flask imports
from flask import (Blueprint, flash, g, render_template,
                   request, url_for, jsonify,
                   session, redirect
                   )


# date time
import datetime

# login_required
from .user import login_required

from src.models import Donacion
from src.schema import DonacionDao

# Create the donation blueprint
bp = Blueprint('donation', __name__, url_prefix='/donation')

# create a route for the donation blueprint


@bp.route('/', methods=['GET'])
def index():

    # database connection
    database = DataBase()

    # project dao
    donacion_dao = DonacionDao(database.connection, database.cursor)

    # get all donation

    donations = []

    donations = donacion_dao.get_all_donations()

    return render_template('donation/index.html', donaciones=donations)


@bp.route('/register/<string:project_id>', methods=['POST'])
@login_required
def register(project_id):
    if request.method == 'POST':

        try:

            # validate form

            donacion = Donacion()

            donacion.monto = request.form['amount']

            date = datetime.date.today()

            donacion.fecha_donacion = date.strftime("%d-%m-%Y")

            donacion.id_usuario = g.user.id_usuario

            donacion.id_proyecto = project_id

            donacion.generateHashId()

            # database connection

            database = DataBase()

            # donacion dao

            donacion_dao = DonacionDao(database.connection, database.cursor)

            # insert donacion

            donacion_dao.insert(donacion)

            database.close()

            flash("Donacion registrada correctamente", "success")

        except ValueError as error:
            flash(str(error), "error")

        except Exception as error:
            flash(str(error), "error")

    return redirect(url_for('projects.view', id=project_id))
