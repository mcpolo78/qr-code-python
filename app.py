from flask import Flask, render_template, request, redirect, url_for, send_file, abort
import os
import hashlib
import secrets
import sqlite3
import qrcode
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

# Base de données SQLite pour stocker les URLs

def init_db():
    """Initialise la base de données SQLite"""
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    """Obtient une connexion à la base de données et s'assure que la table existe"""
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

def generate_short_code():
    """Génère un code court unique"""
    while True:
        code = secrets.token_urlsafe(6)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM urls WHERE short_code = ?', (code,))
        if not cursor.fetchone():
            conn.close()
            return code
        conn.close()

def save_url(short_code, original_url):
    """Sauvegarde l'URL dans la base de données"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO urls (short_code, original_url) VALUES (?, ?)', 
                   (short_code, original_url))
    conn.commit()
    conn.close()

def get_original_url(short_code):
    """Récupère l'URL originale depuis la base de données"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT original_url FROM urls WHERE short_code = ?', (short_code,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form.get('url')
    
    if not original_url:
        return render_template('index.html', error='URL is required')
    
    if not original_url.startswith(('http://', 'https://')):
        original_url = 'https://' + original_url
    
    short_code = generate_short_code()
    
    # Sauvegarder dans la base de données
    save_url(short_code, original_url)
    
    short_url = request.url_root + short_code
    
    return render_template('result.html', 
                         short_url=short_url, 
                         short_code=short_code,
                         original_url=original_url)

@app.route('/<short_code>')
def redirect_to_url(short_code):
    original_url = get_original_url(short_code)
    if original_url:
        return redirect(original_url)
    else:
        abort(404)

@app.route('/qr/<short_code>')
def generate_qr(short_code):
    original_url = get_original_url(short_code)
    if not original_url:
        abort(404)
    
    short_url = request.url_root + short_code
    
    # Créer le QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(short_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convertir l'image en bytes pour l'envoyer
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    return send_file(img_buffer, mimetype='image/png')

if __name__ == '__main__':
    init_db()
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)