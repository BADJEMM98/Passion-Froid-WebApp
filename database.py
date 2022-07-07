from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.sql import SqlManagementClient


RESOURCE_GROUP = 'gr-passion-froid'
LOCATION = 'francecentral' 
SQL_SERVER = 'sql_server_passion_froid'
SQL_DB = 'YOUR_SQLDB_NAME'
USERNAME = 'admin'
PASSWORD = 'admin'

sql_client = get_client_from_cli_profile(ResourceManagementClient)

# Create a SQL database in the Basic tier
database = sql_client.databases.create_or_update(
    RESOURCE_GROUP,
    SQL_SERVER,
    SQL_DB,
    {
        'location': LOCATION,
        'collation': 'SQL_Latin1_General_CP1_CI_AS',
        'create_mode': 'default',
        'requested_service_objective_name': 'Basic'
    }
)