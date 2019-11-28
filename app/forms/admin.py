

from wtforms import StringField, PasswordField, Form, SelectField, SubmitField, RadioField, DateField, DateTimeField, \
    HiddenField, IntegerField
from wtforms.validators import Length, Email, ValidationError, EqualTo, Required

from .base import DataRequired
import boto3

db = boto3.resource('dynamodb')

class AdminLoginForm(Form):
    nickname = StringField('Usermane', validators=[DataRequired(), Length(2, 10)])
    password = PasswordField('Password', validators=[DataRequired(),
                                               EqualTo('repeat_password'), Length(6, 20)])



class AddTicketForm(Form):
    cities = [('Toronto', 'Toronto'), ('Montreal', 'Montreal'), ('Vancouver', 'Vancouver'), ('Edmonton', 'Edmonton'),
              ('Regina', 'Regina'), ('Halifax', 'Halifax'), ('Fredericton', 'Fredericton'), ('Regina', 'Regina')]

    id = HiddenField('id')
    submit = SubmitField('Submit')

    single_double = RadioField('Trip Type', choices=[('One-way', 'One-way'), ('Round-trip', 'Round-trip')])
    name = StringField('Airline', validators=[Length(2, 10)])
    company_name = SelectField(label="Airline Company", validators=[DataRequired("Please choose")])

    depart_city = SelectField("From:", choices=cities, validators=[DataRequired(), Length(2, 10)])
    arrive_city = SelectField("To:", choices=cities, validators=[DataRequired(), Length(2, 10)])

    depart_date = DateField(label='Departure Date', format='%m/%d/%Y')
    depart_time = StringField('Departire Time')
    arrive_date = DateField(label='Arrival Date', format='%m/%d/%Y')
    arrive_time = StringField('Arrival Time')
    return_date = DateField(label='Return Date', format='%m/%d/%Y')
    return_time = StringField('Return Time')

    first_class_price = IntegerField('First Class Price')
    second_class_price = IntegerField('Business Class Price')
    third_class_price = IntegerField('Economy Class Price')
    first_class_num = IntegerField('First Class Ticket Amount', validators=[DataRequired()])
    second_class_num = IntegerField('Business Ticket Amount', validators=[DataRequired()])
    third_class_num = IntegerField('Economy Ticket Amount', validators=[DataRequired()])

    depart_airport = StringField('Departure Airport')
    arrive_airport = StringField('Arrival Airport')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # company选择内容从数据库读取
        company_t = db.Table('company')
        response = company_t.scan()
        com = response['Items']
        self.company_name.choices = [(c['company_name'], c['company_name']) for c in com]


class AddAdminForm(Form):
    nickname = StringField('Add New Admin', validators=[DataRequired(), Length(2, 10)])
    password = PasswordField('Password', validators=[DataRequired(),
                                                 EqualTo('repeat_password'), Length(6, 20)])
    repeat_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(6, 20)])


class AddCompanyForm(Form):
    En_name = StringField('Company Abbreviation', validators=[DataRequired()])
    company_name = StringField('Company Name', validators=[DataRequired(), Length(2, 10)])


class ChangeCompanyForm(Form):
    En_name = StringField('Company Abbreviation')
    company_name = StringField('Company Abbreviation', validators=[DataRequired()])
