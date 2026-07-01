# URL Shortener

A simple URL shortener API built with Django and Django REST Framework.

## Features

* Create a short URL for a given URL.
* Resolve a short code back to the original URL.
* Idempotent creation – creating a short link for the same URL returns the existing one.
* Secure 8-character short code generation using Python's `secrets` module.
* Automatic collision handling with retry logic.
* Unit and API tests.

---

## Tech Stack

* Python
* Django
* Django REST Framework
* SQLite

---

## API

### Create a short URL

**POST** `/api/short-links/`

Request:

```json
{
  "original_url": "https://example.com"
}
```

Response (`201 Created`):

```json
{
  "short_url": "http://localhost:8000/shrt/V8LpKUIr/"
}
```

---

### Resolve a short URL

**GET** `/shrt/<code>/`

Example:

```http
GET /shrt/V8LpKUIr/
```

Response (`200 OK`):

```json
{
  "original_url": "https://example.com"
}
```

If the short code does not exist:

```http
404 Not Found
```

---

## Running the project

Clone the repository:

```bash
git clone git@github.com:tomekf1988/homework.git
cd homework
```

Create and activate a virtual environment.

Linux / macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install the project:

```bash
pip install -e .
```

Apply database migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

The API will be available at:

```text
http://localhost:8000/
```

---

## Running tests

```bash
python manage.py test
```


---

## Running tests

```bash
python manage.py test
```

---

## Design

* Business logic is encapsulated in the service layer.
* The database guarantees uniqueness of both the original URL and generated short codes.
* Short codes are generated using Python's `secrets` module to provide cryptographically secure randomness.
* Rare short code collisions are handled by retrying after an `IntegrityError`.
* The implementation intentionally focuses on the requested functionality while keeping the codebase simple and easy to extend.

---

## Possible Improvements

* Redirect endpoint returning HTTP 302/307.
* Custom aliases for short URLs.
* Expiration date for generated links.
* Click statistics.
* Rate limiting.
* Redis caching for frequently resolved URLs.
