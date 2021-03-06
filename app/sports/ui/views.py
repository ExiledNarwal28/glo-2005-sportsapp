from abc import abstractmethod, ABCMeta

from flask import render_template, request, Blueprint, session, flash, redirect, url_for
from flask.views import View
from flask_paginate import Pagination, get_page_args
from injector import inject

from app.recommendations.forms import AddRecommendationForm
from app.recommendations.services import RecommendationService
from app.sports.exceptions import SportNotFoundException
from app.sports.forms import SportSearchForm
from app.sports.repositories import SportRepository

sport_blueprint = Blueprint('sports', __name__)


@sport_blueprint.route('/sports', methods=('GET', 'POST'))
def sports(sport_repository: SportRepository):
    form = SportSearchForm(request.form)
    request_form = form if request.method == 'POST' and form.validate_on_submit() else None

    page, per_page, offset = get_page_args()
    total = sport_repository.get_count(request_form)
    paged_sports = sport_repository.get_all(request_form, offset, per_page)

    pagination = Pagination(page=page, per_page=per_page, total=total, record_name='sports',
                            format_total=True, format_number=True)
    return render_template('sports.html', sports=paged_sports, page=page, per_page=per_page,
                           pagination=pagination, form=form)


@sport_blueprint.route('/sports/<sport_id>', methods=('GET', 'POST'))
def sport_details(sport_repository: SportRepository,
                  recommendation_service: RecommendationService, sport_id):
    try:
        sport = sport_repository.get(sport_id)
    except ValueError:
        return not_found()
    except SportNotFoundException:
        return not_found()

    form = AddRecommendationForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            recommendation_service.add_to_sport(session['_user_id'], sport, form)
            return redirect(url_for('sports.sport_details', sport_id=sport_id), 302)

        flash('Error adding recommendation.', 'error')

    return render_template('sport_details.html', sport=sport, form=form)


def not_found():
    flash('Sport not found', 'error')
    return redirect(url_for('sports.sports'), 303)


class SportView(View):
    __metaclass__ = ABCMeta

    @abstractmethod
    def dispatch_request(self):
        """ abstract method """

    @inject
    def __init__(self, sport_repository: SportRepository,
                 recommendation_service: RecommendationService):
        self.sport_repository = sport_repository
        self.recommendation_service = recommendation_service
