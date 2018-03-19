# Critique

## Link Relations

### add-user

Creates a new user via `POST`.

#### GET /critique/link-relations/add-user

Return the link relation description in HTML format.

```json
POSSIBLE RESPONSES

200:
    HEADER
        Response: 200
        Content-Type: text/html
```

### user-inbox

Returns the posts sent to the user which are currently not public via `GET`.

#### GET /critique/link-relations/user-inbox

Return the link relation description in HTML format.

```json
POSSIBLE RESPONSES

200:
    HEADER
        Response: 200
        Content-Type: text/html
```

### user-river

Returns the posts sent to the user which are currently public via `GET`.

#### GET /critique/link-relations/user-river

Return the link relation description in HTML format.

```json
POSSIBLE RESPONSES

200:
    HEADER
        Response: 200
        Content-Type: text/html
```

### user-ratings

Returns the ratings sent to the user via `GET`.

#### GET /critique/link-relations/ratings

Return the link relation description in HTML format.

```json
POSSIBLE RESPONSES

200:
    HEADER
        Response: 200
        Content-Type: text/html
```

### delete

Deletes the current context. Use via `DELETE`.

#### GET /critique/link-relations/delete

Return the link relation description in HTML format.

```json
POSSIBLE RESPONSES

200:
    HEADER
        Response: 200
        Content-Type: text/html
```

## Profiles

### Error Profile

Profile definition for all errors messages in the system. Related [profile call](#get-critiqueprofileserror_profile).

#### Error Semantic Descriptors

##### Data Type Error

- `resource_url` (string): URL of the resource generating the error.

### GET /critique/profiles/error_profile

Return the User Profile in HTML format.

```json
POSSIBLE RESPONSES

200:
    HEADER
        Response: 200
        Content-Type: text/html
```

### User Profile

Profile definition for all user resources. Related [profile call](#get-critiqueprofilesuser_profile).

#### User Dependencies

This profile inherits:

- Some semantic descriptors from [Person](http://schema.org/Person)
- Some link relations from IANA Web linking [RFC5988](https://www.iana.org//assignmentscritique/link-/relationscritique/link-relations.xhtml)

#### User Relations

- [`add-user`](#add-user)
- [`delete`](#delete)
- [`user-inbox`](#user-inbox)
- [`user-river`](#user-river)
- [`user-ratings`](#user-ratings)

Inherited from IANA RFC5988:

- [`collection`](http://tools.ietf.org/html/rfc6573): Only accessible through `GET`.
- [`edit`](https://tools.ietf.org/html/rfc5023#section-11.1): This link allows editing the user via `PUT`.
- [`profile`](https://tools.ietf.org/html/rfc6906): The link contains the location of the resource profile.

#### User Semantic Descriptors

##### Data Type User

- `nickname` (string): Nickname of the user. Mandatory in representations in which a new user is generated.
- `avatar` (string): Avatar of the user. Optional in representations in which a new user is generated.
- `bio` (string): Signiture of the user. Optional in representations in which a new user is generated.

Inherited from [Person](http://schema.org/Person):

- [`givenName`](http://schema.org/givenName) (string): Mandatory in representations in which a new user is generated.
- [`familyName`](http://schema.org/familyName) (string): Optional in representations in which a new user is generated.
- [`email`](http://schema.org/email) (string): Mandatory in representations in which a new user is generated.
- [`birthDate`](http://schema.org/birthDate) (string): Optional in representations in which a new user is generated.
- [`telephone`](http://schema.org/telephone) (string): Optional in representations in which a new user is generated.
- [`gender`](http://schema.org/gender) (string): Optional in representations in which a new user is generated.

### GET /critique/profiles/user_profile

Return the User Profile in HTML format.

```json
POSSIBLE RESPONSES

200:
    HEADER
        Response: 200
        Content-Type: text/html
```

## Users

All these resources use the [User Profile](#user-profile).

In addition all error messages follow the [Error Profile](#error-profile).

### GET /critique/api/users/

A list of all users in the platform.

```json
REQUEST
    HEADER
        Accept: application/vnd.mason+json
```

```json
POSSIBLE RESPONSES

200:
    HEADER
        Response: 200 (Successful.)
        Content-Type: application/vnd.mason+json
    BODY
        {
            "items": [
                {
                    "givenName": "Scott",
                    "familyName": "Pilgrim",
                    "bio": "Best bass in town. Ramona <3",
                    "avatar": "photo1.jpg",
                    "@controls": {
                        "self": {
                            "href": "/critique/api/users/Scott/"
                        },
                        "profile": {
                            "href": "/critique/profiles/user-profile/"
                        }
                    }
                },
                {
                    "givenName": "Kim",
                    "familyName": "Pine",
                    "bio": "Drums! Dont irritate me...",
                    "avatar": "photo3.jpg",
                    "@controls": {
                        "self": {
                            "href": "/critique/api/users/Kim/"
                        },
                        "profile": {
                            "href": "/critique/profiles/user-profile/"
                        }
                    }
                }
            ],
            "@namespaces": {
                "critique": {
                    "name": "/critique/link-relations/"
                }
            },
            "@controls": {
                "self": {
                    "href": "/forum/api/users/"
                },
                "critique:add-user": {
                    "href": "/forum/api/users/",
                    "encoding": "json",
                    "method": "POST",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "nickname": {
                                "title": "Nickname",
                                "description": "User nickname",
                                "type": "string"
                            },
                            "givenName": {
                                "title": "Given name",
                                "description": "User given name",
                                "type": "string"
                            },
                            "email": {
                                "title": "Email",
                                "description": "User email",
                                "type": "string"
                            }
                        },
                        "required": ["nickname", "givenName", "email"]
                    }
                }
            }
        }
    RELATIONS
        self
        profile
        add-user
```

### POST /critique/api/users/

Create a new user.

```json
REQUEST

    HEADER
        Content-Type: application/json
        Accept: application/vnd.mason+json
    BODY
        {
            "nickname": "alkila",
            "givenName": "Sercan",
            "email": "sercan@mail.com"
        }
```

```json
POSSIBLE RESPONSES

201:
    HEADER
        Response: 201 (User created successfully.)
        Location: URL of the newly created resource.

400:
    HEADER
        Response: 400
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "User info is not well formed or entity body is missing."
            },
            "resource_url": "/critique/api/users/"
        }

415:
    HEADER
        Response: 415
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Format of the input is not json."
            },
            "resource_url": "/critique/api/users/"
        }

422:
    HEADER
        Response: 422
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Nickname, email, or mobile already exist in the users list."
            },
            "resource_url": "/critique/api/users/"
        }

500:
    HEADER
        Response: 500
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "The system has failed. Please, contact the administrator."
            },
            "resource_url": "/critique/api/users/"
        }
```

### GET /critique/api/users/{nickname}/

Receives the information of a particular user.

```json
PARAMETERS
    nickname: The nickname of the user. Example, Scott.
```

```json
REQUEST
    HEADER
        Accept: application/vnd.mason+json
```

```json
POSSIBLE RESPONSES

200:
    HEADER
        Response: 200 (Successful.)
        Content-Type: application/vnd.mason+json
    BODY
        {
            "givenName": "Scott",
            "familyName": "Pilgrim",
            "avatar": "photo1.jpg",
            "bio": "Best bass in town. Ramona <3",
            "email": "scott@outlook.com",
            "birthdate": "1998-01-22",
            "telephone": null,
            "gender": "male",
            "@namespaces": {
                "critique": {
                    "name": "/critique/link-relations/"
                }
            },
            "@controls": {
                "self": {
                    "href": "/critique/api/users/Scott/"
                },
                "profile": {
                    "href": "/critique/profiles/user-profile/"
                },
                "collection": {
                    "href": "/forum/api/users/"
                },
                "edit": {
                    "title": "Edit this user",
                    "href": "/forum/api/users/Scott/",
                    "encoding": "json",
                    "method": "PUT",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "givenName": {
                                "title": "given name",
                                "description": "user given name",
                                "type": "string"
                            },
                            "familyName": {
                                "title": "family name",
                                "description": "user family name",
                                "type": "string"
                            },
                            "avatar": {
                                "title": "avatar",
                                "description": "user avatar",
                                "type": "string"
                            },
                            "bio": {
                                "title": "bio",
                                "description": "user bio",
                                "type": "string"
                            },
                            "email": {
                                "title": "email",
                                "description": "user email",
                                "type": "string"
                            },
                            "birthdate": {
                                "title": "birthdate",
                                "description": "user birthdate",
                                "type": "string"
                            },
                            "telephone": {
                                "title": "telephone",
                                "description": "user telephone",
                                "type": "string"
                            },
                            "gender": {
                                "title": "gender",
                                "description": "user gender",
                                "type": "string"
                            }
                        },
                        "required": [ ]
                    }
                },
                "critique:delete": {
                    "href": "/critique/api/users/Scott/",
                    "method": "DELETE"
                },
                "critique:user-inbox": {
                    "href": "/critique/api/users/Scott/inbox"
                },
                "critique:user-river": {
                    "href": "/critique/api/users/Scott/river"
                },
                "critique:user-ratings": {
                    "href": "/critique/api/users/Scott/ratings"
                }
            }
        }
    RELATIONS
        self
        profile
        collection
        edit
        delete
        user-inbox
        user-river
        user-ratings

404:
    HEADER
        Response: 404
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "User not found."
            },
            "resource_url": "/critique/api/users/{nickname}/"
        }
```

### PUT /critique/api/users/{nickname}/

Edit the information of a particular user.

```json
PARAMETERS
    nickname: The nickname of the user. Example, Scott.
```

```json
REQUEST

    HEADER
        Content-Type: application/json
        Accept: application/vnd.mason+json
    BODY
        {
            "givenName": "Scott",
            "familyName": "Pilgrim",
            "avatar": "photo1.jpg",
            "bio": "Best bass in town. Ramona <3",
            "email": "scott@outlook.com",
            "birthdate": "1998-01-22",
            "telephone": null,
            "gender": "male"
        }
```

```json
POSSIBLE RESPONSES

204:
    HEADER
        Response: 204 (User modified successfully.)
        Location: URL of the newly edited resource.

400:
    HEADER
        Response: 400
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "User info is not well formed or it is empty."
            },
            "resource_url": "/critique/api/users/{nickname}/"
        }

404:
    HEADER
        Response: 404
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "User not found."
            },
            "resource_url": "/critique/api/users/{nickname}/"
        }

415:
    HEADER
        Response: 415
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Format of the input is not json."
            },
            "resource_url": "/critique/api/users/{nickname}/"
        }

422:
    HEADER
        Response: 422
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Nickname, email, or mobile already exist in the users list."
            },
            "resource_url": "/critique/api/users/{nickname}/"
        }

500:
    HEADER
        Response: 500
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "The system has failed. Please, contact the administrator."
            },
            "resource_url": "/critique/api/users/{nickname}/"
        }
```

### DELETE /critique/api/users/{nickname}/

```json
PARAMETERS
    nickname: The nickname of the user. Example, Scott.
```

```json
POSSIBLE RESPONSES

204:
    HEADER
        Response: 204 (User deleted successfully.)

404:
    HEADER
        Response: 404
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "User not found."
            },
            "resource_url": "/critique/api/users/{nickname}/"
        }

500:
    HEADER
        Response: 500
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "The system has failed. Please, contact the administrator."
            },
            "resource_url": "/critique/api/users/{nickname}/"
        }
```

### GET /critique/api/users/{nickname}/ratings/

```json
PARAMETERS
    TODO
```

```json
REQUEST
    HEADER
        Accept: application/vnd.mason+json
```

```json
POSSIBLE RESPONSES

200:
    HEADER
        Response: 200 (Successful.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO
    RELATIONS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

404:
    HEADER
        Response: 404
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "User not found."
            },
            "resource_url": "/critique/api/users/{nickname}/ratings/"
        }
```

### GET /critique/api/users/{nickname}/river/

```json
PARAMETERS
    nickname: The nickname of the user. for example: Scott.
```

```json
REQUEST
    HEADER
        Accept: application/vnd.mason+json
```

```json
POSSIBLE RESPONSES

200:
    HEADER
        Response: 200 (Successful.)
        Content-Type: application/vnd.mason+json
    BODY
        CHECK_THIS
        {
            "items": [

                {
                    "givenName": "Scott",
                    "avatar": "photo1.jpg",
                    "text":"this is a river text 01.",
                    "@controls":{
                        "self":{
                            "href": "/critique/api/users/mina/river/01"
                        },
                        "profile": {
                            "href": "/critique/profiles/user-profile/"
                        },
                        "critique:user-ratings": {
                            "href": "/critique/api/users/Scott/ratings"
                        }
                    }
                },
                {
                    "givenName": "Moamen",
                    "avatar": "photoMoamen.jpg",
                    "text":"this is a river text of Moamen.",
                    "@controls":{
                        "self":{
                            "href": "/critique/api/users/mina/river/02"
                        },
                        "profile": {
                            "href": "/critique/profiles/user-profile/"
                        },
                        "critique:user-ratings": {
                            "href": "/critique/api/users/Moamen/ratings"
                        }
                    }
                }
            ]
        }
    RELATIONS
        Self
        Profile
        user-ratings
404:
    HEADER
        Response: 404
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "User not found."
            },
            "resource_url": "/critique/api/users/{nickname}/river/"
        }
```

### GET /critique/api/users/{nickname}/inbox/

```json
PARAMETERS
    nickname: The nickname of the user. for example: Scott.
```

```json
REQUEST
    HEADER
        Accept: application/vnd.mason+json
```

```json
POSSIBLE RESPONSES

200:
    HEADER
        Response: 200 (Successful.)
        Content-Type: application/vnd.mason+json
    BODY
        CHECK_THIS
        {
            "items": [
                {
                    "givenName": "Walcott",
                    "avatar": "photoWalcott.jpg",
                    "text":"this is an inbox post text 01.",
                    "@controls":{
                        "self":{
                            "href": "/critique/api/users/mina/inbox/"
                        },
                        "profile": {
                            "href": "/critique/profiles/user-profile/"
                        },
                        "critique:user-ratings": {
                            "href": "/critique/api/users/Walcott/ratings"
                        }
                    }
                },
                {
                    "givenName": "Modric",
                    "avatar": "photoModric.jpg",
                    "text":"this is an inbox post text from Modric.",
                    "@controls":{
                        "self":{
                            "href": "/critique/api/users/mina/river/"
                        },
                        "profile": {
                            "href": "/critique/profiles/user-profile/"
                        },
                        "critique:user-ratings": {
                            "href": "/critique/api/users/Modric/ratings"
                        }
                    }
                }
            ]
        }
    RELATIONS
        Self
        Profile
        user-ratings

404:
    HEADER
        Response: 404
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "User not found."
            },
            "resource_url": "/critique/api/users/{nickname}/inbox/"
        }
```

## Posts

TODO
### GET /critique/api/posts/

A list of all posts in the platform

```json
REQUEST
    HEADER
        Accept: application/vnd.mason+json
```

```json
POSSIBLE RESPONSES

200:
    HEADER
        Response: 200 (Successful.)
        Content-Type: application/vnd.mason+json
    BODY
        {
            "items":[
                {
                    "sender":"Mina",
                    "receiver": "Sercant",
                    "text": "Hey man, nice work on PWP.",
                    "@controls": {
                        "self": {
                            "href": "/critique/api/posts/"
                        },
                        "profile": {
                            "href": "/critique/profiles/user-profile/"
                        }
                    }
                },
                {
                    "sender":"Brian",
                    "receiver": "Armadillo",
                    "text": "You have weird working ethics.",
                    "@controls": {
                        "self": {
                            "href": "/critique/api/posts/"
                        },
                        "profile": {
                            "href": "/critique/profiles/user-profile/"
                        }
                    }
                }
            ],
            "@namespace": {
                "critique": {
                    "name": "/critique/link-relations/"
                }
            },

        }
    RELATIONS
        Self
        Profile

```

### POST /critique/api/posts/

Creates a new post.

```json
REQUEST

    HEADER
        Content-Type: application/json
        Accept: application/vnd.mason+json
    BODY
        {
            "sender": "lisa",
            "receiver": "ibiza",
            "text": "You startup is amazing, keep up the good work."
        }
```

```json
POSSIBLE RESPONSES

201:
    HEADER
        Response: 201 (Post created successfully.)
        Location: URL of the newly created resource.

400:
    HEADER
        Response: 400
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Post info is not well formed or entity body is missing."
            },
            "resource_url": "/critique/api/posts/"
        }

415:
    HEADER
        Response: 415
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Format of the input is not json."
            },
            "resource_url": "/critique/api/posts/"
        }

422:
    HEADER
        Response: 422
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Sender or receiver not found."
            },
            "resource_url": "/critique/api/posts/"
        }

500:
    HEADER
        Response: 500
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "The system has failed. Please, contact the administrator."
            },
            "resource_url": "/critique/api/posts/"
        }
```

### GET /critique/api/posts/{postId}/

Gets a specific post from the platform

```json
PARAMETERS
    postId: the specific post ID required to retrieve the post. ex: 113
```

```json
REQUEST
    HEADER
        Accept: application/vnd.mason+json
```

```json
POSSIBLE RESPONSES

200:
    HEADER
        Response: 200 (Successful.)
        Content-Type: application/vnd.mason+json
    BODY
        {
            "sender": "Jeff",
            "receiver": "Audrey",
            "text": "I love you.",
            "rating": 5,
            "@namespaces": {
                "critique": {
                    "name": "/critique/link-relations/"
                }
            },
            "@controls": {
                "self": {
                    "href": "/critique/api/posts/113/"
                },
                "profile": {
                    "href": "/critique/profiles/user-profile/"
                },
                "collection": {
                    "href": "/critique/api/posts/"
                },
                "edit": {
                    "title": "Edit this post",
                    "href": "/critique/api/posts/113/",
                    "encoding": "json",
                    "method": "PUT",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "title": "post's text",
                                "description": "contents of the post",
                                "type": "string"
                            }
                        }
                    }
                },
                "critique:delete":{
                    "href": "/critique/api/posts/113",
                    "method": "DELETE"
                },
                "critique:user-ratings": {
                    "href": "/critique/api/users/Jeff/ratings"
                }
            },

        }
    RELATIONS
        self
        Profile
        collection
        edit
        delete
        user-ratings

404:
    HEADER
        Response: 404
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Post not found."
            },
            "resource_url": "/critique/api/posts/{postId}/"
        }
```

### POST /critique/api/posts/{postId}/

add a reply to an existing post

```json
PARAMETERS
    postId: the parent post ID which gets the reply.
```

```json
REQUEST

    HEADER
        Content-Type: application/json
        Accept: application/vnd.mason+json
    PARAMETERS
        {
            "receiverNickname": "Hammam"
        }
    BODY
        {
            "senderNickname": "Shazam",
            "text": "hey man, I would really appreciate if we could meet."
        }
```

```json
POSSIBLE RESPONSES

201:
    HEADER
        Response: 201 (Post created successfully.)
        Location: URL of the newly created resource.

400:
    HEADER
        Response: 400
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Post info is not well formed or entity body is missing."
            },
            "resource_url": "/critique/api/posts/{postId}/"
        }

415:
    HEADER
        Response: 415
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Format of the input is not json."
            },
            "resource_url": "/critique/api/posts/{postId}/"
        }

404:
    HEADER
        Response: 404
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Post not found."
            },
            "resource_url": "/critique/api/posts/{postId}/"
        }

422:
    HEADER
        Response: 422
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Sender not found."
            },
            "resource_url": "/critique/api/posts/{postId}/"
        }

500:
    HEADER
        Response: 500
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "The system has failed. Please, contact the administrator."
            },
            "resource_url": "/critique/api/posts/{postId}/"
        }
```

### PUT /critique/api/posts/{postId}/

Edit an existing post.

```json
PARAMETERS
    postId: ID of specific post to edit.
```

```json
REQUEST

    HEADER
        Content-Type: application/json
        Accept: application/vnd.mason+json
    PARAMETERS
        {
            "postId": 113
        }
    BODY
        {
            "text": "I hate you, it is the edited reply"
        }
```

```json
POSSIBLE RESPONSES

204:
    HEADER
        Response: 204 (Post modified successfully.)
        Location: URL of the newly edited resource.

400:
    HEADER
        Response: 400
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Post info is not well formed or it is empty."
            },
            "resource_url": "/critique/api/posts/{postId}/"
        }

404:
    HEADER
        Response: 404
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Post not found."
            },
            "resource_url": "/critique/api/posts/{postId}/"
        }

415:
    HEADER
        Response: 415
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Format of the input is not json."
            },
            "resource_url": "/critique/api/posts/{postId}/"
        }

500:
    HEADER
        Response: 500
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "The system has failed. Please, contact the administrator."
            },
            "resource_url": "/critique/api/posts/{postId}/"
        }
```

### DELETE /critique/api/posts/{postId}/

Deletes an existing post.

```json
PARAMETERS
    postId: ID of the post to delete.
```

```json
POSSIBLE RESPONSES

204:
    HEADER
        Response: 204 (Post deleted successfully.)

404:
    HEADER
        Response: 404
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Post not found."
            },
            "resource_url": "/critique/api/posts/{postId}/"
        }

500:
    HEADER
        Response: 500
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "The system has failed. Please, contact the administrator."
            },
            "resource_url": "/critique/api/posts/{postId}/"
        }
```

## Ratings

TODO description

### POST /critique/api/ratings/

```json
REQUEST

    HEADER
        Content-Type: application/json
        Accept: application/vnd.mason+json
    PARAMETERS
        TODO
    BODY
        TODO
```

```json
POSSIBLE RESPONSES

201:
    HEADER
        Response: 201 (Rating created successfully.)
        Location: URL of the newly created resource.

400:
    HEADER
        Response: 400
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Rating info is not well formed or entity body is missing."
            },
            "resource_url": "/critique/api/ratings/"
        }

415:
    HEADER
        Response: 415
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Format of the input is not json."
            },
            "resource_url": "/critique/api/ratings/"
        }

422:
    HEADER
        Response: 422
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Sender or receiver not found."
            },
            "resource_url": "/critique/api/ratings/"
        }

500:
    HEADER
        Response: 500
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "The system has failed. Please, contact the administrator."
            },
            "resource_url": "/critique/api/ratings/"
        }
```

### GET /critique/api/ratings/{ratingId}/

```json
PARAMETERS
    TODO
```

```json
REQUEST
    HEADER
        Accept: application/vnd.mason+json
```

```json
POSSIBLE RESPONSES

200:
    HEADER
        Response: 200 (Successful.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO
    RELATIONS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

404:
    HEADER
        Response: 404
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Rating not found."
            },
            "resource_url": "/critique/api/ratings/{ratingId}/"
        }
```

### PUT /critique/api/ratings/{ratingId}/

```json
PARAMETERS
    TODO
```

```json
REQUEST

    HEADER
        Content-Type: application/json
        Accept: application/vnd.mason+json
    PARAMETERS
        TODO
    BODY
        TODO
```

```json
POSSIBLE RESPONSES

204:
    HEADER
        Response: 204 (Rating modified successfully.)
        Location: URL of the newly edited resource.

400:
    HEADER
        Response: 400
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Rating info is not well formed or it is empty."
            },
            "resource_url": "/critique/api/ratings/{ratingId}/"
        }

404:
    HEADER
        Response: 404
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Rating not found."
            },
            "resource_url": "/critique/api/ratings/{ratingId}/"
        }

415:
    HEADER
        Response: 415
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Format of the input is not json."
            },
            "resource_url": "/critique/api/ratings/{ratingId}/"
        }

500:
    HEADER
        Response: 500
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "The system has failed. Please, contact the administrator."
            },
            "resource_url": "/critique/api/ratings/{ratingId}/"
        }
```

### DELETE /critique/api/ratings/{ratingId}/

```json
PARAMETERS
    TODO
```

```json
POSSIBLE RESPONSES

204:
    HEADER
        Response: 204 (Rating deleted successfully.)

404:
    HEADER
        Response: 404
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "Rating not found."
            },
            "resource_url": "/critique/api/ratings/{ratingId}/"
        }

500:
    HEADER
        Response: 500
        Content-Type: application/vnd.mason+json
    BODY
        {
            "@error": {
                "@message": "The system has failed. Please, contact the administrator."
            },
            "resource_url": "/critique/api/ratings/{ratingId}/"
        }
```
