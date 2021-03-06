from app.shops.ui.views import ShopView
from tests.interfaces.ui.test_views import ViewTests
from tests.shops.fakes import shop1, shop2, shop3
from tests.shops.mocks import shop_repository


class ShopsViewTests(ViewTests):

    def test_construct_should_inject_repository(self):
        view = ShopView(shop_repository)
        self.assertEqual(shop_repository, view.shop_repository)

    def get_path(self):
        return '/shops'

    def get_view_title(self):
        return 'Shops'

    def test_shops_with_no_shop_should_display_no_shop(self):
        self.remove_shops()
        response = self.request_get()
        self.assert_page_is_found(response)
        self.assert_items_are_not_listed(response, [shop1.name, shop2.name, shop3.name])

    def test_shops_with_shops_should_display_shops(self):
        response = self.request_get()
        self.assert_page_is_found(response)
        self.assert_items_are_listed(response, [shop1.name, shop2.name, shop3.name])

    def test_shops_with_form_should_display_filtered_shops(self):
        response = self.request_post()
        self.assert_page_is_found(response)
        self.assert_items_are_listed(response, [shop1.name])
        self.assert_items_are_not_listed(response, [shop2.name, shop3.name])

    def test_shop_details_should_display_shop_details(self):
        self.assert_item_details_are_displayed([
            (shop1.id, self.get_shop_details(shop1)),
            (shop2.id, self.get_shop_details(shop2)),
            (shop3.id, self.get_shop_details(shop3))
        ])

    def test_shop_details__without_shop_should_respond_not_found(self):
        self.remove_shops()
        self.assert_item_details_are_not_found([(shop1.id, shop1.name)])

    def test_shop_details_should_display_announces(self):
        self.assert_item_details_are_displayed([
            (shop1.id, self.get_announces_details(shop1)),
            (shop2.id, self.get_announces_details(shop2)),
            (shop3.id, self.get_announces_details(shop3))
        ])

    @staticmethod
    def get_shop_details(shop):
        return [shop.name, shop.email, shop.phone_number]

    @staticmethod
    def get_announces_details(shop):
        details = []
        for announce in shop.announces:
            details += [announce.equipment_name, announce.state]
        return details
