# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         __init__.py
# Date:         2019/4/9
# -------------------------------------------------------------------------------
from flask import Flask, url_for
from flask_login import LoginManager
from flask_mail import Mail
from werkzeug.security import generate_password_hash

from app.models.admin import Admin
from app.models.base import db

from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime

login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__)

    app.config.from_object('app.config')

    register_blueprint(app)

    #db.init_app(app)


    mail.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = 'Please login or register'

    admin_t = db.Table('admin')
    response = admin_t.scan(
        FilterExpression=Attr('nickname').eq('admin')
    )
    items = response['Items']
    if not len(items):
        admin_t.put_item(
            Item={
                'id': 1,
                'nickname': 'admin',
                'role': 'super',
                'password': generate_password_hash('123456'),
                'create_time': int(datetime.now().timestamp())
            }
        )
    return app




def register_blueprint(app):
    from app.web import web
    from app.admin import admin
    app.register_blueprint(admin)
    app.register_blueprint(web)


