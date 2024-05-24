from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import login_required, current_user

from BigfootSightings.forms import AddSightingForm, SearchSightingForm, BackToMainForm
from BigfootSightings.models import Sighting
from BigfootSightings.queries import insert_sighting, get_all_sightings, search_sightings

Sightings = Blueprint('Sighting', __name__)


@Sightings.route("/backToMainFromAdd", methods=['GET', 'POST'])
def backToMainFromAdd():
    form = BackToMainForm()
    if request.method == 'POST':
            if form.validate_on_submit():
                return redirect(url_for('Login.home'))

    return render_template('pages/add-sighting-landing.html', form=form)



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

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Sighting.backToMainFromAdd'))

    return render_template('pages/add-sighting.html', form=form)

@Sightings.route("/all-sightings", methods=['GET', 'POST'])
def all_sightings():

    form = SearchSightingForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            sightings = search_sightings(form.search_text.data)
    
    else: sightings = get_all_sightings()

    return render_template(
        'pages/all-sightings.html',
        sightings=sightings,
        form = form)

