# -*- coding: utf-8 -*-
"""
    File Name：    user
    Date：         2019/4/10
    Description :
"""

from flask import render_template, request, redirect, url_for, flash, app
from flask_login import login_user, logout_user, current_user, login_required

from app.forms.auth import RegisterForm, LoginForm, ChangeInfoForm
from app.models.base import db
from app.models.user import User, get_user
from . import web
from datetime import datetime


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':  # and form.validate():
        user_t = db.Table('user')
        user_t.put_item(
            Item={
                'name': form.name.data,
                'create_time': int(datetime.now().timestamp()),
                'single_double': form.single_double.data,
                'company_name': form.company_name.data,
                'depart_city': form.depart_city.data,
                'arrive_city': form.arrive_city.data,
                'depart_time': form.depart_time.data,
                'depart_date': str(form.depart_date.data),
                'arrive_time': form.arrive_time.data,
                'arrive_date': str(form.arrive_date.data),
                'return_date': str(form.return_date.data),
                'return_time': form.return_time.data,
                'first_class_price': form.first_class_price.data,
                'first_class_num': form.first_class_num.data,
                'second_class_price': form.second_class_price.data,
                'second_class_num': form.second_class_num.data,
                'third_class_price': form.third_class_price.data,
                'third_class_num': form.third_class_num.data,
                'depart_airport': form.depart_airport.data,
                'arrive_airport': form.arrive_airport.data
            }
        )
        return redirect(url_for('web.login'))
    return render_template('web/SignUp.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(nickname=form.nickname.data).first()
        if user and user.check_passward(form.password.data):
            from flask import session
            from datetime import timedelta

            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=30)
            login_user(user, remember=True)
            next = request.args.get('next')
            print(next)
            if not next:  # or not next.startwith('/'):
                next = url_for('web.personal_info')
            return redirect(next)
        else:
            flash('账号不存在或密码错误')
    return render_template('web/VIPSignIn.html', form=form)


@web.route('/personalInfo', methods=['GET', 'POST'])
@login_required
def personal_info():
    form = ChangeInfoForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(nickname=form.nickname.data).first()
        changed = user.change_info(form)
        if changed:
            return redirect(url_for('web.personal_info'))
    userid = current_user.id
    user = get_user(userid)
    form.nickname.default = user.nickname
    form.password.default = user.password
    form.name.default = user.name
    form.id_card.default = user.id_card
    form.phone_number.default = user.phone_number
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
