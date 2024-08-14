from .models import UserAccount, EndDestination
import secrets
from cassandra.util import uuid_from_time

def create_user_account(account_data):
    app_secret_token = secrets.token_hex(16)
    account = UserAccount.create(
        email=account_data.email,
        account_name=account_data.account_name,
        app_secret_token=app_secret_token,
        website=account_data.website
    )
    return account

def get_user_account_by_id(account_id):
    return UserAccount.objects(id=uuid_from_time(account_id)).first()

def get_user_account_by_token(token):
    return UserAccount.objects(app_secret_token=token).first()

def create_end_destination(destination_data, account_id):
    destination = EndDestination.create(
        url=destination_data.url,
        http_method=destination_data.http_method,
        headers=destination_data.headers,
        account_id=account_id
    )
    return destination

def get_end_destinations_by_account_id(account_id):
    return EndDestination.objects(account_id=account_id).all()
