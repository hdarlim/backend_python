class Produto:
    """Representa e gerencia operações de produtos no banco de dados."""

    def __init__(self, db):
        self.db = db

    def cadastrar(self, tipo, nome, descricao=None, valor_unitario=0.0):
        """Insere um novo produto e retorna o id gerado."""
        conn = self.db.conectar()
        try:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO Produto (tipo, descricao, nome, valor_unitario)
                VALUES (?, ?, ?, ?)
                ''',
                (tipo, descricao, nome, valor_unitario)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def listar(self):
        """Retorna todos os produtos."""
        conn = self.db.conectar()
        try:
            rows = conn.cursor().execute('SELECT id_produto, tipo, descricao, nome, valor_unitario FROM Produto').fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()
