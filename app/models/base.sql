CREATE TABLE topico (
    nome_topico varchar(63) NOT NULL,
    PRIMARY KEY (nome_topico)
);

CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,
    nome_usuario varchar(31) NOT NULL UNIQUE,
    nome_real varchar(127),
    biografia varchar(255),
    senha varchar(255),
    foto varchar(255),
    visibilidade BOOLEAN NOT NULL
);

CREATE TABLE relacao (
    tipo SMALLINT,
    origem INTEGER NOT NULL,
    alvo INTEGER NOT NULL,
    FOREIGN KEY (origem) REFERENCES usuario(id_usuario),
    FOREIGN KEY (alvo) REFERENCES usuario(id_usuario),
    PRIMARY KEY (origem, alvo)
);

CREATE TABLE opiniao (
    id_post SERIAL PRIMARY KEY,
    texto varchar(511),
    foto varchar(255),
    dono INTEGER NOT NULL,
    data_post TIMESTAMP,
    FOREIGN KEY (dono) REFERENCES usuario(id_usuario)
);

CREATE TABLE postagem (
    id_post INTEGER NOT NULL,
    PRIMARY KEY (id_post),
    FOREIGN KEY (id_post) REFERENCES opiniao(id_post)
);

CREATE TABLE comentario (
    id_post INTEGER NOT NULL,
    id_postagem INTEGER NOT NULL,
    PRIMARY KEY (id_post),
    FOREIGN KEY (id_post) REFERENCES opiniao(id_post),
    FOREIGN KEY (id_postagem) REFERENCES postagem(id_post)
);

CREATE TABLE citacao_topico (
    id_citacao_topico SERIAL PRIMARY KEY,
    id_post INTEGER NOT NULL,
    nome_topico varchar(63) NOT NULL,
    FOREIGN KEY (id_post) REFERENCES opiniao(id_post),
    FOREIGN KEY (nome_topico) REFERENCES topico (nome_topico)
);

CREATE TABLE marcacoes (
    id_marcacoes SERIAL PRIMARY KEY,
    id_post INTEGER NOT NULL,
    id_usuario INTEGER NOT NULL,
    FOREIGN KEY (id_post) REFERENCES opiniao(id_post),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE notificacao (
    id_notificacao SERIAL PRIMARY KEY,
    tipo SMALLINT,
    lida BOOLEAN NOT NULL,
    data_evento TIMESTAMP,
    dono_notificacao INTEGER NOT NULL,
    mencionado INTEGER,
    conteudo INTEGER,
    FOREIGN KEY (dono_notificacao) REFERENCES usuario(id_usuario),
    FOREIGN KEY (mencionado) REFERENCES usuario(id_usuario),
    FOREIGN KEY (conteudo) REFERENCES opiniao(id_post)
);
