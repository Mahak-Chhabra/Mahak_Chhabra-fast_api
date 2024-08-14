from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
from cassandra.util import uuid4

class UserAccount(Model):
    __keyspace__ = 'fastapi_keyspace'
    id = columns.UUID(primary_key=True, default=uuid4)
    email = columns.Text(required=True)
    account_name = columns.Text(required=True)
    app_secret_token = columns.Text(required=True)
    website = columns.Text(required=False)

class EndDestination(Model):
    __keyspace__ = 'fastapi_keyspace'
    id = columns.UUID(primary_key=True, default=uuid4)
    url = columns.Text(required=True)
    http_method = columns.Text(required=True)
    headers = columns.Map(columns.Text, columns.Text, required=True)
    account_id = columns.UUID(required=True)
