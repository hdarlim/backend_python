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
    html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Sistema Papa da Wal</title>
      <style>
        body { font-family: Arial, Helvetica, sans-serif; background: #e6f4ea; margin:0; padding:20px; }
        .wrap { max-width:900px; margin:0 auto; }
        header { background:#8bc34a; color:#fff; padding:18px 20px; border-radius:8px; text-align:center; }
        header h1 { margin:0; font-size:1.6rem; }
        section { background:#fff; padding:14px; border-radius:8px; margin-top:12px; }
        label { display:block; margin-top:8px; font-weight:600; }
        input[type=text], input[type=email], input[type=number], input[type=date], textarea, select { width:100%; padding:8px; margin-top:6px; border:1px solid #ddd; border-radius:6px; }
        button { margin-top:10px; padding:10px; background:#4caf50; color:#fff; border:none; border-radius:6px; cursor:pointer; }
        .row { display:flex; gap:12px; }
        .col { flex:1; }
        .small { font-size:0.9rem; color:#555; }
        .list { margin-top:8px; }
        .item { border:1px solid #eee; padding:10px; border-radius:6px; margin-bottom:8px; }
        .muted { color:#777; font-size:0.9rem }
      </style>
    </head>
    <body>
      <div class="wrap">
        <header>
          <h1>🥗 Sistema Papa da Wal</h1>
          <div class="small">Cadastro e gerenciamento básico de pedidos para empresa de alimentos</div>
        </header>

        <section>
          <h2>Novo Cliente</h2>
          <label>Nome</label>
          <input id="nome_cliente" type="text" placeholder="João Silva" />
          <label>Email</label>
          <input id="email_cliente" type="email" placeholder="joao@email.com" />
          <label>Senha</label>
          <input id="senha_cliente" type="text" placeholder="senha" />
          <label>Telefone</label>
          <input id="telefone_cliente" type="text" placeholder="(11) 99999-9999" />
          <label>Endereço</label>
          <input id="endereco_cliente" type="text" placeholder="Rua..." />
          <button onclick="cadastrarCliente()">Cadastrar Cliente</button>
          <div id="msg_cliente" class="muted"></div>
        </section>

        <section>
          <h2>Novo Produto</h2>
          <label>Tipo</label>
          <input id="tipo_produto" type="text" placeholder="Fixo" />
          <label>Nome</label>
          <input id="nome_produto" type="text" placeholder="Salada de frutas" />
          <label>Preço unitário (R$)</label>
          <input id="preco_produto" type="number" step="0.01" value="0.00" />
          <label>Descrição</label>
          <textarea id="descricao_produto" rows="2"></textarea>
          <button onclick="cadastrarProduto()">Cadastrar Produto</button>
          <div id="msg_produto" class="muted"></div>
        </section>

        <section>
          <h2>Novo Pedido</h2>
          <label>Cliente</label>
          <select id="select_cliente_pedido"></select>
          <label>Data</label>
          <input id="data_pedido" type="date" />
          <label>Status</label>
          <select id="status_pedido"><option>pendente</option><option>em produção</option><option>concluído</option><option>cancelado</option></select>
          <button onclick="cadastrarPedido()">Abrir Pedido</button>
          <div id="msg_pedido" class="muted"></div>
        </section>

        <section>
          <h2>Adicionar Item ao Pedido</h2>
          <label>Pedido (ID)</label>
          <select id="select_pedido"></select>
          <label>Produto</label>
          <select id="select_produto"></select>
          <div class="row">
            <div class="col">
              <label>Quantidade</label>
              <input id="qtd_item" type="number" value="1" min="1" />
            </div>
          </div>
          <button onclick="adicionarItem()">Adicionar</button>
          <div id="msg_item" class="muted"></div>
        </section>

        <section>
          <h2>Lista de Pedidos</h2>
          <button onclick="listarPedidos()">Atualizar lista</button>
          <div id="lista_pedidos" class="list"></div>
        </section>

      </div>

      <script>
        // Inicialização
        document.getElementById('data_pedido').valueAsDate = new Date();
        window.addEventListener('load', () => { fetchClientes(); fetchProdutos(); fetchPedidosIds(); listarPedidos(); });

        function showMsg(id, text) { document.getElementById(id).textContent = text; }

        async function cadastrarCliente() {
          const nome = document.getElementById('nome_cliente').value;
          const email = document.getElementById('email_cliente').value;
          const senha = document.getElementById('senha_cliente').value;
          const telefone = document.getElementById('telefone_cliente').value;
          const endereco = document.getElementById('endereco_cliente').value;
          if (!nome || !email || !senha) { showMsg('msg_cliente','Preencha nome, email e senha'); return; }
          try {
            const r = await fetch('/clientes', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({nome,email,senha,telefone,endereco}) });
            const j = await r.json();
            showMsg('msg_cliente', r.ok ? 'Cliente cadastrado (id: '+j.id_cliente+')' : ('Erro: '+(j.erro||JSON.stringify(j))));
            if (r.ok) { document.getElementById('nome_cliente').value=''; document.getElementById('email_cliente').value=''; document.getElementById('senha_cliente').value=''; fetchClientes(); }
          } catch(e){ showMsg('msg_cliente','Erro: '+e.message); }
        }

        async function cadastrarProduto() {
          const tipo = document.getElementById('tipo_produto').value || 'Fixo';
          const nome = document.getElementById('nome_produto').value || 'Salada de frutas';
          const descricao = document.getElementById('descricao_produto').value;
          const valor_unitario = parseFloat(document.getElementById('preco_produto').value) || 0.0;
          if (!tipo || !nome) { showMsg('msg_produto','Preencha tipo e nome'); return; }
          try {
            const r = await fetch('/produtos', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({tipo,nome,descricao,valor_unitario}) });
            const j = await r.json();
            showMsg('msg_produto', r.ok ? 'Produto cadastrado (id: '+j.id_produto+')' : ('Erro: '+(j.erro||JSON.stringify(j))));
            if (r.ok) { document.getElementById('tipo_produto').value=''; document.getElementById('nome_produto').value=''; document.getElementById('descricao_produto').value=''; document.getElementById('preco_produto').value='0.00'; fetchProdutos(); }
          } catch(e){ showMsg('msg_produto','Erro: '+e.message); }
        }

        async function cadastrarPedido(){
          const id_cliente = document.getElementById('select_cliente_pedido').value;
          const data = document.getElementById('data_pedido').value;
          const status = document.getElementById('status_pedido').value;
          if (!id_cliente || !data) { showMsg('msg_pedido','Selecione cliente e data'); return; }
          try{
            const r = await fetch('/pedidos',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id_cliente:parseInt(id_cliente),data,status})});
            const j = await r.json();
            showMsg('msg_pedido', r.ok ? 'Pedido criado (id: '+j.id_pedido+')' : ('Erro: '+(j.erro||JSON.stringify(j))));
            if (r.ok) { fetchPedidosIds(); listarPedidos(); }
          }catch(e){ showMsg('msg_pedido','Erro: '+e.message); }
        }

        async function adicionarItem(){
          const id_pedido = parseInt(document.getElementById('select_pedido').value || 0);
          const id_produto = parseInt(document.getElementById('select_produto').value || 0);
          const qtd = parseInt(document.getElementById('qtd_item').value || 0);
          if (!id_pedido || !id_produto || qtd<=0){ showMsg('msg_item','Preencha pedido, produto e quantidade'); return; }
          try{
            const r = await fetch('/itens-pedido',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id_pedido,id_produto,qtd_pedido:qtd})});
            const j = await r.json();
            showMsg('msg_item', r.ok ? 'Item adicionado' : ('Erro: '+(j.erro||JSON.stringify(j))));
            if (r.ok){ listarPedidos(); }
          }catch(e){ showMsg('msg_item','Erro: '+e.message); }
        }

        async function fetchProdutos(){ try{ const r=await fetch('/produtos'); const j=await r.json(); const sel=document.getElementById('select_produto'); sel.innerHTML=''; if(Array.isArray(j)){ j.forEach(p=>{ const o=document.createElement('option'); o.value=p.id_produto; o.textContent=`${p.id_produto} - ${p.nome}`; sel.appendChild(o); }); } }catch(e){ console.error(e); } }

        async function fetchClientes(){ try{ const r=await fetch('/clientes'); const j=await r.json(); const sel=document.getElementById('select_cliente_pedido'); sel.innerHTML='<option value="">-- selecione --</option>'; if(Array.isArray(j)){ j.forEach(c=>{ const o=document.createElement('option'); o.value=c.id_cliente; o.textContent=`${c.id_cliente} - ${c.nome}`; sel.appendChild(o); }); } }catch(e){ console.error(e); } }

        async function fetchPedidosIds(){ try{ const r=await fetch('/pedidos/completos'); const j=await r.json(); const sel=document.getElementById('select_pedido'); sel.innerHTML=''; if(Array.isArray(j)){ j.forEach(p=>{ const o=document.createElement('option'); o.value=p.id_pedido; o.textContent=`${p.id_pedido} - ${p.nome_cliente||'Cliente'}`; sel.appendChild(o); }); } }catch(e){ console.error(e); } }

        function renderSimpleList(lista){ const el=document.getElementById('lista_pedidos'); el.innerHTML=''; if(!Array.isArray(lista)||lista.length===0){ el.textContent='Nenhum pedido.'; return; } lista.forEach(p=>{ const d=document.createElement('div'); d.className='item'; d.innerHTML=`<strong>Pedido #${p.id_pedido}</strong> - ${p.nome_cliente||'Cliente'} <div class="muted">Data: ${p.data} • Status: ${p.status} • Total: R$ ${Number(p.total||0).toFixed(2)}</div>`; if(p.itens && p.itens.length){ const ul=document.createElement('ul'); p.itens.forEach(i=>{ const li=document.createElement('li'); li.textContent=`${i.nome_produto} — qtd:${i.qtd_pedido} — R$ ${Number(i.valor_unitario).toFixed(2)}`; ul.appendChild(li); }); d.appendChild(ul); } el.appendChild(d); }); }

        async function listarPedidos(){ try{ const r=await fetch('/pedidos/completos'); const j=await r.json(); renderSimpleList(j); fetchPedidosIds(); }catch(e){ console.error(e); } }

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
    erro = validar_json(dados, ['tipo', 'nome', 'valor_unitario'])
    if erro:
        return erro
    id_gerado = produtos.cadastrar(
        tipo=dados['tipo'],
        nome=dados['nome'],
        descricao=dados.get('descricao'),
        valor_unitario=dados.get('valor_unitario', 0.0),
    )
    return jsonify({"mensagem": "Produto cadastrado com sucesso!", "id_produto": id_gerado}), 201


@app.route('/produtos', methods=['GET'])
def listar_produtos():
    return jsonify(produtos.listar()), 200


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


@app.route('/clientes', methods=['GET'])
def listar_clientes():
    return jsonify(clientes.listar()), 200


@app.route('/pedidos', methods=['GET'])
def listar_pedidos():
    status = request.args.get('status')
    dados = pedidos.listar_completos()
    if status:
        dados = [p for p in dados if str(p.get('status')).lower() == status.lower()]
    return jsonify(dados), 200


@app.route('/pedidos/<int:id_pedido>/status', methods=['PATCH'])
def atualizar_status_pedido(id_pedido):
    dados = request.get_json(silent=True) or {}
    novo = dados.get('status')
    if not novo:
        return jsonify({'erro': 'Campo status é obrigatório.'}), 400
    try:
        atualizado = pedidos.alterar_status(id_pedido, novo)
        if atualizado:
            return jsonify({'mensagem': 'Status atualizado com sucesso.'}), 200
        return jsonify({'erro': 'Pedido não encontrado.'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/pedidos/ids', methods=['GET'])
def listar_pedidos_ids():
    dados = pedidos.listar_completos()
    simples = [{'id_pedido': p['id_pedido'], 'nome_cliente': p.get('nome_cliente')} for p in dados]
    return jsonify(simples), 200


# ---------------------------------------------------------------------------
# Rotas - Itens de Pedido
# ---------------------------------------------------------------------------

@app.route('/itens-pedido', methods=['POST'])
def adicionar_item_pedido():
    dados = request.get_json(silent=True) or {}
    erro = validar_json(dados, ['id_pedido', 'id_produto', 'qtd_pedido'])
    if erro:
        return erro
    try:
        itens.adicionar(
            id_pedido=dados['id_pedido'],
            id_produto=dados['id_produto'],
            qtd_pedido=dados['qtd_pedido'],
        )
        return jsonify({"mensagem": "Item adicionado ao pedido com sucesso!"}), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
