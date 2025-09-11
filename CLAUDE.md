# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a QR code generator web application built with Flask. The application allows users to input text or URLs and generates downloadable QR codes. Features a simple web interface with French localization and is designed for local development and Heroku deployment.

## Development Commands

### Local Development
- **Start development server**: `python app.py`
- **Install dependencies**: `pip install -r requirements.txt`
- **Environment setup**: Create `.env` file with `FLASK_DEBUG=True` and `SECRET_KEY`

### Heroku Deployment
- **Deploy to Heroku**: `git push heroku master`
- **View Heroku logs**: `heroku logs --tail`
- **Heroku app info**: `heroku info`

## Architecture

### Application Structure
- `app.py` - Main Flask application with QR code generation logic
- `templates/` - Jinja2 HTML templates with French interface
  - `base.html` - Base template with CSS styling
  - `index.html` - Home page with text input form
  - `result.html` - Results page with QR code generation trigger
- Environment variables loaded via `python-dotenv`

### Core Functionality
- `generate_qr_code()` - POST `/generate` - Processes form input and renders result page
- `generate_qr()` - POST `/qr` - Creates QR code image using `qrcode` library and returns PNG
- QR codes generated with PIL/Pillow imaging and returned as BytesIO streams

### API Endpoints
- `GET /` - Home page with text input form
- `POST /generate` - Process text input and show result page (form data: `text`)
- `POST /qr` - Generate and download QR code PNG image (form data: `text`)

### Dependencies
- `Flask==2.3.3` - Web framework
- `qrcode[pil]==7.4.2` - QR code generation with PIL imaging
- `python-dotenv==1.1.1` - Environment variable management
- `gunicorn==21.2.0` - Production WSGI server

### Environment Configuration
- `FLASK_DEBUG` - Controls debug mode (default: True)
- `PORT` - Server port (default: 5000)
- `SECRET_KEY` - Flask secret key (default: 'dev-key-change-in-production')

### Deployment
- Heroku deployment via `Procfile` using `gunicorn app:app`
- No persistent storage - stateless QR code generation