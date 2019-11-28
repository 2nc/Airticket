from flask import render_template, request, redirect, url_for

from app.data.admin import AdminInfo
from app.forms.admin import AddAdminForm
from app.forms.auth import LoginForm

from app.config import db
from . import admin

from boto3.dynamodb.conditions import Key, Attr
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


# 大多数函数的作用大部分都在函数名中体现了。get方法是获取登录页面，post方法如果登陆成功是返回管理员管理。
@admin.route('/admin/login', methods=['GET', 'POST'])
def login():

    form = LoginForm(request.form)
    if request.method == 'POST':  # and form.validate():
        admin_t = db.Table('admin')
        response = admin_t.scan(
            FilterExpression=Attr('nickname').eq(form.nickname.data)
        )
        ad = response['Items'][0]['password']

        if ad and check_password_hash(ad,form.password.data):
            return redirect(url_for('admin.admin_manage'))
    return render_template('admin/AdminSignIn.html', form=form)


# 管理员管理
@admin.route('/admin/manage')
def admin_manage():
    form = AddAdminForm(request.form)
    admin_t = db.Table('admin')
    response = admin_t.scan()
    admins=response['Items']
    return render_template('admin/AdminManage.html', form=form, admins=admins)


# 添加管理员
@admin.route('/admin/addAdmin', methods=['GET', 'POST'])
def add_admin():
    form = AddAdminForm(request.form)
    admin_t = db.Table('admin')
    response = admin_t.scan()
    admins = response['Items']
    if request.method == 'POST':  # and form.validate():
        admin_t.put_item(
            Item={
                'nickname': form.nickname.data,
                'role': 'super',
                'password': generate_password_hash(form.password.data),
                'create_time': int(datetime.now().timestamp())
            }
        )
        return redirect(url_for('admin.admin_manage'))
    return render_template('admin/AdminManage.html', form=form, admins=admins)


@admin.route('/admin/changeInfo/<nickname>', methods=['GET', 'POST'])
def change_info(nickname):
    form = AddAdminForm(request.form)
    form.nickname.default = nickname
    form.process()
    admin_t = db.Table('admin')
    response = admin_t.scan(
        FilterExpression=Attr('nickname').eq(nickname)
    )
    ad = response['Items'][0]
    print(ad)
    if request.method == 'POST':  # and form.validate():
        changed = ad.change_info(form)
        if changed:
            print('管理员信息修改成功')
    if request.method == 'GET':
        admin_t.delete_item(
            Key={
                'nickname': nickname,
            }
        )
    return redirect(url_for('admin.admin_manage'))
