# -*- coding: utf-8 -*-
"""
    File Name：    user
    Date：         2019/4/10
    Description :
"""

from flask import render_template, request, redirect, url_for, flash, app, session
from flask_login import login_user, logout_user, current_user, login_required, UserMixin

from app.forms.auth import RegisterForm, LoginForm, ChangeInfoForm
from app.models.base import db
from app.models.user import User
from . import web
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from boto3.dynamodb.conditions import Key, Attr
from app import login_manager

class User(UserMixin):
    def is_authenticated(self):
        return True

    def is_actice(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return "1"

@login_manager.user_loader
def get_user(uid):
    user=User()
    return user

@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':  # and form.validate():
        user_t = db.Table('user')
        user_t.put_item(
            Item={
                'nickname': form.nickname.data,
                'create_time': int(datetime.now().timestamp()),
                'name': form.name.data,
                'phone_number': form.phone_number.data,
                'id_card': form.id_card.data,
                'password': generate_password_hash(form.password.data),
            }
        )
        return redirect(url_for('web.login'))
    return render_template('web/SignUp.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user_t = db.Table('user')
        response = user_t.scan(
            FilterExpression=Attr('nickname').eq(form.nickname.data)
        )
        userc = response['Items'][0]['nickname']
        pw = response['Items'][0]['password']
        if userc and check_password_hash(pw,form.password.data):
            from flask import session
            from datetime import timedelta

            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=30)
            user=User()
            login_user(user, remember=True)
            session['usernickname'] = userc
            next = request.args.get('next')
            print(next)
            if not next:  # or not next.startwith('/'):
                next = url_for('web.personal_info')
            return redirect(next)
        else:
            flash('账号不存在或密码错误')
    return render_template('web/VIPSignIn.html', form=form)


@web.route('/personalInfo/', methods=['GET', 'POST'])
@login_required
def personal_info():
    form = ChangeInfoForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(nickname=form.nickname.data).first()
        changed = user.change_info(form)
        if changed:
            return redirect(url_for('web.personal_info'))
    user_t = db.Table('user')
    response = user_t.scan(
        FilterExpression=Attr('nickname').eq(session['usernickname'])
    )
    user=response['Items'][0]
    form.nickname.default = user['nickname']
    form.password.default = user['password']
    form.name.default = user['name']
    form.id_card.default = user['id_card']
    form.phone_number.default = user['phone_number']
    form.process()
    return render_template('web/VIPInfo.html', form=form)


@web.route('/changeInfo', methods=['GET', 'POST'])
@login_required
def change_info():
    form = ChangeInfoForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(nickname=form.nickname.data).first()
        changed = user.change_info(form)

        if changed:
            return '用户信息更改成功'
    return redirect(url_for('web.personal_info'))


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    pass


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    pass


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('web.index'))
