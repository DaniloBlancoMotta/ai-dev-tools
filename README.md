# TODO Application - Django

Uma aplicação web de gerenciamento de tarefas (TODO) construída com Django.

## Funcionalidades

-  Criar novos TODOs
-  Editar TODOs existentes
-  Deletar TODOs
-  Atribuir datas de vencimento
-  Marcar TODOs como resolvidos/não resolvidos
-  Interface moderna e responsiva

## Requisitos

- Python 3.12+
- uv (gerenciador de pacotes Python)

## Instalação e Execução

O projeto já está configurado! Para executar:

```bash
# Ativar o ambiente virtual
source .venv/bin/activate

# Executar o servidor
python manage.py runserver
```

O servidor estará disponível em: http://localhost:8000

## Acesso ao Admin

Para acessar o painel administrativo do Django em http://localhost:8000/admin:

- **Usuário:** admin
- **Senha:** admin

## Estrutura do Projeto

```
ai-dev-tools/
├── todoproject/          # Configurações do projeto Django
│   ├── settings.py      # Configurações principais
│   └── urls.py          # URLs principais
├── todos/               # App de TODOs
│   ├── models.py        # Modelo Todo
│   ├── views.py         # Views da aplicação
│   ├── urls.py          # URLs do app
│   ├── admin.py         # Configuração do admin
│   └── templates/       # Templates HTML
│       └── todos/
│           ├── base.html              # Template base
│           ├── todo_list.html         # Lista de TODOs
│           ├── todo_form.html         # Formulário criar/editar
│           └── todo_confirm_delete.html # Confirmação de deleção
├── manage.py            # CLI do Django
└── db.sqlite3          # Banco de dados SQLite
```

## Modelo de Dados

O modelo `Todo` possui os seguintes campos:

- **title** (CharField): Título do TODO
- **description** (TextField): Descrição detalhada (opcional)
- **due_date** (DateField): Data de vencimento (opcional)
- **resolved** (BooleanField): Status de resolução
- **created_at** (DateTimeField): Data de criação (automático)
- **updated_at** (DateTimeField): Data de atualização (automático)

## Uso

### Página Principal
Acesse http://localhost:8000 para ver a lista de TODOs.

### Criar TODO
Clique em "Create New TODO" e preencha o formulário.

### Editar TODO
Clique no botão "Edit" em qualquer TODO.

### Marcar como Resolvido
Clique no botão "Mark Resolved" para alternar o status.

### Deletar TODO
Clique no botão "Delete" e confirme a ação.

## Tecnologias Utilizadas

- **Django 5.2.8**: Framework web Python
- **SQLite**: Banco de dados
- **uv**: Gerenciador de pacotes Python
- **HTML/CSS**: Interface do usuário
