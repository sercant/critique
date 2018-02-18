'''
Created on 18.02.2018
Database interface testing for all users related methods.
The user has a data model represented by the following User dictionary:
    {
        'nickname': '', 'registrationdate': ,
        'lastlogindate': '','firstname': '','lastname': '',
        'email': '','mobile': '','gender': '',
        'avatar': '','birthdate': '','bio': ''
    }
    where:
     - registrationdate: UNIX timestamp when the user registered in
                         the system
     - lastlogindate: UNIX timestamp when the user last logged in
                         to the system
     - nickname: nickname of the user
     - bio: text chosen by the user for bio
     - avatar: name of the image file used as avatar
     - firstname: given name of the user
     - lastname: of the user
     - email: current email of the user.
     - mobile: string showing the user's phone number
     - gender: User's gender ('male' or 'female').
     - birthday: int with the birthday of the user.


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
