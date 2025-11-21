from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time

# PostgreSQL configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/expense_tracker"
)

DB_INITIALIZED_FLAG = "/tmp/expense_tracker_db_initialized"
SQL_SETUP_FILE = "./database_setup_postgres.sql"

engine = create_engine(DATABASE_URL, echo=False)

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
    """Executa o script SQL se o banco de dados não foi inicializado"""
    
    # Verificar se já foi inicializado
    if os.path.exists(DB_INITIALIZED_FLAG):
        print("Database already initialized.")
        return
    
    # Aguardar PostgreSQL estar pronto
    max_retries = 30
    retry_count = 0
    while retry_count < max_retries:
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("PostgreSQL is ready!")
            break
        except Exception as e:
            retry_count += 1
            print(f"Waiting for PostgreSQL... ({retry_count}/{max_retries})")
            time.sleep(1)
    
    if retry_count >= max_retries:
        raise Exception("Could not connect to PostgreSQL")
    
    # Verificar se as tabelas já existem
    try:
        with engine.connect() as connection:
            result = connection.execute(text(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'category')"
            ))
            table_exists = result.scalar()
            
            if table_exists:
                print("Database tables already exist.")
                # Marcar como inicializado
                with open(DB_INITIALIZED_FLAG, 'w') as f:
                    f.write('initialized')
                return
    except Exception as e:
        print(f"Error checking tables: {e}")
    
    # Executar script SQL
    print("Initializing database from SQL script...")
    if os.path.exists(SQL_SETUP_FILE):
        with open(SQL_SETUP_FILE, 'r') as f:
            sql_script = f.read()
        
        try:
            with engine.connect() as connection:
                # PostgreSQL pode executar múltiplos statements de uma vez
                connection.execute(text(sql_script))
                connection.commit()
            
            print("Database initialized successfully!")
            
            # Marcar como inicializado
            with open(DB_INITIALIZED_FLAG, 'w') as f:
                f.write('initialized')
                
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise
    else:
        print(f"Warning: {SQL_SETUP_FILE} not found. Creating tables from models...")
        Base.metadata.create_all(bind=engine)
