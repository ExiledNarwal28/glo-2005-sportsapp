from app.practice_centers.ui.views import PracticeCenterView
from tests.interfaces.ui.test_views import ViewTests
from tests.practice_centers.fakes import center1, center2, center3
from tests.practice_centers.mocks import practice_center_repository


class PracticeCentersViewTests(ViewTests):

    def test_construct_should_inject_repository(self):
        view = PracticeCenterView(practice_center_repository)
        self.assertEqual(practice_center_repository, view.practice_center_repository)

    def get_path(self):
        return '/practice-centers'

    def get_view_title(self):
        return 'Practice Centers'

    def test_practice_centers_with_no_practice_center_should_display_no_practice_center(self):
        self.remove_practice_centers()
        response = self.request_get()
        self.assert_page_is_found(response)
        self.assert_items_are_not_listed(response, [center1.name, center2.name, center3.name])

    def test_practice_centers_with_practice_centers_should_display_practice_centers(self):
        response = self.request_get()
        self.assert_page_is_found(response)
        self.assert_items_are_listed(response, [center1.name, center2.name, center3.name])

    # TODO : Test average note

    def test_practice_centers_with_form_should_display_filtered_practice_centers(self):
        response = self.request_post()
        self.assert_page_is_found(response)
        self.assert_items_are_listed(response, [center1.name])
        self.assert_items_are_not_listed(response, [center2.name, center3.name])

    def test_practice_center_details_should_display_practice_center_details(self):
        self.assert_item_details_are_displayed([
            (center1.id, self.get_center_details(center1)),
            (center2.id, self.get_center_details(center2)),
            (center3.id, self.get_center_details(center3))
        ])

    def test_practice_center_details__without_practice_center_should_respond_not_found(self):
        self.remove_practice_centers()
        self.assert_item_details_are_not_found([(center1.id, center1.name)])

    def test_practice_center_details_should_display_recommendations(self):
        self.assert_item_details_are_displayed([
            (center1.id, self.get_recommendations_details(center1)),
            (center2.id, self.get_recommendations_details(center2)),
            (center3.id, self.get_recommendations_details(center3))
        ])

    def get_center_details(self, center):
        return [center.name, center.email, center.phone_number] + \
               self.list_detail_list_names(center.climates)

    @staticmethod
    def get_recommendations_details(center):
        details = []
        for recommendation in center.recommendations:
            details += [recommendation.username]
        return details
