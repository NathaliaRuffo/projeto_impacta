# Gerenciador de Itens

Este projeto é um sistema de gerenciamento de itens desenvolvido com Flask e MySQL.

## Funcionalidades

- Adicionar novos itens com nome, quantidade e preço
- Listar todos os itens cadastrados
- Buscar produtos cadastrados
- Atualizar informações de itens existentes
- Ativar/desativar itens

## Tecnologias Utilizadas

- Python 3.x
- Flask
- SQLAlchemy
- MySQL
- HTML/CSS

## Configuração do Ambiente

1. Clone o repositório:
https://github.com/NathaliaRuffo/projeto_impacta.git

2. Instale as dependências:
   pip install -r requirements.txt


3. Configure o banco de dados MySQL:
   - Crie um banco de dados chamado `projeto_impacta`
   - Atualize a string de conexão em `app.py`:
     ```
     app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://seu_usuario:sua_senha@localhost/projeto_impacta'
     ```

4. Execute a aplicação:
   python app.py
   

5. Acesse a aplicação em `http://localhost:5000`

## Estrutura do Projeto

- `app.py`: Arquivo principal da aplicação Flask
- `templates/`: Diretório contendo os templates HTML
- `index.html`: Página principal com lista de itens e formulário de adição
- `update.html`: Página para atualização de itens
- `static/`: Diretório contendo arquivos estáticos
- `styles.css`: Estilos CSS para a aplicação
- `update_product.css`: Estilos CSS para a página de atualização
