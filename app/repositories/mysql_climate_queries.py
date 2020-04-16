from app.repositories.mysql_filters import MySQLFilter
from app.repositories.mysql_queries import MySQLQuery
from app.repositories.mysql_tables import MySQLClimatesTable, MySQLSportClimatesTable, \
    MySQLPracticeCenterClimatesTable


class MySQLClimatesQuery(MySQLQuery):
    fake_name_col = 'name'

    def get_all_for_sport(self, sport_id):
        return self.get_all_for_type(sport_id,
                                     MySQLSportClimatesTable.sport_id_col,
                                     MySQLSportClimatesTable.climate_name_col,
                                     MySQLSportClimatesTable.table_name)

    def get_all_for_practice_center(self, practice_center_id):
        return self.get_all_for_type(practice_center_id,
                                     MySQLPracticeCenterClimatesTable.practice_center_id_col,
                                     MySQLPracticeCenterClimatesTable.climate_name_col,
                                     MySQLPracticeCenterClimatesTable.table_name)

    def get_all_for_type(self, type_id, type_id_col, climate_name_col, table_name):
        operation = (f'SELECT {climate_name_col} AS {self.fake_name_col}'
                     f' FROM {table_name}')

        filters = [MySQLFilter.filter_equal(type_id_col, type_id)]

        orders = [climate_name_col]

        return self.build_query(operation, filters, orders)

    def add(self):
        operation = (f'INSERT INTO {MySQLClimatesTable.table_name}'
                     f' ({MySQLClimatesTable.name_col})'
                     f' VALUES (%s)')

        return self.build_query(operation)

    def add_for_sport(self):
        return self.add_for_type(MySQLSportClimatesTable.table_name,
                                 MySQLSportClimatesTable.climate_name_col,
                                 MySQLSportClimatesTable.sport_id_col)

    def add_for_practice_center(self):
        return self.add_for_type(MySQLPracticeCenterClimatesTable.table_name,
                                 MySQLPracticeCenterClimatesTable.climate_name_col,
                                 MySQLPracticeCenterClimatesTable.practice_center_id_col)

    def add_for_type(self, table_name, climate_name_col, type_id_col):
        operation = (f'INSERT INTO {table_name}'
                     f' ({climate_name_col}'
                     f', {type_id_col})'
                     f' VALUES (%s, %s);')

        return self.build_query(operation)
