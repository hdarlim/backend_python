import sqlite3
from werkzeug.security import generate_password_hash


class Cliente:
    """Representa e gerencia operações de clientes no banco de dados."""

    def __init__(self, db):
        self.db = db  # instância de Database

    def cadastrar(self, nome, email, senha, endereco=None, telefone=None):
        """
        Insere um novo cliente.
        Retorna o id gerado ou lança ValueError se o e-mail já existir.
        """
        senha_hash = generate_password_hash(senha)
        conn = self.db.conectar()
        try:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO Cliente (nome, endereco, telefone, email, senha)
                VALUES (?, ?, ?, ?, ?)
                ''',
                (nome, endereco, telefone, email, senha_hash)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError("Este e-mail já está cadastrado.")
        finally:
            conn.close()

    def listar(self):
        """Retorna todos os clientes (sem expor a senha)."""
        conn = self.db.conectar()
        try:
            cursor = conn.cursor()
            rows = cursor.execute(
                'SELECT id_cliente, nome, endereco, telefone, email FROM Cliente'
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()
