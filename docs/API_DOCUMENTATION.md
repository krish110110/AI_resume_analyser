# API Documentation

Base URL: `/api/v1`

## Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT tokens
- `POST /auth/refresh` - Refresh access token
- `POST /auth/forgot-password` - Request password reset

## Users
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update current user profile

## Resumes
- `POST /resumes/upload` - Upload resume file
- `GET /resumes` - List current user's resumes
- `GET /resumes/{id}` - Get resume details
- `DELETE /resumes/{id}` - Delete resume

## Job Descriptions
- `POST /jobs` - Create job description
- `GET /jobs` - List job descriptions
- `GET /jobs/{id}` - Get job description

## Analysis
- `POST /analysis` - Run analysis
- `GET /analysis/{id}` - Get analysis result

## Reports
- `GET /reports` - List reports
- `GET /reports/{id}` - Get report details

## Dashboard
- `GET /dashboard/user` - User dashboard stats
- `GET /dashboard/admin` - Admin dashboard stats

## Admin
- `GET /admin/stats` - Admin system stats
- `GET /admin/users` - List all users
- `DELETE /admin/users/{id}` - Delete user
- `GET /admin/resumes` - List all resumes
- `DELETE /admin/resumes/{id}` - Delete resume
- `GET /admin/analytics` - Get analytics data

## Health
- `GET /health` - Health check
