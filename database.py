import sqlite3

DATABASE = 'sistema_extensao.db'


class Database:
    """Gerencia a conexão e inicialização do banco de dados SQLite."""

    def __init__(self, caminho=DATABASE):
        self.caminho = caminho

    def conectar(self):
        """Abre e retorna uma conexão com o banco, com suporte a chaves estrangeiras."""
        conn = sqlite3.connect(self.caminho)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def inicializar(self):
        """Cria as tabelas caso ainda não existam."""
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Cliente (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nome       TEXT NOT NULL,
                endereco   TEXT,
                telefone   TEXT,
                email      TEXT UNIQUE NOT NULL,
                senha      TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Produto (
                id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo       TEXT NOT NULL,
                descricao  TEXT,
                nome       TEXT NOT NULL,
                valor_unitario REAL DEFAULT 0.0
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Pedido (
                id_pedido  INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER NOT NULL,
                data       TEXT NOT NULL,
                status     TEXT NOT NULL,
                total      REAL DEFAULT 0.0,
                FOREIGN KEY (id_cliente) REFERENCES Cliente (id_cliente)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Item_Pedido (
                id_pedido      INTEGER NOT NULL,
                id_produto     INTEGER NOT NULL,
                qtd_pedido     INTEGER NOT NULL,
                valor_unitario REAL NOT NULL,
                PRIMARY KEY (id_pedido, id_produto),
                FOREIGN KEY (id_pedido)  REFERENCES Pedido  (id_pedido)  ON DELETE CASCADE,
                FOREIGN KEY (id_produto) REFERENCES Produto (id_produto)
            )
        ''')

        conn.commit()
        # Garantir compatibilidade: adicionar coluna valor_unitario se não existir
        try:
            cursor.execute("ALTER TABLE Produto ADD COLUMN valor_unitario REAL DEFAULT 0.0")
            conn.commit()
        except sqlite3.OperationalError:
            # coluna já existe
            pass
        conn.close()
