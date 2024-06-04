from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import login_required, current_user

from BigfootSightings.forms import AddSightingForm, SearchSightingForm, BackToMainForm
from BigfootSightings.models import Sighting
from BigfootSightings.queries import (
    insert_sighting,
    get_all_sightings,
    search_sightings,
    show_timezone,
)

Sightings = Blueprint("Sighting", __name__)


@Sightings.route("/backToMainFromAdd", methods=["GET", "POST"])
def backToMainFromAdd():
    form = BackToMainForm()
    if request.method == "POST":
        if form.validate_on_submit():
            return redirect(url_for("Login.login"))  # Change endpoint to 'Login.login'

    return render_template("pages/add-sighting-landing.html", form=form)


@Sightings.route("/add-sighting", methods=["GET", "POST"])
@login_required
def add_sighting():
    form = AddSightingForm()
    if request.method == "POST":
        if form.validate_on_submit():

            sighting_data = {}
            sighting_data["title"] = form.title.data
            sighting_data["latitude"] = form.latitude.data
            sighting_data["longitude"] = form.longitude.data

            username = current_user.username

            insert_sighting(username, sighting_data)

            next_page = request.args.get("next")
            return (
                redirect(next_page)
                if next_page
                else redirect(url_for("Sighting.backToMainFromAdd"))
            )

    return render_template("pages/add-sighting.html", form=form)


@Sightings.route("/all-sightings", methods=["GET", "POST"])
def all_sightings():

    timezone = show_timezone()
    form = SearchSightingForm()

    if request.method == "POST":

        if form.validate_on_submit():
            if form.reset.data:
                sightings = get_all_sightings()
                return render_template(
                    "pages/all-sightings.html",
                    sightings=sightings,
                    form=form,
                    timezone=timezone,
                )

            sightings = search_sightings(
                search_text=form.search_text.data,
                username=form.username.data,
                lat=form.lat.data,
                long=form.long.data,
                location_id=form.location_id.data,
                time=form.date.data,
                country=form.country.data,
                state=form.state.data,
                city=form.city.data,
            )
    else:
        sightings = get_all_sightings()
    return render_template(
        "pages/all-sightings.html", sightings=sightings, form=form, timezone=timezone
    )
