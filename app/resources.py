'''
Created on 31.03.2018
@author: Sercan Turkmen
'''

import json

from urllib.parse import unquote

from flask import Flask, request, Response, g, _request_ctx_stack, redirect, send_from_directory
from flask_restful import Resource, Api, abort
from werkzeug.exceptions import NotFound, UnsupportedMediaType

from app.utils import RegexConverter
from app import database
from app.model.mason import MasonObject

# Constants for hypermedia formats and profiles
MASON = "application/vnd.mason+json"
JSON = "application/json"
CRITIQUE_USER_PROFILE = "/profiles/user-profile/"
ERROR_PROFILE = "/profiles/error-profile"

ATOM_THREAD_PROFILE = "https://tools.ietf.org/html/rfc4685"

# Fill these in
# Fill with the correct Apiary url"
APIARY_PROJECT = "https://critique.docs.apiary.io"
APIARY_PROFILES_URL = APIARY_PROJECT+"/#reference/profiles/"
APIARY_RELATIONS_URL = APIARY_PROJECT+"/#reference/link-relations/"

CREATE_USER_SCHEMA = json.load(open('app/schema/create_user.json'))
EDIT_USER_SCHEMA = json.load(open('app/schema/edit_user.json'))

PRIVATE_PROFILE_SCHEMA_URL = "/critique/schema/private-profile/"
LINK_RELATIONS_URL = "/critique/link-relations/"

# Define the application and the api
app = Flask(__name__, static_folder="static", static_url_path="/.")
app.debug = True
# Set the database Engine. In order to modify the database file (e.g. for
# testing) provide the database path   app.config to modify the
# database to be used (for instance for testing)
app.config.update({"Engine": database.Engine()})
# Start the RESTFUL API.
api = Api(app)


class CritiqueObject(MasonObject):
    """
    A convenience subclass of MasonObject that defines a bunch of shorthand
    methods for inserting application specific objects into the document. This
    class is particularly useful for adding control objects that are largely
    context independent, and defining them in the resource methods would add a
    lot of noise to our code - not to mention making inconsistencies much more
    likely!

    In the code this object should always be used for root document as
    well as any items in a collection type resource.
    """

    def __init__(self, **kwargs):
        """
        Calls dictionary init method with any received keyword arguments. Adds
        the controls key afterwards because hypermedia without controls is not
        hypermedia.
        """

        super(CritiqueObject, self).__init__(**kwargs)
        self["@controls"] = {}

    def add_control_users_collection(self):
        """
        This adds the user collection link to an object. Intended for the document object.
        """

        self["@controls"]["collection"] = {
            "href": api.url_for(Users),
            "title": "List users"
        }

    def add_control_add_user(self):
        """
        This adds the add-user control to an object. Intended for the
        document object. Instead of adding a schema dictionary we are pointing
        to a schema url instead for two reasons: 1) to demonstrate both options;
        2) the user schema is relatively large.
        """

        self["@controls"]["critique:add-user"] = {
            "href": api.url_for(Users),
            "title": "Create a new user",
            "encoding": "json",
            "method": "POST",
            "schema": CREATE_USER_SCHEMA
        }

    def add_control_user_inbox(self, nickname):
        """
        This adds the user-inbox control to an object. Intended for the
        document object.

        : param str nickname: The nickname of the user
        """

        self["@controls"]["critique:user-inbox"] = {
            "href": api.url_for(UserInbox, nickname=nickname),
        }

    def add_control_user_river(self, nickname):
        """
        This adds the user-river control to an object. Intended for the
        document object.

        : param str nickname: The nickname of the user
        """

        self["@controls"]["critique:user-river"] = {
            "href": api.url_for(UserRiver, nickname=nickname),
        }

    def add_control_user_ratings(self, nickname):
        """
        This adds the user-ratings control to an object. Intended for the
        document object.

        : param str nickname: The nickname of the user
        """

        self["@controls"]["critique:user-ratings"] = {
            "href": api.url_for(UserRatings, nickname=nickname),
        }

    def add_control_delete_user(self, nickname):
        """
        Adds the delete control to an object. This is intended for any
        object that represents a user.

        : param str nickname: The nickname of the user to remove
        """

        self["@controls"]["critique:delete"] = {
            "href": api.url_for(User, nickname=nickname),
            "title": "Delete a user",
            "method": "DELETE"
        }

    def add_control_edit_user(self, nickname):
        """
        Adds the edit control to an object. This is intended for any
        object that represents a user.

        : param str nickname: The nickname of the user to edit
        """

        self["@controls"]["edit"] = {
            "href": api.url_for(User, nickname=nickname),
            "title": "Edit this user",
            "method": "PUT",
            "schema": EDIT_USER_SCHEMA
        }


def create_error_response(status_code, title, message=None):
    """
    Creates a: py: class:`flask.Response` instance when sending back an
    HTTP error response

    : param integer status_code: The HTTP status code of the response
    : param str title: A short description of the problem
    : param message: A long description of the problem
    : rtype:: py: class:`flask.Response`
    """

    resource_url = None
    # We need to access the context in order to access the request.path
    ctx = _request_ctx_stack.top
    if ctx is not None:
        resource_url = request.path
    envelope = MasonObject(resource_url=resource_url)
    envelope.add_error(title, message)

    return Response(json.dumps(envelope), status_code, mimetype=MASON+";"+ERROR_PROFILE)


@app.errorhandler(404)
def resource_not_found(error):
    return create_error_response(404, "Resource not found",
                                 "This resource url does not exit")


@app.errorhandler(400)
def resource_not_found(error):
    return create_error_response(400, "Malformed input format",
                                 "The format of the input is incorrect")


@app.errorhandler(500)
def unknown_error(error):
    return create_error_response(500, "Error",
                                 "The system has failed. Please, contact the administrator")


# HOOKS
@app.before_request
def connect_db():
    """
    Creates a database connection before the request is proccessed.

    The connection is stored in the application context variable flask.g .
    Hence it is accessible from the request object.
    """

    g.con = app.config["Engine"].connect()


@app.teardown_request
def close_connection(exc):
    """
    Closes the database connection
    Check if the connection is created. It might be exception appear before
    the connection is created.
    """

    if hasattr(g, "con"):
        g.con.close()


class Users(Resource):

    def get(self):
        """
        Gets a list of all the users in the database.

        It returns always status code 200.

        RESPONSE ENTITY BODY:

         OUTPUT:
            * Media type: application/vnd.mason+json
                https://github.com/JornWildt/Mason
            * Profile: User
                /profiles/user-profile

        Link relations used in items: self, profile

        Semantic descriptions used in items: nickname, givenName, familyName, bio, avatar

        Link relations used in links: self, profile, add-user

        Semantic descriptors used in template: items

        NOTE:
         * The attribute givenName is obtained from the column users_profile.firstname
         * The attribute familyName is obtained from the column users_profile.lastname
         * The rest of attributes match one-to-one with column names in the
           database.
        """
        # PERFORM OPERATIONS
        # create users list
        users_db = g.con.get_users()

        # FILTER AND GENERATE THE RESPONSE
        # Create the envelope
        envelope = CritiqueObject()

        envelope.add_namespace("critique", LINK_RELATIONS_URL)

        envelope.add_control_add_user()
        envelope.add_control("self", href=api.url_for(Users))

        items = envelope["items"] = []

        for user in users_db:
            item = CritiqueObject(
                nickname=user["nickname"],
                givenName=user['firstname'],
                familyName=user['lastname'],
                avatar=user['avatar'],
                bio=user['bio']
            )
            # item.add_control_messages_history(user["nickname"])
            item.add_control("self", href=api.url_for(
                User, nickname=user["nickname"]))
            item.add_control("profile", href=CRITIQUE_USER_PROFILE)
            items.append(item)

        # RENDER
        return Response(json.dumps(envelope), 200, mimetype=MASON+";" + CRITIQUE_USER_PROFILE)

    def post(self):
        """
        Adds a new user in the database.

        REQUEST ENTITY BODY:
         * Media type: JSON
         * Profile: Critique_User

        Semantic descriptors used in template: nickname(mandatory), givenName(mandatory),
        email(mandatory).

        RESPONSE STATUS CODE:
         * Returns 201 + the url of the new resource in the Location header
         * Return 400 User info is not well formed or entity body is missing.
         * Return 415 if it receives a media type != application/json
         * Return 422 Conflict if there is another user with the same nickname, email, mobile

        NOTE:
         * The attribute givenName is obtained from the column users_profile.firstname
         * The attribute familyName is obtained from the column users_profile.lastname
         * The rest of attributes match one-to-one with column names in the
           database.

        NOTE:
        The: py: method:`Connection.append_user()` receives as a parameter a
        dictionary with the following format.

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

        """

        if JSON != request.headers.get("Content-Type", ""):
            abort(415)

        # PARSE THE REQUEST:
        request_body = request.get_json(force=True)
        if not request_body:
            return create_error_response(415,
                                         "Unsupported Media Type")

        # pick up nickname, email, and firstName so we can check for conflicts
        try:
            nickname = request_body["nickname"]
            firstName = request_body["givenName"]
            email = request_body["email"]
        except KeyError:
            return create_error_response(400,
                                         "Wrong request format")

        # Conflict if user already exist
        if g.con.contains_user_extended(nickname, email):
            return create_error_response(422,
                                         "Nickname, email, or mobile already exist in the users list.")

        user = {
            'summary': {
                'nickname': nickname
            },
            'details': {
                'firstname': firstName,
                'email': email,
            }
        }

        try:
            nickname = g.con.create_user(nickname, user)
        except ValueError:
            return create_error_response(400,
                                         "Wrong request format")

        # CREATE RESPONSE AND RENDER
        return Response(status=201,
                        headers={"Location": api.url_for(User, nickname=nickname)})


class User(Resource):
    """
    Resource has the basic information of a specific user.
    Bio is where the user should enter information about himself/herself,
    so it should be text. Email and telephone are unique texts as they
    will not repeat for other users. Gender, avatar and birthdate are texts.
    """

    def get(self, nickname):
        """
        Extract information of a user.

        INPUT PARAMETER:

        :param str nickname: Nickname of the required user.

        OUTPUT:
         * Return 200 if the nickname exists.
         * Return 404 if the nickname is not stored in the system.

        RESPONSE ENTITY BODY:

        OUTPUT:
            * Media type: application/vnd.mason+json
                https://github.com/JornWildt/Mason
            * Profile: User
                /profiles/user-profile

        Link relations used: self, collection, delete, user-inbox, edit,
        user-river, user-ratings, profile

        Semantic descriptors used: nickname, givenName, familyName, avatar,
        bio, email, birthday, telephone, gender

        NOTE:
         * The attribute givenName is obtained from the column users_profile.firstname
         * The attribute familyName is obtained from the column users_profile.lastname
         * The attribute telephone is obtained from the column users_profile.mobile
         * The rest of attributes match one-to-one with column names in the
           database.

        NOTE:
        The: py: method:`Connection.get_user()` returns a dictionary with the
        the following format.

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
        """

        # PERFORM OPERATIONS
        user_db = g.con.get_user(nickname)
        if not user_db:
            return create_error_response(404, "User not found.")

        summary = user_db['summary']
        details = user_db['details']

        # FILTER AND GENERATE RESPONSE
        # Create the envelope:
        envelope = CritiqueObject(
            nickname=nickname,
            givenName=details.get('firstname', None),
            familyName=details.get('lastname', None),
            avatar=summary.get('avatar', None),
            bio=summary.get('bio', None),
            email=details.get('email', None),
            birthdate=details.get('birthdate', None),
            telephone=details.get('mobile', None),
            gender=details.get('gender', None)
        )

        envelope.add_namespace("critique", LINK_RELATIONS_URL)

        envelope.add_control("self", href=api.url_for(User, nickname=nickname))
        envelope.add_control("profile", href=CRITIQUE_USER_PROFILE)
        envelope.add_control("collection", href=api.url_for(Users))
        envelope.add_control_edit_user(nickname)
        envelope.add_control_delete_user(nickname)
        envelope.add_control_user_inbox(nickname)
        envelope.add_control_user_river(nickname)
        envelope.add_control_user_ratings(nickname)

        return Response(json.dumps(envelope), 200, mimetype=MASON+";" + CRITIQUE_USER_PROFILE)

    def put(self, nickname):
        """
        Modifies mutable attributes of the specified user.

        REQUEST ENTITY BODY:
         * Media type: JSON
         * Profile: Critique_User

        Semantic descriptors used in template: givenName(optional), familyName(optional),
        avatar(optional), bio(optional), email(optional), birthdate(optional), telephone(optional),
        gender(optional)

        RESPONSE STATUS CODE:
         * Returns 204 + the url of the edited resource in the Location header
         * Return 400 User info is not well formed or entity body is missing.
         * Return 404 If user not found with given nickname.
         * Return 415 if it receives a media type != application/json
         * Return 422 Conflict if there is another user with the same nickname, email, mobile

        NOTE:
         * The attribute givenName is obtained from the column users_profile.firstname
         * The attribute familyName is obtained from the column users_profile.lastname
         * The attribute telephone is obtained from the column users_profile.mobile
         * The rest of attributes match one-to-one with column names in the
           database.

        NOTE:
        The: py: method:`Connection.edit_user()` receives as a parameter a
        dictionary with the following format.

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
        """

        user_db = g.con.get_user(nickname)
        if not user_db:
            return create_error_response(404, "User not found.")

        summary = user_db['summary']
        details = user_db['details']

        request_body = request.get_json()
        if not request_body:
            return create_error_response(415, "Format of the input is not json.")

        email = request_body.get('email', None)
        if email is not None and details['email'] != email and g.con.contains_user_email(email):
            return create_error_response(
                422, "Nickname, email, or mobile already exist in the users list.")

        summary['avatar'] = request_body.get(
            'avatar', summary['avatar'])
        summary['bio'] = request_body.get(
            'bio', summary['bio'])

        details['firstname'] = request_body.get(
            'givenName', details['firstname'])
        details['lastname'] = request_body.get(
            'familyName', details['lastname'])
        details['mobile'] = request_body.get(
            'telephone', details['mobile'])
        details['email'] = request_body.get(
            'email', details['email'])
        details['birthdate'] = request_body.get(
            'birthdate', details['birthdate'])
        details['gender'] = request_body.get(
            'gender', details['gender'])

        if not g.con.modify_user(nickname, summary, details):
            return create_error_response(500, "The system has failed. Please, contact the administrator.")

        return Response(status=204,
                        headers={"Location": api.url_for(User, nickname=nickname)})

    def delete(self, nickname):
        """
        Deletes the specified user.

        :param str nickname: The nickname of the user. Example: Scott.

        RESPONSE STATUS CODE:

            * If the user is deleted returns 204.
            * If the nickname does not exist return 404
            * If there was a db error return 500

        """
        # PEROFRM OPERATIONS

        userExist = g.con.contains_user(nickname)
        if not userExist:
            return create_error_response(404, "User not found.")

        # Try to delete the user. If it could not be deleted, the database
        # returns None.
        try:
            if g.con.delete_user(nickname):
                # RENDER RESPONSE
                return Response('', 204)
            else:
                # GENERATE ERROR RESPONSE
                return create_error_response(404, "User not found.")
        except:
            return create_error_response(500,
                                         "The system has failed. Please, contact the administrator.")


class UserInbox(Resource):
    def get(self, nickname):
        return Response('NOT IMPLEMENTED', 200)


class UserRiver(Resource):
    def get(self, nickname):
        return Response('NOT IMPLEMENTED', 200)


class UserRatings(Resource):
    def get(self, nickname):
        return Response('NOT IMPLEMENTED', 200)


# Add the Regex Converter so we can use regex expressions when we define the
# routes
app.url_map.converters["regex"] = RegexConverter

# Define the routes

api.add_resource(Users, "/critique/api/users/",
                 endpoint="users")
api.add_resource(User, "/critique/api/users/<nickname>/",
                 endpoint="user")
api.add_resource(UserInbox, "/critique/api/users/<nickname>/inbox",
                 endpoint="inbox")
api.add_resource(UserRiver, "/critique/api/users/<nickname>/river",
                 endpoint="river")
api.add_resource(UserRatings, "/critique/api/users/<nickname>/ratings",
                 endpoint="ratings")

# Redirect profile


@app.route("/profiles/<profile_name>/")
def redirect_to_profile(profile_name):
    return redirect(APIARY_PROFILES_URL + profile_name)


@app.route("/critique/link-relations/<rel_name>/")
def redirect_to_relations(rel_name):
    return redirect(APIARY_RELATIONS_URL + rel_name)

# Send our schema file(s)


# @app.route("/critique/schema/<schema_name>/")
# def send_json_schema(schema_name):
#     #return send_from_directory("static/schema", "{}.json".format(schema_name))
#     return send_from_directory(app.static_folder, "schema/{}.json".format(schema_name))


# Start the application
# DATABASE SHOULD HAVE BEEN POPULATED PREVIOUSLY
if __name__ == '__main__':
    # Debug true activates automatic code reloading and improved error messages
    app.run(debug=True)
