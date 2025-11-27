from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.main_routes import router as main_router


def create_app() -> FastAPI:
    """Factory function para criar a aplicação FastAPI"""
    app = FastAPI(
        title="Personal Finance API",
        description="API para gerenciamento de finanças pessoais via WhatsApp",
        version="1.0.0"
    )

    # CORS
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check
    @app.get("/")
    def health_check():
        return {
            "status": "online",
            "service": "Personal Finance API",
            "version": "1.0.0"
        }

    @app.get("/health")
    def health():
        return {"status": "healthy"}

    # Registra rotas
    app.include_router(main_router)

    return app

# Create the application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
