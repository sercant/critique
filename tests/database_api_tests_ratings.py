'''
Created on 25.02.2018
Database interface testing for all users related methods.

A ratings object is a dictionary which contains the following keys:
      - ratingsid: id of the message (int)
      - timestamp: UNIX timestamp (long integer) that specifies when the
                   message was created.
      - sender: The nickname of the message's creator
      - reciever: The nickname of the message's reciever
      - rating: The rating the sender send to reciever.

A rating' list has the following format:
[{'ratingid':'', 'timestamp':, 'sender':'', 'reciever':'', 'rating':'',}]

@author: moamen
'''

import sqlite3, unittest

from forum import database

#Path to the database file, different from the deployment db
DB_PATH = 'db/forum_test.db'
ENGINE = database.Engine(DB_PATH)


#CONSTANTS DEFINING DIFFERENT USERS AND USER PROPERTIES
RATING1_ID = 'rating-1'

RATING1 = {'ratings_id': 'rating-1',
            'timestamp': 1362017481, 
            'receiver': 'Scott', 
            'sender': 'Young',
            'rating': 7}

RATING1_MODIFIED = {'ratings_id': RATING1_ID,
                     'timestamp': 1362017481, 
                     'receiver': 'Young',
                     'sender': 'Kim', 
                     'rating': 5}

RATING2_ID = 'rating-10'

RATING2 = {'ratings_id': 'rating-10',
            'timestamp': 1362017481,
            'receiver': 'Knives',
            'sender': 'Kim',
            'rating': 9}

WRONG_RATING_ID = 'rating-200'

INITIAL_SIZE = 17


class RatingDBAPITestCase(unittest.TestCase):
    '''
    Test cases for the ratings related methods.
    '''
    #INITIATION AND TEARDOWN METHODS
    @classmethod
    def setUpClass(cls):
        ''' Creates the database structure. Removes first any preexisting
            database file
        '''
        print("Testing ", cls.__name__)
        ENGINE.remove_database()
        ENGINE.create_tables()

    @classmethod
    def tearDownClass(cls):
        '''Remove the testing database'''
        print("Testing ENDED for ", cls.__name__)
        ENGINE.remove_database()

    def setUp(self):
        '''
        Populates the database
        '''
        try:
          #This method load the initial values from forum_data_dump.sql
          ENGINE.populate_tables()
          #Creates a Connection instance to use the API
          self.connection = ENGINE.connect()
        except Exception as e: 
        #For instance if there is an error while populating the tables
          ENGINE.clear()

    def tearDown(self):
        '''
        Close underlying connection and remove all records from database
        '''
        self.connection.close()
        ENGINE.clear()

    def test_ratings_table_created(self):
        '''
        Checks that the table initially contains 17 ratings (check
        forum_data_dump.sql). 
        
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

    def test_create_ratings_object(self):
        '''
        Check that the method _create_ratings_object works return adequate
        values for the first database row. NOTE: Do not use Connection instace
        to extract data from database but call directly SQL.
        '''
        print('('+self.test_create_ratings_object.__name__+')', \
              self.test_create_ratings_object.__doc__)
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM messages WHERE message_id = 1'
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
        ratings = self.connection._create_ratings_object(row)
        self.assertDictContainsSubset(ratings, RATING1)

    def test_get_ratings(self):
        '''
        Test get_ratings with id msg-1 and msg-10
        '''
        print('('+self.test_get_ratings.__name__+')', \
              self.test_get_ratings.__doc__)
        #Test with an existing message
        ratings = self.connection.get_ratings(RATING1_ID)
        self.assertDictContainsSubset(ratings, RATING1)
        ratings = self.connection.get_ratings(MESSAGE2_ID)
        self.assertDictContainsSubset(ratings, RATING1)

    def test_get_ratings_malformedid(self):
        '''
        Test get_ratings with id 1 (malformed)
        '''
        print('('+self.test_get_ratings_malformedid.__name__+')', \
              self.test_get_ratings_malformedid.__doc__)
        #Test with an existing message
        with self.assertRaises(ValueError):
            self.connection.get_ratings('1')

    def test_get_ratings_noexistingid(self):
        '''
        Test get_ratings with msg-200 (no-existing)
        '''
        print('('+self.test_get_ratings_noexistingid.__name__+')',\
              self.test_get_ratings_noexistingid.__doc__)
        #Test with an existing message
        ratings = self.connection.get_ratings(WRONG_RATING_ID)
        self.assertIsNone(ratings)

    def test_get_ratings(self):
        '''
        Test that get_messages work correctly
        '''
        print('('+self.test_get_ratings.__name__+')', self.test_get_ratings.__doc__)
        ratings = self.connection.get_ratings()
        #Check that the size is correct
        self.assertEqual(len(ratings), INITIAL_SIZE)
        #Iterate throug ratings and check if the ratings with RATING1_ID and
        #MESSAGE2_ID are correct:
        for rating in messages:
            if rating['ratings_id'] == RATING1_ID:
                self.assertEqual(len(rating), 4)
                self.assertDictContainsSubset(rating, RATING1)
            elif ratings['ratings_id'] == RATING2_ID:
                self.assertEqual(len(rating), 4)
                self.assertDictContainsSubset(rating, RATING2)

    def test_get_ratings_specific_user(self):
        '''
        Get all ratings from user Mystery. Check that their ids are 13 and 14.
        '''
        #Ratings sent from Mystery are 13 and 14
        print('('+self.test_get_ratings_specific_user.__name__+')', \
              self.test_get_ratings_specific_user.__doc__)
        ratings = self.connection.get_ratings(nickname="Mystery")
        self.assertEqual(len(ratings), 2)
        #Ratings id are 13 and 14
        for rating in ratings:
            self.assertIn(rating['ratings_id'], ('rating-13', 'rating-14'))
            self.assertNotIn(rating['ratings_id'], ('rating-1', 'rating-2',
                                                    'rating-3', 'rating-4'))

    def test_modify_rating(self):
        '''
        Test that the rating rating-1 is modifed
        '''
        print('('+self.test_modify_ratings.__name__+')', \
              self.test_modify_ratings.__doc__)
        resp = self.connection.modify_rating(RATING1_ID, "new title",
                                              "new body", "new editor")
        self.assertEqual(resp, RATING1_ID)
        #Check that the messages has been really modified through a get
        resp2 = self.connection.get_ratings(RATING1_ID)
        self.assertDictContainsSubset(resp2, RATING1_MODIFIED)

    def test_modify_ratings_malformedid(self):
        '''
        Test that trying to modify message wit id ='2' raises an error
        '''
        print('('+self.test_ratings_message_malformedid.__name__+')',\
              self.test_ratings_message_malformedid.__doc__)
        #Test with an existing message
        with self.assertRaises(ValueError):
            self.connection.modify_message('1', "new title", "new body",
                                           "editor")

    def test_modify_ratings_noexistingid(self):
        '''
        Test modify_ratings with  msg-200 (no-existing)
        '''
        print('('+self.test_modify_ratings_noexistingid.__name__+')',\
              self.test_modify_ratings_noexistingid.__doc__)
        #Test with an existing message
        resp = self.connection.modify_message(WRONG_MESSAGE_ID, "new title",
                                              "new body", "editor")
        self.assertIsNone(resp)

    def test_create_rating(self):
        '''
        Test that a new rating can be created
        '''
        print('('+self.test_create_ratings.__name__+')',\
              self.test_create_ratings.__doc__)
        ratingid = self.connection.create_ratings("new title", "new body",
                                                   "Koodari")
        self.assertIsNotNone(ratingid)
        #Get the expected modified rating
        new_rating = {}
        new_rating['title'] = 'new title'
        new_rating['body'] = 'new body'
        new_rating['sender'] = 'Koodari'
        #Check that the messages has been really modified through a get
        resp2 = self.connection.get_message(ratingid)
        self.assertDictContainsSubset(new_rating, resp2)
        #CHECK NOW NOT REGISTERED USER
        ratingid = self.connection.create_rating("new title", "new body",
                                                   "anonymous_User")
        self.assertIsNotNone(ratingid)
        #Get the expected modified message
        new_rating = {}
        new_rating['title'] = 'new title'
        new_rating['body'] = 'new body'
        new_rating['sender'] = 'anonymous_User'
        #Check that the messages has been really modified through a get
        resp2 = self.connection.get_message(ratingid)
        self.assertDictContainsSubset(new_rating, resp2)

    def test_not_contains_ratings(self):
        '''
        Check if the database does not contain ratings with id rating-200

        '''
        print('('+self.test_contains_ratings.__name__+')', \
              self.test_contains_ratings.__doc__)
        self.assertFalse(self.connection.contains_ratings(WRONG_MESSAGE_ID))

    def test_contains_ratings(self):
        '''
        Check if the database contains ratings with id msg-1 and msg-10

        '''
        print('('+self.test_contains_ratings.__name__+')', \
              self.test_contains_ratings.__doc__)
        self.assertTrue(self.connection.contains_ratings(RATING1_ID))
        self.assertTrue(self.connection.contains_ratings(RATING2_ID))

if __name__ == '__main__':
    print('Start running rating tests')
    unittest.main()
