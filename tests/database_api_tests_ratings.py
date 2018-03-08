'''
Created on 25.02.2018
Database interface testing for all ratings related methods.

A ratings object is a dictionary which contains the following keys:
      - ratingsid: id of the rating (int)
      - timestamp: UNIX timestamp (long integer) that specifies when the
                   rating was created.
      - sender: The nickname of the rating's creator
      - receiver: The nickname of the rating's receiver
      - rating: The rating the sender send to receiver.

A rating' list has the following format:
[{'rating_id':'', 'timestamp':, 'sender':'', 'receiver':'', 'rating':''},{'rating_id':'', 'timestamp':, 'sender':'', 'receiver':'', 'rating':''}]

@author: moamen
REFERENCEs:
-   Programmable Web Projects, Exercise 1, database_api_tests_messages.py
'''

import sqlite3, unittest

from app import database

#Path to the database file, different from the deployment db
DB_PATH = 'db/critique_test.db'
ENGINE = database.Engine(DB_PATH)


#CONSTANTS DEFINING DIFFERENT USERS AND USER PROPERTIES
RATING1_ID = 'rating-1'

RATING1 = {
    'rating_id': RATING1_ID,
    'timestamp': 1362022401,
    'sender': 'Scott',
    'receiver': 'Kim',
    'rating': 3
}

RATING1_MODIFIED = {
    'rating_id': RATING1_ID,
    'timestamp': 1362022401,
    'sender': 'Scott',
    'receiver': 'Kim',
    'rating': 4
}

RATING2_ID = 'rating-2'

RATING2 = {
    'rating_id': RATING2_ID,
    'timestamp': 1362022411,
    'sender': 'Scott',
    'receiver': 'Stephen',
    'rating': 5
}

WRONG_RATING_ID = 'rating-200'

INITIAL_SIZE = 17


class RatingDBAPITestCase(unittest.TestCase):
    '''
    Test cases for the ratings related methods.
    '''
    #INITIATION AND TEARDOWN METHODS
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
        try:
          #This method load the initial values from critique_data_dump.sql
          ENGINE.populate_tables()

          #Creates a Connection instance to use the API
          self.connection = ENGINE.connect()
        except Exception as e:

        #For instance if there is an error while populating the tables
          ENGINE.clear()

    def tearDown(self):
        '''
        Close underlying connection and remove all records from database

        :references:

        :[1]: Exercise1, forum.database.py
        '''
        self.connection.close()
        ENGINE.clear()

    def test_ratings_table_created(self):
        '''
        Checks that the table initially contains 17 ratings (check
        critique_data_dump.sql).

        NOTE: Do not use Connection instance but
        call directly SQL.
        '''
        print('('+self.test_ratings_table_created.__name__+')', \
                  self.test_ratings_table_created.__doc__)

        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM ratings'

        #Get the sqlite3 con from the Connection instance
        con = self.connection.con
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            #Provide support for foreign keys
            cur.execute(keys_on)

            #Execute main SQL Statement
            cur.execute(query)
            ratings = cur.fetchall()

            #Assert
            self.assertEqual(len(ratings), INITIAL_SIZE)

    def test_create_rating_object(self):
        '''
        Check that the method _create_rating_object works return adequate
        values for the first database row. NOTE: Do not use Connection instace
        to extract data from database but call directly SQL.
        '''
        print('('+self.test_create_rating_object.__name__+')', \
              self.test_create_rating_object.__doc__)

        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT ratings.*, sender.nickname sender, receiver.nickname receiver FROM ratings INNER JOIN users sender on sender.user_id = ratings.sender_id INNER JOIN users receiver on receiver.user_id = ratings.receiver_id WHERE ratings.rating_id = 1'

        #Get the sqlite3 con from the Connection instance
        con = self.connection.con
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            #Provide support for foreign keys
            cur.execute(keys_on)

            #Execute main SQL Statement
            cur.execute(query)

            #Extrac the row
            row = cur.fetchone()

        #Test the method
        ratings = self.connection._create_rating_object(row)
        self.assertDictContainsSubset(ratings, RATING1)

    def test_get_ratings(self):
        '''
        Test get_rating with id rating-1 and rating-2
        '''
        print('('+self.test_get_ratings.__name__+')', \
              self.test_get_ratings.__doc__)

        #Test with an existing rating
        rating = self.connection.get_rating(RATING1_ID)
        self.assertDictContainsSubset(rating, RATING1)
        rating = self.connection.get_rating(RATING2_ID)
        self.assertDictContainsSubset(rating, RATING2)

    def test_get_rating_malformedid(self):
        '''
        Test get_rating with id 1 (malformed)
        '''
        print('('+self.test_get_rating_malformedid.__name__+')', \
              self.test_get_rating_malformedid.__doc__)

        #Test with an existing rating
        with self.assertRaises(ValueError):
            self.connection.get_rating('1')

    def test_get_rating_noexistingid(self):
        '''
        Test get_rating with rating-200 (no-existing)
        '''
        print('('+self.test_get_rating_noexistingid.__name__+')',\
              self.test_get_rating_noexistingid.__doc__)

        #Test with an existing rating
        rating = self.connection.get_rating(WRONG_RATING_ID)
        self.assertIsNone(rating)

    def test_get_ratings(self):
        '''
        Test that get_ratings work correctly
        '''
        print('('+self.test_get_ratings.__name__+')', self.test_get_ratings.__doc__)
        ratings = self.connection.get_ratings()

        #Check that the size is correct
        self.assertEqual(len(ratings), INITIAL_SIZE)

        #Iterate through ratings and check if the ratings with RATING1_ID and
        #RATING2_ID are correct:
        for rating in ratings:
            if rating['rating_id'] == RATING1_ID:
                self.assertEqual(len(rating), 5)
                self.assertDictContainsSubset(rating, RATING1)
            elif rating['rating_id'] == RATING2_ID:
                self.assertEqual(len(rating), 5)
                self.assertDictContainsSubset(rating, RATING2)

    def test_get_ratings_for_specific_user(self):
        '''
        Get all ratings for user Scott. Check that their ids are 5, 9, 13 and 17.
        '''
        #Ratings sent from Scott are 5, 9, 13 and 17
        print('('+self.test_get_ratings_for_specific_user.__name__+')',
              self.test_get_ratings_for_specific_user.__doc__)
        ratings = self.connection.get_ratings(receiver="Scott")
        self.assertEqual(len(ratings), 4)

        #Ratings id are 5, 9, 13 and 17
        for rating in ratings:
            self.assertIn(rating['rating_id'],
                          ('rating-5', 'rating-9', 'rating-13', 'rating-17'))

    def test_get_ratings_of_specific_user(self):
        '''
        Get all ratings of user Scott. Check that their ids are 1, 2, 3 and 4.
        '''
        #Ratings sent from Scott are 1, 2, 3 and 4.
        print('('+self.test_get_ratings_of_specific_user.__name__+')',
              self.test_get_ratings_of_specific_user.__doc__)
        ratings = self.connection.get_ratings(sender="Scott")
        self.assertEqual(len(ratings), 4)

        #Ratings id are 1, 2, 3 and 4
        for rating in ratings:
            self.assertIn(rating['rating_id'],
                          ('rating-1', 'rating-2', 'rating-3', 'rating-4'))

    def test_modify_rating(self):
        '''
        Test that the rating rating-1 is modifed
        '''
        print('('+self.test_modify_rating.__name__+')', \
              self.test_modify_rating.__doc__)
        resp = self.connection.modify_rating(
            RATING1_ID, RATING1_MODIFIED['rating'])
        self.assertEqual(resp, RATING1_ID)

        #Check that the ratings has been really modified through a get
        resp2 = self.connection.get_rating(RATING1_ID)
        self.assertDictContainsSubset(resp2, RATING1_MODIFIED)

    def test_modify_ratings_malformedid(self):
        '''
        Test that trying to modify rating with id ='2' raises an error
        '''
        print('('+self.test_modify_ratings_malformedid.__name__+')',
              self.test_modify_ratings_malformedid.__doc__)

        #Test with an existing rating
        with self.assertRaises(ValueError):
            self.connection.modify_rating('2', 2)

    def test_modify_ratings_noexistingid(self):
        '''
        Test modify_ratings with rating-200 (no-existing)
        '''
        print('('+self.test_modify_ratings_noexistingid.__name__+')',\
              self.test_modify_ratings_noexistingid.__doc__)

        #Test with an existing rating
        resp = self.connection.modify_rating(WRONG_RATING_ID, 5)
        self.assertIsNone(resp)

    def test_create_rating(self):
        '''
        Test that a new rating can be created
        '''
        print('('+self.test_create_rating.__name__+')',\
              self.test_create_rating.__doc__)
        rating_id = self.connection.create_rating("Knives", "Kim", 3)
        self.assertIsNotNone(rating_id)

        #Get the expected modified rating
        new_rating = {}
        new_rating['sender'] = 'Knives'
        new_rating['receiver'] = 'Kim'
        new_rating['rating'] = 3

        #Check that the ratings has been really modified through a get
        resp2 = self.connection.get_rating(rating_id)
        self.assertDictContainsSubset(new_rating, resp2)

    def test_crate_rating_unregistered_user(self):
        '''
        Test that a new rating can not be created with unregistered user
        '''
        print('('+self.test_create_rating.__name__+')',
              self.test_create_rating.__doc__)

        #Check unregistered user (REE) can't rate
        with self.assertRaises(ValueError):
            rating_id = self.connection.create_rating("REE", "Kim", 3)

    def test_not_contains_rating(self):
        '''
        Check if the database does not contain rating with id rating-200

        '''
        print('('+self.test_not_contains_rating.__name__+')',
              self.test_not_contains_rating.__doc__)
        self.assertFalse(self.connection.contains_rating(WRONG_RATING_ID))

    def test_contains_rating(self):
        '''
        Check if the database contains ratings with id rating-1 and rating-2

        '''
        print('('+self.test_contains_rating.__name__+')', \
              self.test_contains_rating.__doc__)
        self.assertTrue(self.connection.contains_rating(RATING1_ID))
        self.assertTrue(self.connection.contains_rating(RATING2_ID))

if __name__ == '__main__':
    '''

    :references:

    :[1]: Exercise1, forum.database.py
    '''
    print('Start running rating tests')
    unittest.main()
