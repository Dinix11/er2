# Variáveis de Ambiente para o Render

## Por que precisa configurar?

O arquivo `.env` está no `.gitignore` e não é enviado para o GitHub por segurança. Por isso, você precisa configurar as variáveis de ambiente diretamente no painel do Render.

## Como Configurar no Render:

1. Acesse https://dashboard.render.com
2. Selecione seu serviço (web service)
3. Vá na aba **"Environment"** (ou **"Environment Variables"**)
4. Clique em **"Add Environment Variable"**
5. Adicione cada variável abaixo:

## Variáveis Obrigatórias:

### Flask:
```
SECRET_KEY=sua-chave-secreta-aqui-mude-em-producao
ADMIN_PASSWORD=teste123
PORT=5000
FLASK_DEBUG=false
```

### Cloudflare R2:
```
R2_ACCOUNT_ID=da53541a35783da7ffb5ba2d8f15035a
R2_ACCESS_KEY_ID=3fcae40e98b5dca1a2b0e5a4baa6e636
R2_SECRET_ACCESS_KEY=d81133ed45b1504b87511331cd189d0b194edbcd439dfaf546ca6597cfd0bd7e
R2_BUCKET_NAME=fotos
```

### Storage (opcional - usa padrão se não informar):
```
STORAGE_LIMIT_GB=10
STORAGE_WARNING_THRESHOLD=0.80
```

## Passo a Passo no Render:

### 1. Acesse o Dashboard
- Vá para https://dashboard.render.com
- Faça login

### 2. Selecione o Serviço
- Clique no seu serviço web (ex: "er2" ou "encomendas-mirantes")

### 3. Vá em Environment
- No menu lateral, clique em **"Environment"**
- Ou na aba **"Environment Variables"**

### 4. Adicione as Variáveis
Clique em **"Add Environment Variable"** para cada uma:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | `sua-chave-secreta-aqui-mude-em-producao` |
| `ADMIN_PASSWORD` | `teste123` |
| `PORT` | `5000` |
| `FLASK_DEBUG` | `false` |
| `R2_ACCOUNT_ID` | `da53541a35783da7ffb5ba2d8f15035a` |
| `R2_ACCESS_KEY_ID` | `3fcae40e98b5dca1a2b0e5a4baa6e636` |
| `R2_SECRET_ACCESS_KEY` | `d81133ed45b1504b87511331cd189d0b194edbcd439dfaf546ca6597cfd0bd7e` |
| `R2_BUCKET_NAME` | `fotos` |

### 5. Salve e Reinicie
- Clique em **"Save Changes"** ou **"Update"**
- O Render irá reiniciar o serviço automaticamente

## Verificando se Funcionou:

### 1. Verifique os Logs:
- No Render, vá em **"Logs"**
- Procure por mensagens como:
  ```
  ✅ CLOUDFLARE R2 CONFIGURADO - usando armazenamento na nuvem
  Bucket: X arquivos, X.XX GB de 10 GB
  ```

### 2. Teste o Upload:
- Acesse seu site no Render
- Cadastre uma encomenda com foto
- Verifique se a foto aparece

### 3. Verifique no R2:
- Acesse https://dash.cloudflare.com
- Vá em R2 → bucket "fotos"
- Verifique se a foto aparece na lista de objetos

## Troubleshooting:

### Erro: "Cloudflare R2 não configurado"
- Verifique se todas as variáveis foram adicionadas corretamente
- Verifique se não há espaços extras nos valores
- Verifique se o serviço foi reiniciado após adicionar as variáveis

### Erro: "Bucket não encontrado"
- Verifique se o bucket "fotos" existe no R2
- Verifique se o nome do bucket está correto (case-sensitive)

### Erro: "SignatureDoesNotMatch"
- Verifique se as credenciais estão corretas
- Verifique se o token tem permissão "Object Read & Write"

### Fotos não aparecem no R2
- Verifique se o CORS está configurado no bucket
- Verifique os logs do Render para erros
- Teste localmente primeiro com `python diagnosticar_upload_r2.py`

## ⚠️ Segurança:

- **NUNCA** comite o arquivo `.env` no GitHub
- **NUNCA** compartilhe suas credenciais do R2
- Use senhas fortes para `SECRET_KEY` e `ADMIN_PASSWORD` em produção
- Considere usar domínios específicos no CORS ao invés de `*`

## Dica:

Para testar localmente antes de deployar:
```bash
# Certifique-se que o .env está configurado localmente
python diagnosticar_upload_r2.py

# Se passar, faça o deploy
git push
```

Depois configure as variáveis no Render e teste novamente.