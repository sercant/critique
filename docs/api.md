# Critique

## Profiles

### User Profile

Profile definition for all user resources. Related [profile call](#get-profilesuser_profile).

#### Dependencies

This profile inherits:

- Some semantic descriptors from [Person](http://schema.org/Person)
- Some link relations from IANA Web linking [RFC5988](https://www.iana.org/assignments/link-relations/link-relations.xhtml)

#### Link Relations

- [`create`](#create)
- [`delete`](#delete)

Inherited from IANA RFC5988:

- [`collection`](http://tools.ietf.org/html/rfc6573): Only accessible through `GET`.
- [`edit`](https://tools.ietf.org/html/rfc5023#section-11.1): This link allows editing the user via `PUT`.
- [`profile`](https://tools.ietf.org/html/rfc6906): The link contains the location of the resource profile.

#### Semantic Descriptors

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

## Profile Responses

### GET /profiles/user_profile

#### Possible Responses

```json
200:
    HEADER
        Response: 200
        Content-Type: text/html
```

## API Responses

### GET /critique/users/

#### Possible Responses

```json
200:
    HEADER
        Response: 200 (Successful.)
        Content-Type: application/vnd.mason+json
    BODY
        Profile: TODO
        Example:
            TODO
    LINKS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS
```

### POST /critique/users/

#### Request

```json
    HEADER
        Content-Type: application/json
    PARAMETERS
        TODO
    EXAMPLE
        TODO
```

#### Possible Responses

```json
201:
    HEADER
        Response: 201 (User created successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        Profile: TODO
        Example:
            TODO
    LINKS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

400:
    HEADER
        Response: 400
        Content-Type: application/json
    BODY
        {
            "error": "User info is not well formed or entity body is missing."
        }

415:
    HEADER
        Response: 415
        Content-Type: application/json
    BODY
        {
            "error": "Format of the input is not json."
        }

422:
    HEADER
        Response: 422
        Content-Type: application/json
    BODY
        {
            "error": "Nickname, email, or mobile already exist in the users list."
        }

500:
    HEADER
        Response: 500
        Content-Type: application/json
    BODY
        {
            "error": "The system has failed. Please, contact the administrator."
        }
```

### GET /critique/users/{nickname}/

#### Possible Responses

```json
201:
    HEADER
        Response: 201 (Successful.)
        Content-Type: application/vnd.mason+json
    BODY
        Profile: TODO
        Example:
            TODO
    LINKS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

404:
    HEADER
        Response: 404
        Content-Type: application/json
    BODY
        {
            "error": "User not found."
        }
```

### PUT /critique/users/{nickname}/

#### Request

```json
    HEADER
        Content-Type: application/json
    PARAMETERS
        TODO
    EXAMPLE
        TODO
```

#### Possible Responses

```json
204:
    HEADER
        Response: 204 (User modified successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        Profile: TODO
        Example:
            TODO
    LINKS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

400:
    HEADER
        Response: 400
        Content-Type: application/json
    BODY
        {
            "error": "User info is not well formed or it is empty."
        }

404:
    HEADER
        Response: 404
        Content-Type: application/json
    BODY
        {
            "error": "User not found."
        }

415:
    HEADER
        Response: 415
        Content-Type: application/json
    BODY
        {
            "error": "Format of the input is not json."
        }

422:
    HEADER
        Response: 422
        Content-Type: application/json
    BODY
        {
            "error": "Nickname, email, or mobile already exist in the users list."
        }

500:
    HEADER
        Response: 500
        Content-Type: application/json
    BODY
        {
            "error": "The system has failed. Please, contact the administrator."
        }
```

### DELETE /critique/users/{nickname}/

#### Possible Responses

```json
204:
    HEADER
        Response: 204 (User deleted successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        Profile: TODO
        Example:
            TODO
    LINKS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

404:
    HEADER
        Response: 404
        Content-Type: application/json
    BODY
        {
            "error": "User not found."
        }

500:
    HEADER
        Response: 500
        Content-Type: application/json
    BODY
        {
            "error": "The system has failed. Please, contact the administrator."
        }
```

### GET /critique/users/{nickname}/ratings/

#### Possible Responses

```json
200:
    HEADER
        Response: 200 (Successful.)
        Content-Type: application/vnd.mason+json
    BODY
        Profile: TODO
        Example:
            TODO
    LINKS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

404:
    HEADER
        Response: 404
        Content-Type: application/json
    BODY
        {
            "error": "User not found."
        }
```

### GET /critique/users/{nickname}/river/

#### Possible Responses

```json
200:
    HEADER
        Response: 200 (Successful.)
        Content-Type: application/vnd.mason+json
    BODY
        Profile: TODO
        Example:
            TODO
    LINKS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

404:
    HEADER
        Response: 404
        Content-Type: application/json
    BODY
        {
            "error": "User not found."
        }
```

### GET /critique/posts/

#### Possible Responses

```json
200:
    HEADER
        Response: 200 (Successful)
        Content-Type: application/vnd.mason+json
    BODY
        Profile: TODO
        Example:
            TODO
    LINKS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS
```

### POST /critique/posts/

#### Request

```json
    HEADER
        Content-Type: application/json
    PARAMETERS
        TODO
    EXAMPLE
        TODO
```

#### Possible Responses

```json
201:
    HEADER
        Response: 201 (Post created successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        Profile: TODO
        Example:
            TODO
    LINKS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

400:
    HEADER
        Response: 400
        Content-Type: application/json
    BODY
        {
            "error": "Post info is not well formed or entity body is missing."
        }

415:
    HEADER
        Response: 415
        Content-Type: application/json
    BODY
        {
            "error": "Format of the input is not json."
        }

422:
    HEADER
        Response: 422
        Content-Type: application/json
    BODY
        {
            "error": "Sender or receiver not found."
        }

500:
    HEADER
        Response: 500
        Content-Type: application/json
    BODY
        {
            "error": "The system has failed. Please, contact the administrator."
        }
```

### GET /critique/posts/{postId}/

#### Possible Responses

```json
201:
    HEADER
        Response: 201 (Successful.)
        Content-Type: application/vnd.mason+json
    BODY
        Profile: TODO
        Example:
            TODO
    LINKS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

404:
    HEADER
        Response: 404
        Content-Type: application/json
    BODY
        {
            "error": "Post not found."
        }
```

### POST /critique/posts/

#### Request

```json
    HEADER
        Content-Type: application/json
    PARAMETERS
        TODO
    EXAMPLE
        TODO
```

#### Possible Responses

```json
201:
    HEADER
        Response: 201 (Post created successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        Profile: TODO
        Example:
            TODO
    LINKS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

400:
    HEADER
        Response: 400
        Content-Type: application/json
    BODY
        {
            "error": "Post info is not well formed or entity body is missing."
        }

415:
    HEADER
        Response: 415
        Content-Type: application/json
    BODY
        {
            "error": "Format of the input is not json."
        }

404:
    HEADER
        Response: 404
        Content-Type: application/json
    BODY
        {
            "error": "Post not found."
        }

422:
    HEADER
        Response: 422
        Content-Type: application/json
    BODY
        {
            "error": "Sender not found."
        }

500:
    HEADER
        Response: 500
        Content-Type: application/json
    BODY
        {
            "error": "The system has failed. Please, contact the administrator."
        }
```

### PUT /critique/posts/{postId}/

#### Request

```json
    HEADER
        Content-Type: application/json
    PARAMETERS
        TODO
    EXAMPLE
        TODO
```

#### Possible Responses

```json
204:
    HEADER
        Response: 204 (Post modified successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        Profile: TODO
        Example:
            TODO
    LINKS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

400:
    HEADER
        Response: 400
        Content-Type: application/json
    BODY
        {
            "error": "Post info is not well formed or it is empty."
        }

404:
    HEADER
        Response: 404
        Content-Type: application/json
    BODY
        {
            "error": "Post not found."
        }

415:
    HEADER
        Response: 415
        Content-Type: application/json
    BODY
        {
            "error": "Format of the input is not json."
        }

500:
    HEADER
        Response: 500
        Content-Type: application/json
    BODY
        {
            "error": "The system has failed. Please, contact the administrator."
        }
```

### DELETE /critique/posts/{postId}/

#### Possible Responses

```json
204:
    HEADER
        Response: 204 (Post deleted successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        Profile: TODO
        Example:
            TODO
    LINKS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

404:
    HEADER
        Response: 404
        Content-Type: application/json
    BODY
        {
            "error": "Post not found."
        }

500:
    HEADER
        Response: 500
        Content-Type: application/json
    BODY
        {
            "error": "The system has failed. Please, contact the administrator."
        }
```

### POST /critique/ratings/

#### Request

```json
    HEADER
        Content-Type: application/json
    PARAMETERS
        TODO
    EXAMPLE
        TODO
```

#### Possible Responses

```json
201:
    HEADER
        Response: 201 (Rating created successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        Profile: TODO
        Example:
            TODO
    LINKS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

400:
    HEADER
        Response: 400
        Content-Type: application/json
    BODY
        {
            "error": "Rating info is not well formed or entity body is missing."
        }

415:
    HEADER
        Response: 415
        Content-Type: application/json
    BODY
        {
            "error": "Format of the input is not json."
        }

422:
    HEADER
        Response: 422
        Content-Type: application/json
    BODY
        {
            "error": "Sender or receiver not found."
        }

500:
    HEADER
        Response: 500
        Content-Type: application/json
    BODY
        {
            "error": "The system has failed. Please, contact the administrator."
        }
```

### GET /critique/ratings/{ratingId}/

#### Possible Responses

```json
201:
    HEADER
        Response: 201 (Successful.)
        Content-Type: application/vnd.mason+json
    BODY
        Profile: TODO
        Example:
            TODO
    LINKS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

404:
    HEADER
        Response: 404
        Content-Type: application/json
    BODY
        {
            "error": "Rating not found."
        }
```

### PUT /critique/ratings/{ratingId}/

#### Request

```json
    HEADER
        Content-Type: application/json
    PARAMETERS
        TODO
    EXAMPLE
        TODO
```

#### Possible Responses

```json
204:
    HEADER
        Response: 204 (Rating modified successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        Profile: TODO
        Example:
            TODO
    LINKS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

400:
    HEADER
        Response: 400
        Content-Type: application/json
    BODY
        {
            "error": "Rating info is not well formed or it is empty."
        }

404:
    HEADER
        Response: 404
        Content-Type: application/json
    BODY
        {
            "error": "Rating not found."
        }

415:
    HEADER
        Response: 415
        Content-Type: application/json
    BODY
        {
            "error": "Format of the input is not json."
        }

500:
    HEADER
        Response: 500
        Content-Type: application/json
    BODY
        {
            "error": "The system has failed. Please, contact the administrator."
        }
```

### DELETE /critique/ratings/{ratingId}/

#### Possible Responses

```json
204:
    HEADER
        Response: 204 (Rating deleted successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        Profile: TODO
        Example:
            TODO
    LINKS
        Self: TODO
        Profile: TODO
        TODO OTHER LINKS

404:
    HEADER
        Response: 404
        Content-Type: application/json
    BODY
        {
            "error": "Rating not found."
        }

500:
    HEADER
        Response: 500
        Content-Type: application/json
    BODY
        {
            "error": "The system has failed. Please, contact the administrator."
        }
```
