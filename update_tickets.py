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

table_ticket = dynamodb.Table('ticket')

response_ticket = table_ticket.scan()

for item in response_ticket['Items']:
    print(item)
    date_now = datetime.now().strftime('%Y-%m-%d')
    item['name'] = item['name'] + date_now
    item['depart_date']=date_now
    print(item)

    response = table_ticket.put_item(
        Item=item
    )

    print("PutItem succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))