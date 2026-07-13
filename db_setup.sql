-- SQL para criar as tabelas no Supabase (Postgres)
-- Rode isso no SQL Editor do Supabase

CREATE TABLE IF NOT EXISTS unidades (
    id BIGSERIAL PRIMARY KEY,
    numero TEXT NOT NULL UNIQUE,
    telefone TEXT NOT NULL,
    nome_residente TEXT,
    bloco TEXT,
    criado_em TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS encomendas (
    id BIGSERIAL PRIMARY KEY,
    unidade_id BIGINT NOT NULL REFERENCES unidades(id),
    data_recebimento TIMESTAMP NOT NULL DEFAULT NOW(),
    descricao TEXT,
    foto_url TEXT,  -- URL pública do Supabase Storage
    codigo TEXT NOT NULL,
    status TEXT DEFAULT 'pendente',
    data_entrega TIMESTAMP,
    entregue_por TEXT
);

CREATE TABLE IF NOT EXISTS notificacoes (
    id BIGSERIAL PRIMARY KEY,
    encomenda_id BIGINT,
    telefone TEXT,
    mensagem TEXT,
    link_whatsapp TEXT,
    enviado_em TIMESTAMP DEFAULT NOW()
);

-- Índice para buscas rápidas por código
CREATE INDEX IF NOT EXISTS idx_encomendas_codigo ON encomendas (codigo);
CREATE INDEX IF NOT EXISTS idx_encomendas_status ON encomendas (status);