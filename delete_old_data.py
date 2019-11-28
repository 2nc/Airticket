from __future__ import print_function # Python 2/3 compatibility
import boto3
from botocore.exceptions import ClientError
import json
import decimal
from datetime import datetime


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table_order = dynamodb.Table('order')
table_ticket = dynamodb.Table('ticket')

response_order = table_order.scan()
response_ticket = table_ticket.scan()

for item in response_order['Items']:
    order_id = item['order_id']
    year = int(item['depart_time'][0:4])
    month = int(item['depart_time'][5:7])
    date = int(item['depart_time'][8:10])
    depart_date = datetime(year, month, date)
    date_now = datetime.now()

    if depart_date < date_now:
        try:
            response = table_order.delete_item(
                Key={
                    'order_id':order_id
                }
            )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
            else:
                raise
        else:
            print("DeleteItem succeeded:")
            print(json.dumps(response, indent=4, cls=DecimalEncoder))


for item in response_ticket['Items']:
    print(item)
    name = item['name']
    year = int(item['depart_date'][0:4])
    month = int(item['depart_date'][5:7])
    date = int(item['depart_date'][8:10])
    depart_date = datetime(year, month, date)
    date_now = datetime.now()
    print(depart_date)
    print(date_now)

    if depart_date < date_now:
        try:
            response = table_ticket.delete_item(
                Key={
                    'name':name
                }
            )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
            else:
                raise
        else:
            print("DeleteItem succeeded:")
            print(json.dumps(response, indent=4, cls=DecimalEncoder))