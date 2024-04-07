# Referral System API

## Objective
The objective of this task is to build a referral system API that allows users to register, view their details, and view their referrals.

## Requirements

1. **User Registration Endpoint**:
    - **Method**: POST
    - **URL**: /api/register/
    - **Required Fields**: name, email, password
    - **Optional Field**: referral\_code (if provided, the user who referred this user should receive a point)
    - **Response**: Unique user ID and a success message

2. **User Details Endpoint**:
    - **Method**: GET
    - **URL**: /api/details/
    - **Headers**: Authorization with a valid token
    - **Response**: User's details (name, email, referral\_code, timestamp of registration)

3. **Referrals Endpoint**:
    - **Method**: GET
    - **URL**: /api/referrals/
    - **Headers**: Authorization with a valid token
    - **Response**: 
        - List of users who registered using the current user's referral\_code (if any)
        - Paginated response (e.g., 20 users per page)
        - Timestamp of registration for each referral

## Authentication
JWT (JSON Web Token) authentication is used for accessing protected endpoints. Clients need to include a valid JWT token in the Authorization header to authenticate requests.


