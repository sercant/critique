"""
Created on 01.05.2018
@author: sercant
"""

import unittest
import copy
import json

import flask

import app.resources as resources
import app.database as database

DB_PATH = "db/forum_test.db"
ENGINE = database.Engine(DB_PATH)

MASON_JSON = "application/vnd.mason+json"
JSON = "application/json"
CRITIQUE_USER_PROFILE = "/profiles/user-profile/"
ATOM_THREAD_PROFILE = "https://tools.ietf.org/html/rfc4685"

# Tell Flask that I am running it in testing mode.
resources.app.config["TESTING"] = True
# Necessary for correct translation in url_for
resources.app.config["SERVER_NAME"] = "localhost:5000"

# Database Engine utilized in our testing
resources.app.config.update({"Engine": ENGINE})

# Other database parameters.
initial_users = 5


class ResourcesAPITestCase(unittest.TestCase):
    # INITIATION AND TEARDOWN METHODS
    @classmethod
    def setUpClass(cls):
        """ Creates the database structure. Removes first any preexisting
            database file
        """
        print("Testing ", cls.__name__)
        ENGINE.remove_database()
        ENGINE.create_tables()

    @classmethod
    def tearDownClass(cls):
        """Remove the testing database"""
        print("Testing ENDED for ", cls.__name__)
        ENGINE.remove_database()

    def setUp(self):
        """
        Populates the database
        """
        # This method load the initial values from forum_data_dump.sql
        ENGINE.populate_tables()
        # Activate app_context for using url_for
        self.app_context = resources.app.app_context()
        self.app_context.push()
        # Create a test client
        self.client = resources.app.test_client()

    def tearDown(self):
        """
        Remove all records from database
        """
        ENGINE.clear()
        self.app_context.pop()


class UsersTestCase (ResourcesAPITestCase):

    user_1_request = {
        "nickname": "alkila",
        "givenName": "Sercan",
        "email": "sercan@mail.com"
    }

    user_wrong_1_request = {
        "nickname": "Scott",  # existing username
        "givenName": "Sercan",
        "email": "sercsssdan@mail.com"
    }

    user_wrong_2_request = {
        "nickname": "alkilaaa",
        "givenName": "Sercan",
        "email": "scott@outlook.com"  # existing email
    }

    # missing nickname
    user_wrong_3_request = {
        "givenName": "Sercan",
        "email": "sercsssdan@mail.com"
    }

    # missing givenName
    user_wrong_4_request = {
        "nickname": "aslkdmakldsm",
        "email": "sercsssdan@mail.com"
    }

    # missing email
    user_wrong_5_request = {
        "nickname": "aslkdmakldsm",
        "givenName": "Sercan"
    }

    CREATE_USER_SCHEMA = json.load(open('app/schema/create_user.json'))

    def setUp(self):
        super(UsersTestCase, self).setUp()
        self.url = resources.api.url_for(resources.Users,
                                         _external=False)

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        _url = "/critique/api/users/"
        print("("+self.test_url.__name__+")", self.test_url.__doc__, end=' ')
        with resources.app.test_request_context(_url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.Users)

    def test_get_users(self):
        """
        Checks that GET users return correct status code and data format
        """
        print("("+self.test_get_users.__name__+")", self.test_get_users.__doc__)
        # Check that I receive status code 200
        resp = self.client.get(flask.url_for("users"))
        self.assertEqual(resp.status_code, 200)

        # Check that I receive a collection and adequate href
        data = json.loads(resp.data.decode("utf-8"))

        controls = data["@controls"]
        self.assertIn("self", controls)
        self.assertIn("critique:add-user", controls)

        self.assertIn("href", controls["self"])
        self.assertEqual(controls["self"]["href"], self.url)

        add_ctrl = controls["critique:add-user"]
        self.assertIn("href", add_ctrl)
        self.assertEqual(add_ctrl["href"], self.url)
        self.assertIn("encoding", add_ctrl)
        self.assertEqual(add_ctrl["encoding"], "json")
        self.assertIn("method", add_ctrl)
        self.assertEqual(add_ctrl["method"], "POST")
        self.assertIn("schema", add_ctrl)
        self.assertEqual(add_ctrl["schema"], self.CREATE_USER_SCHEMA)

        items = data["items"]
        self.assertEqual(len(items), initial_users)
        for item in items:
            self.assertIn("nickname", item)
            self.assertIn("givenName", item)
            self.assertIn("familyName", item)

            self.assertIn("@controls", item)
            self.assertIn("self", item["@controls"])
            self.assertIn("href", item["@controls"]["self"])

            self.assertEqual(item["@controls"]["self"]["href"], resources.api.url_for(
                resources.User, nickname=item["nickname"], _external=False))

            self.assertIn("profile", item["@controls"])
            self.assertEqual(item["@controls"]["profile"]
                             ["href"], CRITIQUE_USER_PROFILE)


if __name__ == "__main__":
    print("Start running tests")
    unittest.main()
