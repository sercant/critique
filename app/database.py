'''
Created on 17.02.2018

Provides the database API to access the critique persistent data.

@author: sercant
@author: mina
@author: moamen

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
        rating_id INTEGER PRIMARY KEY AUTOINCREMENT,\
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
        :references:

        :[1]: Exercise1, forum.database.py
        '''

        super(Engine, self).__init__()
        if db_path is not None:
            self.db_path = db_path
        else:
            self.db_path = DEFAULT_DB_PATH

    def connect(self):
        '''
        Creates a connection to the database.

        :references:

        :[1]: Exercise1, forum.database.py

        :returns: A Connection instance
        :rtype: Connection

        '''
        return Connection(self.db_path)

    def remove_database(self):
        '''
        Removes the database file from the filesystem.

        :references:

        :[1]: Exercise1, forum.database.py
        '''
        if os.path.exists(self.db_path):
            # THIS REMOVES THE DATABASE STRUCTURE
            os.remove(self.db_path)

    def clear(self):
        '''
        Purge the database removing all records from the tables. However,
        it keeps the database schema (meaning the table structure)

        :references:

        :[1]: Exercise1, forum.database.py

        '''
        # THIS KEEPS THE SCHEMA AND REMOVE VALUES
        keys_on = 'PRAGMA foreign_keys = ON'

        con = sqlite3.connect(self.db_path)
        # Activate foreing keys support
        with con:
            cur = con.cursor()
            cur.execute(keys_on)
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

        :references:

        :[1]: Exercise1, forum.database.py

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

        :references:

        :[1]: Exercise1, forum.database.py

        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()

        # Activate foreing keys support
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

    :references:

    :[1]: Exercise1, forum.database.py

    :param db_path: Location of the database file.
    :type dbpath: str

    '''

    def __init__(self, db_path):
        '''
        :references:

        :[1]: Exercise1, forum.database.py

        '''
        super(Connection, self).__init__()
        self.con = sqlite3.connect(db_path)
        self._isclosed = False

    def isclosed(self):
        '''
        :references:

        :[1]: Exercise1, forum.database.py

        :returns: ``True`` if connection has already being closed.
        '''
        return self._isclosed

    def close(self):
        '''
        :references:

        :[1]: Exercise1, forum.database.py

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

        :references:

        :[1]: Exercise1, forum.database.py


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

        :references:

        :[1]: Exercise1, forum.database.py

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

        :references:

        :[1]: Exercise1, forum.database.py

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
            'bio': row['bio'],
            'avatar': row['avatar'],
            'firstname': row['firstname'],
            'lastname': row['lastname']
        }

    def _create_user_object(self, row):
        '''
        It takes a database Row and transform it into a python dictionary.

        :param dict row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary with the following format:

            .. code-block:: javascript

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

    # Ratings helpers
    def _create_rating_object(self, row):
        '''
        Creates the rating object

        :param row: The row obtained from the database.
        :type row: sqlite3.Row

        :returns: a dictionary with the keys ``rating_id`` (str), ``timestamp`` (int), ``sender`` (str), ``receiver`` (str) and ``rating`` (int)

        '''
        return {
            'rating_id': 'rtg-' + str(row['rating_id']),
            'timestamp': row['timestamp'],
            'sender': row['sender'],
            'receiver': row['receiver'],
            'rating': row['rating']
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
    def get_ratings(self, sender=None, receiver=None):
        '''
        Extracts ratings in the database for a user

        :returns: ratings for each user
            contains following keys: ``id`` (integer), ``timestamp``
            (long representing UNIX timestamp), ``sender`` (str), ``receiver`` (str) and ``rating`` (integer).
            None is returned if the database has no ratings.

        '''

        # Create the SQL Statements
        # SQL Statement for retrieving the ratings
        query = 'SELECT ratings.*, sender.nickname sender, receiver.nickname receiver FROM ratings INNER JOIN users sender on sender.user_id = ratings.sender_id INNER JOIN users receiver on receiver.user_id = ratings.receiver_id'

        pval = None
        if sender is not None or receiver is not None:
            query += " WHERE "
            if sender is not None:
                query += "sender = ?"
                pval = (sender,)
            if receiver is not None:
                if sender is not None:
                    query += " AND "
                query += "receiver = ?"
                if pval is not None:
                    pval = (sender, receiver)
                else:
                    pval = (receiver,)

        # Activate foreign key support
        self.set_foreign_keys_support()

        # Create the cursor
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()

        # Execute main SQL Statement
        if pval is None:
            cur.execute(query)
        else:
            cur.execute(query, pval)

        # Process the results
        rows = cur.fetchall()
        if rows is None:
            return None

        # Process the response.
        rating = []
        for row in rows:
            rating.append(self._create_rating_object(row))
        return rating

    def get_rating(self, rating_id):
        '''
        Extracts rating in the database for given rating id

        :param str rating_id: rating id in the database in format ``rtg-(\d+)``

        :returns: rating information for the given rating id
            contains following keys: ``id`` (integer), ``timestamp``
            (long representing UNIX timestamp), ``sender`` (str), ``receiver`` (str) and ``rating`` (integer).
            None is returned if the rating_id doesn't exist.

        :raises ValueError: when ``rating_id`` is not valid format

        '''

        m = re.match('rtg-(\d+)', rating_id)
        if m is None or m.group(1) is None:
            raise ValueError('rating id is malformed')
        rating_id = int(m.group(1))

        # Create the SQL Statements
        # SQL Statement for retrieving the ratings
        query = 'SELECT ratings.*, sender.nickname sender, receiver.nickname receiver FROM ratings INNER JOIN users sender on sender.user_id = ratings.sender_id INNER JOIN users receiver on receiver.user_id = ratings.receiver_id WHERE ratings.rating_id = ?'

        # Activate foreign key support
        self.set_foreign_keys_support()

        # Create the cursor
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()

        # Execute main SQL Statement
        cur.execute(query, (rating_id,))

        # Process the results
        row = cur.fetchone()
        if row is None:
            return None
        return self._create_rating_object(row)

    def modify_rating(self, rating_id, new_rating):
        '''
        Modify the rating of the rating with id ``rating_id``

        :param str rating_id: The id of the rating to modify. Note that
            rating_id is a string with format rtg-\d+

        :param int new_rating: the rating's rating

        :return: the id of the edited rating or None if the rating was
              not found. The id of the rating has the format ``rtg-\d+``,
              where \d+ is the id of the rating in the database.

        :raises ValueError: if the rating_id has a wrong format.

        '''
        # Extracts the int which is the id for a rating in the database
        match = re.match('rtg-(\d+)', rating_id)
        if match is None:
            raise ValueError("The rating_id is malformed")
        rating_id = int(match.group(1))

        # SQL Statement to update the ratings table
        query = 'UPDATE ratings SET rating = ? WHERE rating_id = ?'

        # Activate foreign key support
        self.set_foreign_keys_support()

        # Cursor and row initialization
        self.con.row_factory = sqlite3.Row

        try:
            cur = self.con.cursor()
            # Execute the statement to extract the id associated to a nickname
            pvalue = (new_rating, rating_id)
            cur.execute(query, pvalue)
            self.con.commit()
        except sqlite3.Error as excp:
            print("Error %s:" % excp.args[0])
            return None

        # Check that I have modified the user
        if cur.rowcount < 1:
            return None
        return 'rtg-' + str(rating_id)

    def delete_rating(self, rating_id=None):
        '''
        Delete the rating with id given as parameter.

        :param rating_id: id of the rating to remove.
        :type rating_id: integer
        :return: True if the message has been deleted, False otherwise
        :raises ValueError: if the rating_id not inserted.

        '''
        if rating_id is None:
            raise ValueError("No rating ID inserted to delete.")
        m=re.search('\d+')
        rating_id = m.group(1)
        queryParameter = (rating_id, )

        # Create the SQL Statement
        query = 'DELETE FROM ratings WHERE rating_id = ?'

        # Activate foreign key support
        self.set_foreign_keys_support()

        # Cursor and row initialization
        self.con.row_factory = sqlite3.Row

        # Execute main SQL Statement
        try:
            # Get the cursor object.
            # It allows to execute SQL code and traverse the result set
            cur = self.con.cursor()
            # execute the pragma command, OFF
            cur.execute(query, queryParameter, [last])
            if cur.rowcount < 1:
                print("No ratings with rating_id = %s" % str(rating_id))
                return False
            print("%s rating deleted" % str(rating_id))
            self.con.commit()
        except sqlite3.Error as excp:
            print("Error %s:" % excp.args[0])
            return False
        return True

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
            # Commit the delete
            self.con.commit()
        except sqlite3.Error as e:
            print("Error %s:" % (e.args[0]))
        return bool(cur.rowcount)

    def create_rating(self, sender, receiver, rating):
        '''
        Create a new rating with the data provided as arguments.

        :param str sender: the nickname of the person who is sending this
            rating.
        :param str receiver: the nickname of the person who is receiving this
            rating.
        :param int rating: rating given to the receiver.

        :return: the id of the created rating or None if the rating created.
            Note that it is a string with the format rtg-\d+.

        :raises DatabaseError: if the database could not be modified.

        :raises ValueError: if the sender or receiver was not found or rating is already given.

        '''

        # check if the rating is given to the user already by the sender
        ratings = self.get_ratings(sender=sender, receiver=receiver)
        if ratings is not None and len(ratings) is not 0:
            raise ValueError(
                'rating is already given by this sender to the receiver. try modifying the rating.')

        # Create the SQL statment
        # SQL Statement for getting the user id given a nickname
        query_user_id = 'SELECT user_id from users WHERE nickname = ?'

        # SQL Statement for inserting the data
        stmnt = 'INSERT INTO ratings(timestamp,sender_id,receiver_id,rating) \
                 VALUES(?,?,?,?)'

        # Variables for the statement.
        # sender_id is obtained from first statement.
        sender_id = None

        # receiver_id is obtained from first statement.
        receiver_id = None
        timestamp = time.mktime(datetime.now().timetuple())

        # Activate foreign key support
        self.set_foreign_keys_support()

        # Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()

        # Provide support for foreign keys
        # Execute SQL Statement to get user_id given nickname
        pvalue = (sender,)
        cur.execute(query_user_id, pvalue)

        # Extract user id
        row = cur.fetchone()
        if row is not None:
            sender_id = row["user_id"]

        # Execute SQL Statement to get user_id given nickname
        pvalue = (receiver,)
        cur.execute(query_user_id, pvalue)

        # Extract user id
        row = cur.fetchone()
        if row is not None:
            receiver_id = row["user_id"]

        if sender_id is None or receiver_id is None:
            raise ValueError('sender or receiver nickname is not found')

        # Generate the values for SQL statement
        pvalue = (timestamp, sender_id, receiver_id, rating)

        # Execute the statement
        cur.execute(stmnt, pvalue)
        self.con.commit()

        # Extract the id of the added rating
        lid = cur.lastrowid

        # Return the id in
        if lid is None:
            return None
        return 'rtg-' + str(lid)

    def _create_post_object(self, row):
        '''
        It takes a :py:class:`sqlite.Row` and transform it into a dictionary
        with key-value pairs.

            :param row: the row returned from the database.
            :type row: sqlite3.Row
            :return: a dictionary containing the following keys:

                * ``post_id``: id of the post
                * ``timestamp``: the time of creation (int)
                * ``sender``: nickname of the sending user
                * ``receiver``: nickname of the receiving user
                * ``reply_to``: if of the parent post
                * ``post_text``: post's text
                * ``rating``: rating of the post given by users (int)
                * ``anonymous``: (int) that represents the anonymity
                    of the post, if "0" it is False, if "1" it is True.
                * ``public``: (int) that represents the publicity
                    of the post, if "0" it is False, if "1" it is True.

        Examples:
            $ cursor.execute(query)
            $ row = cursor.fetchone()
            $ self._create_post_object(row)

        All values are returned as string, containing the value in the
        mentioned data type.

        REFERENCEs:
        -   [1]
        '''
        post = {
            'post_id': row['post_id'],
            'timestamp': row['timestamp'],
            'sender': row['sender'],
            'receiver': row['receiver'],
            'reply_to': row['reply_to'],
            'post_text': row['post_text'],
            'rating': row['rating'],
            'anonymous': row['anonymous'],
            'public': row['public'],
        }

        return post

    def get_post(self, post_id=None):
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
        query = 'SELECT posts.*, sender.nickname sender, receiver.nickname receiver FROM posts INNER JOIN users sender ON sender.user_id = posts.sender_id INNER JOIN users receiver ON receiver.user_id = posts.receiver_id WHERE post_id = ? '

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

    def modify_user(self, nickname, summary, details):
        '''
        Modifies the user in the database.

        :param str nickname: The nickname of the user to modify.

        :param dict summary: Updated version of the summary of the user.
            The dictionary has the following structure:

            .. code-block:: javascript

                    'summary': {
                        'bio': '',
                        'avatar': ''
                    }

        :param dict details: Updated version of the details of the user.
            The dictionary has the following structure:

            .. code-block:: javascript

                    'details': {
                        'firstname': '',
                        'lastname': '',
                        'email': '',
                        'mobile': '',
                        'gender': '',
                        'birthdate': '',
                    }

            where:

            * ``firstname``: given name of the user
            * ``lastname``: family name of the user
            * ``email``: current email of the user.
            * ``mobile``: string showing the user's phone number. Can be None.
            * ``gender``: User's gender ('male' or 'female').
            * ``avatar``: name of the image file used as avatar
            * ``birthdate``: string containing the birth date of the user in yyyy-mm-dd format.
            * ``bio``: text chosen by the user for biography

            Note that all values are string if they are not otherwise indicated.

        :return: the nickname of the modified user or None if the
            ``nickname`` passed as parameter is not in the database.

        :raise ValueError: if the user argument is not well formed.

        '''
        user_id = self.get_user_id_w_nickname(nickname)
        if user_id is None:
            return None

        # Create the SQL Statements
        # SQL Statement to update the user_profile table
        query = 'UPDATE users_profile SET firstname = ?, lastname = ?, email = ?, mobile = ?, gender = ?, avatar = ?, birthdate = ?, bio = ? WHERE user_id = ?'

        _firstname = None if not details else details.get('firstname', None)
        _lastname = None if not details else details.get('lastname', None)
        _email = None if not details else details.get('email', None)
        _mobile = None if not details else details.get('mobile', None)
        _gender = None if not details else details.get('gender', None)
        _avatar = None if not summary else summary.get('avatar', None)
        _birthdate = None if not details else details.get('birthdate', None)
        _bio = None if not summary else summary.get('bio', None)

        # Activate foreign key support
        self.set_foreign_keys_support()

        # Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()

        # execute the main statement
        pvalue = (
            _firstname,
            _lastname,
            _email,
            _mobile,
            _gender,
            _avatar,
            _birthdate,
            _bio,
            user_id,
        )
        cur.execute(query, pvalue)
        self.con.commit()

        # Check that I have modified the user
        if cur.rowcount < 1:
            return None
        return nickname

    def create_user(self, nickname, user):
        '''
        Create a new user in the database.

        :param str nickname: The nickname of the user to modify
        :param dict user: a dictionary with the information to be modified. The
                dictionary has the following structure:

                .. code-block:: javascript

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
            * ``registrationdate``: (Optional) UNIX timestamp when the user registered in the system (long integer)
            * ``lastlogindate``: (Optional) UNIX timestamp when the user last logged in to the system (long integer)
            * ``firstname``: given name of the user
            * ``lastname``: family name of the user
            * ``email``: current email of the user.
            * ``mobile``: string showing the user's phone number. Can be None.
            * ``gender``: User's gender ('male' or 'female').
            * ``avatar``: name of the image file used as avatar
            * ``birthdate``: string containing the birth date of the user in yyyy-mm-dd format.
            * ``bio``: text chosen by the user for biography

            Note that all values are string if they are not otherwise indicated.

        :return: the nickname of the modified user or None if the
            ``nickname`` passed as parameter is not in the database.

        :rtype: str

        :raise ValueError: if the user argument is not well formed.

        '''
        # Check if nickname already exists in the database
        if self.get_user_id_w_nickname(nickname) is not None:
            return None

        # Create the SQL Statements
        # SQL Statement to create the row in  users table
        query1 = 'INSERT INTO users(nickname,regDate,lastLoginDate)\
                  VALUES(?,?,?)'

        # SQL Statement to create the row in user_profile table
        query2 = 'INSERT INTO users_profile (user_id,firstname,lastname, \
                                             email,mobile, \
                                             gender,avatar, \
                                             birthdate,bio)\
                  VALUES (?,?,?,?,?,?,?,?,?)'

        # timestamp will be used for lastlogin and regDate if not provided.
        timestamp = time.mktime(datetime.now().timetuple())

        summary = user.get('summary', None)
        details = user.get('details', None)

        if summary is None or details is None:
            raise ValueError("User dictionary is not well formed")

        # temporal variables for user table
        _firstname = details.get('firstname', None)
        _lastname = details.get('lastname', None)
        _email = details.get('email', None)
        _mobile = details.get('mobile', None)
        _gender = details.get('gender', None)
        _avatar = summary.get('avatar', None)
        _birthdate = details.get('birthdate', None)
        _bio = summary.get('bio', None)
        _registrationdate = summary.get('registrationdate', timestamp)
        _lastlogindate = details.get('lastlogindate', timestamp)

        if _registrationdate is None or _firstname is None:
            raise ValueError(
                "User dictionary is not well formed, registrationdate and firstname can not be None")

        # Activate foreign key support
        self.set_foreign_keys_support()

        # Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()

        # Add the row in users table
        # Execute the statement
        pvalue = (
            nickname,
            _registrationdate,
            _lastlogindate
        )
        cur.execute(query1, pvalue)

        # Extrat the rowid => user-id
        lid = cur.lastrowid

        # Add the row in users_profile table
        # Execute the statement
        pvalue = (
            lid,
            _firstname,
            _lastname,
            _email,
            _mobile,
            _gender,
            _avatar,
            _birthdate,
            _bio,
        )

        cur.execute(query2, pvalue)
        self.con.commit()

        # We do not do any comprobation and return the nickname
        return nickname

    # Utils
    def _get_user_w(self, field, value):
        '''
        Get the key of the database row which contains the user with the given
        field.

        :param str field: The field of the user to search.
        :param str value: The value of the field to match.
        :return: the database attribute user_id or None if ``field`` with ``value`` does
            not exit.
        :rtype: str

        '''
        query = 'SELECT users.user_id FROM users, users_profile \
                 WHERE users.user_id = users_profile.user_id and '                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   + field + ' = ?'

        # Activate foreign key support
        self.set_foreign_keys_support()

        # Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()

        # Execute the  main SQL statement
        pvalue = (value,)
        cur.execute(query, pvalue)

        # Process the response.
        # Just one row is expected
        row = cur.fetchone()
        if row is None:
            return None

        # Build the return object
        else:
            return row[0]

    def get_user_id_w_nickname(self, nickname):
        '''
        Get the key of the database row which contains the user with the given
        nickname.

        :param str nickname: The nickname of the user to search.
        :return: the database attribute user_id or None if ``nickname`` does
            not exit.
        :rtype: str

        '''
        return self._get_user_w('nickname', nickname)

    def get_user_id_w_email(self, email):
        '''
        Get the key of the database row which contains the user with the given
        email.

        :param str email: The email of the user to search.
        :return: the database attribute user_id or None if ``email`` does
            not exit.
        :rtype: str

        '''
        return self._get_user_w('email', email)

    def get_user_id_w_mobile(self, mobile):
        '''
        Get the key of the database row which contains the user with the given
        mobile.

        :param str mobile: The mobile of the user to search.
        :return: the database attribute user_id or None if ``mobile`` does
            not exit.
        :rtype: str

        '''
        return self._get_user_w('mobile', mobile)

    def _create_post_list_object(self, row):
        '''
        used to make list objects for list appending, when the API
        is requested to make a list of a number of tweets.

            :param row: a row obtained from the database
            :type row: sqlite3.Row
            :return: a dictionary with the following keys:

                * ``post_id``: id of the post from the row input
                * ``receiver``: the receiver of the post
                * ``timestamp``: (int) timestamp of the post
                * ``reply_to``: id of the parent post
                * ``post_text``: text of the post
                * ``rating``: rating of the post
                * ``anonymous``: (int) shows the anonymity of the post
                    0 is False, 1 is True
                * ``public``: (int) shows the publicity of the post
                    0 is False, 1 is True
        Note: all returned values are strings, unless otherwise stated.
        '''
        post = {
            'post_id': str(row['post_id']),
            'receiver': row['receiver'],
            'sender': row['sender'],
            'timestamp': row['timestamp'],
            'reply_to': str(row['reply_to']),
            'post_text': row['post_text'],
            'rating': row['rating'],
            'anonymous': row['anonymous'],
            'public': row['public']
        }
        return post

    def get_posts_by_user(self, nickname=None, is_sender=True):
        '''
        Used to retrieve some posts posted by a user.

        :param user_id: default is None, takes the user id of the user
            that you want the posts of. if the parameter is None, it
            will raise a ValueError exception.
        :type nickname: nickname of the user

        :return: a list of posts made by the mentioned user. each
            message is a dictionary containing the keys mentioned in
            :py:meth:`_create_posts_list_object`

            or returns None, if no posts found for the specified
            user.
        '''
        postsCounter = 1
        # check if the user_id is not None
        if nickname is None:
            raise ValueError("No input user nickname input")

        # initialize the query parameter as a tuple
        queryParameter = (nickname, )

        # create the SQL query
        # TODO : this might need to change format
        field = 'sender'
        if not is_sender:
            field = 'receiver'
        query = 'SELECT posts.*, sender.nickname sender, receiver.nickname receiver FROM posts INNER JOIN users sender ON sender.user_id = posts.sender_id INNER JOIN users receiver ON receiver.user_id = posts.receiver_id WHERE ' + field + ' = ? ORDER BY timestamp DESC'

        # set foreign keys support
        self.set_foreign_keys_support()

        # using cursor and row initalization to enable
        # reading and returning the data in a dictionary
        # format, with key-value pairs
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()

        # execute the SQL query
        cur.execute(query, queryParameter)

        # fetching the results
        rows = cur.fetchall()

        # check if there are posts fetched or not
        if rows is None:
            return None

        # initiate the list object to hold the returned posts
        posts = []
        for row in rows:
            post = self._create_post_list_object(row)
            posts.append(post)
        return posts

    def delete_post(self, post_id=None):
        '''
        Delete the post with id given as parameter.

        :param post_id: id of the post to remove.
        :type post_id: integer
        :return: True if the message has been deleted, False otherwise
        :raises ValueError: if the post_id not inserted.

        '''
        if post_id is None:
            raise ValueError("No post ID inserted to delete.")
        queryParameter = (post_id, )

        # Create the SQL Statement
        query = 'DELETE FROM posts WHERE post_id = ?'

        # Activate foreign key support
        self.set_foreign_keys_support()

        # Cursor and row initialization
        self.con.row_factory = sqlite3.Row

        # Execute main SQL Statement
        try:
            # Get the cursor object.
            # It allows to execute SQL code and traverse the result set
            cur = self.con.cursor()
            # execute the pragma command, OFF
            cur.execute(query, queryParameter)
            if cur.rowcount < 1:
                print("No posts with post_id = %s" % str(post_id))
                return False
            print("%s post deleted" % str(post_id))
            self.con.commit()
        except sqlite3.Error as excp:
            print("Error %s:" % excp.args[0])
            return False
        return True

    def contains_user(self, nickname):
        '''
        :returns: ``True`` if the user is in the database else ``False``
        '''
        return self.get_user_id_w_nickname(nickname) is not None

    def contains_user_email(self, email):
        '''
        :returns: ``True`` if the user is in the database else ``False``
        '''
        return self.get_user_id_w_email(email) is not None

    def contains_user_extended(self, nickname, email):
        '''
        :returns: ``True`` if the user is in the database else ``False``
        '''
        return self.get_user_id_w_nickname(nickname) is not None or self.get_user_id_w_email(email) is not None

    def contains_rating(self, rating_id):
        '''
        :returns: ``True`` if the rating is in the database else ``False``
        '''
        rating = self.get_rating(rating_id)

        return rating is not None

    def contains_post(self, post_id):
        '''
        :returns: ``True`` if the post is in the database, else ``False``
        '''

        return self.get_post(post_id) is not None

    def modify_post(self, post_id, post_text):
        '''
        Modify the body text with the id ``post_id``

        :param int post_id: The id of the post to remove.
        :param str post_text: the post's content
        :return: the id of the edited post or None if the post was
              not found.
        :raises ValueError: if the post id not input.

        '''
        # SQL Statement to update the messages table
        query = 'UPDATE posts SET post_text = ? WHERE post_id = ?'

        # Activate foreign key support
        self.set_foreign_keys_support()

        # Cursor and row initialization
        self.con.row_factory = sqlite3.Row

        try:
            cur = self.con.cursor()
            # Execute the statement to extract the id associated to a nickname
            pvalue = (post_text, post_id)
            cur.execute(query, pvalue)
            self.con.commit()
        except sqlite3.Error as excp:
            print("Error %s:" % excp.args[0])
            return None

        # Check that I have modified the user
        if cur.rowcount < 1:
            print("I am making NONE")
            return None
        return post_id

    def create_post(self, sender_nickname=None, receiver_nickname=None, reply_to=None, post_text=None, anonymous=None, public=None, rating=None):
        '''
        Create a new post with the data provided as arguments.

        :param str sender_nickname: the post's sender
        :param str receiver_nickname: the post's receiver
        :param int reply_to: the id of the parent post (if any)
        :param str post_text: the body text of the post
        :param int anonymous: the anonymity of the post, 0 is False,
                            1 is True.
        :param int public: the publicity of the post, 0 is False,
                            1 is True.
        :return: the id of the created post or None if the reply_to post was
            not found.

        :raises ForumDatabaseError: if the database could not be modified.
        :raises ValueError: if the replyto has a wrong format.

        '''
        if reply_to is not None:
            # there can not be a rating.
            rating = None

        if sender_nickname is None:
            raise ValueError("No input Sender nickname")
        if receiver_nickname is None:
            raise ValueError("No input Receiver nickname")
        if post_text is None:
            raise ValueError("Empty post")

        if anonymous is None:
            anonymous = 1
        if public is None:
            public = 1

        # Create the SQL statment
        # SQL to test that the message which I am answering does exist
        query1 = 'SELECT * from posts WHERE post_id = ?'

        # SQL Statement for getting the user id given a nickname
        query2 = 'SELECT user_id from users WHERE nickname = ?'

        # SQL Statement for inserting the data
        stmnt = 'INSERT INTO posts (timestamp,sender_id,receiver_id,reply_to, \
                 post_text,rating,anonymous,public) \
                 VALUES(?,?,?,?,?,?,?,?)'

        # Variables for the statement.
        # sender_id is obtained from executing query2 statement.
        # and timestamp is calculated with a function
        sender_id = None
        receiver_id = None
        timestamp = time.mktime(datetime.now().timetuple())

        # Activate foreign key support
        self.set_foreign_keys_support()

        # Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()

        # If exists the replyto argument, check that the post exists in
        # the database table
        if reply_to is not None:
            pvalue = (reply_to,)
            cur.execute(query1, pvalue)
            posts = cur.fetchall()
            if len(posts) < 1:
                return None

        # Execute SQL Statement to get sender id given nickname
        pvalue = (sender_nickname,)
        cur.execute(query2, pvalue)

        # Extract user id
        row = cur.fetchone()
        if row is not None:
            sender_id = row["user_id"]
        else:
            return None

        # Execute SQL Statement to get sender id given nickname
        pvalue = (receiver_nickname,)
        cur.execute(query2, pvalue)

        # Extract user id
        row = cur.fetchone()
        if row is not None:
            receiver_id = row["user_id"]
        else:
            return None

        # Generate the values for SQL statement
        pvalue = (timestamp, sender_id, receiver_id, reply_to,
                  post_text, rating, anonymous, public)

        # Execute the statement
        cur.execute(stmnt, pvalue)
        self.con.commit()

        # Extract the id of the added message
        lid = cur.lastrowid

        # Return the id in
        return lid if lid is not None else None
