from flask import render_template, request
from flask.views import View
from injector import inject

from app import sports_blueprint
from app.sports.exceptions import SportNotFoundException
from app.sports.forms import SportsSearchForm
from app.sports.repositories import SportsRepository


@sports_blueprint.route('/sports', methods=('GET', 'POST'))
def sports(sports_repository: SportsRepository):
    form = SportsSearchForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        all_sports = sports_repository.get_all(form)
    else:
        all_sports = sports_repository.get_all(None)

    return render_template('sports.html', sports=all_sports, form=form)


@sports_blueprint.route('/sports/<sport_id>')
def sport_details(sports_repository: SportsRepository, sport_id):
    try:
        sport = sports_repository.get(sport_id)
    except SportNotFoundException:
        return render_template('404.html'), 404

    return render_template('sport_details.html', sport=sport)


class SportView(View):
    def dispatch_request(self):
        pass

    @inject
    def __init__(self, sports_repository: SportsRepository):
        self.sports_repository = sports_repository
