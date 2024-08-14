from cassandra.cluster import Cluster
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import connection
from cassandra.util import uuid4

# Set up the Cassandra connection
cluster = Cluster(['127.0.0.1'])  # Replace with your Cassandra cluster address
session = cluster.connect()
connection.set_session(session)

# Define your keyspace
KEYSPACE = "fastapi_keyspace"

# Create keyspace if it doesn't exist
session.execute(f"""
    CREATE KEYSPACE IF NOT EXISTS {KEYSPACE}
    WITH REPLICATION = {{ 'class' : 'SimpleStrategy', 'replication_factor' : 1 }}
""")
session.set_keyspace(KEYSPACE)





from .models import UserAccount, EndDestination
from cassandra.cqlengine.management import sync_table

sync_table(UserAccount)
sync_table(EndDestination)
