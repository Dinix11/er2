# Configuração de CORS no Cloudflare R2

## Por que configurar CORS?

O CORS (Cross-Origin Resource Sharing) é necessário para permitir que o navegador acesse as fotos armazenadas no R2 diretamente, sem bloqueios de segurança.

## Como Configurar:

### 1. Acesse o Cloudflare Dashboard
- Vá para https://dash.cloudflare.com
- Navegue até **R2** → **Overview**
- Clique no bucket **"encomendas-fotos"**

### 2. Acesse a aba CORS
- No bucket, clique na aba **"CORS"**
- Clique em **"Add CORS rule"**

### 3. Configure a Regra CORS

Preencha os campos com:

**Origins (Origens permitidas):**
```
*
```
Ou para maior segurança, especifique seu domínio:
```
https://seu-dominio.com
https://www.seu-dominio.com
```

**Methods (Métodos permitidos):**
```
GET
HEAD
```

**Allowed Headers (Headers permitidos):**
```
*
```

**Exposed Headers (Headers expostos):**
```
Content-Type
Content-Length
Last-Modified
```

**Max Age (Tempo de cache):**
```
3600
```

### 4. Salve a Configuração
- Clique em **"Save"**

## ⚠️ Segurança

### Opção 1: Permitir todos os domínios (Mais simples)
```
AllowedOrigins: ["*"]
```
- ✅ Fácil de configurar
- ✅ Funciona em qualquer ambiente
- ⚠️ Menos seguro (qualquer site pode acessar suas imagens)

### Opção 2: Domínios específicos (Mais seguro)
```
AllowedOrigins: [
  "https://seu-app.onrender.com",
  "https://seu-dominio.com",
  "http://localhost:5000"
]
```
- ✅ Mais seguro
- ✅ Apenas seus domínios acessam as imagens
- ⚠️ Precisa atualizar quando mudar de domínio

## Testando a Configuração

Após configurar CORS, execute o diagnóstico:

```bash
cd ../Encomendas-Mirantes-R2
python diagnosticar_upload_r2.py
```

O teste de upload deve passar agora.

## Verificando se está funcionando

1. Faça upload de uma encomenda pelo sistema
2. Abra o DevTools do navegador (F12)
3. Vá na aba **Network**
4. Tente visualizar uma foto da encomenda
5. Verifique se não há erros de CORS

## Troubleshooting

### Erro: "No 'Access-Control-Allow-Origin' header"
- Verifique se o CORS está configurado no bucket
- Confira se o Origin está correto

### Erro: "Method GET not allowed"
- Verifique se GET está na lista de Methods permitidos

### Erro: "Preflight request failed"
- Verifique se os Headers estão configurados corretamente
- Tente usar `"*"` em AllowedHeaders para teste

## Nota Importante

O Cloudflare R2 **não** suporta CORS para operações de escrita (PUT, POST, DELETE) via navegador. O upload é feito pelo servidor Python (backend), que não tem restrições de CORS.

O CORS é necessário apenas para **leitura** das imagens (GET) pelo navegador.