# API Responses

## GET /users/

### Responses

```json
200:
    HEADER
        Response: 200 (Successful.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO
```

## POST /users/

### Request

```json
    HEADER
        Content-Type: application/json
    BODY
        TODO
```

### Responses

```json
201:
    HEADER
        Response: 201 (User created successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO

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

## GET /users/{nickname}/

### Responses

```json
201:
    HEADER
        Response: 201 (Successful.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO

404:
    HEADER
        Response: 404
        Content-Type: application/json
    BODY
        {
            "error": "User not found."
        }
```

## PUT /users/{nickname}/

### Request

```json
    HEADER
        Content-Type: application/json
    BODY
        TODO
```

### Responses

```json
204:
    HEADER
        Response: 204 (User modified successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO

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

## DELETE /users/{nickname}/

### Responses

```json
204:
    HEADER
        Response: 204 (User deleted successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO

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

## GET /users/{nickname}/ratings/

### Responses

```json
200:
    HEADER
        Response: 200 (Successful.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO

404:
    HEADER
        Response: 404
        Content-Type: application/json
    BODY
        {
            "error": "User not found."
        }
```

## GET /users/{nickname}/river/

### Responses

```json
200:
    HEADER
        Response: 200 (Successful.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO

404:
    HEADER
        Response: 404
        Content-Type: application/json
    BODY
        {
            "error": "User not found."
        }
```

## GET /posts/

### Responses

```json
200:
    HEADER
        Response: 200 (Successful)
        Content-Type: application/vnd.mason+json
    BODY
        TODO
```

## POST /posts/

### Request

```json
    HEADER
        Content-Type: application/json
    BODY
        TODO
```

### Responses

```json
201:
    HEADER
        Response: 201 (Post created successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO

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

## GET /posts/{postId}/

### Responses

```json
201:
    HEADER
        Response: 201 (Successful.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO

404:
    HEADER
        Response: 404
        Content-Type: application/json
    BODY
        {
            "error": "Post not found."
        }
```

## POST /posts/

### Request

```json
    HEADER
        Content-Type: application/json
    BODY
        TODO
```

### Responses

```json
201:
    HEADER
        Response: 201 (Post created successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO

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

## PUT /posts/{postId}/

### Request

```json
    HEADER
        Content-Type: application/json
    BODY
        TODO
```

### Responses

```json
204:
    HEADER
        Response: 204 (Post modified successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO

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

## DELETE /posts/{postId}/

### Responses

```json
204:
    HEADER
        Response: 204 (Post deleted successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO

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

## POST /ratings/

### Request

```json
    HEADER
        Content-Type: application/json
    BODY
        TODO
```

### Responses

```json
201:
    HEADER
        Response: 201 (Rating created successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO

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

## GET /ratings/{ratingId}/

### Responses

```json
201:
    HEADER
        Response: 201 (Successful.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO

404:
    HEADER
        Response: 404
        Content-Type: application/json
    BODY
        {
            "error": "Rating not found."
        }
```

## PUT /ratings/{ratingId}/

### Request

```json
    HEADER
        Content-Type: application/json
    BODY
        TODO
```

### Responses

```json
204:
    HEADER
        Response: 204 (Rating modified successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO

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

## DELETE /ratings/{ratingId}/

### Responses

```json
204:
    HEADER
        Response: 204 (Rating deleted successfully.)
        Content-Type: application/vnd.mason+json
    BODY
        TODO

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
