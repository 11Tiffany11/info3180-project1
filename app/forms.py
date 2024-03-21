from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DecimalField, SubmitField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired


class PropertiesForm(FlaskForm):
    prop_title = StringField('Property Title', validators=[InputRequired()])
    prop_description = TextAreaField('Description', validators=[InputRequired()])
    prop_rooms = IntegerField('No. of Rooms', validators=[InputRequired()])
    prop_bathrooms = IntegerField('No. of Bathrooms', validators=[InputRequired()])
    prop_price = DecimalField('Price', validators=[InputRequired()])
    prop_type = SelectField('Property Type', choices=[('house', 'House'), ('apartment', 'Apartment')])
    prop_location = StringField('Location', validators=[InputRequired()])
    prop_photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images Only!')])
    submit = SubmitField("Add Property")
