# Flowise Login Fix - Email Format Required

## Issue
Flowise login form requires an **email address**, not just a username.

## Solution

### Correct Login Credentials:

**Email:** `admin@flowise.com` (or any valid email format)
**Password:** `lDWblThqRTLTf1EL`

### Alternative Email Formats:
- `admin@example.com`
- `admin@localhost`
- `admin@flowise.local`
- Any valid email format with `@` symbol

### Steps:
1. Go to http://localhost:3001
2. In the **Email** field, enter: `admin@flowise.com`
3. In the **Password** field, enter: `lDWblThqRTLTf1EL`
4. Click "Login"

## Why This Happens

Flowise's authentication system expects an email address format (with `@` symbol) even though the username is just "admin". This is a common pattern in modern web applications.

## Note

The actual username stored is "admin", but Flowise's login form validates that the input looks like an email address. You can use any email format as long as it contains `@` - the system will match it to the "admin" user account.

