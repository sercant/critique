import dredd_hooks as hooks
from app import database

e = database.Engine()
e.connect()

@hooks.after_each
def cleanDb(transaction):
    e.clear()
    e.populate_tables()
