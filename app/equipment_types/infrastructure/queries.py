from app.equipment_types.infrastructure.tables import MySQLEquipmentTypeTable as EquipmentTypes, \
    MySQLSportEquipmentTypeTable as SportEquipmentTypes
from app.interfaces.infrastructure.filters import MySQLFilter
from app.interfaces.infrastructure.queries import MySQLQuery


# TODO : Test
class MySQLEquipmentTypeQuery(MySQLQuery):
    def add(self):
        operation = (f'INSERT INTO {EquipmentTypes.table_name}'
                     f'({EquipmentTypes.name_col}) VALUES (%s)')

        return self.build_query(operation)

    def get_all_for_sport(self, sport_id):
        operation = (f'SELECT E.{EquipmentTypes.id_col}, E.{EquipmentTypes.name_col} '
                     f'FROM {EquipmentTypes.table_name} E '
                     f'JOIN {SportEquipmentTypes.table_name} S ON '
                     f'S.{SportEquipmentTypes.equipment_id_col} = E.{EquipmentTypes.id_col}')

        filters = [MySQLFilter.filter_equal(SportEquipmentTypes.sport_id_col, sport_id)]

        orders = [f'E.{EquipmentTypes.name_col}']

        return self.build_query(operation, filters, orders)
