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

### User Profile

Profile definition for all user resources. Related [profile call](#get-profilesuser_profile).

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
                            },
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

```json
REQUEST

    HEADER
        Content-Type: application/json
        Accept: application/vnd.mason+json
    PARAMETERS
        TODO
    EXAMPLE
        TODO
```

```json
POSSIBLE RESPONSES

201:
    HEADER
        Response: 201 (User created successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO
    RELATIONS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

400:
    HEADER
        Response: 400
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "User info is not well formed or entity body is missing."
            },
            "resource_url": "TODO"
        }

415:
    HEADER
        Response: 415
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Format of the input is not json."
            },
            "resource_url": "TODO"
        }

422:
    HEADER
        Response: 422
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Nickname, email, or mobile already exist in the users list."
            },
            "resource_url": "TODO"
        }

500:
    HEADER
        Response: 500
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "The system has failed. Please, contact the administrator."
            },
            "resource_url": "TODO"
        }
```

### GET /critique/api/users/{nickname}/

```json
REQUEST
    HEADER
        Accept: application/vnd.mason+json
```

```json
POSSIBLE RESPONSES

201:
    HEADER
        Response: 201 (Successful.)
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
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "User not found."
            },
            "resource_url": "TODO"
        }
```

### PUT /critique/api/users/{nickname}/

```json
REQUEST

    HEADER
        Content-Type: application/json
        Accept: application/vnd.mason+json
    PARAMETERS
        TODO
    EXAMPLE
        TODO
```

```json
POSSIBLE RESPONSES

204:
    HEADER
        Response: 204 (User modified successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO
    RELATIONS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

400:
    HEADER
        Response: 400
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "User info is not well formed or it is empty."
            },
            "resource_url": "TODO"
        }

404:
    HEADER
        Response: 404
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "User not found."
            },
            "resource_url": "TODO"
        }

415:
    HEADER
        Response: 415
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Format of the input is not json."
            },
            "resource_url": "TODO"
        }

422:
    HEADER
        Response: 422
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Nickname, email, or mobile already exist in the users list."
            },
            "resource_url": "TODO"
        }

500:
    HEADER
        Response: 500
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "The system has failed. Please, contact the administrator."
            },
            "resource_url": "TODO"
        }
```

### DELETE /critique/api/users/{nickname}/

```json
POSSIBLE RESPONSES

204:
    HEADER
        Response: 204 (User deleted successfully.)
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
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "User not found."
            },
            "resource_url": "TODO"
        }

500:
    HEADER
        Response: 500
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "The system has failed. Please, contact the administrator."
            },
            "resource_url": "TODO"
        }
```

### GET /critique/api/users/{nickname}/ratings/

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
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "User not found."
            },
            "resource_url": "TODO"
        }
```

### GET /critique/api/users/{nickname}/river/

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
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "User not found."
            },
            "resource_url": "TODO"
        }
```

### GET /critique/api/users/{nickname}/inbox/

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
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "User not found."
            },
            "resource_url": "TODO"
        }
```

## Posts

TODO description

### GET /critique/api/posts/

```json
REQUEST
    HEADER
        Accept: application/vnd.mason+json
```

```json
POSSIBLE RESPONSES

200:
    HEADER
        Response: 200 (Successful)
        Content-Type: application/vnd.mason+json
    BODY
        TODO
    RELATIONS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS
```

### POST /critique/api/posts/

```json
REQUEST

    HEADER
        Content-Type: application/json
        Accept: application/vnd.mason+json
    PARAMETERS
        TODO
    EXAMPLE
        TODO
```

```json
POSSIBLE RESPONSES

201:
    HEADER
        Response: 201 (Post created successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO
    RELATIONS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

400:
    HEADER
        Response: 400
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Post info is not well formed or entity body is missing."
            },
            "resource_url": "TODO"
        }

415:
    HEADER
        Response: 415
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Format of the input is not json."
            },
            "resource_url": "TODO"
        }

422:
    HEADER
        Response: 422
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Sender or receiver not found."
            },
            "resource_url": "TODO"
        }

500:
    HEADER
        Response: 500
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "The system has failed. Please, contact the administrator."
            },
            "resource_url": "TODO"
        }
```

### GET /critique/api/posts/{postId}/

```json
REQUEST
    HEADER
        Accept: application/vnd.mason+json
```

```json
POSSIBLE RESPONSES

201:
    HEADER
        Response: 201 (Successful.)
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
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Post not found."
            },
            "resource_url": "TODO"
        }
```

### POST /critique/api/posts/{postId}/

```json
REQUEST

    HEADER
        Content-Type: application/json
        Accept: application/vnd.mason+json
    PARAMETERS
        TODO
    EXAMPLE
        TODO
```

```json
POSSIBLE RESPONSES

201:
    HEADER
        Response: 201 (Post created successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO
    RELATIONS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

400:
    HEADER
        Response: 400
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Post info is not well formed or entity body is missing."
            },
            "resource_url": "TODO"
        }

415:
    HEADER
        Response: 415
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Format of the input is not json."
            },
            "resource_url": "TODO"
        }

404:
    HEADER
        Response: 404
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Post not found."
            },
            "resource_url": "TODO"
        }

422:
    HEADER
        Response: 422
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Sender not found."
            },
            "resource_url": "TODO"
        }

500:
    HEADER
        Response: 500
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "The system has failed. Please, contact the administrator."
            },
            "resource_url": "TODO"
        }
```

### PUT /critique/api/posts/{postId}/

```json
REQUEST

    HEADER
        Content-Type: application/json
        Accept: application/vnd.mason+json
    PARAMETERS
        TODO
    EXAMPLE
        TODO
```

```json
POSSIBLE RESPONSES

204:
    HEADER
        Response: 204 (Post modified successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO
    RELATIONS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

400:
    HEADER
        Response: 400
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Post info is not well formed or it is empty."
            },
            "resource_url": "TODO"
        }

404:
    HEADER
        Response: 404
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Post not found."
            },
            "resource_url": "TODO"
        }

415:
    HEADER
        Response: 415
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Format of the input is not json."
            },
            "resource_url": "TODO"
        }

500:
    HEADER
        Response: 500
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "The system has failed. Please, contact the administrator."
            },
            "resource_url": "TODO"
        }
```

### DELETE /critique/api/posts/{postId}/

```json
POSSIBLE RESPONSES

204:
    HEADER
        Response: 204 (Post deleted successfully.)
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
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Post not found."
            },
            "resource_url": "TODO"
        }

500:
    HEADER
        Response: 500
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "The system has failed. Please, contact the administrator."
            },
            "resource_url": "TODO"
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
    EXAMPLE
        TODO
```

```json
POSSIBLE RESPONSES

201:
    HEADER
        Response: 201 (Rating created successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO
    RELATIONS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

400:
    HEADER
        Response: 400
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Rating info is not well formed or entity body is missing."
            },
            "resource_url": "TODO"
        }

415:
    HEADER
        Response: 415
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Format of the input is not json."
            },
            "resource_url": "TODO"
        }

422:
    HEADER
        Response: 422
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Sender or receiver not found."
            },
            "resource_url": "TODO"
        }

500:
    HEADER
        Response: 500
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "The system has failed. Please, contact the administrator."
            },
            "resource_url": "TODO"
        }
```

### GET /critique/api/ratings/{ratingId}/

```json
REQUEST
    HEADER
        Accept: application/vnd.mason+json
```

```json
POSSIBLE RESPONSES

201:
    HEADER
        Response: 201 (Successful.)
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
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Rating not found."
            },
            "resource_url": "TODO"
        }
```

### PUT /critique/api/ratings/{ratingId}/

```json
REQUEST

    HEADER
        Content-Type: application/json
        Accept: application/vnd.mason+json
    PARAMETERS
        TODO
    EXAMPLE
        TODO
```

```json
POSSIBLE RESPONSES

204:
    HEADER
        Response: 204 (Rating modified successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO
    RELATIONS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

400:
    HEADER
        Response: 400
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Rating info is not well formed or it is empty."
            },
            "resource_url": "TODO"
        }

404:
    HEADER
        Response: 404
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Rating not found."
            },
            "resource_url": "TODO"
        }

415:
    HEADER
        Response: 415
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Format of the input is not json."
            },
            "resource_url": "TODO"
        }

500:
    HEADER
        Response: 500
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "The system has failed. Please, contact the administrator."
            },
            "resource_url": "TODO"
        }
```

### DELETE /critique/api/ratings/{ratingId}/

```json
POSSIBLE RESPONSES

204:
    HEADER
        Response: 204 (Rating deleted successfully.)
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
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "Rating not found."
            },
            "resource_url": "TODO"
        }

500:
    HEADER
        Response: 500
        Content-Type: application/json
    BODY
        {
            "@error": {
                "@message": "The system has failed. Please, contact the administrator."
            },
            "resource_url": "TODO"
        }
```
