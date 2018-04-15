'''
Created on 31.03.2018
@author: Sercan Turkmen
         Moamen Ibrahim
         Mina Ghobrial
    REFERENCEs:
    -   [1] Programmable Web Project, Exercise3, resources.py
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
CRITIQUE_POST_PROFILE = "/profiles/post_profile/"
CRITIQUE_RATING_PROFILE = "/profiles/rating-profile/"
ERROR_PROFILE = "/profiles/error-profile"

# Fill these in
# Fill with the correct Apiary url"
APIARY_PROJECT = "https://critique.docs.apiary.io"
APIARY_PROFILES_URL = APIARY_PROJECT+"/#reference/profiles/"
APIARY_RELATIONS_URL = APIARY_PROJECT+"/#reference/link-relations/"

CREATE_USER_SCHEMA = json.load(open('app/schema/create_user.json'))
CREATE_RATING_SCHEMA = json.load(open('app/schema/create_rating.json'))
EDIT_USER_SCHEMA = json.load(open('app/schema/edit_user.json'))
CREATE_POSTS_SCHEMA = json.load(open('app/schema/create_posts.json'))
EDIT_RATING_SCHEMA = json.load(open('app/schema/edit_rating.json'))
EDIT_POST_SCHEMA = json.load(open('app/schema/edit_post.json'))


PRIVATE_PROFILE_SCHEMA_URL = "/critique/schema/private-profile/"
LINK_RELATIONS_URL = "/critique/link-relations/"

# Borrowed from lab exercises [1]
# Define the application and the api
app = Flask(__name__, static_folder="static", static_url_path="/.")
app.debug = True
# Set the database Engine. In order to modify the database file (e.g. for
# testing) provide the database path   app.config to modify the
# database to be used (for instance for testing)
app.config.update({"Engine": database.Engine()})
# Start the RESTFUL API.
api = Api(app)


class CritiqueObject(MasonObject):  # Borrowed from lab exercises [1]
    '''
    A convenience subclass of MasonObject that defines a bunch of shorthand
    methods for inserting application specific objects into the document. This
    class is particularly useful for adding control objects that are largely
    context independent, and defining them in the resource methods would add a
    lot of noise to our code - not to mention making inconsistencies much more
    likely!

    In the code this object should always be used for root document as
    well as any items in a collection type resource.
    '''

    def __init__(self, **kwargs):  # Borrowed from lab exercises [1]
        '''
        Calls dictionary init method with any received keyword arguments. Adds
        the controls key afterwards because hypermedia without controls is not
        hypermedia.
        '''

        super(CritiqueObject, self).__init__(**kwargs)
        self["@controls"] = {}

    def add_control_users_collection(self):
        '''
        This adds the user collection link to an object. Intended for the document object.
        '''

        self["@controls"]["collection"] = {
            "href": api.url_for(Users),
            "title": "List users"
        }

    def add_control_all_posts(self):
        '''
        This adds the posts collection link to an object. Intended for the document object.
        '''

        self["@controls"]["all-posts"] = {
            "href": api.url_for(Posts),
            "title": "List posts"
        }

    def add_control_all_users(self):
        '''
        This adds the users collection link to an object. Intended for the document object.
        '''

        self["@controls"]["all-users"] = {
            "href": api.url_for(Users),
            "title": "List users"
        }

    def add_control_add_user(self):
        '''
        This adds the add-user control to an object. Intended for the
        document object.
        '''

        self["@controls"]["critique:add-user"] = {
            "href": api.url_for(Users),
            "title": "Create a new user",
            "encoding": "json",
            "method": "POST",
            "schema": CREATE_USER_SCHEMA
        }

    def add_control_user_inbox(self, nickname):
        '''
        This adds the user-inbox control to an object. Intended for the
        document object.

        : param str nickname: The nickname of the user
        '''

        self["@controls"]["critique:user-inbox"] = {
            "href": api.url_for(UserInbox, nickname=nickname),
        }

    def add_control_user_river(self, nickname):
        '''
        This adds the user-river control to an object. Intended for the
        document object.

        : param str nickname: The nickname of the user
        '''

        self["@controls"]["critique:user-river"] = {
            "href": api.url_for(UserRiver, nickname=nickname),
        }

    def add_control_user_ratings(self, nickname):
        '''
        This adds the user-ratings control to an object. Intended for the
        document object.

        : param str nickname: The nickname of the user
        '''

        self["@controls"]["critique:user-ratings"] = {
            "href": api.url_for(UserRatings, nickname=nickname),
        }

    def add_control_reply_to(self, receiver):
        '''
        This adds the reply to a post control to an object. Intended for the
        document object.

        : param str receiver: The receiver of the reply
        '''

        self["@controls"]["critique:add-reply"] = {
            "href": api.url_for(Posts, receiver=receiver),
        }

    def add_control_delete_user(self, nickname):
        '''
        Adds the delete control to an object. This is intended for any
        object that represents a user.

        : param str nickname: The nickname of the user to remove
        '''

        self["@controls"]["critique:delete"] = {
            "href": api.url_for(User, nickname=nickname),
            "title": "Delete a user",
            "method": "DELETE"
        }

    def add_control_delete_post(self, nickname, post_id):
        '''
        Adds the delete control to an object. This is intended for any
        object that represents a user's post.

        : param str nickname: The nickname of the user to remove
        : param integer post_id : The id of the post to be deleted
        '''

        self["@controls"]["critique:delete"] = {
            "href": api.url_for(UserRiver, nickname=nickname, postId = post_id),
            "title": "Delete a user's post",
            "method": "DELETE"
        }

    def add_control_edit_user(self, nickname):
        '''
        Adds the edit control to an object. This is intended for any
        object that represents a user.

        : param str nickname: The nickname of the user to edit
        '''

        self["@controls"]["edit"] = {
            "href": api.url_for(User, nickname=nickname),
            "title": "Edit this user",
            "method": "PUT",
            "encoding": "json",
            "schema": EDIT_USER_SCHEMA
        }

    def add_control_add_rating(self, nickname):
        '''
        This adds the add-rating control to an object. Intended for the
        document object.
        '''

        self["@controls"]["critique:add-rating"] = {
            "href": api.url_for(UserRatings, nickname=nickname),
            "title": "Create a new rating",
            "encoding": "json",
            "method": "POST",
            "schema": CREATE_RATING_SCHEMA
        }

    def add_control_sender(self, nickname):
        '''
        This adds the sender control to an object. Intended for the
        document object.
        '''

        self["@controls"]["critique:sender"] = {
            "href": api.url_for(User, nickname=nickname),
            "title": "Sender of the resource",
        }

    def add_control_receiver(self, nickname):
        '''
        This adds the receiver control to an object. Intended for the
        document object.
        '''

        self["@controls"]["critique:receiver"] = {
            "href": api.url_for(User, nickname=nickname),
            "title": "Receiver of the resource",
        }

    def add_control_edit_rating(self,nickname, ratingId):
        '''
        This adds the link to edit a given rating for the
        document object.
        '''
        self["@controls"]["edit"] = {
            "href": api.url_for(Rating, ratingId=ratingId),
            "title": "Edit Rating",
            "method": "PUT",
            "encoding": "json",
            "schema": EDIT_USER_SCHEMA
        }

    def add_control_delete_rating(self, nickname, ratingId):
        '''
        This adds the link to delete a given rating for the
        document object.
        '''
        self["@controls"]["critique:delete"] = {
            "href": api.url_for(Rating, ratingId=ratingId),
            "method": "DELETE"
        }

    def add_control_edit_post(self, postId):
        '''
        Adds the edit control to an object. Intended for any object
        that represents a post.

        :param str postId: ID of a specific post.
        '''
        self["@controls"]["edit"] = {
            "href": api.url_for(Post, postId=postId),
            "title": "Edit a post",
            "method": "PUT",
            "encoding": "json",
            "schema": EDIT_POST_SCHEMA
        }


# Borrowed from lab exercises [1]
def create_error_response(status_code, title, message=None):
    '''
    Creates a: py: class:`flask.Response` instance when sending back an
    HTTP error response

    : param integer status_code: The HTTP status code of the response
    : param str title: A short description of the problem
    : param message: A long description of the problem
    : rtype:: py: class:`flask.Response`
    '''

    resource_url = None
    # We need to access the context in order to access the request.path
    ctx = _request_ctx_stack.top
    if ctx is not None:
        resource_url = request.path
    envelope = MasonObject(resource_url=resource_url)
    envelope.add_error(title, message)

    return Response(json.dumps(envelope), status_code, mimetype=MASON+";"+ERROR_PROFILE)


@app.errorhandler(404)
def resource_not_found(error):  # Borrowed from lab exercises [1]
    return create_error_response(404, "Resource not found",
                                 "This resource url does not exit")


@app.errorhandler(400)
def resource_not_found(error):  # Borrowed from lab exercises [1]
    return create_error_response(400, "Malformed input format",
                                 "The format of the input is incorrect")


@app.errorhandler(500)
def unknown_error(error):  # Borrowed from lab exercises [1]
    return create_error_response(500, "Error",
                                 "The system has failed. Please, contact the administrator")


# Borrowed from lab exercises [1]
# HOOKS
@app.before_request
def connect_db():  # Borrowed from lab exercises [1]
    '''
    Creates a database connection before the request is proccessed.

    The connection is stored in the application context variable flask.g .
    Hence it is accessible from the request object.
    '''

    g.con = app.config["Engine"].connect()


@app.teardown_request
def close_connection(exc):  # Borrowed from lab exercises [1]
    '''
    Closes the database connection
    Check if the connection is created. It might be exception appear before
    the connection is created.
    '''

    if hasattr(g, "con"):
        g.con.close()


class Users(Resource):

    def get(self):
        '''
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
        '''
        # PERFORM OPERATIONS
        # create users list
        users_db = g.con.get_users()

        # FILTER AND GENERATE THE RESPONSE
        # Create the envelope
        envelope = CritiqueObject()

        items = envelope["items"] = []

        for user in users_db:
            item = CritiqueObject(
                nickname=user["nickname"],
                givenName=user['firstname'],
                familyName=user['lastname'],
                avatar=user['avatar'],
                bio=user['bio']
            )
            items.append(item)
            item.add_control("self", href=api.url_for(
                User, nickname=user["nickname"]))
            item.add_control("profile", href=CRITIQUE_USER_PROFILE)

        envelope.add_namespace("critique", LINK_RELATIONS_URL)
        envelope.add_control_all_posts()

        envelope.add_control_add_user()
        envelope.add_control("self", href=api.url_for(Users))

        # RENDER
        return Response(json.dumps(envelope), 200, mimetype=MASON+";" + CRITIQUE_USER_PROFILE)

    def post(self):
        '''
        Adds a new user in the database.

        REQUEST ENTITY BODY:
         * Media type: JSON
         * Profile: Critique_User

        Semantic descriptors used in template: nickname(mandatory), givenName(mandatory),
        email(mandatory), bio(optional), avatar(optional), familyName(optional),
        birthDate(optional), telephone(optional), gender(optional)

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
        The: py: method:`Connection.create_user()` receives as a parameter a
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

        '''

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
        # optional fields

        # Conflict if user already exist
        if g.con.contains_user_extended(nickname, email):
            return create_error_response(422,
                                         "Nickname, email, or mobile already exist in the users list.")

        user = {
            'summary': {
                'nickname': nickname,
                'bio': request_body.get('bio', None),
                'avatar': request_body.get('avatar', None)
            },
            'details': {
                'firstname': firstName,
                'lastname': request_body.get('familyName', None),
                'email': email,
                'mobile': request_body.get('telephone', None),
                'gender': request_body.get('gender', None),
                'birthdate': request_body.get('birthDate', None),
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
    '''
    Resource has the basic information of a specific user.
    Bio is where the user should enter information about himself/herself,
    so it should be text. Email and telephone are unique texts as they
    will not repeat for other users. Gender, avatar and birthdate are texts.
    '''

    def get(self, nickname):
        '''
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
                /critique/profiles/user-profile/

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
        '''

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
        '''
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
        The: py: method:`Connection.modify_user()` receives as a parameter a
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
        '''

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
        '''
        Deletes the specified user.

        :param str nickname: The nickname of the user. Example: Scott.

        RESPONSE STATUS CODE:

            * If the user is deleted returns 204.
            * If the nickname does not exist return 404
            * If there was a db error return 500

        '''
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


class UserRatings(Resource):
    '''
    Contains the ratings list with ratings from all other users to this specific user.
    It should have a track of the ratings made by users to each other including the person
    who made the rating and that who received it. Also, it contains the rating id to keep
    track of the ratings.
    '''

    # def post(self, nickname):
    #    '''
    #     Adds a new rating in the database.

    #     REQUEST ENTITY BODY:
    #      * Media type: JSON
    #      * Profile: rating-profile

    #     Semantic descriptors used in template: nickname (string), avatar (string), bio (string)


    #     RESPONSE STATUS CODE:
    #      * Returns 201 + the url of the new resource in the Location header
    #      * Return 400 User info is not well formed or entity body is missing.
    #      * Return 415 if it receives a media type != application/json

    #     NOTE:
    #      * The attribute givenName is obtained from the column users_profile.firstname
    #      * The attribute familyName is obtained from the column users_profile.lastname
    #      * The rest of attributes match one-to-one with column names in the
    #        database.

    #     NOTE:
    #     The: py: method:`Connection.append_rating()` receives as a parameter a
    #     dictionary with the following format.

    #         {
    #             'rating_id': '',
    #             'timestamp': '',
    #             'sender': '',
    #             'receiver': '',
    #             'rating': ''
    #         }

    #     '''
    #     if JSON != request.headers.get("Content-Type", ""):
    #         abort(415)

    #     # PARSE THE REQUEST:
    #     request_body = request.get_json(force=True)
    #     if not request_body:
    #         return create_error_response(415,
    #                                      "Unsupported Media Type")

    #     # pick up rating_id so we can check for conflicts
    #     try:
    #         sender = request_body["sender"]
    #         receiver = request_body["receiver"]
    #         rating = request_body["rating"]

    #     except KeyError:
    #         return create_error_response(400,
    #                                      "Wrong request format")
    #     # optional fields

    #     # Conflict if user already exist
    #     if g.con.contains_rating(rating_id):
    #         return create_error_response(422,
    #                                      "Rating id already exist in the users list.")

    #     try:
    #         rating_id = g.con.create_rating(nickname, sender, receiver, rating)
    #     except ValueError:
    #         return create_error_response(400,
    #                                      "Wrong request format")

    #     # CREATE RESPONSE AND RENDER
    #     return Response(status=201,
    #                     headers={"Location": api.url_for(User, nickname=nickname)})


    def get(self, nickname):
        '''
        Extracts the ratings given to the user.

        INPUT PARAMETER:

        :param str nickname: The nickname of the user. Example: `Scott`.

        OUTPUT:
            * Return 200 if the nickname exists.
            * Return 404 if the nickname not found.

        RESPONSE ENTITY BODY:

        OUTPUT:
            * Media type: application/vnd.mason+json
                https://github.com/JornWildt/Mason
            * Profile: Rating
                /profiles/rating-profile

        Link relations used in items: self, profile

        Semantic descriptions used in items: ratingId, bestRating, ratingValue, sender, receiver

        Link relations used in links: self, add-rating

        Semantic descriptors used in template: items

        NOTE:
            * The attribute ratingId is obtained from the column ratings.rating_id
            * The attribute ratingValue is obtained from the column ratings.rating

        NOTE:
            * Database returns in this format
                {
                    rating_id: "string",
                    timestamp: "number",
                    sender: "string",
                    receiver: "string",
                    rating: "string",
                }
        '''

        userExist = g.con.contains_user(nickname)
        if not userExist:
            return create_error_response(404, "User not found.")

        # PERFORM OPERATIONS
        # create ratings list
        ratings_db = g.con.get_ratings(receiver=nickname)

        # FILTER AND GENERATE THE RESPONSE
        # Create the envelope
        envelope = CritiqueObject()

        items = envelope["items"] = []

        for rating in ratings_db:
            item = CritiqueObject(
                ratingId=rating["rating_id"],
                bestRating=10,
                ratingValue=rating['rating'],
                sender=rating['sender'],
                receiver=rating['receiver']
            )

            items.append(item)
            item.add_control_sender(rating['sender'])
            item.add_control_receiver(rating['receiver'])
            item.add_control("self",
                             href=api.url_for(Rating, nickname=nickname, ratingId=rating["rating_id"]))
            item.add_control("profile", href=CRITIQUE_RATING_PROFILE)

        envelope.add_namespace("critique", LINK_RELATIONS_URL)

        envelope.add_control("self", href=api.url_for(
            UserRatings, nickname=nickname))
        envelope.add_control_add_rating(nickname)

        # RENDER
        return Response(json.dumps(envelope), 200, mimetype=MASON+";" + CRITIQUE_RATING_PROFILE)


class UserInbox(Resource):
    
    '''
    Contains private posts sent to the user, it should include text as the actual post,
    however, rating is optional in the message.
    '''

    def get(self, nickname):
        '''
        Get posts sent to the user which are currently not public

        INPUT PARAMETER:

       :param user_id: default is None, takes the user id of the user
            that you want the posts of. if the parameter is None, it
            will raise a ValueError exception.
        :type nickname: nickname of the user

        OUTPUT:
            * Return 200 if the nickname exists.
            * Return 404 if the nickname not found.

        RESPONSE ENTITY BODY:

        OUTPUT:
            * Media type: application/vnd.mason+json
                https://github.com/JornWildt/Mason
            * Profile: Inbox
                /profiles/post_profile

        Link relations used in items: self, profile

        Semantic descriptions used in items: sender, receiver, timestamp, postId, replyTo, body, anonymous, public

        Link relations used in links: self, add-post, add-reply

        Semantic descriptors used in template: items

        '''

        userExist = g.con.contains_user(nickname)
        if not userExist:
            return create_error_response(404, "User not found.")

        # FILTER AND GENERATE THE RESPONSE
        # Create the envelope
        envelope = CritiqueObject()

        items = envelope["items"] = []

        #PEFORM OPERATIONS INITIAL CHECKS
        #Get the post from db
        post_db = g.con.get_posts_by_user(nickname,False)
        if not post_db:
            return create_error_response(404, "Posts not found",
                                         "There is no posts for %s" % nickname)

        for post in post_db:
            item = CritiqueObject(
                postId=post["post_id"],
                ratingValue=post['rating'],
                receiver=post['receiver'],
                replyTo=post['reply_to'],
                post_text=post['post_text'],
                anonymous=post['anonymous'],
                public=post['public']
            )
            if (post['public'] == 0):
                # check if the post is not public and then append
                items.append(item)
                item.add_control("self",
                                 href=api.url_for(UserInbox, nickname=post['receiver']))
                item.add_control("profile", href=CRITIQUE_POST_PROFILE)

        envelope.add_namespace("critique", LINK_RELATIONS_URL)
        envelope.add_control_user_inbox(nickname)
        envelope.add_control_reply_to(nickname)
        envelope.add_control("profile", href=CRITIQUE_POST_PROFILE)
        envelope.add_control("self", href=api.url_for(
            UserInbox, nickname=nickname))

        # if post['reply_to']:
        #     envelope.add_control("atom-thread:in-reply-to",
        #                          href=api.url_for(Post, postId=post['post_id']))
        # else:
        #     envelope.add_control("atom-thread:in-reply-to", href=None)

        #RENDER
        return Response(json.dumps(envelope), 200, mimetype=MASON+";" + CRITIQUE_POST_PROFILE)

    def post(self, nickname):
        '''
        Creates a new post to the list of posts. Returns the post URI.

        INPUT PARAMETERS:
        :param nickname: nickname of the user who is sending.
        :type nickname: string
        :param receiver_nickname: nickname of the user that we are sending to.
        :type receiver_nickname: string

        REQUEST ENTITY BODY:
        * Media type: application/vnd.mason+json
                https://github.com/JornWildt/Mason
        * Profile: Post Profile
                /critique/profiles/post_profile

        Semantic descriptors used in template: post_text(mandatory),
        anonymous(mandatory)

        RESPONSE STATUS CODE:
         * Returns 201 + the url of the new resource in the Location header
         * Return 400 Post info is not well formed or entity body is missing.
         * Return 415 if it receives a media type != application/json
         * Return 422 Conflict if the sender or receiver are not found

        NOTE:
        The: py: method:`Connection.create_post()` receives as a parameter
        a dictionary with the following format:
            {
                'post_id': '',
                'receiver': '',
                'timestamp': '',
                'reply_to': '',
                'post_text': '',
                'rating': '',
                'anonymous': '',
                'public': ''
            }
         '''
        # CONTENT TYPE CHECK
        if JSON != request.headers.get("Content-Type", ""):
            abort(415)

        # PARSE REQUEST
        request_body = request.get_json(force = True)
        if not request_body:
            return create_error_response(415,
                                        "Unsupported Media Type")

        # CHECK IF USER EXISTS
        userExist = g.con.contains_user(nickname)
        if not userExist:
            return create_error_response(404,"Sending user not found")


        # check mandatory fields
        try:
            post_text = request_body["post_text"]
            receiver_nickname = request_body["receiver_nickname"]
            anonymous = request_body["anonymous"]
        except KeyError:
            return create_error_response(400, "Wrong request format", "Post body missing")

        userExist = g.con.contains_user(receiver_nickname)
        if not userExist:
            return create_error_response(404, "Receiving user not found")

        new_post_id = g.con.create_post(sender_nickname = nickname,
                                        receiver_nickname = receiver_nickname,
                                        reply_to = None,
                                        post_text = post_text,
                                        anonymous = anonymous,
                                        public = 0,
                                        rating = None)
        if not new_post_id:
            return create_error_response(500, "Problem with database",
                                            "can not access database.")

        url = api.url_for(UserInbox, postId = new_post_id )

        return Response(status = 201,  headers={"Location": url})


class UserRiver(Resource):
    '''
    Contains public posts sent to the user, it should include text as the actual post,
    however, rating is optional in the posts.
    '''

    def get(self, nickname):
        '''
        Get posts sent to the user which are currently public

        INPUT PARAMETER:

       :param user_id: default is None, takes the user id of the user
            that you want the posts of. if the parameter is None, it
            will raise a ValueError exception.
        :type nickname: nickname of the user

        OUTPUT:
            * Return 200 if the nickname exists.
            * Return 404 if the nickname not found.

        RESPONSE ENTITY BODY:

        OUTPUT:
            * Media type: application/vnd.mason+json
                https://github.com/JornWildt/Mason
            * Profile: River
                /profiles/post_profile

        Link relations used in items: self, profile

        Semantic descriptions used in items: sender, receiver, timestamp, postId, replyTo, body, anonymous, public

        Link relations used in links: self, add-post, add-reply

        Semantic descriptors used in template: items

        '''

        userExist = g.con.contains_user(nickname)
        if not userExist:
            return create_error_response(404, "User not found.",
                                        "can't find a user to retrieve their river")

        # FILTER AND GENERATE THE RESPONSE
        # Create the envelope
        envelope = CritiqueObject()

        items = envelope["items"] = []

        # PEFORM OPERATIONS INITIAL CHECKS
        # Get the post from db and create posts list
        post_db = g.con.get_posts_by_user(nickname,False)
        if not post_db:
            return create_error_response(404, "Message not found",
                                         "There is no a message with id %s" % nickname)

        for post in post_db:
            if post["anonymous"]:
                senderPerson = "Anonymous"
            else:
                senderPerson = post["sender"]
            item = CritiqueObject(
                postId=post["post_id"],
                ratingValue=post['rating'],
                receiver=post['receiver'],
                replyTo=post['reply_to'],
                post_text=post['post_text'],
                anonymous=post['anonymous'],
                public=post['public'],
                sender = senderPerson
            )

            if (post['public'] == 1):
                # check if the post is public and then append
                items.append(item)
                item.add_control("self",
                                 href=api.url_for(UserRiver, nickname=post['receiver']))
                item.add_control("profile", href=CRITIQUE_POST_PROFILE)

        envelope.add_namespace("critique", LINK_RELATIONS_URL)
        envelope.add_control_user_river(nickname)
        envelope.add_control_reply_to(nickname)
        envelope.add_control("profile", href=CRITIQUE_POST_PROFILE)
        envelope.add_control("self", href=api.url_for(
            UserRiver, nickname=nickname))

        # if post['reply_to']:
        #     envelope.add_control("atom-thread:in-reply-to",
        #                          href=api.url_for(Post, postId=post['post_id']))
        # else:
        #     envelope.add_control("atom-thread:in-reply-to", href=None)

        #RENDER
        return Response(json.dumps(envelope), 200, mimetype=MASON+";" + CRITIQUE_POST_PROFILE)


class Ratings(Resource):
    '''
    Contains the ratings list with ratings from all other users to this specific user.
    It should have a track of the ratings made by users to each other including the person
    who made the rating and that who received it. Also, it contains the rating id to keep
    track of the ratings.
    '''

    def get(self):
        return Response('NOT IMPLEMENTED', 200)


class Post(Resource):
    '''
    Returns the information needed from a specific post where it contains the post text,
    timestamp, sender id and receiver id which should not be null value.
    Post_text is the post content that holds the data needed while rating is an integer of
    the ratings to the post from others.
    Public is an integer flag indicating if the post is public or private.
    While anonymous is the same but indicates whether the user wants to post it without being known.
    '''

    def get(self, postId):
        '''
        Extracts a post and all it’s information.

        :param str postId: ID of the requested post

        OUTPUT:
         * Return 200 if the post exists.
         * Return 404 if the post is not found.
         * Return 500 in case of system failure.

        RESPONSE ENTITY BODY:

        OUTPUT:
         * Media type: application/vnd.mason+json
                https://github.com/JornWildt/Mason
         * Profile: Post
                /critique/profiles/post-profile/

        Link relations used: self, profile, add-reply, delete, edit,
        collection, post-rating
        '''
        post_db = g.con.get_post(postId)
        if not post_db:
            return create_error_response(404, "Post not found.")

        envelope = CritiqueObject(
            sender = post_db["sender"],
            receiver = post_db["receiver"],
            timestamp = post_db["timestamp"] ,
            postId = post_db["post_id"] ,
            post_text = post_db["post_text"] ,
            anonymous = post_db["anonymous"] ,
            public = post_db["public"] ,
            bestRating = 10,
            ratingValue = post_db["rating"]
        )
        envelope.add_namespace("critique", LINK_RELATIONS_URL)

        envelope.add_control("self", href=api.url_for(Post, postId = postId))
        envelope.add_control("profile", href=CRITIQUE_POST_PROFILE)
        envelope.add_control("collection", href=api.url_for(Posts))
        envelope.add_control_edit_post(postId = postId)
        envelope.add_control_reply_to(receiver = post_db["receiver"])
        envelope.add_control_delete_post(nickname = post_db["sender"] , post_id = postId)
        envelope.add_control_sender(nickname = post_db["sender"])
        envelope.add_control_receiver(nickname = post_db["receiver"] )

        return Response(json.dumps(envelope), 200, mimetype=MASON+";"+ CRITIQUE_POST_PROFILE)

    def post(self, postId):
        '''
        posts a post as reply.

        REQUEST ENTITY BODY:
         * Media type: JSON
         * Profile: Critique_Post

        RESPONSE STATUS CODE:
         * Returns 201 + the url of the new resource in the Location header
         * Return 400 Post info is not well formed or entity body is missing.
         * Return 404 Post not found.
         * Return 415 if it receives a media type != application/json
         * Return 422 Sender not found.

        NOTE:
        The: py: method:`Connection.create_post()` receives as a parameter
        a dictionary with the following format:
            {
                'post_id': '',
                'sender': '',
                'timestamp': '',
                'reply_to': '',
                'post_text': '',
                'rating': '',
                'anonymous': '',
                'public': ''
            }
        '''
        # check format
        if JSON != request.headers.get("Content-Type", ""):
            abort(415)

        # check if postId is available
        postExists = g.con.contains_post(post_id = postId)
        if not postExists:
            return create_error_response(404, "Post not found",
                                    "There is no post with id %s" %postId)

        # parse request
        request_body = request.get_json(force = True)
        if not request_body:
            return create_error_response(415, "Unsupported Media Type")

        try:
            sender = request_body['sender']
            post_text = request_body['post_text']
        except KeyError:
            return create_error_response(400, "Wrong request format",
             "Post body missing or sender nickname invalid")

        userExist = g.con.contains_user(sender)
        if not userExist:
            return create_error_response(404,"Sending user not found")

        # getting the receiving user
        parent_post_db = g.con.get_post(postId)
        receiver = parent_post_db['sender']

        new_post_id = g.con.create_post(sender_nickname = sender,
                                        receiver_nickname = receiver,
                                        reply_to = postId,
                                        post_text = post_text,
                                        anonymous = request_body.get('anonymous', True),
                                        public = request_body.get('public', False),
                                        rating = None)
        if not new_post_id:
            return create_error_response(500, "Problem with database",
                                            "can not access database.")

        url = api.url_for(Post, postId = new_post_id )

        return Response(status = 201,  headers={"Location": url})

    def delete(self, postId):
        '''
        Deletes a specific post.

        :param str postId: ID of the post to delete.

        RESPONSE STATUS CODE:
         * Return 204 Post deleted successfully.
         * Return 404 Post not found.
         * Return 500 The system has failed. Please, contact the administrator.
        '''
        postExist = g.con.contains_post(postId)
        if not postExist:
            return create_error_response(404, "Post not found.")

        try:
            g.con.delete_post(postId)
        except:
            return create_error_response(500,
                "The system has failed. Please, contact the administrator.")
        return Response('', 204)

    def put(self, postId):
        '''
        Modifies the contents of a specified post.

        REQUEST ENTITY BODY:
         * Media type: JSON
         * Profile: Critique_Post

        Semantic descriptors used in template: post_text (optional)

        RESPONSE STATUS CODE:
         * Returns 204 + the url of the edited resource in the Location header
         * Return 404 If post not found with given id.
         * Return 415 if it receives a media type != application/json

        NOTE:
         * The attribute post_text is obtained from the column posts_profile.post_text
         * The rest of attributes match one-to-one with column names in the
           database.
        '''

        post_db = g.con.get_post(postId)
        if not post_db:
            return create_error_response(404, "Post not found.")

        if JSON != request.headers.get("Content-Type",""):
            return create_error_response(415, "UnsupportedMediaType",
                                         "Use a JSON compatible format")

        request_body = request.get_json(force = True)
        if not request_body:
            return create_error_response(415, "Format of the input is not json.")
        try:
            post_db['post_text'] = request_body.get(
                'post_text', post_db['post_text'])
            post_db['rating'] = request_body.get(
                'ratingValue', post_db['rating'])
            post_db['public'] = request_body.get(
                'public', post_db['public'])
        except KeyError:
            return create_error_response(400, "Wrong request format",
             "Can't acquire, either post body, rating or public value")
        if not g.con.modify_post(postId, post_db['post_text']):
            return create_error_response(500, "The system has failed. Please, contact the administrator.")

        return Response(status=204,
                        headers={"Location": api.url_for(Post, postId=postId)})


class Rating(Resource):
    '''
    Contains the ratings list with ratings from all other users to this specific user.
    It should have a track of the ratings made by users to each other including the person
    who made the rating and that who received it. Also, it contains the rating id to keep
    track of the ratings.
    '''

    def get(self, nickname ,ratingId):
        '''
        Extract a rating from the database.

        Returns status code 404 if the ratingId does not exist in the database.

        INPUT PARAMETER
        :param str ratingId: ID of the rating to be retrieved from the system.

        OUTPUT:
         * Return 200 if the rating ID exists.
         * Return 404 if the rating ID not found.
         * Return 500 in case of system failure.

        RESPONSE ENTITY BODY:

        OUTPUT:
            * Media type: application/vnd.mason+json
                https://github.com/JornWildt/Mason
            * Profile: Rating Profile
                /critique/profiles/rating-profile

        Link relations used: add-rating, edit, delete, self, profile, collection.

        '''

        ratingExist = g.con.contains_rating(ratingId)
        if not ratingExist:
            return create_error_response(404, "Rating not found",
                            "There is no rating with the given ID.")

        userExist = g.con.contains_user(nickname)
        if not userExist:
            return create_error_response(404, "Resquested user not found",
                                    "There is no user with the given nickname")
        # Filter and generate the response
        # Create the envelope
        # get the rating from DB
        rating_db = g.con.get_rating(ratingId)
        item = CritiqueObject(
            ratingId = rating_db["rating_id"],
            bestRating = 10,
            ratingValue = rating_db["rating"],
            sender = rating_db["sender"],
            receiver = rating_db["receiver"]
        )
        item.add_namespace("critique", LINK_RELATIONS_URL)

        item.add_control("self", href = api.url_for(
            Rating, nickname=item["receiver"] , ratingId=item["ratingId"]))
        item.add_control("profile", href = CRITIQUE_RATING_PROFILE)
        item.add_control("collection", href = api.url_for(UserRatings, nickname=item["receiver"]))
        item.add_control_edit_rating(
            ratingId=ratingId, nickname=item["receiver"])
        item.add_control_delete_rating(
            ratingId=ratingId, nickname=item["receiver"])
        item.add_control_sender(nickname = rating_db["sender"])
        item.add_control_receiver(nickname = rating_db["receiver"])

        return Response(json.dumps(item), 200, mimetype=MASON+";" + CRITIQUE_RATING_PROFILE)

    def put(self, ratingId, nickname):
        '''
        Modifies a rating.

        REQUEST ENTITY BODY:
         * Media type: JSON
         * Profile: Critique_User

        Semantic descriptors used in template: ratingId (required), new_rating (optional)

        RESPONSE STATUS CODE:
         * Returns 204 + the url of the edited resource in the Location header
         * Return 404 If rating not found with given id.
         * Return 415 if it receives a media type != application/json
         * Return 500 if there was a db error


        NOTE:
         * The attribute ratingId is obtained from the column ratings_profile.ratingId
         * The attribute new_rating is obtained from the column ratings_profile.new_rating
         * The rest of attributes match one-to-one with column names in the
           database.
        '''

        rating_db = g.con.get_rating(ratingId)
        if not rating_db:
            return create_error_response(404, "User not found.")

        request_body = request.get_json()
        if not request_body:
            return create_error_response(415, "Format of the input is not json.")

        rating_db['rating'] = request_body.get(
            'rating', rating_db['rating'])

        if not g.con.modify_rating(ratingId, rating_db):
            return create_error_response(500, "The system has failed. Please, contact the administrator.")

        return Response(status=204,
                        headers={"Location": api.url_for(Rating, rating_id=ratingId)})

    def delete(self, ratingId, nickname):
        '''
        Deletes the specified rating.

        :param integer ratingId: The id of the a rating. Example: rtg-015.

        RESPONSE STATUS CODE:

            * If the rating is deleted returns 204.
            * If the rating does not exist return 404
            * If there was a db error return 500
        '''
        # PEROFRM OPERATIONS

        ratingExist = g.con.contains_rating(ratingId)
        if not ratingExist:
            return create_error_response(404, "Rating not found.")

        # Try to delete the Rating. If it could not be deleted, the database
        # returns None.

        try:
            if g.con.delete_rating(ratingId):
                # RENDER RESPONSE
                return Response('', 204)
            else:
                # GENERATE ERROR RESPONSE
                return create_error_response(404, "Rating not found.")
        except:
            return create_error_response(500,
                                         "The system has failed. Please, contact the administrator.")


class Posts(Resource):
    def get(self):
        '''
        Gets a list of all posts
        '''
        return Response('NOT IMPLEMENTED', 200)


# Add the Regex Converter so we can use regex expressions when we define the
# routes
# Borrowed from lab exercises [1]
app.url_map.converters["regex"] = RegexConverter


# Define the routes
api.add_resource(Users, "/critique/api/users/",
                 endpoint="users")
api.add_resource(User, "/critique/api/users/<nickname>/",
                 endpoint="user")
api.add_resource(UserInbox, "/critique/api/users/<nickname>/inbox/",
                 endpoint="inbox")
api.add_resource(UserRiver, "/critique/api/users/<nickname>/river/",
                 endpoint="river")
api.add_resource(UserRatings, "/critique/api/users/<nickname>/ratings/",
                 endpoint="user-ratings")
api.add_resource(Rating, "/critique/api/users/<nickname>/ratings/<ratingId>/",
                 endpoint="rating")
api.add_resource(Posts, "/critique/api/posts/",
                 endpoint="posts")
api.add_resource(Post, "/critique/api/posts/<postId>/",
                 endpoint="post")

# Redirect profile


@app.route("/profiles/<profile_name>/")  # Borrowed from lab exercises [1]
def redirect_to_profile(profile_name):
    return redirect(APIARY_PROFILES_URL + profile_name)


# Borrowed from lab exercises [1]
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
if __name__ == '__main__':  # Borrowed from lab exercises [1]
    # Debug true activates automatic code reloading and improved error messages
    app.run(debug=True)
