"""
Created on 01.05.2018
@author: sercant
         moamen

    REFERENCEs:
    -   [1] Programmable Web Project, Exercise3, exercise3_api_tests.py
"""

import unittest
import copy
import json

import flask

import app.resources as resources
import app.database as database

DB_PATH = "db/critique_test.db"
ENGINE = database.Engine(DB_PATH)

MASON_JSON = "application/vnd.mason+json"
JSON = "application/json"
CRITIQUE_USER_PROFILE = "/profiles/user-profile/"
CRITIQUE_RATING_PROFILE = "/profiles/rating-profile/"
CRITIQUE_POST_PROFILE = "/profiles/post_profile/"


# Tell Flask that I am running it in testing mode.
resources.app.config["TESTING"] = True
# Necessary for correct translation in url_for
resources.app.config["SERVER_NAME"] = "localhost:5000"

# Database Engine utilized in our testing
resources.app.config.update({"Engine": ENGINE})

# Other database parameters.
initial_users = 5
scott_ratings_count = 4
scott_posts_count = 2
scott_inbox_count = 1

class ResourcesAPITestCase(unittest.TestCase): # Borrowed from lab exercises [1]
    # INITIATION AND TEARDOWN METHODS
    @classmethod
    def setUpClass(cls):  # Borrowed from lab exercises [1]
        """ Creates the database structure. Removes first any preexisting
            database file
        """
        print("Testing ", cls.__name__)
        ENGINE.remove_database()
        ENGINE.create_tables()

    @classmethod
    def tearDownClass(cls):  # Borrowed from lab exercises [1]
        """Remove the testing database"""
        print("Testing ENDED for ", cls.__name__)
        ENGINE.remove_database()

    def setUp(self):  # Borrowed from lab exercises [1]
        """
        Populates the database
        """
        # This method load the initial values from critique_data_dump.sql
        ENGINE.populate_tables()
        # Activate app_context for using url_for
        self.app_context = resources.app.app_context()
        self.app_context.push()
        # Create a test client
        self.client = resources.app.test_client()

    def tearDown(self):  # Borrowed from lab exercises [1]
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

    user_2_request = {
        "nickname": "nandeska",
        "givenName": "nandesu",
        "email": "nande@mail.com",
        "bio": "hello evermeow!",
        "familyName": "meow"
    }

    user_wrong_1_request = {
        "nickname": "Scott",  # existing nickname
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
        # Borrowed from lab exercises [1]
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

        self.assertIn("href", controls["all-posts"])
        self.assertEqual(controls["all-posts"]["href"], resources.api.url_for(
            resources.Posts, _external=False))

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

    def test_get_users_mimetype(self):
        """
        Checks that GET users return correct status code and data format
        """
        print("("+self.test_get_users_mimetype.__name__+")",
              self.test_get_users_mimetype.__doc__)

        # Check that I receive status code 200
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type", None),
                         "{};{}".format(MASON_JSON, CRITIQUE_USER_PROFILE))

    def test_add_user(self):
        """
        Checks that the user is added correctly
        """
        print("("+self.test_add_user.__name__+")", self.test_add_user.__doc__)

        # With a complete request
        resp = self.client.post(resources.api.url_for(resources.Users),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.user_1_request))

        self.assertEqual(resp.status_code, 201)

        self.assertIn("Location", resp.headers)
        url = resp.headers["Location"]

        resp2 = self.client.get(url)
        self.assertEqual(resp2.status_code, 200)

        data = json.loads(resp2.data.decode("utf-8"))
        for key in self.user_1_request.keys():
            self.assertEqual(data[key], self.user_1_request[key])

        # With a complete request that includes optional fields
        resp = self.client.post(resources.api.url_for(resources.Users),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.user_2_request))

        self.assertEqual(resp.status_code, 201)

        self.assertIn("Location", resp.headers)
        url = resp.headers["Location"]

        resp3 = self.client.get(url)
        self.assertEqual(resp3.status_code, 200)

        data = json.loads(resp3.data.decode("utf-8"))
        for key in self.user_1_request.keys():
            self.assertEqual(data[key], self.user_2_request[key])

    def test_add_user_missing_mandatory(self):
        """
        Test that it returns error when is missing a mandatory data
        """
        print("("+self.test_add_user_missing_mandatory.__name__+")",
              self.test_add_user_missing_mandatory.__doc__)

        # Removing nickname
        resp = self.client.post(resources.api.url_for(resources.Users),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.user_wrong_3_request)
                                )
        self.assertEqual(resp.status_code, 400)

        # Removing givenName
        resp = self.client.post(resources.api.url_for(resources.Users),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.user_wrong_4_request)
                                )
        self.assertEqual(resp.status_code, 400)

        # Removing email
        resp = self.client.post(resources.api.url_for(resources.Users),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.user_wrong_5_request)
                                )
        self.assertEqual(resp.status_code, 400)

    def test_add_existing_user(self):
        """
        Testing that trying to add an existing user will fail

        """
        print("("+self.test_add_existing_user.__name__+")",
              self.test_add_existing_user.__doc__)

        # Existing nickname
        resp = self.client.post(resources.api.url_for(resources.Users),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.user_wrong_1_request)
                                )
        self.assertEqual(resp.status_code, 422)

        # Existing email
        resp = self.client.post(resources.api.url_for(resources.Users),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.user_wrong_2_request)
                                )
        self.assertEqual(resp.status_code, 422)

    def test_wrong_type(self):
        """
        Test that return adequate error if sent incorrect mime type
        """
        print("("+self.test_wrong_type.__name__+")",
              self.test_wrong_type.__doc__)
        resp = self.client.post(resources.api.url_for(resources.Users),
                                headers={"Content-Type": "text/html"},
                                data=json.dumps(self.user_1_request)
                                )
        self.assertEqual(resp.status_code, 415)


class UserTestCase(ResourcesAPITestCase):

    user_mod_req_1 = {
        "givenName": "Scotta",
        "familyName": "Pilgrimu",
        "avatar": "photo6.jpg",
        "telephone": None,
        "gender": "male"
    }

    EDIT_USER_SCHEMA = json.load(open('app/schema/edit_user.json'))

    def setUp(self):
        super(UserTestCase, self).setUp()
        self.url = resources.api.url_for(resources.User,
                                         nickname="Scott",
                                         _external=False)
        self.url_wrong = resources.api.url_for(resources.User,
                                               nickname="Kimo",
                                               _external=False)

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        _url = "/critique/api/users/Scott/"
        print("("+self.test_url.__name__+")", self.test_url.__doc__, end=' ')
        with resources.app.test_request_context(_url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.User)

    def test_wrong_url(self):
        """
        Checks that GET user return correct status code if given a
        wrong nickname
        """
        resp = self.client.get(self.url_wrong)
        self.assertEqual(resp.status_code, 404)

    def test_get_user(self):
        """
        Checks that GET user return correct status code and data format
        """
        print("("+self.test_get_user.__name__+")",
              self.test_get_user.__doc__)
        with resources.app.test_client() as client:
            resp = client.get(self.url)
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.data.decode("utf-8"))

            controls = data["@controls"]
            self.assertIn("self", controls)
            self.assertIn("profile", controls)
            self.assertIn("collection", controls)
            self.assertIn("edit", controls)
            self.assertIn("critique:delete", controls)
            self.assertIn("critique:user-inbox", controls)
            self.assertIn("critique:user-ratings", controls)
            self.assertIn("critique:user-river", controls)

            edit_ctrl = controls["edit"]
            self.assertIn("title", edit_ctrl)
            self.assertIn("href", edit_ctrl)
            self.assertEqual(edit_ctrl["href"], self.url)
            self.assertIn("encoding", edit_ctrl)
            self.assertEqual(edit_ctrl["encoding"], "json")
            self.assertIn("method", edit_ctrl)
            self.assertEqual(edit_ctrl["method"], "PUT")
            self.assertIn("schema", edit_ctrl)
            self.assertEqual(edit_ctrl["schema"], self.EDIT_USER_SCHEMA)

            self.assertIn("href", controls["self"])
            self.assertEqual(controls["self"]["href"], self.url)

            self.assertIn("href", controls["profile"])
            self.assertEqual(controls["profile"]
                             ["href"], CRITIQUE_USER_PROFILE)

            self.assertIn("href", controls["collection"])
            self.assertEqual(controls["collection"]["href"], resources.api.url_for(
                resources.Users, _external=False
            ))

            del_ctrl = controls["critique:delete"]
            self.assertIn("href", del_ctrl)
            self.assertEqual(del_ctrl["href"], self.url)
            self.assertIn("method", del_ctrl)
            self.assertEqual(del_ctrl["method"], "DELETE")

            self.assertIn("href", controls["critique:user-inbox"])
            self.assertEqual(controls["critique:user-inbox"]["href"],  resources.api.url_for(
                resources.UserInbox, _external=False, nickname="Scott"
            ))

            # Check rest attributes
            self.assertIn("nickname", data)
            self.assertIn("givenName", data)
            self.assertIn("familyName", data)
            self.assertIn("avatar", data)
            self.assertIn("bio", data)
            self.assertIn("email", data)
            self.assertIn("birthdate", data)
            self.assertIn("telephone", data)
            self.assertIn("gender", data)

    def test_get_user_mimetype(self):
        """
        Checks that GET user return correct status code and data format
        """
        print("("+self.test_get_user_mimetype.__name__+")",
              self.test_get_user_mimetype.__doc__)

        # Check that I receive status code 200
        resp = self.client.get(self.url)
        # Borrowed from lab exercises [1]
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type", None),
                         "{};{}".format(MASON_JSON, CRITIQUE_USER_PROFILE))

    def test_modify_user(self):
        """
        Modify an existing user and check that the user has been modified correctly in the server
        """
        print("("+self.test_modify_user.__name__+")",
              self.test_modify_user.__doc__)
        resp = self.client.put(self.url,
                               data=json.dumps(self.user_mod_req_1),
                               headers={"Content-Type": JSON})
        self.assertEqual(resp.status_code, 204)

        # Check that the user has been modified
        resp2 = self.client.get(self.url)
        self.assertEqual(resp2.status_code, 200)
        data = json.loads(resp2.data.decode("utf-8"))

        # Check that the fields returned correctly
        for key in self.user_mod_req_1.keys():
            self.assertEqual(data[key], self.user_mod_req_1[key])

    def test_modify_nonexisting_user(self):
        """
        Try to modify a user that does not exist
        """
        print("("+self.test_modify_nonexisting_user.__name__+")",
              self.test_modify_nonexisting_user.__doc__)
        resp = self.client.put(self.url_wrong,
                               data=json.dumps(self.user_mod_req_1),
                               headers={"Content-Type": JSON})
        self.assertEqual(resp.status_code, 404)

    def test_delete_user(self):
        """
        Checks that Delete user return correct status code if corrected delete
        """
        print("("+self.test_delete_user.__name__+")",
              self.test_delete_user.__doc__)
        resp = self.client.delete(self.url)
        self.assertEqual(resp.status_code, 204)
        resp2 = self.client.get(self.url)
        self.assertEqual(resp2.status_code, 404)

    def test_delete_nonexisting_user(self):
        """
        Checks that Delete user return correct status code if given a wrong address
        """
        print("("+self.test_delete_nonexisting_user.__name__+")",
              self.test_delete_nonexisting_user.__doc__)
        resp = self.client.delete(self.url_wrong)
        self.assertEqual(resp.status_code, 404)


class UserRatingsTestCase(ResourcesAPITestCase):

    CREATE_RATING_SCHEMA = json.load(open('app/schema/create_rating.json'))

    def setUp(self):
        super(UserRatingsTestCase, self).setUp()
        self.url = resources.api.url_for(resources.UserRatings,
                                         nickname="Scott",
                                         _external=False)
        self.url_wrong = resources.api.url_for(resources.UserRatings,
                                               nickname="Kimo",
                                               _external=False)

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        _url = "/critique/api/users/Scott/ratings/"
        print("("+self.test_url.__name__+")", self.test_url.__doc__, end=' ')
        with resources.app.test_request_context(_url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.UserRatings)

    def test_wrong_url(self):
        """
        Checks that GET user ratings return correct status code if given a
        wrong nickname
        """
        resp = self.client.get(self.url_wrong)
        self.assertEqual(resp.status_code, 404)

    def test_get_user_ratings(self):
        """
        Checks that GET user_ratings return correct status code and data format
        """
        print("("+self.test_get_user_ratings.__name__+")",
              self.test_get_user_ratings.__doc__)
        # Check that I receive status code 200
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

        # Check that I receive a collection and adequate href
        data = json.loads(resp.data.decode("utf-8"))

        controls = data["@controls"]
        self.assertIn("self", controls)
        self.assertIn("critique:add-rating", controls)

        self.assertIn("href", controls["self"])
        self.assertEqual(controls["self"]["href"], self.url)

        add_ctrl = controls["critique:add-rating"]
        self.assertIn("href", add_ctrl)
        self.assertEqual(add_ctrl["href"], resources.api.url_for(
            resources.UserRatings, nickname="Scott", _external=False))
        self.assertIn("encoding", add_ctrl)
        self.assertEqual(add_ctrl["encoding"], "json")
        self.assertIn("method", add_ctrl)
        self.assertEqual(add_ctrl["method"], "POST")
        self.assertIn("schema", add_ctrl)
        self.assertEqual(add_ctrl["schema"], self.CREATE_RATING_SCHEMA)

        items = data["items"]
        self.assertEqual(len(items), scott_ratings_count)
        for item in items:
            self.assertIn("ratingId", item)
            self.assertIn("bestRating", item)
            self.assertIn("ratingValue", item)
            self.assertIn("sender", item)
            self.assertIn("receiver", item)

            self.assertIn("@controls", item)
            self.assertIn("self", item["@controls"])

            self.assertIn("href", item["@controls"]["self"])
            self.assertEqual(item["@controls"]["self"]["href"], resources.api.url_for(
                resources.Rating, nickname="Scott", ratingId=item["ratingId"], _external=False))

            self.assertIn("href", item["@controls"]["critique:sender"])
            self.assertEqual(item["@controls"]["critique:sender"]["href"], resources.api.url_for(
                resources.User, nickname=item["sender"], _external=False))

            self.assertIn("href", item["@controls"]["critique:receiver"])
            self.assertEqual(item["@controls"]["critique:receiver"]["href"], resources.api.url_for(
                resources.User, nickname=item["receiver"], _external=False))

            self.assertIn("profile", item["@controls"])
            self.assertEqual(item["@controls"]["profile"]
                             ["href"], CRITIQUE_RATING_PROFILE)

    def test_get_user_ratings_mimetype(self):
        """
        Checks that GET user ratings return correct status code and data format
        """
        print("("+self.test_get_user_ratings_mimetype.__name__+")",
              self.test_get_user_ratings_mimetype.__doc__)

        # Check that I receive status code 200
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type", None),
                         "{};{}".format(MASON_JSON, CRITIQUE_RATING_PROFILE))


class UserRiverTestCase(ResourcesAPITestCase):


    CREATE_POSTS_SCHEMA = json.load(open('app/schema/create_posts.json'))

    def setUp(self):
        super(UserRiverTestCase, self).setUp()
        self.url = resources.api.url_for(resources.UserRiver,
                                         nickname="Scott",
                                         _external=False)
        self.url_wrong = resources.api.url_for(resources.UserRiver,
                                               nickname="Kimo",
                                               _external=False)

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        _url = "/critique/api/users/Scott/river/"
        print("("+self.test_url.__name__+")", self.test_url.__doc__, end=' ')
        with resources.app.test_request_context(_url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.UserRiver)

    def test_wrong_url(self):
        """
        Checks that GET user river return correct status code if given a
        wrong nickname
        """
        resp = self.client.get(self.url_wrong)
        self.assertEqual(resp.status_code, 404)

    def test_get_posts_by_user(self):
        """
        Checks that GET get_posts_by_user return correct status code and data format
        """

        print("("+self.test_get_posts_by_user.__name__+")",
              self.test_get_posts_by_user.__doc__)
        # Check that I receive status code 200
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

        # Check that I receive a collection and adequate href
        data = json.loads(resp.data.decode("utf-8"))

        controls = data["@controls"]
        self.assertIn("self", controls)
        self.assertIn("critique:user-river", controls)

        self.assertIn("href", controls["self"])
        self.assertEqual(controls["self"]["href"], self.url)

        add_ctrl = controls["critique:user-river"]
        self.assertIn("href", add_ctrl)
        self.assertEqual(add_ctrl["href"], resources.api.url_for(
            resources.UserRiver, nickname="Scott", _external=False))
        # self.assertIn("encoding", add_ctrl)
        # self.assertEqual(add_ctrl["encoding"], "json")
        # self.assertIn("method", add_ctrl)
        # self.assertEqual(add_ctrl["method"], "POST")
        # self.assertIn("schema", add_ctrl)
        # self.assertEqual(add_ctrl["schema"], self.CREATE_POSTS_SCHEMA)

        items = data["items"]
        self.assertEqual(len(items), scott_posts_count)
        for item in items:
            self.assertIn("postId", item)
            self.assertIn("ratingValue", item)
            self.assertIn("replyTo", item)
            self.assertIn("receiver", item)
            self.assertIn("post_Text", item)
            self.assertIn("anonymous", item)
            self.assertIn("public", item)


            self.assertIn("@controls", item)
            self.assertIn("self", item["@controls"])

            self.assertIn("href", item["@controls"]["self"])
            # self.assertEqual(item["@controls"]["self"]["href"], resources.api.url_for(
            #     resources.UserRiver, nickname="Scott", _external=False))

            # self.assertIn("href", item["@controls"]["critique:sender"])
            # self.assertEqual(item["@controls"]["critique:sender"]["href"], resources.api.url_for(
            #     resources.User, nickname=item["sender"], _external=False))

            # self.assertIn("href", item["@controls"]["critique:receiver"])
            # self.assertEqual(item["@controls"]["critique:receiver"]["href"], resources.api.url_for(
            #     resources.User, nickname=item["receiver"], _external=False))

            self.assertIn("profile", item["@controls"])
            self.assertEqual(item["@controls"]["profile"]
                             ["href"], CRITIQUE_POST_PROFILE)

    def test_get_posts_by_user_mimetype(self):
        """
        Checks that GET user ratings return correct status code and data format
        """
        print("("+self.test_get_posts_by_user_mimetype.__name__+")",
              self.test_get_posts_by_user_mimetype.__doc__)

        # Check that I receive status code 200
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type", None),
                         "{};{}".format(MASON_JSON, CRITIQUE_POST_PROFILE))


class UserInboxTestCase(ResourcesAPITestCase):

    post_mod_req_1 = {
        "anonymous": False,
        "sender": "Scott",
        "receiver": "Kim",
        "reply_to": "Stephen",
        "post_text": "You are such a cool actor. Can we get a photo",
        "ratingValue": 5,
        "public":0
    }

    CREATE_POSTS_SCHEMA = json.load(open('app/schema/create_posts.json'))

    def setUp(self):
        super(UserInboxTestCase, self).setUp()
        self.url = resources.api.url_for(resources.UserInbox,
                                         nickname="Scott",
                                         _external=False)
        self.url_wrong = resources.api.url_for(resources.UserInbox,
                                               nickname="Kimo",
                                               _external=False)

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        _url = "/critique/api/users/Scott/inbox/"
        print("("+self.test_url.__name__+")", self.test_url.__doc__, end=' ')
        with resources.app.test_request_context(_url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.UserInbox)

    def test_wrong_url(self):
        """
        Checks that GET user inbox return correct status code if given a
        wrong nickname
        """
        resp = self.client.get(self.url_wrong)
        self.assertEqual(resp.status_code, 404)

    def test_get_posts_by_user(self):
        """
        Checks that GET get_posts_by_user return correct status code and data format
        """

        print("("+self.test_get_posts_by_user.__name__+")",
              self.test_get_posts_by_user.__doc__)
        # Check that I receive status code 200
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

        # Check that I receive a collection and adequate href
        data = json.loads(resp.data.decode("utf-8"))

        controls = data["@controls"]
        self.assertIn("self", controls)
        self.assertIn("critique:user-inbox", controls)

        self.assertIn("href", controls["self"])
        self.assertEqual(controls["self"]["href"], self.url)

        add_ctrl = controls["critique:user-inbox"]
        self.assertIn("href", add_ctrl)
        self.assertEqual(add_ctrl["href"], resources.api.url_for(
            resources.UserInbox, nickname="Scott", _external=False))
        # self.assertIn("encoding", add_ctrl)
        # self.assertEqual(add_ctrl["encoding"], "json")
        # self.assertIn("method", add_ctrl)
        # self.assertEqual(add_ctrl["method"], "POST")
        # self.assertIn("schema", add_ctrl)
        # self.assertEqual(add_ctrl["schema"], self.CREATE_POSTS_SCHEMA)

        items = data["items"]
        self.assertEqual(len(items), scott_inbox_count)
        for item in items:
            self.assertIn("postId", item)
            self.assertIn("ratingValue", item)
            self.assertIn("replyTo", item)
            self.assertIn("receiver", item)
            self.assertIn("post_Text", item)
            self.assertIn("anonymous", item)
            self.assertIn("public", item)

            self.assertIn("@controls", item)
            self.assertIn("self", item["@controls"])

            self.assertIn("href", item["@controls"]["self"])
            # self.assertEqual(item["@controls"]["self"]["href"], resources.api.url_for(
            #     resources.UserInbox, nickname="Scott", postId=item["postId"], _external=False))

            # self.assertIn("href", item["@controls"]["critique:sender"])
            # self.assertEqual(item["@controls"]["critique:sender"]["href"], resources.api.url_for(
            #     resources.User, nickname=item["sender"], _external=False))

            # self.assertIn("href", item["@controls"]["critique:receiver"])
            # self.assertEqual(item["@controls"]["critique:receiver"]["href"], resources.api.url_for(
            #     resources.User, nickname=item["receiver"], _external=False))

            self.assertIn("profile", item["@controls"])
            self.assertEqual(item["@controls"]["profile"]
                             ["href"], CRITIQUE_POST_PROFILE)

    def test_get_posts_by_user_mimetype(self):
        """
        Checks that GET user ratings return correct status code and data format
        """
        print("("+self.test_get_posts_by_user_mimetype.__name__+")",
              self.test_get_posts_by_user_mimetype.__doc__)

        # Check that I receive status code 200
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type", None),
                         "{};{}".format(MASON_JSON, CRITIQUE_POST_PROFILE))


class UserRatingTestCase(ResourcesAPITestCase):


    rating_mod_req_1 = {
        "sender": "Scott",
        "receiver": "Kim",
        "rating": 2
    }

    CREATE_RATING_SCHEMA = json.load(open('app/schema/create_rating.json'))

    def setUp(self):
        super(UserRatingTestCase, self).setUp()
        self.url = resources.api.url_for(resources.Rating,
                                         nickname="Scott",
                                         ratingId="rtg-1",
                                         _external=False)
        self.url_wrong = resources.api.url_for(resources.Rating,
                                               nickname="Kim",
                                               ratingId="rtg-5",
                                               _external=False)

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        _url = "/critique/api/users/Scott/ratings/rtg-01/"
        print("("+self.test_url.__name__+")", self.test_url.__doc__, end=' ')
        with resources.app.test_request_context(_url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.Rating)

    def test_wrong_url(self):
        """
        Checks that GET user Rating return correct status code if given a
        wrong ratingId
        """
        resp = self.client.get(self.url_wrong)
        self.assertEqual(resp.status_code, 404)

    def test_modify_rating(self):
        """
        Modify an existing Rating and check that the Rating has been modified correctly in the server
        """
        print("("+self.test_modify_rating.__name__+")",
              self.test_modify_rating.__doc__)
        resp = self.client.put(self.url,
                               data=json.dumps(self.rating_mod_req_1),
                               headers={"Content-Type": JSON})
        self.assertEqual(resp.status_code, 204)

        # Check that the Rating has been modified
        resp2 = self.client.get(self.url)
        self.assertEqual(resp2.status_code, 200)
        data = json.loads(resp2.data.decode("utf-8"))

        # Check that the fields returned correctly
        for key in self.rating_mod_req_1.keys():
            self.assertEqual(data[key], self.rating_mod_req_1[key])

    def test_modify_nonexisting_rating(self):
        """
        Try to modify a Rating that does not exist
        """
        print("("+self.test_modify_nonexisting_rating.__name__+")",
              self.test_modify_nonexisting_rating.__doc__)
        resp = self.client.put(self.url_wrong,
                               data=json.dumps(self.rating_mod_req_1),
                               headers={"Content-Type": JSON})
        self.assertEqual(resp.status_code, 404)

    def test_delete_rating(self):
        """
        Checks that Delete Rating return correct status code if corrected delete
        """
        print("("+self.test_delete_rating.__name__+")",
              self.test_delete_rating.__doc__)
        resp = self.client.delete(self.url)
        self.assertEqual(resp.status_code, 204)
        resp2 = self.client.get(self.url)
        self.assertEqual(resp2.status_code, 404)

    def test_delete_nonexisting_rating(self):
        """
        Checks that Delete rating return correct status code if given a wrong address
        """
        print("("+self.test_delete_nonexisting_rating.__name__+")",
              self.test_delete_nonexisting_rating.__doc__)
        resp = self.client.delete(self.url_wrong)
        self.assertEqual(resp.status_code, 404)


class UserPostTestCase(ResourcesAPITestCase):

    post_mod_req_1 = {
        "anonymous": 0,
        "sender": "Scott",
        "receiver": "Kim",
        "reply_to": "Stephen",
        "post_text": "You are the worst actor ever",
        "ratingValue": 2,
        "public": 0
    }

    CREATE_POSTS_SCHEMA = json.load(open('app/schema/create_posts.json'))

    def setUp(self):
        super(UserPostTestCase, self).setUp()
        self.url = resources.api.url_for(resources.Post,
                                         postId="p-1",
                                         _external=False)
        self.url_wrong = resources.api.url_for(resources.Post,
                                               postId="p-2",
                                               _external=False)

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        _url = "/critique/api/posts/"
        print("("+self.test_url.__name__+")", self.test_url.__doc__, end=' ')
        with resources.app.test_request_context(_url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.Posts)

    def test_wrong_url(self):
        """
        Checks that GET user post return correct status code if given a
        wrong post id
        """
        resp = self.client.get(self.url_wrong)
        self.assertEqual(resp.status_code, 404)

    def test_modify_post(self):
        """
        Modify an existing post and check that the post has been modified correctly in the server
        """
        print("("+self.test_modify_post.__name__+")",
              self.test_modify_post.__doc__)
        resp = self.client.put(self.url,
                               data=json.dumps(self.post_mod_req_1),
                               headers={"Content-Type": JSON})
        self.assertEqual(resp.status_code, 204)

        # Check that the post has been modified
        resp2 = self.client.get(self.url)
        self.assertEqual(resp2.status_code, 200)
        data = json.loads(resp2.data.decode("utf-8"))

        # Check that the fields returned correctly
        for key in self.post_mod_req_1.keys():
            self.assertEqual(data[key], self.post_mod_req_1[key])

    def test_modify_nonexisting_post(self):
        """
        Try to modify a post that does not exist
        """
        print("("+self.test_modify_nonexisting_post.__name__+")",
              self.test_modify_nonexisting_post.__doc__)
        resp = self.client.put(self.url_wrong,
                               data=json.dumps(self.post_mod_req_1),
                               headers={"Content-Type": JSON})
        self.assertEqual(resp.status_code, 404)

    # def test_delete_post(self):
    #     """
    #     Checks that Delete post return correct status code if corrected delete
    #     """
    #     print("("+self.test_delete_post.__name__+")",
    #           self.test_delete_post.__doc__)
    #     resp = self.client.delete(self.url)
    #     self.assertEqual(resp.status_code, 204)
    #     resp2 = self.client.get(self.url)
    #     self.assertEqual(resp2.status_code, 404)

    # def test_delete_nonexisting_post(self):
    #     """
    #     Checks that Delete post return correct status code if given a wrong address
    #     """
    #     print("("+self.test_delete_nonexisting_post.__name__+")",
    #           self.test_delete_nonexisting_post.__doc__)
    #     resp = self.client.delete(self.url_wrong)
    #     self.assertEqual(resp.status_code, 404)



if __name__ == "__main__": # Borrowed from lab exercises [1]
    print("Start running tests")
    unittest.main()
