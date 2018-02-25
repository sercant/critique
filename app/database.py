'''
Created on 17.02.2018

Provides the database API to access the critique persistent data.

@author: sercant
@author: mina

    REFERENCEs:
    -   [1] Programmable Web Project, Exercise1, forum.database.py
'''

from datetime import datetime
import time
import sqlite3
import re
import os

# Default paths for .db and .sql files to create and populate the database.
DEFAULT_DB_PATH = 'db/critique.db'
DEFAULT_SCHEMA = "db/critique_schema_dump.sql"
DEFAULT_DATA_DUMP = "db/critique_data_dump.sql"


class Engine(object):
   
    # SQL command to create users table
    create_users_sql = \
        'CREATE TABLE IF NOT EXISTS users(\
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,\
        nickname TEXT UNIQUE,\
        regDate INTEGER NOT NULL,\
        lastLoginDate INTEGER)'

    # SQL command to create user_profile table
    create_users_profile_sql = \
        'CREATE TABLE IF NOT EXISTS users_profile(\
        user_id INTEGER PRIMARY KEY,\
        firstname TEXT NOT NULL,\
        lastname TEXT,\
        email TEXT UNIQUE,\
        mobile TEXT UNIQUE,\
        gender TEXT,\
        avatar TEXT,\
        birthdate TEXT,\
        bio TEXT,\
        FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE)'
    
    # SQL command to create posts table
    create_posts_sql = \
        'CREATE TABLE IF NOT EXISTS posts(\
        post_id INTEGER PRIMARY KEY AUTOINCREMENT,\
        timestamp INTEGER NOT NULL,\
        sender_id INTEGER NOT NULL,\
        receiver_id INTEGER,\
        reply_to INTEGER,\
        post_text TEXT NOT NULL,\
        rating INTEGER,\
        anonymous INTEGER NOT NULL,\
        public INTEGER NOT NULL,\
        FOREIGN KEY(sender_id) REFERENCES users(user_id) ON DELETE CASCADE,\
        FOREIGN KEY(receiver_id) REFERENCES users(user_id) ON DELETE CASCADE,\
        FOREIGN KEY(reply_to) REFERENCES posts(post_id) ON DELETE CASCADE)'
    
    # SQL command to create ratings table
    create_ratings_sql = \
        'CREATE TABLE IF NOT EXISTS ratings(\
        ratings_id INTEGER PRIMARY KEY AUTOINCREMENT,\
        timestamp INTEGER NOT NULL,\
        sender_id INTEGER NOT NULL,\
        receiver_id INTEGER NOT NULL,\
        rating INTEGER NOT NULL,\
        FOREIGN KEY(sender_id) REFERENCES users(user_id) ON DELETE CASCADE,\
        FOREIGN KEY(receiver_id) REFERENCES users(user_id) ON DELETE CASCADE)'

    '''
    Abstraction of the database.

    It includes tools to create, configure,
    populate and connect to the sqlite file. You can access the Connection
    instance, and hence, to the database interface itself using the method
    :py:meth:`connection`.

    :Example:

    >>> engine = Engine()
    >>> con = engine.connect()

    :param db_path: The path of the database file (always with respect to the
        calling script. If not specified, the Engine will use the file located
        at *db/critique.db*

    '''

    def __init__(self, db_path=None):
        '''
        '''

        super(Engine, self).__init__()
        if db_path is not None:
            self.db_path = db_path
        else:
            self.db_path = DEFAULT_DB_PATH

    def connect(self):
        '''
        Creates a connection to the database.

        :returns: A Connection instance
        :rtype: Connection

        '''
        return Connection(self.db_path)

    def remove_database(self):
        '''
        Removes the database file from the filesystem.

        '''
        if os.path.exists(self.db_path):
            # THIS REMOVES THE DATABASE STRUCTURE
            os.remove(self.db_path)

    def clear(self):
        '''
        Purge the database removing all records from the tables. However,
        it keeps the database schema (meaning the table structure)

        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        # THIS KEEPS THE SCHEMA AND REMOVE VALUES
        con = sqlite3.connect(self.db_path)
        # Activate foreing keys support
        cur = con.cursor()
        cur.execute(keys_on)
        with con:
            cur = con.cursor()
            # NOTE Since we have delete on cascade on all the tables to users
            # deleting the user will also delete all other entries
            cur.execute("DELETE FROM users")

    # METHODS TO CREATE AND POPULATE A DATABASE USING DIFFERENT SCRIPTS
    def create_tables(self, schema=None):
        '''
        Create programmatically the tables from a schema file.

        :param schema: path to the .sql schema file. If this parmeter is
            None, then *db/critique_schema_dump.sql* is utilized.

        '''
        con = sqlite3.connect(self.db_path)
        if schema is None:
            schema = DEFAULT_SCHEMA
        try:
            with open(schema, encoding="utf-8") as f:
                sql = f.read()
                cur = con.cursor()
                cur.executescript(sql)
        finally:
            con.close()

    def populate_tables(self, dump=None):
        '''
        Populate programmatically the tables from a dump file.

        :param dump:  path to the .sql dump file. If this parmeter is
            None, then *db/critique_data_dump.sql* is utilized.

        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        con = sqlite3.connect(self.db_path)
        # Activate foreing keys support
        cur = con.cursor()
        cur.execute(keys_on)
        # Populate database from dump
        if dump is None:
            dump = DEFAULT_DATA_DUMP
        try:
            with open(dump, encoding="utf-8") as f:
                sql = f.read()
                cur = con.cursor()
                cur.executescript(sql)
        finally:
            con.close()

    # METHODS TO CREATE THE TABLES PROGRAMMATICALLY WITHOUT USING SQL SCRIPT
    def create_users_table(self):
        '''
        Create the table ``users`` programmatically, without using .sql file.

        Print an error message in the console if it could not be created.

        :returns: ``True`` if the table was successfully created or ``False``
            otherwise.

        '''
        return self._execute_statement(self.create_users_sql)

    def create_user_profile_table(self):
        '''
        Create the table ``users_profile`` programmatically, without using .sql file.

        Print an error message in the console if it could not be created.

        :returns: ``True`` if the table was successfully created or ``False``
            otherwise.

        '''
        return self._execute_statement(self.create_users_profile_sql)

    def create_posts_table(self):
        '''
        Create the table ``posts`` programmatically, without using .sql file.

        Print an error message in the console if it could not be created.

        :returns: ``True`` if the table was successfully created or ``False``
            otherwise.

        '''
        return self._execute_statement(self.create_posts_sql)

    def create_ratings_table(self):
        '''
        Create the table ``ratings`` programmatically, without using .sql file.

        Print an error message in the console if it could not be created.

        :returns: ``True`` if the table was successfully created or ``False``
            otherwise.

        '''
        return self._execute_statement(self.create_ratings_sql)

    def _execute_statement(self, statement):
        '''
        Execute a given sql statement with foreign key support on

        Print an error message in the console if it could not be created.

        :param statement: A ``string`` sql statement to be executed.

        :returns: ``True`` if the sql successfully executed or ``False``
            otherwise.

        '''
        con = sqlite3.connect(self.db_path)
        with con:
            cur = con.cursor()
            try:
                result = con.set_foreign_keys_support()
                if not result:
                    raise Exception('Couldn\'t set foreign key support')
                # execute the statement
                cur.execute(statement)
            except sqlite3.Error as e:
                print("Error %s:" % e.args[0])
                return False
        return True


class Connection(object):
    '''
    API to access the critique database.

    The sqlite3 connection instance is accessible to all the methods of this
    class through the :py:attr:`self.con` attribute.

    An instance of this class should not be instantiated directly using the
    constructor. Instead use the :py:meth:`Engine.connect`.

    Use the method :py:meth:`close` in order to close a connection.
    A :py:class:`Connection` **MUST** always be closed once when it is not going to be
    utilized anymore in order to release internal locks.

    :param db_path: Location of the database file.
    :type dbpath: str

    '''

    def __init__(self, db_path):
        super(Connection, self).__init__()
        self.con = sqlite3.connect(db_path)
        self._isclosed = False

    def isclosed(self):
        '''
        :returns: ``True`` if connection has already being closed.
        '''
        return self._isclosed

    def close(self):
        '''
        Closes the database connection, commiting all changes.

        '''
        if self.con and not self._isclosed:
            self.con.commit()
            self.con.close()
            self._isclosed = True

    # FOREIGN KEY STATUS
    def check_foreign_keys_status(self):
        '''
        Check if the foreign keys has been activated.

        :returns: ``True`` if  foreign_keys is activated and ``False`` otherwise.
        :raises sqlite3.Error: when a sqlite3 error happen. In this case the
            connection is closed.

        '''
        try:
            # Create a cursor to receive the database values
            cur = self.con.cursor()
            # Execute the pragma command
            cur.execute('PRAGMA foreign_keys')
            # We know we retrieve just one record: use fetchone()
            data = cur.fetchone()
            is_activated = data == (1,)
            print("Foreign Keys status: %s" % 'ON' if is_activated else 'OFF')
        except sqlite3.Error as excp:
            print("Error %s:" % excp.args[0])
            self.close()
            raise excp
        return is_activated

    def set_foreign_keys_support(self):
        '''
        Activate the support for foreign keys.

        :returns: ``True`` if operation succeed and ``False`` otherwise.

        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        try:
            # Get the cursor object.
            # It allows to execute SQL code and traverse the result set
            cur = self.con.cursor()
            # execute the pragma command, ON
            cur.execute(keys_on)
            return True
        except sqlite3.Error as excp:
            print("Error %s:" % excp.args[0])
            return False

    def unset_foreign_keys_support(self):
        '''
        Deactivate the support for foreign keys.

        :returns: ``True`` if operation succeed and ``False`` otherwise.

        '''
        keys_on = 'PRAGMA foreign_keys = OFF'
        try:
            # Get the cursor object.
            # It allows to execute SQL code and traverse the result set
            cur = self.con.cursor()
            # execute the pragma command, OFF
            cur.execute(keys_on)
            return True
        except sqlite3.Error as excp:
            print("Error %s:" % excp.args[0])
            return False

    # Helpers
    # Users Helpers
    def _create_user_list_object(self, row):
        '''
        Same as :py:meth:`_create_post_object`. However, the resulting
        dictionary is targeted to build messages in a list.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row

        :returns: a dictionary with the keys ``nickname`` (str), ``registrationdate``
            (long representing UNIX timestamp), ``bio`` (str) and ``avatar`` (str)

        '''
        return {
            'nickname': row['nickname'],
            'registrationdate': row['regDate'],
            'bio': row['bio'],
            'avatar': row['avatar']
        }

    def _create_user_object(self, row):
        '''
        It takes a database Row and transform it into a python dictionary.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary with the following format:

            .. code-block:: javascript

                {
                    'summary': {
                        'nickname': '',
                        'registrationdate': ,
                        'bio': '',
                        'avatar': '']
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

            Note that all values are string if they are not otherwise indicated.

        '''
        return {
            'summary': {
                'nickname': row['nickname'],
                'registrationdate': row['regDate'],
                'bio': row['bio'],
                'avatar': row['avatar']
            },
            'details': {
                'lastlogindate': row['lastLoginDate'],
                'firstname': row['firstname'],
                'lastname': row['lastname'],
                'email': row['email'],
                'mobile': row['mobile'],
                'gender': row['gender'],
                'birthdate': row['birthdate'],
            }
        }

    # Database API

    # User API
    def get_users(self):
        '''
        Extracts all users in the database.

        :returns: list of Users of the database. Each user is a dictionary
            that contains following keys: ``nickname`` (str), ``registrationdate``
            (long representing UNIX timestamp), ``bio`` (str) and ``avatar`` (str). None is returned if the database
            has no users.

        '''
        # Create the SQL Statements
        # SQL Statement for retrieving the users
        query = 'SELECT users.*, users_profile.* FROM users, users_profile \
                 WHERE users.user_id = users_profile.user_id'
        # Activate foreign key support
        self.set_foreign_keys_support()
        # Create the cursor
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        # Execute main SQL Statement
        cur.execute(query)
        # Process the results
        rows = cur.fetchall()
        if rows is None:
            return None
        # Process the response.
        users = []
        for row in rows:
            users.append(self._create_user_list_object(row))
        return users

    def get_user(self, nickname):
        '''
        Extracts all the information of a user.

        :param str nickname: The nickname of the user to search for.
        :returns: dictionary with the format provided in the method:
            :py:meth:`_create_user_object`

        '''
        # Create the SQL Statements
        # SQL Statement for retrieving the user given a nickname
        query1 = 'SELECT user_id from users WHERE nickname = ?'
        # SQL Statement for retrieving the user information
        query2 = 'SELECT users.*, users_profile.* FROM users, users_profile \
                  WHERE users.user_id = ? \
                  AND users_profile.user_id = users.user_id'
        # Variable to be used in the second query.
        user_id = None
        # Activate foreign key support
        self.set_foreign_keys_support()
        # Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        # Execute SQL Statement to retrieve the id given a nickname
        pvalue = (nickname,)
        cur.execute(query1, pvalue)
        # Extract the user id
        row = cur.fetchone()
        if row is None:
            return None
        user_id = row["user_id"]
        # Execute the SQL Statement to retrieve the user information.
        # Create first the valuse
        pvalue = (user_id, )
        # execute the statement
        cur.execute(query2, pvalue)
        # Process the response. Only one possible row is expected.
        row = cur.fetchone()
        return self._create_user_object(row)

    # Ratings API
    def get_ratings(self):
        '''
        Extracts ratings in the database for a user

        :returns: ratings for each user 
            contains following keys: ``id`` (integer), ``timestamp``
            (long representing UNIX timestamp), ``sender`` (str), ``receiver`` (str) and ``rating`` (integer). 
            None is returned if the database has no users.

        '''

        # Create the SQL Statements
        # SQL Statement for retrieving the users
        query = 'SELECT rating.*, sender_id.*, receiver_id.*, FROM users, ratings \
                 WHERE users.user_id = ratings.sender_id \
                 AND users.user_id = ratings.receiver_id'
        # Activate foreign key support
        self.set_foreign_keys_support()
        # Create the cursor
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        # Execute main SQL Statement
        cur.execute(query)
        # Process the results
        rows = cur.fetchall()
        if rows is None:
            return None
        # Process the response.
        rating = []
        for row in rows:
            rating.append(self._create_ratings_list(row))
        return rating
    def delete_user(self, nickname):
        '''
        Deletes the user from the database.

        :param str nickname: The nickname of the user to delete.

        :returns: ``True`` if user is successfully deleted else ``False``.

        '''
        # Create the SQL Statements
        # SQL Statement for deleting the user with nickname
        query = 'DELETE from users WHERE nickname = ?'
        # Activate foreign key support
        self.set_foreign_keys_support()
        # Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        pvalue = (nickname,)
        try:
            cur.execute(query, pvalue)
            #Commit the delete
            self.con.commit()
        except sqlite3.Error as e:
            print("Error %s:" % (e.args[0]))
        return bool(cur.rowcount)

    def _create_post_object(self, row):
        '''
        It takes a :py:class:`sqlite.Row` and transform it into a dictionary
        with key-value pairs.

            :param row: the row returned from the database. 
            :type row: sqlite3.Row
            :return: a dictionary containing the following keys:

                * ``post_id``: id of the post
                * ``timestamp``: the time of creation (int)
                * ``sender_id``: id of the sending user
                * ``receiver_id``: id of the receiving user
                * ``reply_to``: if of the parent post
                * ``rating``: rating of the post given by users (int)
                * ``anonymous``: (int) that represents the anonymity 
                    of the post, if "0" it is False, if "1" it is True.
                * ``public``: (int) that represents the publicity 
                    of the post, if "0" it is False, if "1" it is True.

        All values are returned as string, containing the value in the 
        mentioned data type.
        '''
        post = {
            'post_id'  = str(row['post_id']),
            'timestamp' = row['timestamp'],
            'sender_id' = str(row['sender_id']),
            'receiver_id' = str(row['receiver_id']),
            'reply_to' = str(row['reply_to']),
            'rating' = row['rating'],
            'anonymity' = row['anonymous'],
            'publicity' = row['public'],
        }

        return post

    def get_post(self, post_id):
        '''
        GETs a post from the database using the post_id
        as a query parameter

        :param post_id: post id in the database, which is of
            the type (int)

        :return: returns a dictionary with all the attributes
            of the message. the format is provided in
            :py:meth:`_create_post_object`
            or returns None if the post_id is not matching any ids.
        
        :raises ValueError: when ``post_id`` is not valid format

        REFERENCEs:
        -   [1]
        '''
        # first check if the input is valid
        if post_id is None:
            raise ValueError("No input post id")
        # setting foreign keys support
        self.set_foreign_keys_support()
        # initializing the SQL query
        query = 'SELECT * FROM posts WHERE post_id = ?'
        # using cursor and row initalization to enable 
        # reading and returning the data in a dictionary
        # format, with key-value pairs
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        # putting the query parameter in a tuple
        # to be able to execute.
        queryPostId = (post_id,)
        cur.execute(query, queryPostId)
        # checking if the returned value contains a post
        # or not. if not, function will return None
        row = cur.fetchone()
        if row is None:
            return None
        # however, in case it has returned an actual post
        # it has to be parsed before returning
        return self._create_post_object(row)
