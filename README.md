![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-black?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-lightblue?logo=sqlite&logoColor=white)

# Sistema de Gerenciamento de Pedidos

API REST para gerenciar clientes, produtos e pedidos.

## O que faz

- **Clientes**: Cadastrar clientes com nome, email, senha, telefone e endereço
- **Produtos**: Cadastrar produtos com tipo, nome e descrição
- **Pedidos**: Criar pedidos vinculados a clientes e adicionar itens aos pedidos

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
    "descricao": "Descrição do produto"
  }
  ```

### Pedidos
- `POST /pedidos` - Criar novo pedido
  ```json
  {
    "id_cliente": 1,
    "data": "2026-06-24",
    "status": "pendente",
    "total": 100.00
  }
  ```

- `GET /pedidos/completos` - Listar todos os pedidos com detalhes

## Tecnologias

- **Python** - Linguagem de programação
- **Flask** - Framework web
- **SQLite** - Banco de dados
- **Flask-CORS** - Suporte para CORS
