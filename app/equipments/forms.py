from wtforms import StringField
from wtforms.validators import Length

from app.search.forms import GeneralSearchForm


class EquipmentSearchForm(GeneralSearchForm):
    name = StringField('Name', validators=[Length(max=100)])
    manufacturer = StringField('Manufacturer', validators=[Length(max=100)])
    equipment_type = StringField('Equipment type', validators=[Length(max=100)])
    description = StringField('Description', validators=[Length(max=200)])
