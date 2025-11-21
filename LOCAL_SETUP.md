# Guia de Execução Local (Sem Docker)

Este guia explica como executar o Expense Tracker localmente para desenvolvimento sem usar Docker.

## Pré-requisitos

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Git

## 1. Configurar PostgreSQL

### Ubuntu/Debian

```bash
# Instalar PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Iniciar serviço
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Acessar como usuário postgres
sudo -u postgres psql

# Criar banco e usuário (no psql)
CREATE DATABASE expense_tracker;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE expense_tracker TO postgres;
\q
```

### Executar script de inicialização

```bash
# Conectar ao banco
psql -U postgres -d expense_tracker

# Executar o script (dentro do psql)
\i /caminho/completo/para/expense-tracker-app/backend/database_setup_postgres.sql

# Verificar tabelas criadas
\dt
\df

# Sair
\q
```

## 2. Configurar Backend

```bash
# Navegar para o diretório backend
cd backend

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variável de ambiente (opcional, já tem default)
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/expense_tracker"

# Executar servidor
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

O backend estará disponível em:
- API: http://localhost:8000
- Documentação: http://localhost:8000/docs

## 3. Configurar Frontend

**Em outro terminal:**

```bash
# Navegar para o diretório frontend
cd frontend

# Instalar dependências
npm install

# Configurar variável de ambiente (opcional, já tem default)
export VITE_API_URL="http://localhost:8000"

# Executar servidor de desenvolvimento
npm run dev
```

O frontend estará disponível em:
- Aplicação: http://localhost:5173
- Logs de Auditoria: http://localhost:5173/audit (senha: 123)

## 4. Verificar Instalação

### Testar Backend

```bash
# Verificar saúde da API
curl http://localhost:8000/health

# Listar categorias
curl http://localhost:8000/categories
```

### Testar Stored Procedures

```bash
# Conectar ao PostgreSQL
psql -U postgres -d expense_tracker

# Testar procedures
SELECT * FROM get_expense_summary();
SELECT * FROM get_expenses_by_category();

# Ver logs de auditoria
SELECT * FROM transaction_log ORDER BY log_timestamp DESC LIMIT 10;
```

## 5. Estrutura de Desenvolvimento

### Backend (FastAPI)

- **main.py**: Entry point da aplicação
- **database.py**: Conexão PostgreSQL e inicialização
- **models.py**: Modelos ORM (SQLAlchemy)
- **schemas.py**: Validação de dados (Pydantic)
- **crud.py**: Lógica de negócio e queries
- **routes.py**: Endpoints da API

### Frontend (Vue.js)

- **src/main.js**: Entry point + configuração router
- **src/App.vue**: Componente principal com validação
- **src/views/**: Componentes de página
- **src/api.js**: Cliente HTTP (Axios)

## 6. Desenvolvimento

### Hot Reload

Ambos backend e frontend possuem hot reload ativado:
- **Backend**: Uvicorn com `--reload` recarrega ao detectar mudanças em `.py`
- **Frontend**: Vite recarrega ao detectar mudanças em `.vue`, `.js`

### Adicionar Dependências

**Backend:**
```bash
cd backend
source venv/bin/activate
pip install nome-pacote
pip freeze > requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install nome-pacote
```

## 7. Resetar Banco de Dados

Se precisar limpar e recriar o banco:

```bash
# Conectar ao PostgreSQL como superusuário
sudo -u postgres psql

# Dropar e recriar banco
DROP DATABASE expense_tracker;
CREATE DATABASE expense_tracker;
GRANT ALL PRIVILEGES ON DATABASE expense_tracker TO postgres;
\q

# Executar script novamente
psql -U postgres -d expense_tracker -f backend/database_setup_postgres.sql

# Remover flag de inicialização (se existir)
rm /tmp/expense_tracker_db_initialized
```

## 8. Testes Manuais

### Testar CRUD de Categorias

```bash
# Criar categoria
curl -X POST http://localhost:8000/categories \
  -H "Content-Type: application/json" \
  -d '{"name": "Alimentação"}'

# Listar categorias
curl http://localhost:8000/categories

# Atualizar categoria
curl -X PUT http://localhost:8000/categories/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Alimentação e Bebidas"}'

# Deletar categoria
curl -X DELETE http://localhost:8000/categories/1
```

### Testar CRUD de Transações

```bash
# Criar categoria primeiro
curl -X POST http://localhost:8000/categories \
  -H "Content-Type: application/json" \
  -d '{"name": "Transporte"}'

# Criar transação
curl -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{"amount": 50.00, "description": "Uber", "category_id": 1}'

# Listar transações
curl http://localhost:8000/transactions

# Ver estatísticas
curl http://localhost:8000/statistics/monthly
curl http://localhost:8000/statistics/budget
curl http://localhost:8000/statistics/by-category
```

### Testar Audit Logs

```bash
# Criar, atualizar e deletar algumas transações
# Depois verificar os logs:

curl http://localhost:8000/audit-logs

# Ou via PostgreSQL:
psql -U postgres -d expense_tracker -c "SELECT * FROM transaction_log ORDER BY log_timestamp DESC;"
```

## 9. Variáveis de Ambiente

### Backend (.env ou export)

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/expense_tracker
PYTHONUNBUFFERED=1
```

### Frontend (.env.local)

```bash
VITE_API_URL=http://localhost:8000
```

## 10. Troubleshooting

### Erro: "ModuleNotFoundError"
```bash
# Certifique-se que o venv está ativado
source venv/bin/activate
pip install -r requirements.txt
```

### Erro: "psycopg2 not found"
```bash
# Instalar dependências do PostgreSQL
sudo apt install libpq-dev python3-dev
pip install psycopg2-binary
```

### Erro: "ENOSPC" (Frontend)
```bash
# Aumentar limite de watchers (Linux)
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### Erro: "Connection refused" ao PostgreSQL
```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Verificar porta 5432
sudo netstat -tuln | grep 5432

# Ver logs do PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

### Porta 8000 ou 5173 já em uso
```bash
# Encontrar processo usando a porta
sudo lsof -i :8000
sudo lsof -i :5173

# Matar processo
kill -9 <PID>

# Ou usar outra porta:
uvicorn main:app --port 8001 --reload
npm run dev -- --port 5174
```

## 11. Build para Produção

### Frontend

```bash
cd frontend
npm run build
# Arquivos estáticos gerados em: dist/
```

### Backend

```bash
# Usar gunicorn ao invés de uvicorn
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 12. Próximos Passos

- Implementar testes unitários (pytest para backend, vitest para frontend)
- Adicionar autenticação JWT
- Implementar paginação nas listagens
- Adicionar filtros e ordenação
- Criar dashboard com gráficos (Chart.js)
- Exportar relatórios (PDF, Excel)
