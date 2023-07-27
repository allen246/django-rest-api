# Text Snippet


## Description

A web application to save and retrieve short text snippets with tags using Django and Django REST framework.

## Features

- User authentication using JWT (JSON Web Tokens)
- Create, retrieve, update, and delete (CRUD) operations for snippets and tags
- Tag snippets and check for existing tags before creating new ones
- Batch delete for snippets
- Swagger API documentation for easy exploration

## How to use API Documentation

- Create a jwt access token by using user name and password
- Authorize that refresh token with 'Bearer' as prefix.
- Then you will be able to access all the endpoint without any Authorization issue
