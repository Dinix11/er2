# Instruções para corrigir o problema de reset no Render

## Problema
Quando o serviço dorme no Render (plano gratuito), todos os dados salvos em SQLite local são perdidos.

## Solução
Usar Supabase (banco na nuvem) de forma consistente.

## Passos obrigatórios

### 1. Configure as variáveis de ambiente no Render
Vá no seu serviço no Render → Environment e adicione:

- SUPABASE_URL = https://xxxx.supabase.co
- SUPABASE_KEY = eyJhbGci... (chave anon/public)
- ADMIN_PASSWORD = (sua senha)

Depois salve e faça um novo deploy.

### 2. Crie o bucket de fotos no Supabase Storage
1. Abra seu projeto no Supabase
2. Vá em **Storage**
3. Clique em **New bucket**
4. Nome: `fotos`
5. Marque como **Public bucket**
6. Clique em **Create bucket**

### 3. Rode o script SQL no Supabase (só uma vez)
1. Vá em **SQL Editor**
2. Cole todo o conteúdo do arquivo `db_setup.sql`
3. Clique em **Run**

### 4. Faça deploy das mudanças
Faça push ou Manual Deploy no Render.

## O que foi corrigido no código
- Todas as consultas agora usam Supabase quando as variáveis estão configuradas
- index(), historico(), gerar_código, api, etc.
- Suporte correto ao PORT do Render
- Rota de foto aceita URLs remotas
- Adicionado gunicorn + render.yaml

## Como aplicar essas mudanças
Copie os seguintes arquivos do projeto corrigido:

- requirements.txt
- render.yaml (novo)
- app.py (modificado)
- (Opcional) db_setup.sql

Depois faça commit e push.

## Verificação
Depois do deploy, olhe os logs do Render.
Você deve ver: "✅ Usando Supabase (dados persistentes)"

Se aparecer "Usando SQLite local", as variáveis de ambiente não estão configuradas corretamente.
