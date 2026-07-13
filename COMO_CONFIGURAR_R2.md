# Guia Passo a Passo: Configurar Cloudflare R2

Este guia vai te ajudar a configurar o Cloudflare R2 para armazenar as fotos das encomendas.

## 📋 Pré-requisitos

- Conta no Cloudflare (gratuita)
- Python 3.12+ instalado
- Dependências instaladas: `pip install -r requirements.txt`

---

## 🚀 Passo 1: Criar Conta no Cloudflare

1. Acesse: https://dash.cloudflare.com/sign-up
2. Crie uma conta gratuita
3. Confirme seu e-mail

---

## 📦 Passo 2: Criar Bucket R2

1. No painel do Cloudflare, vá em **R2** (menu lateral esquerdo)
2. Clique em **"Create bucket"**
3. Preencha:
   - **Bucket name**: `encomendas-fotos` (ou outro nome de sua preferência)
   - **Location**: Escolha a localização mais próxima (ex: `sfo` para São Francisco)
4. Clique em **"Create bucket"**

✅ Bucket criado com sucesso!

---

## 🔑 Passo 3: Obter Credenciais

1. No menu lateral, vá em **R2** > **Overview**
2. Anote o **Account ID** (ex: `abc123def456...`)

3. Clique em **"Manage R2 API Tokens"**
4. Clique em **"Create API Token"**
5. Preencha:
   - **Token name**: `encomendas-app`
   - **Permissions**: Selecione **"Object Read & Write"**
   - **Bucket**: Selecione o bucket que você criou (`encomendas-fotos`)
6. Clique em **"Create API Token"**

✅ Token criado! Anote as credenciais:
- **Access Key ID** (ex: `abc123...`)
- **Secret Access Key** (ex: `xyz789...`)

⚠️ **IMPORTANTE**: Guarde essas credenciais em local seguro. O Secret Access Key só aparece uma vez!

---

## ⚙️ Passo 4: Configurar Variáveis de Ambiente

1. Na pasta do projeto, copie o arquivo `.env.example` para `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Abra o arquivo `.env` e preencha com suas credenciais:
   ```env
   # Configurações do Flask
   SECRET_KEY=sua-chave-secreta-aqui-mude-em-producao
   ADMIN_PASSWORD=setordentregas123
   PORT=5000
   FLASK_DEBUG=false

   # Cloudflare R2
   R2_ACCOUNT_ID=seu-account-id-aqui
   R2_ACCESS_KEY_ID=seu-access-key-id-aqui
   R2_SECRET_ACCESS_KEY=seu-secret-access-key-aqui
   R2_BUCKET_NAME=encomendas-fotos

   # Limites de armazenamento
   STORAGE_LIMIT_GB=10
   STORAGE_WARNING_THRESHOLD=0.80
   ```

3. Substitua os valores de exemplo pelas suas credenciais reais

---

## 🧪 Passo 5: Testar a Conexão

Execute o script de teste:
```powershell
python test_r2.py
```

Você verá uma saída como esta:
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
   📈 Porcentagem: 0.0%
   ✅ Espaço OK

5. Testando upload de imagem...
   ✅ Upload realizado com sucesso!
   🔗 URL: https://abc123.r2.cloudflarestorage.com/encomendas-fotos/...

6. Limpando arquivo de teste...
   ✅ Arquivo de teste removido

============================================================
✅ TESTE CONCLUÍDO COM SUCESSO!
============================================================
```

✅ Tudo funcionando!

---

## 🎯 Passo 6: Configurar Bucket como Público

Para que as fotos possam ser acessadas via URL:

1. No Cloudflare Dashboard, vá em **R2** > Seu bucket
2. Clique na aba **"Settings"**
3. Em **"Public access"**, clique em **"Enable public access"**
4. Confirme clicando em **"Enable"**

✅ Bucket agora é público!

---

## 🚀 Passo 7: Executar o Sistema

```powershell
python app.py
```

Acesse: **http://127.0.0.1:5000**

---

## 📊 Monitoramento

### Ver estatísticas do bucket

Adicione ao código ou execute no Python:
```python
from cloudflare_r2 import get_bucket_stats

stats = get_bucket_stats()
print(f"Arquivos: {stats['total_arquivos']}")
print(f"Espaço: {stats['espaco_usado_gb']:.2f} GB de {stats['espaco_limite_gb']} GB")
print(f"Uso: {stats['porcentagem_uso']:.1f}%")
```

### Limpeza automática

O sistema limpa automaticamente os 20% mais antigos quando atingir 80% do limite.

Para limpar manualmente:
1. Cloudflare Dashboard > R2 > Seu bucket
2. Selecione os arquivos antigos
3. Clique em **"Delete"**

---

## 🔧 Solução de Problemas

### Erro: "Não foi possível conectar ao R2"
- Verifique se as credenciais no `.env` estão corretas
- Confira se o Account ID está correto
- Verifique se o Access Key ID e Secret estão corretos

### Erro: "Bucket não encontrado"
- Crie o bucket no Cloudflare R2
- Verifique se o nome do bucket no `.env` está correto

### Erro: "Permission denied"
- Verifique se o token tem permissões de **Read & Write**
- Confira se o bucket está configurado como público

### Imagens não aparecem
- Verifique se o bucket está público (Passo 6)
- Confira se a URL está sendo gerada corretamente
- Verifique os logs do console para erros

### Espaço cheio
- O sistema limpa automaticamente aos 80%
- Delete arquivos manualmente no painel R2
- Aumente o limite em `STORAGE_LIMIT_GB` no `.env`

---

## 📝 Checklist de Configuração

- [ ] Conta Cloudflare criada
- [ ] Bucket R2 criado
- [ ] API Token gerado
- [ ] Credenciais anotadas
- [ ] Arquivo `.env` configurado
- [ ] Teste `python test_r2.py` executado com sucesso
- [ ] Bucket configurado como público
- [ ] Sistema executado com `python app.py`

---

## 💡 Dicas

1. **Segurança**: Nunca compartilhe o arquivo `.env` ou suas credenciais
2. **Backup**: Faça backup regular do banco de dados SQLite
3. **Monitoramento**: Verifique o espaço do bucket periodicamente
4. **Performance**: O Cloudflare R2 é rápido e gratuito até 10GB
5. **Fallback**: Se o R2 falhar, o sistema usa armazenamento local automaticamente

---

## 🆘 Suporte

Se tiver problemas:
1. Verifique os logs do console
2. Consulte a documentação oficial: https://developers.cloudflare.com/r2/
3. Verifique se todas as credenciais estão corretas

---

**Pronto!** Seu sistema está configurado e funcionando com Cloudflare R2! 🎉