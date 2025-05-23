# Authentication API Documentation

This document describes the authentication endpoints for the Taskforce API.

## Base URL

All authentication endpoints are prefixed with `/api/auth/`

## Authentication Overview

The API uses JSON Web Tokens (JWT) for authentication. Tokens are returned in two forms:

- **Access Token**: Short-lived (60 minutes) - used for API authentication
- **Refresh Token**: Long-lived (7 days) - used to get new access tokens

## Endpoints

### 1. User Registration

**POST** `/api/auth/register/`

Register a new user account.

#### Request Body

```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### Response (201 Created)

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "username": "user",
    "first_name": "John",
    "last_name": "Doe",
    "avatar": null,
    "phone": null,
    "date_joined": "2024-01-15T10:30:00Z",
    "last_login": null
  }
}
```

### 2. User Login

**POST** `/api/auth/login/`

Authenticate a user and receive tokens.

#### Request Body

```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

#### Response (200 OK)

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "username": "user",
    "first_name": "John",
    "last_name": "Doe",
    "avatar": null,
    "phone": null,
    "date_joined": "2024-01-15T10:30:00Z",
    "last_login": "2024-01-15T11:00:00Z"
  }
}
```

### 3. User Logout

**POST** `/api/auth/logout/`

Logout and blacklist the refresh token.

**Authentication Required**: Yes

#### Request Body (Optional)

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Response (200 OK)

```json
{
  "message": "Successfully logged out"
}
```

### 4. Get User Profile

**GET** `/api/auth/profile/`

Get current user's profile information.

**Authentication Required**: Yes

#### Response (200 OK)

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "username": "user",
  "first_name": "John",
  "last_name": "Doe",
  "avatar": null,
  "phone": "+1234567890",
  "date_joined": "2024-01-15T10:30:00Z",
  "last_login": "2024-01-15T11:00:00Z"
}
```

### 5. Update User Profile

**PATCH** `/api/auth/profile/`

Update current user's profile information.

**Authentication Required**: Yes

#### Request Body (all fields optional)

```json
{
  "first_name": "John",
  "last_name": "Smith",
  "phone": "+1234567890",
  "avatar": "https://example.com/avatar.jpg"
}
```

#### Response (200 OK)

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "username": "user",
  "first_name": "John",
  "last_name": "Smith",
  "avatar": "https://example.com/avatar.jpg",
  "phone": "+1234567890",
  "date_joined": "2024-01-15T10:30:00Z",
  "last_login": "2024-01-15T11:00:00Z"
}
```

### 6. Change Password

**POST** `/api/auth/change-password/`

Change the current user's password.

**Authentication Required**: Yes

#### Request Body

```json
{
  "old_password": "currentpassword",
  "new_password": "newsecurepassword123"
}
```

#### Response (200 OK)

```json
{
  "message": "Password updated successfully"
}
```

### 7. Refresh Token

**POST** `/api/auth/token/refresh/`

Get a new access token using the refresh token.

#### Request Body

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Response (200 OK)

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Authentication Methods

### 1. Authorization Header

Include the access token in the Authorization header:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### 2. Cookies (if configured)

Tokens can also be stored in HTTP-only cookies for browser-based applications.

## Error Responses

### 400 Bad Request

```json
{
  "email": ["This field is required."],
  "password": ["This field is required."]
}
```

### 401 Unauthorized

```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

### 403 Forbidden

```json
{
  "detail": "You do not have permission to perform this action."
}
```

## Usage Examples

### Frontend JavaScript Example

```javascript
// Register
const registerResponse = await fetch("/api/auth/register/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    email: "user@example.com",
    password: "securepassword123",
    first_name: "John",
    last_name: "Doe",
  }),
});

const { access, refresh, user } = await registerResponse.json();

// Store tokens
localStorage.setItem("access_token", access);
localStorage.setItem("refresh_token", refresh);

// Make authenticated requests
const profileResponse = await fetch("/api/auth/profile/", {
  headers: {
    Authorization: `Bearer ${localStorage.getItem("access_token")}`,
  },
});
```

### Python Requests Example

```python
import requests

# Login
login_data = {
    'email': 'user@example.com',
    'password': 'securepassword123'
}

response = requests.post('http://localhost:8000/api/auth/login/', json=login_data)
tokens = response.json()

# Use access token for authenticated requests
headers = {
    'Authorization': f'Bearer {tokens["access"]}'
}

profile_response = requests.get('http://localhost:8000/api/auth/profile/', headers=headers)
user_profile = profile_response.json()
```

### cURL Examples

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'

# Get profile (replace TOKEN with actual access token)
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer TOKEN"
```

## Security Considerations

1. **Access tokens** should be stored securely (e.g., in memory for SPAs)
2. **Refresh tokens** should be stored in HTTP-only cookies when possible
3. Always use HTTPS in production
4. Implement proper token refresh logic in your frontend
5. Consider implementing rate limiting for authentication endpoints
6. Use strong passwords and implement password complexity requirements
