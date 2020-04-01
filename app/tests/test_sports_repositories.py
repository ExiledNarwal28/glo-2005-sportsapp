from app.repositories.mysql_sport_repositories import MySQLSportsRepository
from app.sports.exceptions import SportNotFoundException
from app.tests.fakes import sport1, sport2, sport3
from app.tests.forms import FakeSportsForm
from app.tests.mocks import climates_repository, recommendations_repository
from app.tests.test_basic_repositories import BasicRepositoryTests


def get_climates_for_sport(sport_id):
    return get_sport(sport_id).climates


def get_recommendations_for_sport(sport_id):
    return get_sport(sport_id).recommendations


def get_sport(sport_id):
    if sport_id == sport1.id:
        return sport1
    if sport_id == sport2.id:
        return sport2
    if sport_id == sport3.id:
        return sport3


class SportsRepositoryTests(BasicRepositoryTests):

    def setUp(self):
        super().setUp()
        climates_repository.get_all_for_sport.side_effect = get_climates_for_sport
        recommendations_repository.get_all_for_sport.side_effect = get_recommendations_for_sport
        self.repository = MySQLSportsRepository(climates_repository, recommendations_repository)

    def test_get_with_no_sport_should_raise_sport_not_found_exception(self):
        self.reset_repositories()
        self.assertRaises(SportNotFoundException, self.repository.get, 1)

    def test_get_with_non_existent_sport_should_raise_sport_not_found_exception(self):
        self.assertRaises(SportNotFoundException, self.repository.get, -1)

    def test_get_should_get_sport(self):
        sport = self.repository.get(sport1.id)
        self.assertEqual(sport1, sport)
        sport = self.repository.get(sport2.id)
        self.assertEqual(sport2, sport)
        sport = self.repository.get(sport3.id)
        self.assertEqual(sport3, sport)

    def test_get_should_get_sport_climates(self):
        sport = self.repository.get(sport1.id)
        self.assertCountEqual(sport1.climates, sport.climates)
        sport = self.repository.get(sport2.id)
        self.assertCountEqual(sport2.climates, sport.climates)
        sport = self.repository.get(sport3.id)
        self.assertCountEqual(sport3.climates, sport.climates)

    def test_get_should_get_sport_recommendations(self):
        sport = self.repository.get(sport1.id)
        self.assertCountEqual(sport1.recommendations, sport.recommendations)
        sport = self.repository.get(sport2.id)
        self.assertCountEqual(sport2.recommendations, sport.recommendations)
        sport = self.repository.get(sport3.id)
        self.assertCountEqual(sport3.recommendations, sport.recommendations)

    def test_get_all_with_no_sport_get_no_sport(self):
        self.reset_repositories()
        sports = self.repository.get_all()
        self.assertEqual(0, len(sports))

    def test_get_all_get_sports(self):
        sports = self.repository.get_all()
        self.assertIn(sport1, sports)
        self.assertIn(sport2, sports)
        self.assertIn(sport3, sports)

    def test_get_all_with_name_filter_sports(self):
        form = FakeSportsForm(sport1.name)
        sports = self.repository.get_all(form)
        self.assertIn(sport1, sports)
        self.assertNotIn(sport2, sports)
        self.assertNotIn(sport3, sports)
