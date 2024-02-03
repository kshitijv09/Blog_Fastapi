# Blog API Documentation

This document provides information about the BlogAPI built using FastAPI.

## Introduction

Welcome to our Blog CRUD Application!. This app allows users to create, read, delete and update blog posts. It also includes authentication and authorization to ensure secure access to system.

## Base URL

The base URL for the API is: `http://localhost:8000`
The API is currently under deployment

# Authentication


## Endpoints

The following endpoints are available for authentication in the Blog API:


#### `POST user/register`

Description: Register to use the Blog API

Example Request:{
    "email":"aman@kumar.com",
    "password":"amankumar",
    "username":"aman01",
    "interests":[{"name":"Sports"},{"name":"Technology"},{"name":"Photography"}]
}

#### `POST user/login`

Description: Login into the Blog API

Example Request:{
    "email":"aman@kumar.com",
    "password":"amankumar"
}

# User


## Endpoints

The following endpoints are available for users in the Blog API:


### Users

#### `PUT user/profile/{username}`

Description: Update User Profile

Example Request:{
    "username": "aman02"
}

#### `GET user/{user_id}`

Description: Fetch user details by user_id


Example Response : {
    "name":"Sunny",
    "title":"Technical Fest",
    "content":"Atrang"
}

#### `PUT user/interests/{username}`

Description: Update list of interets/tags for User
 
Example Request:{
  "interests": {
    "name": "Entertainment"
  }
}

#### `DELETE user/interests/{username}/{interest_id}`

Description: Deletes interest/tags for a user

Parameters:
- `username`: username
- `interest_id`: unique interest id

Example Response:"interest removed from user sucessfully"

# Blog


## Endpoints

The following endpoints are available for blogs in the Blog API:


### Blogs

#### `GET /blog`

Description: Get list of all available blogs

Example Response:[
  {
    "id": "65ba350733edb786324bc5bf",
    "title": "Trending Tech",
    "tag": "Blockchain",
    "content": "trending",
    "date": "today",
    "author": "myself"
  },
  {
    "id": "65bb1bde14b3458450c5a4da",
    "title": "Tech-latest",
    "tag": "Technology",
    "content": "Hot Stuff",
    "date": "Today",
    "author": "Ano"
  },
  {
    "id": "65bb7dd71f468d91d944b893",
    "title": "Wildlife photograph of the Year",
    "tag": "Photography",
    "content": "Mark Ronson wins photo of the Year Award",
    "date": "02/02/2024",
    "author": "Times Magazine"
  },
  {
    "id": "65bbabd1a8e26388a116c73d",
    "title": "Sample Blog",
    "tag": "Technology",
    "content": "This is a sample blog content.",
    "date": "2024-01-31",
    "author": "John Doe"
  },
  {
    "id": "65bbadf41914b36850405846",
    "title": "Sample Blog",
    "tag": "Technology",
    "content": "This is a sample blog content.",
    "date": "2024-01-31",
    "author": "John Doe"
  }
]

#### `POST /blog`

Description: Add a blog


Example Request : {
  "title": "Football",
  "tag": "Sports",
  "content": "Ballon'dor List",
  "date": "03/02/2024",
  "author": "Richard Feynman"
}

#### `GET blog/{blog_id}`

Description: Get individual blog by id
 
Example Response:{
  "id": "65bb7dd71f468d91d944b893",
  "title": "Wildlife photograph of the Year",
  "tag": "Photography",
  "content": "Mark Ronson wins photo of the Year Award",
  "date": "02/02/2024",
  "author": "Times Magazine"
}

#### `PUT blog/{blog_id}`

Description: Update an individual blog
 
Example Request:{
  "title": "string",
  "tag": "string",
  "content": "string",
  "date": "string",
  "author": "string"
}

#### `DELETE blog/{blog_id}`

Description: Delete a particular blog
 
Example Request:"blog deleted successfully"

#### `GET blog/{user_id}`

Description: Get list of blogs sorted by user's interests
 
Example Response:[
  {
    "id": "65ba350733edb786324bc5bf",
    "title": "Trending Tech",
    "tag": "Blockchain",
    "content": "trending",
    "date": "today",
    "author": "myself"
  },
  {
    "id": "65ba835db52be9858fe5cb8a",
    "title": "string",
    "tag": "Sports",
    "content": "string",
    "date": "string",
    "author": "string"
  },
  {
    "id": "65bb1bde14b3458450c5a4da",
    "title": "Tech-latest",
    "tag": "Technology",
    "content": "Hot Stuff",
    "date": "Today",
    "author": "Ano"
  },
  {
    "id": "65bb7dd71f468d91d944b893",
    "title": "Wildlife photograph of the Year",
    "tag": "Photography",
    "content": "Mark Ronson wins photo of the Year Award",
    "date": "02/02/2024",
    "author": "Times Magazine"
  },
  {
    "id": "65bbabd1a8e26388a116c73d",
    "title": "Sample Blog",
    "tag": "Technology",
    "content": "This is a sample blog content.",
    "date": "2024-01-31",
    "author": "John Doe"
  }
]

