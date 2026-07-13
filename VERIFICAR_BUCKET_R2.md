# 🔍 Verificar Bucket no Cloudflare R2

## Problema:
Token tem permissão "Object Read & Write" ✅
Mas ainda recebe: `AccessDenied` ❌

---

## ✅ SOLUÇÃO DIRETA:

### 1. Verifique se o Bucket Existe:

**Acesse**: https://dash.cloudflare.com
1. Menu lateral → **R2**
2. Clique em **Buckets**
3. Verifique se existe: **`Encomendas-fotos`**

⚠️ **ATENÇÃO**: O nome é **case-sensitive**!
- ✅ Correto: `Encomendas-fotos`
- ❌ Errado: `encomendas-fotos` (minúsculas)
- ❌ Errado: `ENCOMENDAS-FOTOS` (maiúsculas)

---

### 2. Se NÃO Existir, Crie:

1. Clique em **"Create bucket"**
2. **Nome**: `Encomendas-fotos` (exatamente assim!)
3. **Location**: Escolha a mais próxima
4. Clique em **"Create bucket"**

---

### 3. Verifique o Token:

1. Vá em **R2** → **Manage R2 API Tokens**
2. Clique no token: **R2 Account Token**
3. Verifique:
   - ✅ Permission: `Object Read & Write`
   - ✅ Applied to: `encomendas-fotos` (ou All buckets)

---

### 4. Verifique o .env:

Abra o arquivo `.env` e confirme:

```env
R2_BUCKET_NAME=Encomendas-fotos
```

⚠️ **DEVE SER EXATAMENTE IGUAL** ao nome do bucket!

---

### 5. Teste:

```bash
cd ../Encomendas-Mirantes-R2
python diagnosticar_r2_avancado.py
```

---

## 🎯 CHECKLIST:

- [ ] Bucket `Encomendas-fotos` existe?
- [ ] Nome no .env é EXATAMENTE `Encomendas-fotos`?
- [ ] Token tem permissão "Object Read & Write"?
- [ ] Token aplicado ao bucket correto?

---

## 💡 DICA:

Se o bucket existe e o nome está correto, tente criar um **NOVO token**:

1. Delete o token atual
2. Crie novo token com permissão "Object Read & Write"
3. Atualize o .env
4. Reinicie: `python app.py`

---

## 🔧 SE AINDA NÃO FUNCIONAR:

Me envie o resultado completo do diagnóstico:

```bash
python diagnosticar_r2_avancado.py
```

Vou identificar o problema exato!