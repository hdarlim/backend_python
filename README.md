![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-black?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-lightblue?logo=sqlite&logoColor=white)

# Sistema de Gerenciamento de Pedidos

API REST para gerenciar clientes, produtos e pedidos.

## O que faz

- **Clientes**: Cadastrar clientes com nome, email, senha, telefone e endereço
- **Produtos**: Cadastrar produtos com tipo, nome e descrição
- **Pedidos**: Criar pedidos vinculados a clientes e adicionar itens aos pedidos
  - **Produtos**: Cadastrar produtos com tipo, nome, descrição e preço unitário (`valor_unitario`)
  - **Itens de pedido**: Ao adicionar um item, o sistema usa o `valor_unitario` cadastrado no produto; não é necessário (nem permitido) enviar o preço ao adicionar o item. O total do pedido é calculado automaticamente como soma(qtd * valor_unitario).

## Como usar

### Instalação

```bash
pip install flask flask-cors werkzeug
```

### Iniciar

```bash
python main.py
```

O servidor estará disponível em `http://localhost:5000`

## Interface Web

Acesse `http://localhost:5000` no navegador para usar a **interface gráfica** com:
- 📝 Formulário para cadastrar clientes
- 🛍️ Formulário para cadastrar produtos
- 🛍️ Formulário para cadastrar produtos (agora com campo de preço unitário)
- 📋 Formulário para criar pedidos
- 📊 Visualização de todos os pedidos

## Endpoints da API

### Clientes
- `POST /clientes` - Cadastrar novo cliente
  ```json
  {
    "nome": "João Silva",
    "email": "joao@email.com",
    "senha": "123456",
    "telefone": "11999999999",
    "endereco": "Rua..., Número..."
  }
  ```

### Produtos
- `POST /produtos` - Cadastrar novo produto
  ```json
  {
    "tipo": "Extensão",
    "nome": "Curso de Python",
    "descricao": "Descrição do produto",
    "valor_unitario": 49.90
  }
  ```

### Pedidos
- `POST /pedidos` - Criar novo pedido
  ```json
  {
    "id_cliente": 1,
    "data": "2026-06-24",
    "status": "pendente"
  }
  ```

- `GET /pedidos/completos` - Listar todos os pedidos com detalhes

## Tecnologias

- **Python** - Linguagem de programação
- **Flask** - Framework web
- **SQLite** - Banco de dados
- **Flask-CORS** - Suporte para CORS

## Observações rápidas
- Ao adicionar um item ao pedido (`POST /itens-pedido`) envie apenas: `id_pedido`, `id_produto`, `qtd_pedido`.
- O campo `valor_unitario` do item é preenchido a partir do produto no momento da inserção, preservando o preço histórico do item.
