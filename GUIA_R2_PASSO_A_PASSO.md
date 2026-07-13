# Guia Visual Passo a Passo - Cloudflare R2 (Interface 2024)

Este guia vai te mostrar **exatamente onde clicar** na interface atual do Cloudflare R2.

---

## 📋 O Que Você Vai Precisar

Ao final deste guia, você terá:
- ✅ **Account ID** (encontra em 10 segundos)
- ✅ **Access Key ID** (criado em 2 minutos)
- ✅ **Secret Access Key** (criado em 2 minutos)
- ✅ **Bucket criado** (em 1 minuto)

**Tempo total:** ~5 minutos

---

## 🚀 Passo 1: Acessar o Cloudflare R2

### **1.1 Acesse o Dashboard**
1. Abra seu navegador
2. Vá para: **https://dash.cloudflare.com**
3. Faça login com sua conta

### **1.2 Acesse o R2**
1. No menu lateral esquerdo, procure por **"Storage & databases"**
2. Clique em **"Storage & databases"**
3. Procure por **"R2"** na lista
4. Clique em **"R2"**

**Você verá uma página como esta:**
```
┌─────────────────────────────────────┐
│  R2                                 │
│  Object Storage                     │
│                                     │
│  [Create bucket]  ← CLIQUE AQUI    │
│                                     │
│  Buckets:                            │
│  (nenhum bucket ainda)              │
└─────────────────────────────────────┘
```

---

## 📦 Passo 2: Criar o Bucket (Pasta)

### **2.1 Clique em "Create bucket"**

Você verá um formulário:

### **2.2 Preencha os dados**

**Bucket name:**
```
encomendas-fotos
```

**Location:**
- Clique no dropdown
- Selecione: **`sfo`** (São Francisco) ou **`lax`** (Los Angeles)

**Clique em "Create bucket"**

✅ **Pronto!** Bucket criado!

**Você verá:**
```
┌─────────────────────────────────────┐
│  R2 > encomendas-fotos              │
│                                     │
│  [Overview] [Objects] [Settings]    │
│                                     │
│  Bucket name: encomendas-fotos      │
│  Location: sfo                      │
└─────────────────────────────────────┘
```

---

## 🔑 Passo 3: Obter o Account ID

### **3.1 Na página do R2, olhe no TOPO**

Você verá algo assim:
```
┌──────────────────────────────────────────────────┐
│  R2                                               │
│  Account ID: abc123def456789...  [Copy]           │
│                                                  │
│  [Manage R2 API Tokens]                          │
└──────────────────────────────────────────────────┘
```

### **3.2 Copie o Account ID**

- Clique em **"Copy"** ao lado do Account ID
- Ou selecione e copie manualmente

**Exemplo de Account ID:**
```
abc123def4567890123456789012345678901
```

✅ **Account ID obtido!**

---

## 🔐 Passo 4: Criar API Token (Para Obter Access Key e Secret Key)

### **4.1 Clique em "Manage R2 API Tokens"**

Na mesma página do R2 (topo), clique em **"Manage R2 API Tokens"**

**Você verá:**
```
┌─────────────────────────────────────┐
│  R2 API Tokens                      │
│                                     │
│  [Create API Token]                 │
│                                     │
│  Tokens:                             │
│  (nenhum token ainda)               │
└─────────────────────────────────────┘
```

### **4.2 Clique em "Create API Token"**

**Você verá várias opções de templates:**

### **4.3 Selecione o Template**

Procure por um destes:
- **"Edit Cloudflare Workers"**
- **"Custom token"**
- **"R2 Token"**

Clique em **"Edit Cloudflare Workers"** (ou o mais próximo)

**Você verá:**
```
┌─────────────────────────────────────┐
│  Create API Token                   │
│                                     │
│  Token name:                        │
│  [________________]                 │
│                                     │
│  Permissions:                       │
│  [Add a permission]                 │
│                                     │
│  [Continue to summary]              │
└─────────────────────────────────────┘
```

### **4.4 Preencha o Nome do Token**

**Token name:**
```
encomendas-app
```

### **4.5 Adicione Permissões**

1. Clique em **"Add a permission"**
2. Você verá um menu com categorias:
   ```
   Account
   Cloudflare Workers
   R2
   ...
   ```
3. Clique em **"R2"**
4. Selecione **"Edit"** ou **"Read & Write"**

**Você verá:**
```
Permissions:
  Account > R2 > Edit
```

### **4.6 Clique em "Continue to summary"**

**Você verá um resumo:**
```
┌─────────────────────────────────────┐
│  Summary                             │
│                                     │
│  Token name: encomendas-app         │
│  Permissions:                       │
│    - Account > R2 > Edit            │
│                                     │
│  [Create token]                     │
└─────────────────────────────────────┘
```

### **4.7 Clique em "Create token"**

---

## ⚠️ Passo 5: ANOTAR AS CREDENCIAIS (MUITO IMPORTANTE!)

### **5.1 Você verá uma tela com as credenciais**

```
┌──────────────────────────────────────────────────┐
│  ✅ API Token Created                            │
│                                                  │
│  Token:                                         │
│  abc123def4567890123456789012345678901           │
│                                                  │
│  Access Key ID:                                 │
│  abc123def4567890123456789012345678901           │
│                                                  │
│  Secret Access Key:                             │
│  xyz7890123456789012345678901234567890           │
│                                                  │
│  ⚠️  Make sure to copy your Secret Access Key   │
│     now. You won't be able to see it again!     │
│                                                  │
│  [Done]                                         │
└──────────────────────────────────────────────────┘
```

### **5.2 ANOTE AGORA!**

**Copie e guarde em local seguro:**

1. **Access Key ID:**
   ```
   abc123def4567890123456789012345678901
   ```

2. **Secret Access Key:**
   ```
   xyz7890123456789012345678901234567890
   ```

⚠️ **ATENÇÃO:** 
- O **Secret Access Key** aparece **APENAS UMA VEZ**
- Se você fechar esta página, **não verá novamente**
- Você terá que criar um **novo token** se perder

### **5.3 Clique em "Done"**

---

## ⚙️ Passo 6: Configurar o Bucket como Público

### **6.1 Volte para o R2**

1. No menu lateral, clique em **"Storage & databases"**
2. Clique em **"R2"**
3. Clique no bucket **"encomendas-fotos"**

### **6.2 Clique na aba "Settings"**

Você verá:
```
┌─────────────────────────────────────┐
│  Settings                           │
│                                     │
│  Public access                      │
│  [Disabled]                         │
│                                     │
│  [Enable public access]             │
└─────────────────────────────────────┘
```

### **6.3 Clique em "Enable public access"**

**Você verá uma confirmação:**
```
┌─────────────────────────────────────┐
│  Enable public access?              │
│                                     │
│  This will make all objects in this │
│  bucket publicly accessible.        │
│                                     │
│  [Cancel]  [Enable]                 │
└─────────────────────────────────────┘
```

### **6.4 Clique em "Enable"**

✅ **Bucket agora é público!**

---

## 📝 Passo 7: Configurar o Sistema

### **7.1 Crie o arquivo .env**

```powershell
cd "C:\Users\Diniz\Encomendas-Mirantes-R2"

Copy-Item .env.example .env

notepad .env
```

### **7.2 Preencha com suas credenciais**

```env
# Configurações do Flask
SECRET_KEY=sua-chave-secreta-aqui-mude-em-producao
ADMIN_PASSWORD=setordentregas123
PORT=5000
FLASK_DEBUG=false

# Cloudflare R2
R2_ACCOUNT_ID=abc123def4567890123456789012345678901
R2_ACCESS_KEY_ID=abc123def4567890123456789012345678901
R2_SECRET_ACCESS_KEY=xyz7890123456789012345678901234567890
R2_BUCKET_NAME=encomendas-fotos

# Limites de armazenamento
STORAGE_LIMIT_GB=10
STORAGE_WARNING_THRESHOLD=0.80
```

**Substitua pelos seus valores reais!**

### **7.3 Salve o arquivo**

---

## 🧪 Passo 8: Testar a Conexão

```powershell
cd "C:\Users\Diniz\Encomendas-Mirantes-R2"
python test_r2.py
```

**Você verá:**
```
============================================================
TESTE DE INTEGRAÇÃO CLOUDFLARE R2
============================================================

1. Verificando dependências...
   ✅ boto3 instalado
   ✅ Pillow instalado

2. Verificando variáveis de ambiente...
   ✅ R2_ACCOUNT_ID: abc123def456...
   ✅ R2_ACCESS_KEY_ID: abc123...
   ✅ R2_SECRET_ACCESS_KEY: ***
   ✅ R2_BUCKET_NAME: encomendas-fotos

3. Testando conexão com Cloudflare R2...
   ✅ Conexão com R2 estabelecida

4. Verificando bucket...
   ✅ Bucket: 0 arquivos
   📊 Espaço usado: 0.00 GB de 10 GB
   ✅ Espaço OK

5. Testando upload de imagem...
   ✅ Upload realizado com sucesso!
   🔗 URL: https://abc123.r2.cloudflarestorage.com/...

6. Limpando arquivo de teste...
   ✅ Arquivo de teste removido

============================================================
✅ TESTE CONCLUÍDO COM SUCESSO!
============================================================
```

✅ **Tudo funcionando!**

---

## 🚀 Passo 9: Deploy no Render

### **9.1 Envie para GitHub**

```powershell
cd "C:\Users\Diniz\Encomendas-Mirantes-R2"

git init
git config user.name "Seu Nome"
git config user.email "seu-email@exemplo.com"
git add .
git commit -m "Sistema de encomendas - Versão R2"
git remote add origin https://github.com/SEU_USUARIO/encomendas-mirantes.git
git branch -M main
git push -u origin main
```

### **9.2 Configure no Render**

1. Acesse: **https://render.com**
2. Clique em **"New +"** > **"Web Service"**
3. Conecte com GitHub
4. Selecione o repositório
5. Configure:
   - **Name**: `encomendas-mirantes`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
6. Adicione as variáveis de ambiente (mesmas do .env)
7. Clique em **"Create Web Service"**

---

## ✅ Checklist Completo

- [ ] Acessei o Cloudflare Dashboard
- [ ] Criei o bucket `encomendas-fotos`
- [ ] Copiei o Account ID
- [ ] Criei o API Token
- [ ] ANOTEI o Access Key ID
- [ ] ANOTEI o Secret Access Key
- [ ] Configurei o bucket como público
- [ ] Criei o arquivo .env
- [ ] Preenchi o .env com as credenciais
- [ ] Testei com `python test_r2.py`
- [ ] Enviei para GitHub
- [ ] Configurei no Render
- [ ] Deploy concluído

---

## 🆘 Se Algo Der Errado

### **"Não encontro o R2 no menu"**
- Verifique se você está logado na conta correta
- O R2 pode não estar disponível em todas as contas
- Tente acessar diretamente: https://dash.cloudflare.com/r2

### **"Não vejo 'Manage R2 API Tokens'"**
- Procure por: **"API Tokens"** no menu
- Ou acesse: https://dash.cloudflare.com/profile/api-tokens

### **"Perdi a Secret Access Key"**
- Você terá que criar um **novo token**
- O antigo não pode mais ser visualizado

### **"Bucket não aparece como público"**
- Vá em R2 > bucket > Settings
- Clique em "Enable public access"

---

## 📞 Suporte

Se tiver dúvidas:
1. Verifique os logs do Render
2. Verifique o arquivo `COMO_CONFIGURAR_R2.md`
3. Me envie screenshots (oculte credenciais!)

---

**Pronto!** Agora você tem todas as credenciais e sabe exatamente onde encontrar cada uma! 🎉