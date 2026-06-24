from flask import Flask, request, jsonify
from flask_cors import CORS

from database import Database
from models.cliente import Cliente
from models.produto import Produto
from models.pedido import Pedido, ItemPedido

app = Flask(__name__)
CORS(app)

# Instâncias compartilhadas
db          = Database()
clientes    = Cliente(db)
produtos    = Produto(db)
pedidos     = Pedido(db)
itens       = ItemPedido(db)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def validar_json(dados, campos_obrigatorios):
    """Retorna uma resposta de erro se algum campo obrigatório estiver ausente."""
    if not isinstance(dados, dict):
        return jsonify({"erro": "Requisição JSON inválida."}), 400
    ausentes = [c for c in campos_obrigatorios if dados.get(c) is None]
    if ausentes:
        return jsonify({"erro": f"Campos obrigatórios ausentes: {', '.join(ausentes)}."}), 400
    return None


# ---------------------------------------------------------------------------
# Rotas - Clientes
# ---------------------------------------------------------------------------

@app.route('/clientes', methods=['POST'])
def cadastrar_cliente():
    dados = request.get_json(silent=True) or {}
    erro = validar_json(dados, ['nome', 'email', 'senha'])
    if erro:
        return erro
    try:
        id_gerado = clientes.cadastrar(
            nome=dados['nome'],
            email=dados['email'],
            senha=dados['senha'],
            endereco=dados.get('endereco'),
            telefone=dados.get('telefone'),
        )
        return jsonify({"mensagem": "Cliente cadastrado com sucesso!", "id_cliente": id_gerado}), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


# ---------------------------------------------------------------------------
# Rotas - Produtos
# ---------------------------------------------------------------------------

@app.route('/produtos', methods=['POST'])
def cadastrar_produto():
    dados = request.get_json(silent=True) or {}
    erro = validar_json(dados, ['tipo', 'nome'])
    if erro:
        return erro
    id_gerado = produtos.cadastrar(
        tipo=dados['tipo'],
        nome=dados['nome'],
        descricao=dados.get('descricao'),
    )
    return jsonify({"mensagem": "Produto cadastrado com sucesso!", "id_produto": id_gerado}), 201


# ---------------------------------------------------------------------------
# Rotas - Pedidos
# ---------------------------------------------------------------------------

@app.route('/pedidos', methods=['POST'])
def cadastrar_pedido():
    dados = request.get_json(silent=True) or {}
    erro = validar_json(dados, ['id_cliente', 'data', 'status'])
    if erro:
        return erro
    try:
        id_gerado = pedidos.cadastrar(
            id_cliente=dados['id_cliente'],
            data=dados['data'],
            status=dados['status'],
            total=dados.get('total', 0.0),
        )
        return jsonify({"mensagem": "Pedido iniciado com sucesso!", "id_pedido": id_gerado}), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@app.route('/pedidos/completos', methods=['GET'])
def listar_pedidos_completos():
    return jsonify(pedidos.listar_completos()), 200


# ---------------------------------------------------------------------------
# Rotas - Itens de Pedido
# ---------------------------------------------------------------------------

@app.route('/itens-pedido', methods=['POST'])
def adicionar_item_pedido():
    dados = request.get_json(silent=True) or {}
    erro = validar_json(dados, ['id_pedido', 'id_produto', 'qtd_pedido', 'valor_unitario'])
    if erro:
        return erro
    try:
        itens.adicionar(
            id_pedido=dados['id_pedido'],
            id_produto=dados['id_produto'],
            qtd_pedido=dados['qtd_pedido'],
            valor_unitario=dados['valor_unitario'],
        )
        return jsonify({"mensagem": "Item adicionado ao pedido com sucesso!"}), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
