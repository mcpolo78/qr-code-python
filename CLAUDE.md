# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a URL shortener web application with QR code generation built with Flask. The application creates short codes for long URLs, stores them in SQLite, and generates QR codes for easy sharing. Designed for local development and Heroku deployment.

## Development Commands

### Local Development
- **Start development server**: `python app.py`
- **Install dependencies**: `pip install -r requirements.txt`
- **Environment setup**: Copy `.env.example` to `.env` and configure values

### Heroku Deployment
- **Deploy to Heroku**: `git push heroku master`
- **View Heroku logs**: `heroku logs --tail`
- **Heroku app info**: `heroku info`

## Architecture

### Application Structure
- `app.py` - Main Flask application with URL shortening logic
- `templates/` - Jinja2 HTML templates for web interface
  - `base.html` - Base template with CSS styling
  - `index.html` - Home page with URL input form  
  - `result.html` - Results page showing shortened URL and QR code
- SQLite database (`urls.db`) for persistent URL storage
- Environment variables loaded via `python-dotenv`

### Core Functionality
The application uses a database-first approach where each function ensures table existence:
- `get_db_connection()` - Creates connection and ensures table schema exists
- `generate_short_code()` - Creates unique 6-character codes using `secrets.token_urlsafe()`
- `save_url()` / `get_original_url()` - Database operations for URL mapping

### API Endpoints
- `GET /` - Home page with URL shortening form
- `POST /shorten` - Create shortened URL (form data: `url`)
- `GET /<short_code>` - Redirect to original URL (302 redirect)
- `GET /qr/<short_code>` - Generate QR code image (PNG format)

### Database Schema
SQLite table `urls`:
- `id` - Primary key
- `short_code` - Unique 6-character identifier
- `original_url` - Original long URL
- `created_at` - Timestamp

### Environment Configuration
- `FLASK_DEBUG` - Controls debug mode (True/False)
- `PORT` - Server port (default: 5000)
- `SECRET_KEY` - Flask secret key for sessions

### Deployment
- Heroku deployment via `Procfile` using gunicorn
- Database auto-initialization on first request (Heroku-compatible)
- SQLite database excluded from git (ephemeral on Heroku)
- Production server: `gunicorn app:app`