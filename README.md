# Expense Tracker App

Sistema de controle de despesas com categorização, estatísticas e auditoria completa.

## Tecnologias

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: Vue.js 3 + Vite + Vue Router
- **Banco de Dados**: PostgreSQL 15 com Stored Procedures
- **Containerização**: Docker + Docker Compose

## Requisitos

- Docker Desktop
- WSL2 (Ubuntu 24.04)

## Como executar

### Com Docker (Recomendado)

1. Clone o repositório

2. Na raiz do projeto, execute:
```bash
docker-compose up --build
```

3. Acesse as aplicações:
   - **Frontend**: http://localhost:5173
   - **Backend API**: http://localhost:8000
   - **Documentação API**: http://localhost:8000/docs
   - **Logs de Auditoria**: http://localhost:5173/audit (senha: 123)
   - **PostgreSQL**: localhost:5432 (usuário: postgres, senha: postgres)

### Desenvolvimento Local

Veja [LOCAL_SETUP.md](LOCAL_SETUP.md) para instruções de execução local sem Docker.

## Recursos Implementados

### Backend (FastAPI + PostgreSQL + ORM)

- ✅ **Validação com restrições**: CHECK constraints no banco de dados (`amount > 0`)
- ✅ **Retorno de códigos de erro**: HTTPException com códigos HTTP apropriados (400, 404, etc.)
- ✅ **CRUD completo**: Inserção, recuperação, atualização e exclusão de dados
- ✅ **Visões SQL**: `View_Monthly_Summary` para agregação de despesas mensais
- ✅ **Stored Procedures**: Procedures reais em PL/pgSQL:
  - `get_expense_summary()` - Retorna total, contagem e média de despesas
  - `get_expenses_by_category()` - Agrupa despesas por categoria
  - `update_budget_on_transaction()` - Trigger function para atualização automática do orçamento
  - `log_transaction_changes()` - Trigger function para auditoria completa

### Sistema de Auditoria

- ✅ **Logs automáticos**: Toda operação (INSERT, UPDATE, DELETE) é registrada
- ✅ **Rastreamento completo**: Valores antigos e novos são armazenados
- ✅ **Interface protegida**: Página `/audit` com autenticação por senha
- ✅ **Visualização detalhada**: Código de cores por tipo de operação (verde=INSERT, azul=UPDATE, vermelho=DELETE)

### Frontend (Vue.js)

- ✅ **Validação de inputs**: Validação client-side antes de enviar ao backend
  - Campos obrigatórios marcados visualmente
  - Validação de valores numéricos (amount > 0)
  - Validação de seleção de categoria
  - Feedback visual de erros
- ✅ **Interface completa**: Gerenciamento de categorias e despesas
- ✅ **Dashboard com estatísticas**: Orçamento total, resumo mensal, análise por categoria
- ✅ **Roteamento SPA**: Vue Router para navegação (home, audit logs, unauthorized)
- ✅ **Integração com API**: Axios para comunicação com backend

## Estrutura do Projeto

```
expense-tracker-app/
├── backend/
│   ├── main.py                      # Aplicação FastAPI
│   ├── database.py                  # Configuração PostgreSQL + inicialização
│   ├── models.py                    # Modelos SQLAlchemy (ORM)
│   ├── schemas.py                   # Schemas Pydantic (validação)
│   ├── routes.py                    # Rotas da API REST
│   ├── crud.py                      # Operações CRUD + chamadas a procedures
│   ├── database_setup_postgres.sql  # Schema PostgreSQL com procedures/triggers
│   ├── requirements.txt             # Dependências Python (FastAPI, psycopg2, etc.)
│   └── Dockerfile                   # Container Python
├── frontend/
│   ├── src/
│   │   ├── views/                   # Componentes de página
│   │   │   ├── AuditLogs.vue       # Página de auditoria (protegida)
│   │   │   └── Unauthorized.vue    # Página de acesso negado
│   │   ├── App.vue                  # Componente principal com validação
│   │   ├── RouterApp.vue            # Wrapper do router
│   │   ├── main.js                  # Entry point + configuração router
│   │   └── api.js                   # Cliente Axios
│   ├── package.json
│   └── Dockerfile                   # Container Node
├── docker-compose.yml               # Orquestração (Postgres + Backend + Frontend)
├── README.md                        # Este arquivo
└── LOCAL_SETUP.md                   # Guia de execução local
```

## Banco de Dados PostgreSQL

### Acessar via terminal

```bash
# Conectar ao PostgreSQL interativo
docker exec -it expense-tracker-postgres psql -U postgres -d expense_tracker

# Comandos úteis no psql:
\dt                              # Listar tabelas
\df                              # Listar funções/procedures
\d table_name                    # Ver estrutura de uma tabela
SELECT * FROM get_expense_summary();        # Executar stored procedure
SELECT * FROM get_expenses_by_category();   # Executar stored procedure
SELECT * FROM transaction_log;              # Ver logs de auditoria
\q                               # Sair
```

### Acessar via DBeaver/pgAdmin

- **Host**: localhost
- **Port**: 5432
- **Database**: expense_tracker
- **Username**: postgres
- **Password**: postgres

## Demonstração de Recursos Acadêmicos

### 1. Validação por Restrições

O banco possui CHECK constraints:
```sql
CHECK (amount > 0)  -- Impede valores negativos ou zero
```

### 2. Visões (VIEWs)

```sql
CREATE VIEW View_Monthly_Summary AS
SELECT TO_CHAR(date, 'YYYY-MM') AS month, SUM(amount) AS total_expenses
FROM Transactions GROUP BY TO_CHAR(date, 'YYYY-MM');
```

### 3. Stored Procedures

```sql
-- Procedure para estatísticas gerais
CREATE OR REPLACE FUNCTION get_expense_summary()
RETURNS TABLE(total_expenses NUMERIC, expense_count BIGINT, average_expense NUMERIC)
...

-- Procedure para análise por categoria  
CREATE OR REPLACE FUNCTION get_expenses_by_category()
RETURNS TABLE(category TEXT, transaction_count BIGINT, total_amount NUMERIC, average_amount NUMERIC)
...
```

### 4. Triggers para Auditoria e Business Logic

```sql
-- Trigger para atualizar orçamento automaticamente
CREATE TRIGGER budget_trigger
AFTER INSERT OR UPDATE OR DELETE ON Transactions
FOR EACH ROW EXECUTE FUNCTION update_budget_on_transaction();

-- Trigger para registrar todas as mudanças
CREATE TRIGGER audit_trigger  
AFTER INSERT OR UPDATE OR DELETE ON Transactions
FOR EACH ROW EXECUTE FUNCTION log_transaction_changes();
```

### 5. Validação Frontend

O frontend Vue.js implementa validação client-side:
- Campos obrigatórios (categoria, valor)
- Validação numérica (amount > 0)
- Feedback visual de erros
- Sanitização antes de envio

## Desenvolvimento

Para parar os containers:
```bash
docker-compose down
```

Para parar e remover volumes (limpar banco):
```bash
docker-compose down -v
```

Para reconstruir após mudanças:
```bash
docker-compose up --build
```

Para ver logs:
```bash
docker-compose logs -f              # Todos os serviços
docker-compose logs -f backend      # Apenas backend
docker-compose logs -f postgres     # Apenas banco
```

## Troubleshooting

**Banco não inicializa**: Remova o flag temporário
```bash
rm /tmp/expense_tracker_db_initialized
docker-compose restart backend
```

**Erro de conexão**: Verifique se o PostgreSQL está saudável
```bash
docker-compose ps
```

**Resetar banco completamente**:
```bash
docker-compose down -v
rm /tmp/expense_tracker_db_initialized  
docker-compose up --build
```
