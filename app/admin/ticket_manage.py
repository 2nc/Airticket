from flask import render_template, request, redirect, url_for, flash

from app.data.order import ManageOrder
from app.forms.admin import AddCompanyForm, AddTicketForm
from app.config import db
from . import admin
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr


@admin.route('/admin/company', methods=['GET', 'POST'])
def company():
    form = AddCompanyForm(request.form)
    company_t = db.Table('company')
    response = company_t.scan()
    companys = response['Items']
    if request.method == 'POST':
        company_t.put_item(
            Item={
                'company_name': form.company_name.data,
                'En_name': form.En_name.data,
                'create_time': int(datetime.now().timestamp())
            }
        )
        return redirect(url_for('admin.company'))
    return render_template('admin/CompanyManage.html', form=form, companys=companys)


@admin.route('/admin/company/<company_name>', methods=['GET', 'POST'])
def change_company(company_name):
    # form = AddCompanyForm(request.form)
    company_t = db.Table('company')
    response = company_t.scan(
        FilterExpression=Attr('En_name').eq(company_name)
    )
    com = response['Items'][0]
    ticket_t = db.Table('ticket')
    response = ticket_t.scan(
        FilterExpression=Attr('company_name').eq(com['company_name'])
    )
    tic = response['Items']
    if len(tic):
        flash("WARNING! There are related airlines!")
        return redirect(url_for('admin.company'))

    company_t.delete_item(
        Key={
            'company_name': com['company_name']
        }
    )
    return redirect(url_for('admin.company'))


@admin.route('/admin/ticket', methods=['GET', 'POST'])
def add_ticket():
    form = AddTicketForm(request.form)
    if request.method == 'POST':  # and form.validate():
        ticket_t = db.Table('ticket')
        ticket = {
            'name': form.name.data,
            'create_time': int(datetime.now().timestamp()),
            'company_name': form.company_name.data,
            'depart_city': form.depart_city.data,
            'arrive_city': form.arrive_city.data,
            'depart_time': form.depart_time.data,
            'depart_date': str(form.depart_date.data),
            'arrive_time': form.arrive_time.data,
            'arrive_date': str(form.arrive_date.data),
            'first_class_price': form.first_class_price.data,
            'first_class_num': form.first_class_num.data,
            'second_class_price': form.second_class_price.data,
            'second_class_num': form.second_class_num.data,
            'third_class_price': form.third_class_price.data,
            'third_class_num': form.third_class_num.data,
            'depart_airport': form.depart_airport.data,
            'arrive_airport': form.arrive_airport.data
        }
        ticket_t.put_item(
            Item=ticket
        )
        return redirect(url_for('admin.add_ticket'))
    return render_template('admin/TicketAdd.html', form=form)


@admin.route('/admin/order/manage', methods=['GET', 'POST'])
def manage_order():
    order_id = request.args.get('order_id')
    if request.method == 'POST':
        order_t = db.Table('order')
        response = order_t.update_item(
            Key={
                'order_id': order_id
            },
            UpdateExpression='SET order_status = :val1',
            ExpressionAttributeValues={
                ':val1': 'Completed'
            }
        )
        return redirect(url_for('admin.manage_order'))
    order_t = db.Table('order')
    response = order_t.scan()
    orders = response['Items']
    orders = ManageOrder(orders).order
    return render_template('admin/OrderManage.html', orders=orders)


@admin.route('/admin/order/dispose_order', methods=['POST'])
def dispose_order():
    order_id = request.args.get('order_id')
    order_t = db.Table('order')
    order_t.delete_item(
        Key={
            'order_id': order_id
        }
    )

    return redirect(url_for('admin.manage_order'))
