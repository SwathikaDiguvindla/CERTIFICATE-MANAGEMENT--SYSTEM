# Certificate Verification Portal - API Contract

## Authentication

### POST /api/auth/login

Request

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Response

```json
{
  "success": true,
  "token": "jwt_token"
}
```

---

## Generate Certificate

### POST /api/generate

Request

```json
{
  "name": "John Doe",
  "email": "john@gmail.com",
  "phone": "9876543210",
  "domain": "Embedded Systems",
  "start_date": "2026-01-01",
  "end_date": "2026-03-01"
}
```

Response

```json
{
  "success": true,
  "certificate_id": "CERT001"
}
```

---

## Bulk Upload

### POST /api/bulk-upload

Upload Excel File

Columns:

- Name
- Email
- Phone
- Domain
- Start_Date
- End_Date

Response

```json
{
  "success": true,
  "processed": 100
}
```

---

## Verify Certificate

### GET /api/verify/:certificate_id

Response

```json
{
  "valid": true,
  "student_name": "John Doe",
  "domain": "Embedded Systems"
}
```

---

## Student Search

### POST /api/student/search

Request

```json
{
  "email": "john@gmail.com"
}
```

Response

```json
{
  "success": true,
  "certificate_id": "CERT001"
}
```

---

## Download Certificate

### GET /api/download/:certificate_id

Response

Returns PDF Certificate