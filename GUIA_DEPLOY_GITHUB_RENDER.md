# 🚀 GUIA: Deploy no GitHub + Render

## 📋 Informações Fornecidas:

**GitHub**: https://github.com/Dinix11/EncomendasR2/tree/main

**Credenciais R2**:
- R2_ACCOUNT_ID: `da53541a35783da7ffb5ba2d8f15035a`
- R2_ACCESS_KEY_ID: `16b999213d3646c894b83f93142fcedf`
- R2_SECRET_ACCESS_KEY: `47c875bc8da39ea4ff8b2ed7e5cefb70c32b3789deb5cdc7a873421deb507f6`
- R2_BUCKET_NAME: `Encomendas-fotos`
- ADMIN_PASSWORD: `teste123`

---

## 🎯 OBJETIVO:

1. ✅ Enviar código para o GitHub
2. ✅ Fazer deploy automático no Render
3. ✅ Sistema funcionando na nuvem

---

## 📤 PASSO 1: ENVIAR PARA GITHUB

### Opção A: Usar o Script Automático (Recomendado)

1. **No VS Code**, execute:
   ```bash
   configurar_github.bat
   ```

2. **Quando solicitado**:
   - Usuário GitHub: `Dinix11`
   - Nome do repositório: `EncomendasR2`

3. **Aguarde** o processo completar

4. **Digite sua senha do GitHub** quando solicitado

### Opção B: Manual (se o script não funcionar)

```bash
# Entre na pasta do projeto
cd ../Encomendas-Mirantes-R2

# Inicialize git (se não existir)
git init

# Adicione arquivos
git add .

# Commit
git commit -m "Sistema de Encomendas R2 - Versão completa"

# Conecte ao repositório
git remote add origin https://github.com/Dinix11/EncomendasR2.git

# Envie para o GitHub
git branch -M main
git push -u origin main
```

---

## 🌐 PASSO 2: DEPLOY NO RENDER

### 2.1 Acesse o Render
1. Abra: https://render.com
2. Faça login (ou crie uma conta gratuita)

### 2.2 Conecte com GitHub
1. Clique em **"New +"** → **"Web Service"**
2. Clique em **"Connect a repository"**
3. Autorize o Render a acessar seu GitHub
4. Selecione: **Dinix11/EncomendasR2**

### 2.3 Configure o Serviço
Preencha assim:

**Name**: `encomendas-mirantes`

**Environment**: `Python 3`

**Build Command**:
```bash
pip install -r requirements.txt
```

**Start Command**:
```bash
python app.py
```

**Plan**: `Free`

### 2.4 Adicione Variáveis de Ambiente
Clique em **"Advanced"** → **"Add Environment Variable"**

Adicione TODAS essas variáveis:

```
SECRET_KEY = sua-chave-secreta-aqui-mude-em-producao
ADMIN_PASSWORD = teste123
PORT = 5000
FLASK_DEBUG = false
R2_ACCOUNT_ID = da53541a35783da7ffb5ba2d8f15035a
R2_ACCESS_KEY_ID = 16b999213d3646c894b83f93142fcedf
R2_SECRET_ACCESS_KEY = 47c875bc8da39ea4ff8b2ed7e5cefb70c32b3789deb5cdc7a873421deb507f6
R2_BUCKET_NAME = Encomendas-fotos
STORAGE_LIMIT_GB = 10
STORAGE_WARNING_THRESHOLD = 0.80
```

### 2.5 Deploy
1. Clique em **"Create Web Service"**
2. Aguarde o deploy (3-5 minutos)
3. Você receberá uma URL: `https://encomendas-mirantes.onrender.com`

---

## ✅ PASSO 3: VERIFICAR

### Acesse o sistema:
```
https://encomendas-mirantes.onrender.com
```

### Login:
```
Senha: teste123
```

### Verifique os logs no Render:
- Deve aparecer: `✅ CLOUDFLARE R2 CONFIGURADO`
- SEM erros de AccessDenied

---

## 🔄 ATUALIZAÇÕES FUTURAS

### Quando modificar o código:

```bash
# 1. Adicione as mudanças
git add .

# 2. Commit
git commit -m "Descrição da mudança"

# 3. Envie para o GitHub
git push

# 4. O Render atualiza automaticamente!
```

---

## 📊 ESTRUTURA FINAL:

```
GitHub (Dinix11/EncomendasR2)
    ↓
Render (Deploy automático)
    ↓
https://encomendas-mirantes.onrender.com
    ↓
Acesso de qualquer lugar!
```

---

## 🆘 TROUBLESHOOTING

### Erro no deploy:
- Verifique os logs no Render
- Verifique se todas as variáveis de ambiente estão configuradas

### Erro de R2:
- Verifique se o bucket está público
- Verifique se as credenciais estão corretas

### Sistema não carrega:
- Verifique se o comando start está correto: `python app.py`
- Verifique se o build foi bem-sucedido

---

## 💡 DICAS:

1. **Render Free Tier**:
   - Dorme após 15 minutos de inatividade
   - Acorda em ~30 segundos quando acessado
   - 750 horas/mês grátis

2. **Banco de Dados**:
   - SQLite funciona no Render
   - Mas dados são perdidos se o serviço for recriado
   - Para produção, use PostgreSQL (Render oferece gratuito)

3. **R2**:
   - Funciona melhor com token com permissões corretas
   - Bucket deve estar público

---

## 🎯 PRONTO!

Após seguir esses passos, você terá:
- ✅ Código no GitHub
- ✅ Sistema online 24/7
- ✅ Acesso de qualquer lugar
- ✅ HTTPS automático

**URL do sistema**: `https://encomendas-mirantes.onrender.com`