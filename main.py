from app import app, db

if __name__ == '__main__':
    db.inicializar()   # Cria as tabelas na primeira execução
    app.run(debug=True)
