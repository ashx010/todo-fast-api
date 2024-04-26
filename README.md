## To-do List API Documentation

### Introduction

This is a RESTful API for managing a to-do list application. It allows users to register, log in, create, read, update, and delete to-do items. The API is secured with JWT authentication.

### Authentication

#### Register User

- **Endpoint:** `/register`
- **Method:** `POST`
- **Description:** Registers a new user with a username and password.
- **Request Body:**
  - `username`: String (required) - The username of the user.
  - `password`: String (required) - The password of the user.
- **Response:** 
  - Status: 200 OK
  - Content: `{ "message": "User registered successfully" }`

#### Obtain Access Token

- **Endpoint:** `/token`
- **Method:** `POST`
- **Description:** Logs in a user and returns an access token.
- **Request Body:**
  - `username`: String (required) - The username of the user.
  - `password`: String (required) - The password of the user.
- **Response:**
  - Status: 200 OK
  - Content: `{ "access_token": "JWT_TOKEN", "token_type": "bearer" }`

### To-do Operations

#### Create To-do

- **Endpoint:** `/todos/`
- **Method:** `POST`
- **Description:** Creates a new to-do item.
- **Request Body:**
  - `title`: String (required) - The title of the to-do.
  - `description`: String (required) - The description of the to-do.
  - `done`: Boolean (optional) - The status of completion (default is `False`).
- **Response:**
  - Status: 200 OK
  - Content: `{ "message": "Todo created successfully", "todo_id": "TODO_ID" }`

#### Read To-dos

- **Endpoint:** `/todos/`
- **Method:** `GET`
- **Description:** Retrieves all to-do items.
- **Response:**
  - Status: 200 OK
  - Content: List of to-do items.

#### Read To-do by Title

- **Endpoint:** `/todos/{todo_title}`
- **Method:** `GET`
- **Description:** Retrieves a specific to-do item by its title.
- **Response:**
  - Status: 200 OK
  - Content: The to-do item.

#### Update To-do

- **Endpoint:** `/todos/{todo_title}`
- **Method:** `PUT`
- **Description:** Updates a specific to-do item.
- **Request Body:**
  - `title`: String (optional) - The new title of the to-do.
  - `description`: String (optional) - The new description of the to-do.
  - `done`: Boolean (optional) - The new status of completion.
- **Response:**
  - Status: 200 OK
  - Content: `{ "message": "Todo updated successfully" }`

#### Delete To-do

- **Endpoint:** `/todos/{todo_title}`
- **Method:** `DELETE`
- **Description:** Deletes a specific to-do item by its title.
- **Response:**
  - Status: 200 OK
  - Content: `{ "message": "Todo deleted successfully" }`

### Authentication Dependency

To access the above endpoints, the user must include an access token in the request header. The access token can be obtained by logging in via the `/token` endpoint.

### Token Verification

The access token must be included in the `Authorization` header of the request in the format `Bearer JWT_TOKEN`.
