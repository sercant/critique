'''
Created on 20.02.2018


Database interface testing for all posts related methods.

A post object is a dictionary which contains the following keys:
    -    post_id: (int) id of the post
    -    timestamp: UNIX timestamp (long integer) that specifies when the
                    post was created.
    -    sender_id: (int) id of the owner of the post.
    -    receiver_id: (int) id of the receiver of the post.
    -    reply_to: (int) id of the parent post.
    -    post_text: post's text.
    -    rating: (int) represents the rating of the post
    -    anonymous: (int) shows the anonymity of the post.
                    0 is False, 1 is True
    -    public: (int) shows the anonymity of the post.
                    0 is False, 1 is True

A posts' list has the following format:
[   {'post_id':'', 'timestamp':'', 'receiver_id':'', 'reply_to':'',
     'post_text':'', 'rating':'', 'anonymous':'', 'public':''},
    {'post_id':'', 'timestamp':'', 'receiver_id':'', 'reply_to':'',
     'post_text':'', 'rating':'', 'anonymous':'', 'public':''},
     ...  ]

@author: Mina
REFERENCEs:
-   Programmable Web Projects, Exercise 1, database_api_tests_messages.py
'''
#   importing the important modules
import sqlite3, unittest

#   load the database
from app import database 

#   path to the database file.
DB_PATH = 'db/critique_test.db'
ENGINE = database.Engine(DB_PATH)




if __name__ == '__main__':
    print('Start running posts tests...')
    unittest.main()