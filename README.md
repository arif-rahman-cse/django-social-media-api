# Django Social Media API
This project contains the APIs required for the proposed social media app.
- Please note that, trailing slash("/") is mandatory for all routes.
- Please add your auth_token in authorization header for the APIs that require login. Example: ```{"Authorization": Token 025d83124c02af9c249b7dbc3a1051234555f107}```

## Account
#### Login
- Request method: POST
- URL: api/account/login/
- Login required: False
- Request:
    ```json
    {
        "username": "user123",
        "password": "password123"
    }
    ```
- Response:
    ```json
    {
        "id": 1,
        "username": "user123",
        "email": "user123@gmail.com",
        "first_name": "",
        "last_name": "",
        "auth_token": "025d83124c02af9c249b7dbc3a1051234555f107"
    }
    ```
    or
    ```json
    {
        "error": "Invalid username or password. Please try again with a valid username or password!"
    }
    ```
  
#### Logout
- Request method: POST
- URL: api/account/logout/
- Login required: True
- Request: None
- Response:
    ```json
    {
        "success": "You have been logged out"
    }
    ```
  
#### Register
- Request method: POST
- URL: api/account/register/
- Login required: False
- Request: 
    ```json
    {
        "username": "user5678",
        "email": "user5678@gmail.com",
        "password": "user5678",
        "first_name": "user",
        "last_name": "5678"
    }
    ```
- Response:
    ```json
    {
        "id": 4,
        "username": "user5678",
        "email": "user5678@gmail.com",
        "first_name": "user",
        "last_name": "5678",
        "auth_token": "9fc79c8f999140f98f5d99eb7d968e416d148b6d"
    }
    ```
    or
    ```json
    {
        "username": [
            "A user with that username already exists."
        ],
        "email": [
            "Enter a valid email address."
        ],
        "password": [
            "This password is too short. It must contain at least 8 characters.",
            "This password is too common."
        ]
    }
    ```
> Registering a user automatically logs him/her in. Use the given token for further operations.

#### Change Password
- Request method: POST
- URL: api/account/change-password/
- Login required: True
- Request: 
    ```json
    {
        "current_password": "current-pass",
        "new_password": "new-pass",
        "new_password_2": "new-pass"
    }
    ```
- Response:
    ```json
    {
        "success": "Password reset successful!"
    }
    ```
    or
    ```json
    {
        "current_password": [
            "This field may not be blank."
        ],
        "new_password": [
            "This field may not be blank."
        ],
        "new_password_2": [
            "This field may not be blank."
        ]
    }
    ```
    or 
    ```json
    {
        "error": "Please provide same password for both new password fields"
    }
    ```
