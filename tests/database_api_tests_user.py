'''
Created on 18.02.2018
Database interface testing for all users related methods.
The user has a data model represented by the following User dictionary:
    {
        'nickname': '',
        'registrationdate': ,
        'lastlogindate': ,
        'firstname': '',
        'lastname': '',
        'email': '',
        'mobile': '',
        'gender': '',
        'avatar': '',
        'age': '',
        'bio': ''
    }

    where:

    * ``nickname``: nickname of the user
    * ``registrationdate``: UNIX timestamp when the user registered in the system (long integer)
    * ``lastlogindate``: UNIX timestamp when the user last logged in to the system (long integer)
    * ``firstname``: given name of the user
    * ``lastname``: family name of the user
    * ``email``: current email of the user.
    * ``mobile``: string showing the user's phone number. Can be None.
    * ``gender``: User's gender ('male' or 'female').
    * ``avatar``: name of the image file used as avatar
    * ``age``: integer containing the age of the user.
    * ``bio``: text chosen by the user for biography



List of users has the following data model:
[{'nickname':'', 'avatar':'', 'bio':'', 'registrationdate':''}, {'nickname':'', 'avatar':'', 'bio':'', 'registrationdate':''}]


@author: sercant
'''

import sqlite3
import unittest

from app import database

# Path to the database file, different from the deployment db
DB_PATH = 'db/critique_test.db'
ENGINE = database.Engine(DB_PATH)
