'''
Test stuff
'''
from ditat_etl.databases import Postgres

config = {
    "database": "gfdywodjgoqjeqtcrelp",
    "user": "postgres",
    "password": "8yvxsZHcf2E9HsMR",
    "host": "gfdywodjgoqjeqtcrelp.db.us-east-1.nhost.run",
    "port": "5432"
}
p = Postgres(config)

p.get_table_cols("account")