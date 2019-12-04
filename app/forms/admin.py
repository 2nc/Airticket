from wtforms import StringField, PasswordField, Form, SelectField, SubmitField, RadioField, DateField, DateTimeField, \
    HiddenField, IntegerField
from wtforms.validators import Length, Email, ValidationError, EqualTo, Required,DataRequired

import boto3

db = boto3.resource('dynamodb')


class AdminLoginForm(Form):
    nickname = StringField('Usermane', validators=[DataRequired(), Length(2, 10,'Length should between 2-10')])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20,'Length should between 6-20')])


class AddTicketForm(Form):
    cities = [('Toronto', 'Toronto'), ('Montreal', 'Montreal'), ('Vancouver', 'Vancouver'), ('Edmonton', 'Edmonton'),
              ('Regina', 'Regina'), ('Halifax', 'Halifax'), ('Fredericton', 'Fredericton'), ('Regina', 'Regina')]

    id = HiddenField('id')
    submit = SubmitField('Submit')
    name = StringField('Airline', validators=[Length(2, 10,'Length should between 2-10')])
    company_name = SelectField(label="Airline Company", validators=[DataRequired("Please choose")])

    depart_city = SelectField("From:", choices=cities, validators=[DataRequired(), Length(2, 10,'Length should between 2-10')])
    arrive_city = SelectField("To:", choices=cities, validators=[DataRequired(), Length(2, 10,'Length should between 2-10')])

    depart_date = DateField(label='Departure Date', format='%m/%d/%Y', validators=DataRequired())
    depart_time = StringField('Departire Time', validators=DataRequired())
    arrive_date = DateField(label='Arrival Date', format='%m/%d/%Y', validators=DataRequired())
    arrive_time = StringField('Arrival Time', validators=DataRequired())

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
        # Read company from database
        company_t = db.Table('company')
        response = company_t.scan()
        com = response['Items']
        self.company_name.choices = [(c['company_name'], c['company_name']) for c in com]


class AddAdminForm(Form):
    nickname = StringField('Add New Admin', validators=[DataRequired(), Length(2, 10,'length should between 2-10')])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('repeat_password'), Length(6, 20),'length should between 6-20'])
    repeat_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(6, 20,'length should between 6-20')])


class AddCompanyForm(Form):
    En_name = StringField('Company Abbreviation', validators=[DataRequired()])
    company_name = StringField('Company Name', validators=[DataRequired(), Length(2, 20,'length should between 2-20')])


class ChangeCompanyForm(Form):
    En_name = StringField('Company Abbreviation')
    company_name = StringField('Company Abbreviation', validators=[DataRequired()])
