'''
Created on 18.02.2018
Database interface testing for all users related methods.
The user has a data model represented by the following User dictionary:
    {
        'summary': {
            'nickname': '',
            'registrationdate': ,
            'bio': '',
            'avatar': ''
        },
        'details': {
            'lastlogindate': ,
            'firstname': '',
            'lastname': '',
            'email': '',
            'mobile': '',
            'gender': '',
            'birthdate': '',
        }
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
            * ``birthdate``: string containing the birth date of the user in yyyy-mm-dd format.
            * ``bio``: text chosen by the user for biography

List of users has the following data model:
[{'nickname':'', 'avatar':'', 'bio':'', 'registrationdate':''}, {'nickname':'', 'avatar':'', 'bio':'', 'registrationdate':''}]


@author: sercant
REFERENCEs:
-   Programmable Web Projects, Exercise 1, database_api_tests_users.py
'''

import sqlite3
import unittest

from app import database

# Path to the database file, different from the deployment db
DB_PATH = 'db/critique_test.db'
ENGINE = database.Engine(DB_PATH)

INITIAL_SIZE = 5

USER1 = {
    'summary': {
        'nickname': 'Scott',
        'registrationdate': 1519557738,
        'bio': 'Best bass in town. Ramona <3',
        'avatar': 'photo1.jpg'
    },
    'details': {
        'lastlogindate': 1519557799,
        'firstname': 'Scott',
        'lastname': 'Pilgrim',
        'email': 'scott@outlook.com',
        'mobile': None,
        'gender': 'male',
        'birthdate': '1998-01-22'
    }
}

MODIFIED_USER1 = {
    'summary': {
        'nickname': 'Scott',
        'registrationdate': 1519557738,
        'bio': 'Best bass in town.',
        'avatar': 'photo8.jpg'
    },
    'details': {
        'lastlogindate': 1519557799,
        'firstname': 'Scott',
        'lastname': 'Pilgrim',
        'email': 'scott_pilgrim@outlook.com',
        'mobile': '+345635454',
        'gender': 'male',
        'birthdate': '1998-01-23'
    }
}

USER2 = {
    'summary': {
        'nickname': 'Kim',
        'registrationdate': 1518557738,
        'bio': 'Drums! Dont irritate me...',
        'avatar': 'photo3.png',
    },
    'details': {
        'lastlogindate': 1519554738,
        'firstname': 'Kim',
        'lastname': 'Pine',
        'email': 'kim@hotmail.com',
        'mobile': None,
        'gender': 'female',
        'birthdate': '2000-11-11',
    }
}

NEW_USER = {
    'summary': {
        'nickname': 'Stacey',
        'registrationdate': 1519585947,
        'bio': 'I hate you Scott!',
        'avatar': 'photo9.png',
    },
    'details': {
        'lastlogindate': 1519585947,
        'firstname': 'Stacey',
        'lastname': 'Pilgrim',
        'email': 'stacey@hotmail.com',
        'mobile': None,
        'gender': 'female',
        'birthdate': '1990-11-11',
    }
}

NEW_USER_MALFORMED1 = {
    'summary': {
        'nickname': 'Staceyb',
        'registrationdate': 1519585947,
        'bio': 'I hate you Scott!',
        'avatar': 'photo9.png',
    },
    'detailsa': {
        'lastlogindate': 1519585947,
        'firstname': 'Stacey',
        'lastname': 'Pilgrim',
        'email': 'stacey@hotmail.com',
        'mobile': None,
        'gender': 'female',
        'birthdate': '1990-11-11',
    }
}

NEW_USER_MALFORMED2 = {
    'summary': {
        'nickname': 'Staceya',
        'registrationdate': 1519585947,
        'bio': 'I hate you Scott!',
        'avatar': 'photo9.png',
    },
    'details': {
        'lastlogindate': 1519585947,
        'firstname': None,
        'lastname': 'Pilgrim',
        'email': 'stacey@hotmail.com',
        'mobile': None,
        'gender': 'female',
        'birthdate': '1990-11-11',
    }
}

USER1_ID = 1
USER2_ID = 2

USER_WRONG_NICKNAME = 'REEE'


class UserDBAPITestCase(unittest.TestCase):
    '''
    Test cases for the Users related methods.

    :references:

    :[1]: Exercise1, forum.database.py
    '''
    # INITIATION AND TEARDOWN METHODS
    @classmethod
    def setUpClass(cls):
        '''
        Creates the database structure. Removes first any preexisting
            database file

        :references:

        :[1]: Exercise1, forum.database.py
        '''
        print("Testing ", cls.__name__)
        ENGINE.remove_database()
        ENGINE.create_tables()

    @classmethod
    def tearDownClass(cls):
        '''
        Remove the testing database

        :references:

        :[1]: Exercise1, forum.database.py
        '''
        print("Testing ENDED for ", cls.__name__)
        ENGINE.remove_database()

    def setUp(self):
        '''
        Populates the database

        :references:

        :[1]: Exercise1, forum.database.py
        '''
        # This method load the initial values from critique_data_dump.sql
        ENGINE.populate_tables()
        # Creates a Connection instance to use the API
        self.connection = ENGINE.connect()

    def tearDown(self):
        '''
        Close underlying connection and remove all records from database

        :references:

        :[1]: Exercise1, forum.database.py
        '''
        self.connection.close()
        ENGINE.clear()

    def test_users_table_created(self):
        '''
        Checks that the table initially contains 5 users (check
        critique_data_dump.sql). NOTE: Do not use Connection instance but
        call directly SQL.

        :references:

        :[1]: Exercise1, forum.database.py
        '''
        print('('+self.test_users_table_created.__name__+')',
              self.test_users_table_created.__doc__)
        # Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query1 = 'SELECT * FROM users'
        query2 = 'SELECT * FROM users_profile'
        # Connects to the database.
        con = self.connection.con
        with con:
            # Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # Provide support for foreign keys
            cur.execute(keys_on)
            # Execute main SQL Statement
            cur.execute(query1)
            users = cur.fetchall()
            # Assert
            self.assertEqual(len(users), INITIAL_SIZE)
            # Check the users_profile:
            cur.execute(query2)
            users = cur.fetchall()
            # Assert
            self.assertEqual(len(users), INITIAL_SIZE)

    def test_create_user_object(self):
        '''
        Check that the method create_user_object works return adequate values
        for the first database row. NOTE: Do not use Connection instace to
        extract data from database but call directly SQL.
        '''
        print('('+self.test_create_user_object.__name__+')',
              self.test_create_user_object.__doc__)
        # Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT users.*, users_profile.* FROM users, users_profile \
                 WHERE users.user_id = users_profile.user_id'
        # Get the sqlite3 con from the Connection instance
        con = self.connection.con
        # I am doing operations after with, so I must explicitly close the
        # the connection to be sure that no locks are kept. The with, close
        # the connection when it has gone out of scope
        # try:
        with con:
            # Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # Provide support for foreign keys
            cur.execute(keys_on)
            # Execute main SQL Statement
            cur.execute(query)
            # Extrac the row
            row = cur.fetchone()
        # Test the method
        user = self.connection._create_user_object(row)
        self.assertDictContainsSubset(user, USER1)

    def test_get_user(self):
        '''
        Test get_user with id Scott and Kim
        '''
        print('('+self.test_get_user.__name__+')',
              self.test_get_user.__doc__)

        # Test with an existing user
        user = self.connection.get_user(USER1['summary']['nickname'])
        self.assertDictContainsSubset(user, USER1)
        user = self.connection.get_user(USER2['summary']['nickname'])
        self.assertDictContainsSubset(user, USER2)

    def test_get_user_noexistingid(self):
        '''
        Test get_user with  msg-200 (no-existing)
        '''
        print('('+self.test_get_user_noexistingid.__name__+')',
              self.test_get_user_noexistingid.__doc__)

        # Test with an existing user
        user = self.connection.get_user(USER_WRONG_NICKNAME)
        self.assertIsNone(user)

    def test_get_users(self):
        '''
        Test that get_users work correctly and extract required user info
        '''
        print('('+self.test_get_users.__name__+')',
              self.test_get_users.__doc__)
        users = self.connection.get_users()
        # Check that the size is correct
        self.assertEqual(len(users), INITIAL_SIZE)
        # Iterate through users and check if the users with USER1_ID and
        # USER2_ID are correct:
        for user in users:
            if user['nickname'] == USER1['summary']['nickname']:
                self.assertDictContainsSubset(user, USER1['summary'])
            elif user['nickname'] == USER2['summary']['nickname']:
                self.assertDictContainsSubset(user, USER2['summary'])

    def test_delete_user(self):
        '''
        Test that the user Scott is deleted
        '''
        print('('+self.test_delete_user.__name__+')',
              self.test_delete_user.__doc__)
        resp = self.connection.delete_user(USER1['summary']['nickname'])
        self.assertTrue(resp)
        # Check that the users has been really deleted through a get
        resp2 = self.connection.get_user(USER1['summary']['nickname'])
        self.assertIsNone(resp2)
        # TODO (sercant): enable when posts implemented
        # # Check that the user does not have associated any message
        # resp3 = self.connection.get_posts(nickname=USER1['nickname'])
        # self.assertEqual(len(resp3), 0)

    def test_delete_user_noexistingnickname(self):
        '''
        Test delete_user with  Batty (no-existing)
        '''
        print('('+self.test_delete_user_noexistingnickname.__name__+')',
              self.test_delete_user_noexistingnickname.__doc__)
        # Test with an existing user
        resp = self.connection.delete_user(USER_WRONG_NICKNAME)
        self.assertFalse(resp)

    def test_modify_user(self):
        '''
        Test that the user Mystery is modifed
        '''
        print('('+self.test_modify_user.__name__+')',
              self.test_modify_user.__doc__)
        # Get the modified user
        resp = self.connection.modify_user(
            USER1['summary']['nickname'], MODIFIED_USER1['summary'], MODIFIED_USER1['details'])

        self.assertEqual(resp, USER1['summary']['nickname'])

        # Check that the users has been really modified through a get
        resp2 = self.connection.get_user(USER1['summary']['nickname'])
        resp_summary = resp2['summary']
        resp_details = resp2['details']

        # Check the expected values
        new_summary = MODIFIED_USER1['summary']
        for key, value in new_summary.items():
            self.assertEqual(value, resp_summary[key])

        new_details = MODIFIED_USER1['details']
        for key, value in new_details.items():
            self.assertEqual(value, resp_details[key])

        self.assertDictContainsSubset(resp2, MODIFIED_USER1)

    def test_modify_user_noexistingnickname(self):
        '''
        Test modify_user with user REE (no-existing)
        '''
        print('('+self.test_modify_user_noexistingnickname.__name__+')',
              self.test_modify_user_noexistingnickname.__doc__)
        # Test with an existing user
        resp = self.connection.modify_user(
            USER_WRONG_NICKNAME, USER1['summary'], USER1['details'])
        self.assertIsNone(resp)

    def test_create_user(self):
        '''
        Test that I can add new users
        '''
        print('('+self.test_create_user.__name__+')',
              self.test_create_user.__doc__)
        nickname = self.connection.create_user(
            NEW_USER['summary']['nickname'], NEW_USER)
        self.assertIsNotNone(nickname)
        self.assertEqual(nickname, NEW_USER['summary']['nickname'])
        # Check that the messages has been really modified through a get
        resp2 = self.connection.get_user(nickname)
        self.assertDictContainsSubset(NEW_USER['summary'],
                                      resp2['summary'])
        self.assertDictContainsSubset(NEW_USER['details'],
                                      resp2['details'])

    def test_create_user_malformed(self):
        '''
        Test that I can't add new malformed users
        '''
        print('('+self.test_create_user_malformed.__name__+')',
              self.test_create_user_malformed.__doc__)
        with self.assertRaises(ValueError):
            nickname = self.connection.create_user(
                NEW_USER_MALFORMED1['summary']['nickname'], NEW_USER_MALFORMED1)
        with self.assertRaises(ValueError):
            nickname = self.connection.create_user(
                NEW_USER_MALFORMED2['summary']['nickname'], NEW_USER_MALFORMED2)

    def test_create_existing_user(self):
        '''
        Test that I cannot add two users with the same name
        '''
        print('('+self.test_create_existing_user.__name__+')',
              self.test_create_existing_user.__doc__)
        nickname = self.connection.create_user(
            USER1['summary']['nickname'], NEW_USER)
        self.assertIsNone(nickname)

    def test_get_user_id(self):
        '''
        Test that get_user_id returns the right value given a nickname
        '''
        print('('+self.test_get_user_id.__name__+')',
              self.test_get_user_id.__doc__)
        id = self.connection.get_user_id(USER1['summary']['nickname'])
        self.assertEqual(USER1_ID, id)
        id = self.connection.get_user_id(USER2['summary']['nickname'])
        self.assertEqual(USER2_ID, id)

    def test_get_user_id_unknown_user(self):
        '''
        Test that get_user_id returns None when the nickname does not exist
        '''
        print('('+self.test_get_user_id.__name__+')',
              self.test_get_user_id.__doc__)
        id = self.connection.get_user_id(USER_WRONG_NICKNAME)
        self.assertIsNone(id)

    def test_not_contains_user(self):
        '''
        Check if the database does not contain users with id REE
        '''
        print('('+self.test_contains_user.__name__+')',
              self.test_contains_user.__doc__)
        self.assertFalse(self.connection.contains_user(USER_WRONG_NICKNAME))

    def test_contains_user(self):
        '''
        Check if the database contains users with nickname Scott and Kim
        '''
        print('('+self.test_contains_user.__name__+')',
              self.test_contains_user.__doc__)
        self.assertTrue(self.connection.contains_user(
            USER1['summary']['nickname']))
        self.assertTrue(self.connection.contains_user(
            USER2['summary']['nickname']))


if __name__ == '__main__':
    '''

    :references:

    :[1]: Exercise1, forum.database.py
    '''
    print('Start running user tests')
    unittest.main()
