from app import app, db
import os

if __name__ == '__main__':
    db.inicializar()   # Cria as tabelas na primeira execução
    app.run()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
