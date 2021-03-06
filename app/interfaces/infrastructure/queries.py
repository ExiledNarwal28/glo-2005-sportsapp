class MySQLQuery:
    @staticmethod
    def build_query(operation, filters=None, orders=None, inner_filtering=True, desc=False,
                    offset=None, per_page=None):
        query = operation

        if filters is not None and len(filters) > 0:
            query += f' WHERE {filters[0]}'

            conjunction = 'AND' if inner_filtering else 'OR'

            for i in range(1, len(filters)):
                query += f' {conjunction} {filters[i]}'

        if orders is not None and len(orders) > 0:
            query += ' ORDER BY '
            desc = ' DESC' if desc else ''

            for order in orders:
                query += order + desc + ' '

        if offset is not None:
            query = f'{query} LIMIT {offset}'

            if per_page is not None:
                query = f'{query}, {per_page}'

        return f'{query};'
