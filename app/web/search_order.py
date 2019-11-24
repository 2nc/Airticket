# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         search_order
# Date:         2019/4/10
# -------------------------------------------------------------------------------
from datetime import datetime

from flask import render_template, request, redirect, url_for, session
from flask_login import current_user, login_required

from app.data.order import MyOrder
from app.data.ticket import SearchTicket
from app.forms.search_order import SearchForm, OrderForm
from app.models.base import db
from app.models.order import Order
from app.models.ticket import Ticket
from . import web
from boto3.dynamodb.conditions import Key, Attr


@web.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm(request.form)
    if request.method == 'POST':  # and form.validate():
        ticket_t = db.Table('ticket')
        response = ticket_t.scan(
            FilterExpression=Attr('single_double').eq(form.single_double.data) and
                             Attr('depart_date').eq(str(form.depart_date.data)) and
                             Attr('depart_city').eq(form.depart_city.data) and
                             Attr('arrive_city').eq(form.arrive_city.data),

        )
        tickets = response['Items']
        tickets = SearchTicket(tickets).tickets  # 列表包含着字典
        return render_template('web/SearchResults.html', tickets=tickets, form=form)

    form.single_double.default = '往返'
    form.process()
    return render_template('web/SearchResults.html', form=form, tickets=[])


@web.route('/order/<plain_id>')
@login_required
def order(plain_id):
    """
    :param plain_id: 代表航班名称,name，需要前端返回。
    :return:
    """
    order_id = 'P' + datetime.now().strftime('%Y%m%d%H%M%S')
    form = OrderForm(request.form)
    ticket_t = db.Table('ticket')
    response = ticket_t.scan(
        FilterExpression=Attr('name').eq(plain_id)
    )
    ticket = response['Items'][0]

    form.order_id.default = order_id
    form.route.default = ticket['depart_city'] + '-' + ticket['arrive_city']
    form.depart_time.default = ticket['depart_date'] + '-' + ticket['depart_time']
    form.process()
    return render_template('web/OrderInfo.html', form=form)


@web.route('/order/save_order', methods=['POST'])
@login_required
def save_order():
    form = OrderForm(request.form)
    if request.method == 'POST':  # and form.validate():
        order_t = db.Table('order')
        order_t.put_item(
            Item={
                'uname': session['usernickname'],
                'create_time': int(datetime.now().timestamp()),
                'order_id': form.order_id.data,
                'route': form.route.data,
                'depart_time': form.depart_time.data,
                'ticket_type': form.ticket_type.data,
                'status': '正在处理'
            }
        )
        return redirect(url_for('web.my_order'))


@web.route('/order/my')
@login_required
def my_order():
    order_t = db.Table('order')
    response = order_t.scan(
        FilterExpression=Attr('uname').eq(session['usernickname'])
    )
    order = response['Items']
    my_order = MyOrder(order).order
    return render_template('web/MyTicket.html', my_order=my_order)
