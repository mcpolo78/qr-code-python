# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple Flask backend API designed for local development and Heroku deployment. The application uses environment variable management and follows a basic REST API structure.

## Development Commands

### Local Development
- **Start development server**: `python app.py`
- **Install dependencies**: `pip install -r requirements.txt`
- **Environment setup**: Copy `.env.example` to `.env` and configure values

### Heroku Deployment
- **Deploy to Heroku**: `git push heroku master`
- **Create Heroku app**: `heroku create [app-name]`

## Architecture

### Application Structure
- `app.py` - Main Flask application with REST API endpoints
- Environment variables loaded via `python-dotenv` from `.env` file
- Configuration managed through `os.getenv()` with fallback defaults

### API Endpoints
- `GET /` - Health check/welcome message
- `GET /api/health` - Service health status
- `GET /api/users` - Retrieve user list (sample data)
- `POST /api/users` - Create new user (expects JSON with name/email)

### Environment Configuration
- `FLASK_DEBUG` - Controls debug mode (True/False)
- `PORT` - Server port (default: 5000)
- `SECRET_KEY` - Flask secret key for sessions
- `DATABASE_URL` - Database connection (prepared for future use)

### Deployment
- Heroku deployment configured via `Procfile` using gunicorn
- Production server runs: `gunicorn app:app`
- Environment variables automatically loaded in both local and production environments