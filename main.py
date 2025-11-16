from flask import Flask
from flask_cors import CORS
from config.settings import Config
from core.utils import setup_logging
from clients.supabase_database_client import Database
import os
from routes.webpage_routes import webpage_bp
from routes.whatsapp_routes import whatsapp_bp
from routes.payment_routes import payment_bp


def create_app():
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__)
    allowed_origins = ["https://elitetrainingai.netlify.app",
                       "https://zp1v56uxy8rdx5ypatb0ockcb9tr6a-oci3--5173--cb7c0bca.local-credentialless.webcontainer-api.io"]
                       #"https://elitetraining-frontend.onrender.com"]
    CORS(app, supports_credentials=True, origins=allowed_origins)

    app.config.from_object(Config)

    # Setup de logging
    setup_logging()

    # Cria diretórios necessários
    os.makedirs('temp', exist_ok=True)
    os.makedirs('db', exist_ok=True)

    # Inicializa banco de dados
    Database()

    # Registra blueprints
    app.register_blueprint(whatsapp_bp, url_prefix='/whatsapp')
    app.register_blueprint(webpage_bp, url_prefix='/webpage')
    app.register_blueprint(payment_bp, url_prefix='/payment')

    # Rota de health check
    @app.route('/')
    def health_check():
        return {
            "status": "online",
            "service": "WhatsApp Backend API",
            "version": "1.0.0"
        }

    @app.route('/health')
    def health():
        return {"status": "healthy"}, 200

    return app


# Create the application instance
app = create_app()

if __name__ == '__main__':
    print("🚀 Iniciando WhatsApp Backend...")
    print(f"📱 Webhook URL: http://localhost:5000/api/webhook/zapi")
    print(f"🔧 Health Check: http://localhost:5000/health")

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
