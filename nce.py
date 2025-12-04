import sqlite3
conexao = sqlite3.connect('nce.db')

cursor = conexao.cursor()

sql = """
PRAGMA foreign_keys = ON;

CREATE TABLE user(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nome VARCHAR(50) NOT NULL,
    matricula VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(400) NOT NULL UNIQUE,
    email VARCHAR(50) NOT NULL UNIQUE,
    tipo VARCHAR(50) NOT NULL
);

CREATE TABLE noticia(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    titulo VARCHAR(200) NOT NULL UNIQUE,
    data_postagem DATE NOT NULL,
    categoria VARCHAR(50),
    conteudo TEXT NOT NULL UNIQUE,
    link1 VARCHAR(200),
    link2 VARCHAR(200),
    link3 VARCHAR(200),
    link4 VARCHAR(200),
    link5 VARCHAR(200),
    img1 VARCHAR(200),
    img2 VARCHAR(200),
    img3 VARCHAR(200)
);
"""

cursor.executescript(sql)
conexao.commit()
conexao.close()
