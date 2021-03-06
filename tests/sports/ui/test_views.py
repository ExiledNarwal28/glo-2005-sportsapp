from app.sports.ui.views import SportView
from tests.interfaces.ui.test_views import ViewTests
from tests.recommendations.mocks import recommendation_service
from tests.sports.fakes import sport1, sport3, sport2
from tests.sports.mocks import sport_repository


class SportsViewsTests(ViewTests):

    def test_construct_should_inject_repository(self):
        view = SportView(sport_repository, recommendation_service)
        self.assertEqual(sport_repository, view.sport_repository)

    def test_construct_should_inject_recommendation_service(self):
        view = SportView(sport_repository, recommendation_service)
        self.assertEqual(recommendation_service, view.recommendation_service)

    def get_path(self):
        return '/sports'

    def get_view_title(self):
        return 'Sports'

    def test_sports_with_no_sport_should_display_no_sport(self):
        self.remove_sports()
        response = self.request_get()
        self.assert_page_is_found(response)
        self.assert_items_are_not_listed(response, [sport1.name, sport2.name, sport3.name])

    def test_sports_with_sports_should_display_sports(self):
        response = self.request_get()
        self.assert_page_is_found(response)
        self.assert_items_are_listed(response, [sport1.name, sport2.name, sport3.name])

    def test_sports_with_form_should_display_filtered_sports(self):
        response = self.request_post()
        self.assert_page_is_found(response)
        self.assert_items_are_listed(response, [sport1.name])
        self.assert_items_are_not_listed(response, [sport2.name, sport3.name])

    def test_sport_details_should_display_sport_details(self):
        self.assert_item_details_are_displayed([
            (sport1.id, self.get_sport_details(sport1)),
            (sport2.id, self.get_sport_details(sport2)),
            (sport3.id, self.get_sport_details(sport3)),
        ])

    def test_sport_details__without_sport_should_respond_not_found(self):
        self.remove_sports()
        self.assert_item_details_are_not_found([(sport1.id, sport1.name)])

    def test_sport_details_should_display_recommendations(self):
        self.assert_item_details_are_displayed([
            (sport1.id, self.get_recommendations_details(sport1)),
            (sport2.id, self.get_recommendations_details(sport2)),
            (sport3.id, self.get_recommendations_details(sport3))
        ])

    def test_sport_details_with_logged_in_user_should_display_add_recommendation_button(self):
        self.logged_in_session()
        response = self.request_get(sport1.id)
        self.assert_page_is_found(response)
        self.assert_items_are_listed(response, ['#addRecommendation'])

    def test_sport_details_with_logged_out_user_should_not_display_add_recommendation_button(self):
        self.logged_out_session()
        response = self.request_get(sport1.id)
        self.assert_page_is_found(response)
        self.assert_items_are_not_listed(response, ['#addRecommendation'])

    def test_sport_details_with_invalid_form_should_flash_error(self):
        self.logged_in_session()
        form = {'note': -1, 'comment': ''}
        response = self.request_post(sport1.id, form)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error adding recommendation.', response.data)

    def test_sport_details_with_valid_form_should_add_recommendation(self):
        self.logged_in_session()
        form = {'note': 3, 'comment': 'This is my comment!'}
        response = self.request_post(sport1.id, form)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(recommendation_service.add_to_sport.called)

    def get_sport_details(self, sport):
        return [sport.name] + \
               self.list_detail_list_names(sport.climates) + \
               self.list_detail_list_names(sport.required_equipment_types)

    @staticmethod
    def get_recommendations_details(sport):
        details = []
        for recommendation in sport.recommendations:
            details += [recommendation.username]
        return details
