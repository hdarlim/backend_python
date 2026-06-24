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

A API estará disponível em `http://localhost:5000`

## Endpoints

### Clientes
- `POST /clientes` - Cadastrar novo cliente

### Produtos
- `POST /produtos` - Cadastrar novo produto

### Pedidos
- `POST /pedidos` - Criar novo pedido
- `GET /pedidos/completos` - Listar pedidos completos

## Tecnologias

- **Python** - Linguagem de programação
- **Flask** - Framework web
- **SQLite** - Banco de dados
- **Flask-CORS** - Suporte para CORS
