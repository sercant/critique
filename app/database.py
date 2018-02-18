'''
Created on 17.02.2018

Provides the database API to access the critique persistent data.

@author: sercant
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
    create_users_sql = \
        'CREATE TABLE IF NOT EXISTS users(\
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,\
        nickname TEXT UNIQUE,\
        regDate INTEGER NOT NULL,\
        lastLogin INTEGER)'
    create_user_profile_sql = \
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
    create_posts_sql = \
        'CREATE TABLE IF NOT EXISTS posts(\
        post_id INTEGER PRIMARY KEY AUTOINCREMENT,\
        timestamp INTEGER NOT NULL,\
        sender_id INTEGER NOT NULL,\
        receiver_id INTEGER NOT NULL,\
        reply_to TEXT,\
        post_text TEXT NOT NULL,\
        rating INTEGER,\
        anonymous INTEGER NOT NULL,\
        public INTEGER NOT NULL,\
        FOREIGN KEY(sender_id) REFERENCES users(user_id) ON DELETE CASCADE,\
        FOREIGN KEY(receiver_id) REFERENCES users(user_id) ON DELETE CASCADE,\
        FOREIGN KEY(reply_to) REFERENCES posts(post_id) ON DELETE CASCADE)'
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

        :return: A Connection instance
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

        :return: ``True`` if the table was successfully created or ``False``
            otherwise.

        '''
        return self._execute_statement(self.create_users_sql)

    def create_user_profile_table(self):
        '''
        Create the table ``users_profile`` programmatically, without using .sql file.

        Print an error message in the console if it could not be created.

        :return: ``True`` if the table was successfully created or ``False``
            otherwise.

        '''
        return self._execute_statement(self.create_user_profile_sql)

    def create_posts_table(self):
        '''
        Create the table ``posts`` programmatically, without using .sql file.

        Print an error message in the console if it could not be created.

        :return: ``True`` if the table was successfully created or ``False``
            otherwise.

        '''
        return self._execute_statement(self.create_posts_sql)

    def create_ratings_table(self):
        '''
        Create the table ``ratings`` programmatically, without using .sql file.

        Print an error message in the console if it could not be created.

        :return: ``True`` if the table was successfully created or ``False``
            otherwise.

        '''
        return self._execute_statement(self.create_ratings_sql)

    def _execute_statement(self, statement):
        '''
        Execute a given sql statement with foreign key support on

        Print an error message in the console if it could not be created.

        :param statement: A ``string`` sql statement to be executed. 

        :return: ``True`` if the sql successfully executed or ``False``
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
        :return: ``True`` if connection has already being closed.  
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

        :return: ``True`` if  foreign_keys is activated and ``False`` otherwise.
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

        :return: ``True`` if operation succeed and ``False`` otherwise.

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

        :return: ``True`` if operation succeed and ``False`` otherwise.

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
