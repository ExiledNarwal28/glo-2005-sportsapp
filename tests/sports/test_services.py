from instance.sports.services import SportPopulationService
from tests.equipment_types.mocks import equipment_type_repository
from tests.sports.mocks import sport_repository
from tests.interfaces.test_basic import BasicTests


class SportPopulationServiceTests(BasicTests):

    def setUp(self):
        self.sport_population_service = SportPopulationService(sport_repository,
                                                               equipment_type_repository)

    def test_db_populate_adds_fakes(self):
        self.sport_population_service.db_populate()
        self.assertTrue(sport_repository.add.called)
