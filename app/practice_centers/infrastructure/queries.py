from app.interfaces.infrastructure.filters import MySQLFilter
from app.interfaces.infrastructure.queries import MySQLQuery
from app.practice_centers.infrastructure.filters import MySQLPracticeCenterFilter as Filter
from app.practice_centers.infrastructure.tables import MySQLPracticeCenterTable as PracticeCenters

all_fields_to_add = (f'{PracticeCenters.name_col}'
                     f', {PracticeCenters.email_col}'
                     f', {PracticeCenters.web_site_col}'
                     f', {PracticeCenters.phone_number_col}')

all_fields = f'{PracticeCenters.id_col}, {all_fields_to_add}'

select_all_operation = f'SELECT {all_fields} FROM {PracticeCenters.table_name}'


class MySQLPracticeCenterQuery(MySQLQuery):
    def get(self, practice_center_id):
        filters = [MySQLFilter.filter_equal(PracticeCenters.id_col, practice_center_id)]

        return self.build_query(select_all_operation, filters)

    def get_all(self, form=None):
        filters, inner_filtering = Filter().build_filters(form)

        orders = [PracticeCenters.name_col]

        return self.build_query(select_all_operation, filters, orders, inner_filtering)

    def add(self):
        operation = (f'INSERT INTO {PracticeCenters.table_name}'
                     f'({all_fields_to_add}) VALUES (%s, %s, %s, %s)')

        return self.build_query(operation)