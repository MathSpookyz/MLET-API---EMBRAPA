from .security import gerar_hash_senha

# Em produção, use banco real
usuarios_fake = {
    "admin": {
        "username": "admin",
        "senha_hash": gerar_hash_senha("admin123")
    }
}