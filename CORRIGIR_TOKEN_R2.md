# ⚠️ CORRIGIR TOKEN DO R2

## Problema Identificado:

O bucket está público ✅, mas o **token não tem permissões** ❌

```
Erro: AccessDenied - PutObject operation: Access Denied
```

## Solução: Criar Novo Token com Permissões Corretas

### Passo 1: Acessar Cloudflare
1. Abra: https://dash.cloudflare.com
2. Faça login

### Passo 2: Acessar R2 API Tokens
1. Menu lateral → **R2**
2. Clique em **Overview** (ou **Buckets**)
3. Procure por: **Manage R2 API Tokens**
4. Clique em **Create API Token**

### Passo 3: Configurar Token
Preencha assim:

**Token name**: `Encomendas-Fotos-Token`

**Permissions** (clique em "Add custom"):
- ✅ **Account** > **Cloudflare R2** > **Edit** (OBRIGATÓRIO)
- ✅ **Account** > **Cloudflare R2** > **Read** (OBRIGATÓRIO)

**Account Resources**:
- Selecione sua conta

**Clique em Create Token**

### Passo 4: Copiar Credenciais
⚠️ **ATENÇÃO**: Você verá as credenciais APENAS UMA VEZ!

Copie:
- **Access Key ID** (32 caracteres)
- **Secret Access Key** (64 caracteres)

### Passo 5: Atualizar .env
Abra o arquivo `.env` e substitua:

```env
# Antes (errado):
R2_ACCESS_KEY_ID=16b999213d3646c894b83f93142fcedf
R2_SECRET_ACCESS_KEY=47c875bc8da39ea4ff8b2ed7e5cefb70c32b3789deb5cdc7a873421deb507f6

# Depois (correto):
R2_ACCESS_KEY_ID=COLE_AQUI_O_NOVO_ACCESS_KEY_ID
R2_SECRET_ACCESS_KEY=COLE_AQUI_O_NOVO_SECRET_ACCESS_KEY
```

### Passo 6: Reiniciar Aplicação
```bash
# No VS Code:
# 1. Pressione CTRL+C (parar servidor)
# 2. Execute:
python app.py
```

### Passo 7: Verificar
Você deve ver:
```
✅ CLOUDFLARE R2 CONFIGURADO - usando armazenamento na nuvem
   Bucket: X arquivos, Y.YY GB de 10 GB
```

SEM erros de AccessDenied!

---

## 🎯 Resumo Visual:

```
┌─────────────────────────────────────────────────────┐
│  1. Cloudflare Dashboard                            │
│     ↓                                               │
│  2. R2 → Manage R2 API Tokens                       │
│     ↓                                               │
│  3. Create API Token                                │
│     ↓                                               │
│  4. Permissões: Edit + Read                         │
│     ↓                                               │
│  5. Copiar Access Key ID e Secret                   │
│     ↓                                               │
│  6. Colar no arquivo .env                           │
│     ↓                                               │
│  7. Reiniciar: python app.py                        │
│     ↓                                               │
│  8. ✅ Pronto! R2 funcionando                       │
└─────────────────────────────────────────────────────┘
```

---

## ⚠️ IMPORTANTE:

- O **Access Key ID** tem 32 caracteres (ex: `abc123...`)
- O **Secret Access Key** tem 64 caracteres (ex: `xyz789...`)
- NÃO confunda com o Account ID (que já está correto)
- NÃO use a URL do bucket como Access Key

---

## 🆘 Se Ainda Não Funcionar:

1. Verifique se o token tem permissões **Edit** e **Read**
2. Verifique se o nome do bucket está correto: `Encomendas-fotos`
3. Verifique se o Account ID está correto: `da53541a35783da7ffb5ba2d8f15035a`
4. Tente criar um NOVO token do zero

---

## 💡 Lembre-se:

**O sistema funciona PERFEITAMENTE sem R2!**

Se não quiser configurar o R2 agora, pode usar apenas armazenamento local.
O R2 é apenas um recurso adicional para backup na nuvem.