import sqlite3
import getpass

def login(con, cursor):

    login = input("Login: ")
    senha = getpass.getpass("Senha: ")

    query = f"""
        SELECT 
            count(*)
        FROM tb_cad_user
        WHERE LOGIN = "{login}" AND SENHA = "{senha}"; 
    """

    try:
        cursor.execute(query)
        con.commit()
        rows = cursor.fetchall()

        for row in rows:
            if row[0] == 1:
                status_login = 1
            else:
                print("Usuário/Senha Inválido")
                status_login = 0

    except sqlite3.Error as error:
        print("Erro ao logar, erro: ", error)
    
    return status_login

def create_user(con, cursor):
    
    nome = input("Digite seu nome completo: ")
    login = input("Login: ")
    senha = getpass.getpass("Senha: ")
    
    query_create_tb_cad_user = """
    CREATE TABLE IF NOT EXISTS tb_cad_user(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NOME VARCHAR(100),
        LOGIN VARCHAR(100),
        SENHA VARCHAR(100),
        UNIQUE (LOGIN)
    );
    """
    try:
        cursor.execute(query_create_tb_cad_user)
        con.commit()
    except sqlite3.Error as error:
        print("Falha ao executar query de verificação tabela tb_cad_user: ", error)

    query_cad_user = f"""
    INSERT INTO tb_cad_user 
    (NOME, LOGIN, SENHA)
    VALUES ("{nome}", "{login}", "{senha}");
    """

    try:
        cursor.execute(query_cad_user)
        con.commit()
        print(f"Usuario {login} cadastrado com sucesso!")
    except sqlite3.Error as error:
        print("Falha ao cadastrar usuário, erro: ", error)


def lista_usuarios(con, cursor):
    query = f"""
        SELECT 
            NOME,
            LOGIN
        FROM tb_cad_user; 
    """

    try:
        cursor.execute(query)
        con.commit()
        rows = cursor.fetchall()

        for row in rows:
            print(f"Nome usuário: {row[0]} | Login: {row[1]}")

    except sqlite3.Error as error:
        print("Erro ao listar users, erro: ", error)

def atualiza_senha(con, cursor):

    login = input("Digite seu Login: ")
    nova_senha = getpass.getpass("Nova senha: ")

    query = f"""
        UPDATE tb_cad_user
        SET senha = "{nova_senha}"
        WHERE LOGIN = "{login}"; 
    """

    try:
        cursor.execute(query)
        con.commit()
    except sqlite3.Error as error:
        print("Erro ao atualizar usuário, erro: ", error)

def deletar_user(con, cursor):

    login = input("Digite seu Login: ")

    if login == "adm":
        print("Não é possível deletar o ADM")
    else:
        query = f"""
            DELETE FROM tb_cad_user
            WHERE LOGIN = "{login}"; 
        """

        try:
            cursor.execute(query)
            con.commit()
        except sqlite3.Error as error:
            print("Erro ao deletar usuário, erro: ", error)

interacao = "OK"

con = sqlite3.connect('db_teste.db')
cursor = con.cursor()

status_login = login(con, cursor)

if status_login == 1:
    while interacao != "s":
        print("\n")
        print("### Sistema de cadastro ###")
        print("### 0 - Para sair do sistema ###")
        print("### 1 - Cadastro de usuários ###")
        print("### 2 - Listagem de usuários ###")
        print("### 3 - Atualizar usuários   ###")
        print("### 4 - Deletar usuários     ###\n")

        opt = str(input("Digite uma opção:"))
        print(f"Opção: {opt}\n")

        if opt == "1":
            create_user(con, cursor)
        elif opt == "2":
            lista_usuarios(con, cursor)
        elif opt == "3":
            atualiza_senha(con, cursor)
        elif opt == "4":
            deletar_user(con, cursor)
        elif opt == "0":
            interacao = 's'
            print("SAINDO")
        else:
            print("Digite uma opção válida\n")


cursor.close()
con.close()