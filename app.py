from flask import Flask, request, render_template, redirect, url_for, flash
from sqlalchemy import create_engine, text, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql

# Configuração do banco de dados
mysql_host = "mysql-aula.cuebxlhckhcy.us-east-1.rds.amazonaws.com"
mysql_dbname = "mysqlaula"
mysql_user = "mysqlaula"
mysql_password = "MySQLAula123!"
mysql_port = 3306

# Construção da URL de conexão
db_url = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_dbname}"
engine = create_engine(db_url)

# Criar uma fábrica de sessões
Session = sessionmaker(bind=engine)

# Declarative Base para definição de modelos
Base = declarative_base()

# Definição do modelo de tabela
class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, default=func.current_timestamp(), nullable=False)

# Criando a tabela no banco de dados
def criar_tabela():
    """
    Cria a tabela 'emails' no banco de dados, caso ela não exista.
    """
    try:
        Base.metadata.create_all(engine)
        print("Tabela criada ou já existente no banco de dados.")
    except Exception as e:
        print(f"Erro ao criar a tabela: {e}")

# Função para inserir email
def inserir_email(email):
    """
    Insere um email na tabela 'emails'.
    
    Args:
        email (str): Endereço de email a ser inserido.
    """
    session = Session()
    try:
        # Inserindo um novo registro
        novo_email = Email(email=email)
        session.add(novo_email)
        session.commit()  # Confirmando a transação
        print(f"E-mail '{email}' inserido com sucesso.")
    except Exception as e:
        print(f"Erro ao executar a query: {e}")
        session.rollback()  # Reverter alterações em caso de erro
    finally:
        session.close()  # Fechar a sessão

# Inicializando o Flask
app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Necessário para o flash

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/salvar_email', methods=['POST'])
def salvar_email():
    email = request.form['email']
    try:
        inserir_email(email)  # Inserindo o email no banco
        flash("Email cadastrado com sucesso!", "success")  # Exibindo mensagem de sucesso
    except Exception as e:
        flash(f"Erro ao cadastrar o email: {e}", "error")  # Exibindo mensagem de erro
    return redirect(url_for('index'))  # Redireciona de volta para a página inicial

if __name__ == '__main__':
    criar_tabela()  # Garante que a tabela exista antes de rodar o app
    app.run(debug=True)
