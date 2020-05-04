from injector import inject

from app.climates.repositories import ClimateRepository
from app.equipment_types.repositories import EquipmentTypeRepository
from app.interfaces.database import Database
from app.recommendations.repositories import RecommendationRepository
from app.sports.exceptions import SportNotFoundException
from app.sports.infrastructure.queries import MySQLSportQuery as Query, select_average_note
from app.sports.infrastructure.tables import MySQLSportTable as Sports
from app.sports.models import Sport
from app.sports.repositories import SportRepository


class MySQLSportRepository(SportRepository):
    @inject
    def __init__(self, database: Database, climate_repository: ClimateRepository,
                 equipment_type_repository: EquipmentTypeRepository,
                 recommendation_repository: RecommendationRepository):
        self.database = database
        self.climate_repository = climate_repository
        self.equipment_type_repository = equipment_type_repository
        self.recommendations_repository = recommendation_repository

    def get_all(self, form=None):
        query = Query().get_all(form)
        return self.get_all_for_query(query)

    def get_all_for_equipment_type(self, type_id):
        query = Query().get_all_for_equipment_type(type_id)
        return self.get_all_for_query(query)

    def get_all_for_query(self, query):
        sports = []

        try:
            with self.database.connect().cursor() as cur:
                cur.execute(query)

                for sport_cur in cur.fetchall():
                    average_note = self.get_average_note(sport_cur[Sports.id_col])
                    sport = self.build_sport(sport_cur, average_note=average_note)
                    sports.append(sport)
        finally:
            cur.close()

        return sports

    def get(self, sport_id):
        sport = None

        try:
            with self.database.connect().cursor() as cur:
                query = Query().get(sport_id)
                cur.execute(query)

                for sport_cur in cur.fetchall():
                    climates = self.climate_repository.get_all_for_sport(sport_id)
                    required_equipment_types = self.equipment_type_repository.\
                        get_all_for_sport(sport_id)
                    recommendations = self.recommendations_repository.get_all_for_sport(sport_id)
                    average_note = self.get_average_note(sport_id)
                    sport = self.build_sport(sport_cur, climates, required_equipment_types,
                                             recommendations, average_note)
        finally:
            cur.close()

        if sport is None:
            raise SportNotFoundException

        return sport

    def get_average_note(self, sport_id):
        try:
            with self.database.connect().cursor() as cur:
                query = select_average_note(sport_id)
                cur.execute(query)

                for note_cur in cur.fetchall():
                    return note_cur[Query.fake_average_note_col]
        finally:
            cur.close()

        return 0

    @staticmethod
    def build_sport(cur, climates=None, required_equipment_types=None, recommendations=None,
                    average_note=None):
        return Sport(cur[Sports.id_col],
                     cur[Sports.name_col],
                     climates,
                     required_equipment_types,
                     recommendations,
                     average_note)

    def add(self, sport):
        try:
            with self.database.connect().cursor() as cur:
                query = Query().add()
                cur.execute(query, sport.name)

                self.database.connect().commit()

                sport.id = cur.lastrowid

                for climate in sport.climates:
                    self.climate_repository.add_to_sport(climate, sport)

                for equipment_type in sport.required_equipment_types:
                    self.equipment_type_repository.add_to_sport(equipment_type, sport)
        finally:
            cur.close()
