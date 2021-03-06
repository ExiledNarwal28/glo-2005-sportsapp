from instance.climates.services import ClimatePopulationService
from tests.climates.mocks import climate_repository
from tests.interfaces.test_basic import BasicTests


class ClimatePopulationServiceTests(BasicTests):

    def setUp(self):
        self.climate_population_service = ClimatePopulationService(climate_repository)

    def test_db_populate_adds_fakes(self):
        self.climate_population_service.db_populate()
        self.assertTrue(climate_repository.add.called)
