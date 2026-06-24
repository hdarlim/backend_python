import sqlite3


class Pedido:
    """Representa e gerencia operações de pedidos no banco de dados."""

    def __init__(self, db):
        self.db = db

    def cadastrar(self, id_cliente, data, status, total=0.0):
        """
        Cria um novo pedido.
        Retorna o id gerado ou lança ValueError se o cliente não existir.
        """
        conn = self.db.conectar()
        try:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO Pedido (id_cliente, data, status, total)
                VALUES (?, ?, ?, ?)
                ''',
                (id_cliente, data, status, total)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError("Cliente informado não existe.")
        finally:
            conn.close()

    def listar_completos(self):
        """
        Retorna todos os pedidos com nome do cliente e itens detalhados.
        """
        conn = self.db.conectar()
        try:
            cursor = conn.cursor()
            pedidos = cursor.execute(
                '''
                SELECT p.id_pedido, p.data, p.status, p.total,
                       c.nome AS nome_cliente
                FROM Pedido p
                JOIN Cliente c ON p.id_cliente = c.id_cliente
                '''
            ).fetchall()

            resultado = []
            for pedido in pedidos:
                dict_pedido = dict(pedido)
                itens = cursor.execute(
                    '''
                    SELECT ip.qtd_pedido, ip.valor_unitario,
                           pr.nome AS nome_produto
                    FROM Item_Pedido ip
                    JOIN Produto pr ON ip.id_produto = pr.id_produto
                    WHERE ip.id_pedido = ?
                    ''',
                    (dict_pedido['id_pedido'],)
                ).fetchall()
                dict_pedido['itens'] = [dict(i) for i in itens]
                resultado.append(dict_pedido)

            return resultado
        finally:
            conn.close()


class ItemPedido:
    """Gerencia itens vinculados a um pedido."""

    def __init__(self, db):
        self.db = db

    def adicionar(self, id_pedido, id_produto, qtd_pedido, valor_unitario):
        """
        Insere um item no pedido e atualiza o total automaticamente.
        Lança ValueError em caso de integridade violada.
        """
        conn = self.db.conectar()
        try:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO Item_Pedido (id_pedido, id_produto, qtd_pedido, valor_unitario)
                VALUES (?, ?, ?, ?)
                ''',
                (id_pedido, id_produto, qtd_pedido, valor_unitario)
            )
            cursor.execute(
                '''
                UPDATE Pedido
                SET total = total + (? * ?)
                WHERE id_pedido = ?
                ''',
                (qtd_pedido, valor_unitario, id_pedido)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError(
                "Erro de integridade. Verifique se o Pedido e o Produto existem, "
                "ou se o item já foi adicionado."
            )
        finally:
            conn.close()
