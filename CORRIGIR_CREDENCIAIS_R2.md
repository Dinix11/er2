# ⚠️ CORRIGIR CREDENCIAIS DO R2

## Problema Atual:
```
SignatureDoesNotMatch: The request signature we calculated does not match
```

**Causa**: Credenciais incorretas ou trocadas no `.env`

---

## 🔍 VERIFICAÇÃO IMEDIATA:

### 1. Abra o arquivo `.env` e verifique:

```env
R2_ACCESS_KEY_ID=16b999213d3646c894b83f93142fcedf
R2_SECRET_ACCESS_KEY=47c875bc8da39ea4ff8b2ed7e5cefb70c32b3789deb5cdc7a873421deb507f6
```

### 2. Verifique no Cloudflare:

Acesse: https://dash.cloudflare.com
1. Menu → **R2** → **Manage R2 API Tokens**
2. Clique no token: **R2 Account Token**
3. Verifique as credenciais:

**Access Key ID** (32 caracteres):
```
Deve ser algo como: 16b999213d3646c894b83f93142fcedf
```

**Secret Access Key** (64 caracteres):
```
Deve ser algo como: 47c875bc8da39ea4ff8b2ed7e5cefb70c32b3789deb5cdc7a873421deb507f6
```

---

## ⚠️ POSSÍVEIS ERROS:

### ❌ ERRO 1: Credenciais trocadas
```env
# ERRADO:
R2_ACCESS_KEY_ID=47c875bc8da39ea4ff8b2ed7e5cefb70c32b3789deb5cdc7a873421deb507f6  # 64 chars (errado!)
R2_SECRET_ACCESS_KEY=16b999213d3646c894b83f93142fcedf  # 32 chars (errado!)

# CORRETO:
R2_ACCESS_KEY_ID=16b999213d3646c894b83f93142fcedf  # 32 chars
R2_SECRET_ACCESS_KEY=47c875bc8da39ea4ff8b2ed7e5cefb70c32b3789deb5cdc7a873421deb507f6  # 64 chars
```

### ❌ ERRO 2: Caracteres faltando ou sobrando
- Access Key ID: **exatamente 32 caracteres**
- Secret Access Key: **exatamente 64 caracteres**

### ❌ ERRO 3: Espaços ou quebras de linha
- Verifique se não há espaços antes/depois
- Verifique se não há quebras de linha

---

## ✅ SOLUÇÃO:

### Opção 1: Usar as credenciais originais (se funcionavam antes)

```env
R2_ACCESS_KEY_ID=16b999213d3646c894b83f93142fcedf
R2_SECRET_ACCESS_KEY=47c875bc8da39ea4ff8b2ed7e5cefb70c32b3789deb5cdc7a873421deb507f6
```

### Opção 2: Criar NOVO token (se perdeu as credenciais)

1. **Delete** o token atual no Cloudflare
2. **Crie novo token**:
   - Nome: `Encomendas-Fotos-Token`
   - Permissão: `Object Read & Write`
   - Bucket Access: `Include` > `Encomendas-fotos`
3. **COPIE IMEDIATAMENTE** as novas credenciais
4. **Cole no .env** (cuidado para não trocar!)

---

## 🧪 Teste:

```bash
cd ../Encomendas-Mirantes-R2
python diagnosticar_r2_avancado.py
```

Você deve ver:
```
✅ Upload BEM-SUCEDIDO!
```

---

## 📋 Checklist:

- [ ] Access Key ID tem 32 caracteres?
- [ ] Secret Access Key tem 64 caracteres?
- [ ] Não estão trocadas?
- [ ] Não há espaços extras?
- [ ] Token tem permissão "Object Read & Write"?
- [ ] Token vinculado ao bucket `Encomendas-fotos`?

---

## 💡 DICA:

Se você criou um token novo, use as credenciais do **NOVO token**, não do antigo!

Cada token tem credenciais DIFERENTES.

---

## 🔄 Após corrigir:

```bash
# 1. CTRL+C (parar servidor)
# 2. Reinicie:
python app.py

# 3. Teste:
python diagnosticar_r2_avancado.py
```

---

**Verifique se as credenciais no .env estão EXATAMENTE IGUAIS às do Cloudflare!**