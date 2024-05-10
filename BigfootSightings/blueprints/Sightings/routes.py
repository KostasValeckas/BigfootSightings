from flask import render_template, request, Blueprint
from flask_login import login_required, current_user

from BigfootSightings.forms import AddSightingForm
from BigfootSightings.models import Sighting
from BigfootSightings.queries import insert_sighting, get_all_sightings

Sightings = Blueprint('Sighting', __name__)



@Sightings.route("/add-sighting", methods=['GET', 'POST'])

#@login_required
def add_sighting():
    form = AddSightingForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            sighting_data = dict(
                title=form.title.data,
                latitude=form.latitude.data,
                longitude=form.longitude.data
            )
            sighting = Sighting(sighting_data)
            insert_sighting(sighting)
    return render_template('pages/add-sighting.html', form=form)

@Sightings.route("/all-sightings")
def all_sightings():
    
    sightings = get_all_sightings()

    return render_template('pages/all-sightings.html', sightings=sightings)

