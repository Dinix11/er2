# Guia: Corrigir Permissões do Cloudflare R2

## Problema Atual
O token do R2 está com permissões insuficientes, causando erro:
```
AccessDenied: An error occurred (AccessDenied) when calling the PutObject operation: Access Denied
```

## Solução: Configurar Permissões do Bucket

### Opção 1: Tornar o Bucket Público (Recomendado para este projeto)

1. **Acesse o Cloudflare Dashboard**
   - Vá para https://dash.cloudflare.com
   - Faça login na sua conta

2. **Acesse R2**
   - No menu lateral, clique em **R2**
   - Clique em **Buckets**

3. **Selecione o Bucket**
   - Clique no bucket `Encomendas-fotos`

4. **Configure Permissões**
   - Clique na aba **Settings** (Configurações)
   - Role até encontrar **Public Access** (Acesso Público)
   - Clique em **Enable Public Access** (Habilitar Acesso Público)
   - Confirme a ação

5. **Configure CORS (se necessário)**
   - Na mesma página, role até **CORS**
   - Adicione a seguinte configuração:
   ```
   Allowed Origins: *
   Allowed Methods: GET, PUT, POST, DELETE
   Allowed Headers: *
   Max Age: 3600
   ```

### Opção 2: Criar Novo Token com Permissões Corretas

Se preferir criar um novo token com permissões específicas:

1. **Acesse API Tokens**
   - No Cloudflare Dashboard, vá em **R2** > **Overview**
   - Clique em **Manage R2 API Tokens**
   - Clique em **Create API Token**

2. **Configure o Token**
   - **Token name**: `Encomendas-Fotos-Token`
   - **Permissions**:
     - ✅ **Account** > **Cloudflare R2** > **Edit** (para escrita)
     - ✅ **Account** > **Cloudflare R2** > **Read** (para leitura)
   - **Account Resources**: Select your account
   - Clique em **Create Token**

3. **Copie as Credenciais**
   - ⚠️ **IMPORTANTE**: Copie o **Access Key ID** e **Secret Access Key** imediatamente
   - Você não verá essas credenciais novamente!

4. **Atualize o arquivo .env**
   ```env
   R2_ACCESS_KEY_ID=novo-access-key-id-aqui
   R2_SECRET_ACCESS_KEY=nova-secret-access-key-aqui
   ```

### Opção 3: Usar Apenas Armazenamento Local (Sem R2)

Se não quiser configurar o R2 agora, o sistema já está funcionando com armazenamento local!

Para desabilitar o R2 completamente, comente as credenciais no `.env`:
```env
# R2_ACCOUNT_ID=da53541a35783da7ffb5ba2d8f15035a
# R2_ACCESS_KEY_ID=16b999213d3646c894b83f93142fcedf
# R2_SECRET_ACCESS_KEY=47c875bc8da39ea4ff8b2ed7e5cefb70c32b3789deb5cdc7a873421deb507f6
# R2_BUCKET_NAME=Encomendas-fotos
```

## Verificação

Após configurar, reinicie o aplicativo:

```bash
cd ../Encomendas-Mirantes-R2
python app.py
```

Você deve ver a mensagem:
```
✅ CLOUDFLARE R2 CONFIGURADO - usando armazenamento na nuvem
   Bucket: X arquivos, Y.YY GB de 10 GB
```

## Teste

1. Acesse o sistema em http://192.168.0.3:5000
2. Faça login (senha: `teste123`)
3. Registre uma encomenda com foto
4. Verifique se a foto foi enviada para o R2 (não deve aparecer o aviso de fallback)

## Notas Importantes

- **Armazenamento Local**: Funciona perfeitamente, mas os arquivos ficam apenas no computador local
- **R2 (Nuvem)**: Permite acesso às fotos de qualquer lugar, com backup automático
- **Limite**: O bucket R2 tem limite de 10GB (configurável)
- **Limpeza Automática**: Quando atingir 80% (8GB), o sistema remove automaticamente os 20% mais antigos

## Suporte

Se continuar com problemas:
1. Verifique se o bucket existe no painel R2
2. Confira se o nome do bucket está correto no `.env`
3. Verifique se o token tem permissões de Read e Write
4. Teste com um novo token se necessário