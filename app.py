from flask import Flask, render_template, request, send_file
import os
import qrcode
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr_code():
    text = request.form.get('text')
    
    if not text:
        return render_template('index.html', error='Text is required')
    
    return render_template('result.html', text=text)

@app.route('/qr', methods=['POST'])
def generate_qr():
    text = request.form.get('text')
    
    if not text:
        return "Text is required", 400
    
    # Créer le QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(text)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convertir l'image en bytes pour l'envoyer
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    return send_file(img_buffer, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)