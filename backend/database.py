from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = "sqlite:///./expense_tracker.db"
DB_FILE = "./expense_tracker.db"
SQL_SETUP_FILE = "./database_setup.sql"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency para obter sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para inicializar o banco com o script SQL
def init_database():
    """Executa o script SQL se o banco de dados não existir"""
    if not os.path.exists(DB_FILE):
        print("Database not found. Running setup script...")
        if os.path.exists(SQL_SETUP_FILE):
            with open(SQL_SETUP_FILE, 'r') as f:
                sql_script = f.read()
            
            # Executar o script SQL
            with engine.connect() as connection:
                # Remover comentários
                lines = []
                for line in sql_script.split('\n'):
                    # Ignorar linhas que são apenas comentários
                    stripped = line.strip()
                    if stripped and not stripped.startswith('--'):
                        # Remover comentários inline
                        if '--' in line:
                            line = line[:line.index('--')]
                        lines.append(line)
                
                clean_sql = '\n'.join(lines)
                
                # Processar statements considerando BEGIN...END
                statements = []
                current_statement = []
                in_trigger = False
                
                for part in clean_sql.split(';'):
                    part = part.strip()
                    if not part:
                        continue
                    
                    current_statement.append(part)
                    
                    # Detectar se estamos dentro de um trigger/procedure
                    if 'BEGIN' in part.upper():
                        in_trigger = True
                    
                    if 'END' in part.upper() and in_trigger:
                        in_trigger = False
                        statements.append(';'.join(current_statement))
                        current_statement = []
                    elif not in_trigger:
                        statements.append(part)
                        current_statement = []
                
                # Executar cada statement
                for statement in statements:
                    statement = statement.strip()
                    if statement:
                        try:
                            connection.execute(text(statement))
                        except Exception as e:
                            print(f"Error executing statement: {statement[:100]}...")
                            print(f"Error: {e}")
                            raise
                
                connection.commit()
            print("Database initialized successfully!")
        else:
            print(f"Warning: {SQL_SETUP_FILE} not found. Creating empty database.")
            Base.metadata.create_all(bind=engine)
