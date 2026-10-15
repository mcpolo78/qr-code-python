# QR Code Generator

A simple Flask web application that generates QR codes from text input.

## Features

- Generate QR codes from any text input
- Web interface for easy use
- Download QR codes as PNG images
- Responsive design

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd qr-code-python
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file (optional):
```
SECRET_KEY=your-secret-key-here
PORT=5000
FLASK_DEBUG=True
```

## Usage

1. Run the application:
```bash
python app.py
```

2. Open your browser and go to `http://localhost:5000`

3. Enter text in the input field and click "Generate QR Code"

4. View the generated QR code or download it as a PNG file

## API Endpoints

- `GET /` - Home page with QR code generator form
- `POST /generate` - Generate QR code and display result page
- `POST /qr` - Generate QR code and return PNG image

## Dependencies

- Flask 2.3.3
- qrcode[pil] 7.4.2
- python-dotenv 1.1.1
- gunicorn 21.2.0 (for production deployment)

## Deployment

This application is configured for deployment on platforms like Heroku with the included `Procfile`.

## License

This project is open source and available under the MIT License.

## Version statique (Vercel)

Le dossier `public/` contient une version 100 % navigateur du générateur (JavaScript, bibliothèque [qrcode-generator](https://github.com/kazuhikoarase/qrcode-generator), licence MIT) : aucun serveur, aucune donnée envoyée. Elle se déploie telle quelle sur Vercel grâce à `vercel.json`. La version Flask d'origine reste disponible sur la branche `main`.
