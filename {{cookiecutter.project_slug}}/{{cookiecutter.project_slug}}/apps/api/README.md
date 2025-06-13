# API Documentation

## Overview

This project provides a RESTful API built with Django REST Framework. The API supports JSON format and uses session-based authentication.

## Base URL

```
/api/v1/
```

## Authentication

Most endpoints require authentication. The API uses session-based authentication, so you need to be logged in through the web interface.

For API-only clients, you can authenticate by:
1. POST to `/accounts/login/` with credentials
2. Include the session cookie in subsequent requests

## Endpoints

### User Management

#### Get User Profile
```
GET /api/v1/users/profile/
```

Response:
```json
{
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "太郎",
    "last_name": "山田",
    "full_name": "太郎 山田",
    "bio": "プロフィール説明",
    "avatar": null,
    "phone_number": "090-1234-5678",
    "email_notifications": true,
    "date_joined": "2024-01-01T00:00:00Z",
    "last_login": "2024-01-15T10:30:00Z"
}
```

#### Update User Profile
```
PATCH /api/v1/users/profile/
```

Request body:
```json
{
    "first_name": "太郎",
    "last_name": "山田",
    "bio": "更新されたプロフィール",
    "phone_number": "090-9876-5432",
    "email_notifications": false
}
```

#### Change Password
```
POST /api/v1/users/password/
```

Request body:
```json
{
    "old_password": "current_password",
    "new_password": "new_password123",
    "confirm_password": "new_password123"
}
```

### Contact Management

#### Create Contact
```
POST /api/v1/contacts/
```

Request body:
```json
{
    "name": "山田太郎",
    "email": "yamada@example.com",
    "subject": "お問い合わせ件名",
    "message": "お問い合わせ内容..."
}
```

#### List Contacts (Staff only)
```
GET /api/v1/contacts/
```

#### Resolve Contact (Staff only)
```
POST /api/v1/contacts/{id}/resolve/
```

### FAQ Management

#### List FAQs
```
GET /api/v1/faqs/
```

Response:
```json
{
    "count": 10,
    "results": [
        {
            "id": 1,
            "question": "よくある質問",
            "answer": "回答内容",
            "category": "general",
            "order": 1,
            "is_active": true,
            "view_count": 42
        }
    ]
}
```

#### Get FAQ Detail
```
GET /api/v1/faqs/{id}/
```

### Dashboard

#### Get Dashboard Statistics
```
GET /api/v1/dashboard/stats/
```

Response:
```json
{
    "total_users": 150,
    "new_users_today": 5,
    "active_users": 120,
    "total_contacts": 45,
    "pending_contacts": 12,
    "total_pages": 8
}
```

#### Get Chart Data
```
GET /api/v1/dashboard/charts/
```

Response:
```json
{
    "labels": ["01/10", "01/11", "01/12", "01/13", "01/14", "01/15", "01/16"],
    "datasets": [
        {
            "label": "新規ユーザー",
            "data": [3, 5, 2, 8, 4, 6, 5],
            "borderColor": "rgb(59, 130, 246)",
            "backgroundColor": "rgba(59, 130, 246, 0.5)"
        },
        {
            "label": "お問い合わせ",
            "data": [1, 2, 0, 3, 2, 4, 1],
            "borderColor": "rgb(16, 185, 129)",
            "backgroundColor": "rgba(16, 185, 129, 0.5)"
        }
    ]
}
```

### Activity Log

#### List User Activities
```
GET /api/v1/activities/
```

Response:
```json
{
    "count": 50,
    "results": [
        {
            "id": 1,
            "user": 1,
            "user_display": "山田太郎",
            "action": "login",
            "description": "ログインしました",
            "ip_address": "192.168.1.1",
            "created_at": "2024-01-15T10:30:00Z"
        }
    ]
}
```

## Error Responses

The API returns standard HTTP status codes:

- `200 OK` - Request succeeded
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

Error response format:
```json
{
    "detail": "Error message here",
    "field_errors": {
        "field_name": ["Error message for this field"]
    }
}
```

## JavaScript API Client

A JavaScript API client is provided at `/static/js/api.js`:

```javascript
// Example usage
const api = new APIClient();

// Get user profile
const profile = await api.get('/users/profile/');

// Update profile
const updated = await api.patch('/users/profile/', {
    first_name: '太郎',
    last_name: '山田'
});

// Submit contact form
const contact = await api.post('/contacts/', {
    name: '山田太郎',
    email: 'yamada@example.com',
    subject: 'お問い合わせ',
    message: 'メッセージ内容'
});
```

## Rate Limiting

Currently, there is no rate limiting implemented. For production use, consider adding rate limiting using packages like `django-ratelimit` or `djangorestframework-simplejwt`.

## CORS

CORS is not configured by default. If you need to access the API from a different domain, configure CORS settings in your Django settings file.