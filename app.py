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
# Frontend
# ---------------------------------------------------------------------------

@app.route('/', methods=['GET'])
def index():
    """Frontend para interagir com a API."""
    html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sistema de Pedidos</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            h1 {
                text-align: center;
                color: white;
                margin-bottom: 40px;
                font-size: 2.5em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 20px;
                margin-bottom: 20px;
            }
            .card {
                background: white;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .card h2 {
                color: #667eea;
                margin-bottom: 20px;
                border-bottom: 2px solid #667eea;
                padding-bottom: 10px;
            }
            .form-group {
                margin-bottom: 15px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                color: #333;
                font-weight: 500;
            }
            input, textarea {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 6px;
                font-family: Arial, sans-serif;
                font-size: 0.95em;
            }
            input:focus, textarea:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            button {
                width: 100%;
                padding: 12px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 1em;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            button:hover {
                background: #5568d3;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            button:active {
                transform: translateY(0);
            }
            .resultado {
                background: #f0f0f0;
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 15px;
                margin-top: 15px;
                font-family: 'Courier New', monospace;
                font-size: 0.85em;
                max-height: 300px;
                overflow-y: auto;
                white-space: pre-wrap;
                word-break: break-all;
            }
            .success {
                color: #28a745;
                background: #d4edda;
                border-color: #c3e6cb;
            }
            .error {
                color: #dc3545;
                background: #f8d7da;
                border-color: #f5c6cb;
            }
            .info {
                color: #004085;
                background: #d1ecf1;
                border-color: #bee5eb;
            }
            .full-width {
                grid-column: 1 / -1;
            }
            .loading {
                display: none;
                text-align: center;
                padding: 20px;
            }
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📦 Sistema de Pedidos</h1>
            
            <div class="grid">
                <!-- Card Clientes -->
                <div class="card">
                    <h2>👤 Novo Cliente</h2>
                    <div class="form-group">
                        <label>Nome</label>
                        <input type="text" id="nome_cliente" placeholder="João Silva">
                    </div>
                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" id="email_cliente" placeholder="joao@email.com">
                    </div>
                    <div class="form-group">
                        <label>Senha</label>
                        <input type="password" id="senha_cliente" placeholder="••••••">
                    </div>
                    <div class="form-group">
                        <label>Telefone</label>
                        <input type="text" id="telefone_cliente" placeholder="(11) 99999-9999">
                    </div>
                    <div class="form-group">
                        <label>Endereço</label>
                        <input type="text" id="endereco_cliente" placeholder="Rua..., Número...">
                    </div>
                    <button onclick="cadastrarCliente()">Cadastrar Cliente</button>
                    <div id="resultado_cliente" class="resultado"></div>
                </div>
                
                <!-- Card Produtos -->
                <div class="card">
                    <h2>🛍️ Novo Produto</h2>
                    <div class="form-group">
                        <label>Tipo</label>
                        <input type="text" id="tipo_produto" placeholder="Extensão">
                    </div>
                    <div class="form-group">
                        <label>Nome</label>
                        <input type="text" id="nome_produto" placeholder="Curso de Python">
                    </div>
                    <div class="form-group">
                        <label>Descrição</label>
                        <textarea id="descricao_produto" placeholder="Descrição do produto" rows="3"></textarea>
                    </div>
                    <button onclick="cadastrarProduto()">Cadastrar Produto</button>
                    <div id="resultado_produto" class="resultado"></div>
                </div>
                
                <!-- Card Pedidos -->
                <div class="card">
                    <h2>📋 Novo Pedido</h2>
                    <div class="form-group">
                        <label>ID Cliente</label>
                        <input type="number" id="id_cliente_pedido" placeholder="1">
                    </div>
                    <div class="form-group">
                        <label>Data</label>
                        <input type="date" id="data_pedido">
                    </div>
                    <div class="form-group">
                        <label>Status</label>
                        <input type="text" id="status_pedido" placeholder="pendente">
                    </div>
                    <div class="form-group">
                        <label>Total</label>
                        <input type="number" id="total_pedido" placeholder="0.00" step="0.01">
                    </div>
                    <button onclick="cadastrarPedido()">Criar Pedido</button>
                    <div id="resultado_pedido" class="resultado"></div>
                </div>
                
                <!-- Card Listar Pedidos -->
                <div class="card full-width">
                    <h2>📊 Pedidos Completos</h2>
                    <button onclick="listarPedidos()">Listar Todos os Pedidos</button>
                    <div id="resultado_listar" class="resultado"></div>
                </div>
            </div>
        </div>

        <script>
            // Configurar data de hoje como padrão
            document.getElementById('data_pedido').valueAsDate = new Date();

            function mostrarResultado(elementId, mensagem, tipo = 'info') {
                const elemento = document.getElementById(elementId);
                elemento.textContent = mensagem;
                elemento.className = 'resultado ' + tipo;
            }

            async function cadastrarCliente() {
                const nome = document.getElementById('nome_cliente').value;
                const email = document.getElementById('email_cliente').value;
                const senha = document.getElementById('senha_cliente').value;
                const telefone = document.getElementById('telefone_cliente').value;
                const endereco = document.getElementById('endereco_cliente').value;

                if (!nome || !email || !senha) {
                    mostrarResultado('resultado_cliente', 'Preencha os campos obrigatórios: Nome, Email e Senha', 'error');
                    return;
                }

                try {
                    const response = await fetch('/clientes', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ nome, email, senha, telefone, endereco })
                    });
                    const data = await response.json();
                    const tipo = response.ok ? 'success' : 'error';
                    mostrarResultado('resultado_cliente', JSON.stringify(data, null, 2), tipo);
                    if (response.ok) {
                        document.getElementById('nome_cliente').value = '';
                        document.getElementById('email_cliente').value = '';
                        document.getElementById('senha_cliente').value = '';
                        document.getElementById('telefone_cliente').value = '';
                        document.getElementById('endereco_cliente').value = '';
                    }
                } catch (error) {
                    mostrarResultado('resultado_cliente', 'Erro: ' + error.message, 'error');
                }
            }

            async function cadastrarProduto() {
                const tipo = document.getElementById('tipo_produto').value;
                const nome = document.getElementById('nome_produto').value;
                const descricao = document.getElementById('descricao_produto').value;

                if (!tipo || !nome) {
                    mostrarResultado('resultado_produto', 'Preencha os campos obrigatórios: Tipo e Nome', 'error');
                    return;
                }

                try {
                    const response = await fetch('/produtos', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ tipo, nome, descricao })
                    });
                    const data = await response.json();
                    const tipo_msg = response.ok ? 'success' : 'error';
                    mostrarResultado('resultado_produto', JSON.stringify(data, null, 2), tipo_msg);
                    if (response.ok) {
                        document.getElementById('tipo_produto').value = '';
                        document.getElementById('nome_produto').value = '';
                        document.getElementById('descricao_produto').value = '';
                    }
                } catch (error) {
                    mostrarResultado('resultado_produto', 'Erro: ' + error.message, 'error');
                }
            }

            async function cadastrarPedido() {
                const id_cliente = document.getElementById('id_cliente_pedido').value;
                const data = document.getElementById('data_pedido').value;
                const status = document.getElementById('status_pedido').value;
                const total = parseFloat(document.getElementById('total_pedido').value) || 0;

                if (!id_cliente || !data || !status) {
                    mostrarResultado('resultado_pedido', 'Preencha todos os campos obrigatórios', 'error');
                    return;
                }

                try {
                    const response = await fetch('/pedidos', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ id_cliente: parseInt(id_cliente), data, status, total })
                    });
                    const dado = await response.json();
                    const tipo_msg = response.ok ? 'success' : 'error';
                    mostrarResultado('resultado_pedido', JSON.stringify(dado, null, 2), tipo_msg);
                    if (response.ok) {
                        document.getElementById('id_cliente_pedido').value = '';
                        document.getElementById('status_pedido').value = '';
                        document.getElementById('total_pedido').value = '';
                    }
                } catch (error) {
                    mostrarResultado('resultado_pedido', 'Erro: ' + error.message, 'error');
                }
            }

            async function listarPedidos() {
                try {
                    const response = await fetch('/pedidos/completos');
                    const data = await response.json();
                    const tipo_msg = response.ok ? 'success' : 'error';
                    mostrarResultado('resultado_listar', JSON.stringify(data, null, 2), tipo_msg);
                } catch (error) {
                    mostrarResultado('resultado_listar', 'Erro: ' + error.message, 'error');
                }
            }
        </script>
    </body>
    </html>
    """
    return html


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
