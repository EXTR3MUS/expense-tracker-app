# Expense Tracker App

Sistema de controle de despesas com categorização e estatísticas.

## Tecnologias

- **Backend**: FastAPI + SQLAlchemy + SQLite
- **Frontend**: Vue.js 3 + Vite
- **Containerização**: Docker + Docker Compose

## Requisitos

- Docker Desktop
- WSL2 (Ubuntu 24.04)

## Como executar

1. Clone o repositório

2. Na raiz do projeto, execute:
```bash
docker-compose up --build
```

3. Acesse as aplicações:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - Documentação API: http://localhost:8000/docs

## Recursos Implementados

### Backend (FastAPI + SQLite + ORM)

- ✅ **Validação com restrições**: CheckConstraints no SQLAlchemy para validar dados
- ✅ **Retorno de códigos de erro**: HTTPException com códigos HTTP apropriados
- ✅ **CRUD completo**: Inserção, recuperação e atualização de dados
- ✅ **Visões**: Funções que simulam views SQL para agregação de dados
- ✅ **Procedures**: Funções que simulam stored procedures para operações complexas

### Frontend (Vue.js)

- Interface completa para gerenciamento de categorias
- Interface completa para gerenciamento de despesas
- Dashboard com estatísticas
- Integração com API via Fetch/Axios

## Estrutura do Projeto

```
expense-tracker-app/
├── backend/
│   ├── main.py           # Aplicação FastAPI
│   ├── database.py       # Configuração do banco de dados
│   ├── models.py         # Modelos SQLAlchemy
│   ├── schemas.py        # Schemas Pydantic
│   ├── routes.py         # Rotas da API
│   ├── crud.py           # Operações CRUD
│   ├── requirements.txt  # Dependências Python
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── views/        # Componentes de página
│   │   ├── App.vue       # Componente principal
│   │   ├── main.js       # Entry point
│   │   └── api.js        # Cliente API
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml
```

## Desenvolvimento

Para parar os containers:
```bash
docker-compose down
```

Para reconstruir após mudanças:
```bash
docker-compose up --build
```

Para ver logs:
```bash
docker-compose logs -f
```
