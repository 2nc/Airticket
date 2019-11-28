import boto3

db = boto3.resource('dynamodb')

DEBUG = True

SECRET_KEY = 'aqwrgsrtkj65476riqw34tare'



WTF_CSRF_CHECK_DEFAULT = False


from datetime import timedelta

REMEMBER_COOKIE_DURATION = timedelta(days=30)
