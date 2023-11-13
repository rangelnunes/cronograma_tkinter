import sqlite3

CRIA_TABELAS = """
create table if not exists semestres (
    ano integer not null,
    semestre integer not null,
    primary key(ano, semestre)
);

create table if not exists disciplinas (
    id integer primary key autoincrement,
    nome varchar(40) not null, 
    carga_horaria integer not null,
    nivel_de_ensino varchar(30) not null
);

create table if not exists oferta(
    id integer primary key autoincrement, 
    ano integer not null references semestres(ano),
    semestre integer not null references semestres(semestre),
    id_disciplina integer not null references disciplinas(id),
    FOREIGN KEY (ano, semestre) REFERENCES semestres (ano, semestre)
);
"""

def conecta_bd():
    conexao = sqlite3.connect('cronograma_20232.db')
    # habita o suporte à foreign key, pois elas são desabilitadas, por padrão
    conexao.execute("PRAGMA foreign_keys = 1")
    return conexao

def cria_tabelas(conexao):
    cursor = conexao.cursor()
    cursor.executescript(CRIA_TABELAS)
    conexao.commit()

def lista_semestres(conexao):
    cursor = conexao.cursor()
    cursor.execute('select * from semestres order by ano desc, semestre desc;')
    return cursor.fetchall()

def lista_disciplinas(conexao):
    cursor = conexao.cursor()
    cursor.execute('select * from disciplinas order by nome;')
    return cursor.fetchall()

def lista_ofertas(conexao):
    cursor = conexao.cursor()
    cursor.execute('select * from oferta join disciplinas on(oferta.id_disciplina = disciplinas.id) order by ano desc, semestre desc, nome asc, nivel_de_ensino asc;')
    return cursor.fetchall()

def consulta_disciplina_por_nome_e_nivel(conexao, nome, nivel):
    cursor = conexao.cursor()
    cursor.execute('select * from disciplinas where (nome = ? and nivel_de_ensino = ?);',(nome, nivel))
    return cursor.fetchall()

def insere_oferta(conexao, ano, semestre, disciplina):
    try:
        cursor = conexao.cursor()
        cursor.execute('insert into oferta (ano, semestre, id_disciplina) values (?, ?, ?)', (ano,semestre,disciplina))
        conexao.commit()
        linhas = cursor.rowcount
        erro = 0
    except Exception as e:
        erro = 1
        print('Erro ao inserir oferta')
    return linhas, erro

def consulta_oferta_com_condicao(conexao, ano, semestre, disciplina):
    cursor = conexao.cursor()
    cursor.execute('select * from oferta where ano = ? and semestre = ? and id_disciplina = ?;', (ano, semestre, disciplina))
    return cursor.fetchall()

def delete_oferta(conexao, id_oferta):
    cursor = conexao.cursor()
    cursor.execute('delete from oferta where id = ?;',(id_oferta,))
    print(f"Oferta excluida com sucesso!")
    conexao.commit()

def insere_semestre(conexao, ano, semestre):
    try:
        cursor = conexao.cursor()
        linhas = None
        erro = None
        cursor.execute('insert into semestres values (?, ?);', (int(ano), int(semestre)))
        conexao.commit()
        linhas = cursor.rowcount
        print('Semestre cadastrado com sucesso!')
    except sqlite3.IntegrityError:
        erro = 1
    except sqlite3.Error:
        erro = 2
        print(f'Erro ao cadastrar o semestre: {erro}')

    return linhas, erro

def deleta_semestre(conexao, ano, semestre):
    try:
        cursor = conexao.cursor()
        linhas = None
        cursor.execute('delete from semestres where ano = ? and semestre = ?;', (ano, semestre))
        conexao.commit()
        linhas = cursor.rowcount
    except sqlite3.IntegrityError:
        print('Erro ao remover o semestre!')
    except sqlite3.OperationalError:
        print('não foi possível remover o semestre')
    return linhas


