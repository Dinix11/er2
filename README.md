# Sistema de Recebimento, Aviso e Entrega de Encomendas (Cloudflare R2)

Sistema completo para condomínios gerenciar o fluxo de encomendas no setor de entregas.
**Versão com Cloudflare R2** - Armazenamento de imagens otimizado com limite de 10GB.

## Funcionalidades

- **Recebimento pela atendente**:
  - Selecionar unidade
  - Inserir descrição
  - Anexar **foto obrigatória** da encomenda
  - Geração automática de **código único** (6 caracteres alfanuméricos)
  - **Compactação automática de imagens** (otimização para economizar espaço)

- **Aviso automático**:
  - Gera link direto para WhatsApp (wa.me)
  - Envia mensagem com:
    - Unidade e descrição
    - **Código de retirada** em destaque
    - Instruções claras

- **Entrega / Baixa**:
  - Morador informa o código à atendente
  - Atendente digita o código no sistema
  - Sistema localiza a encomenda, exibe foto e detalhes
  - Confirmação = baixa registrada
  - O código funciona como **assinatura digital de recebimento**

- **Gerenciamento de Armazenamento**:
  - **Limite de 10GB** no Cloudflare R2
  - **Compactação automática** de imagens (qualidade 75%, max 1920px)
  - **Limpeza automática** aos 80% (libera os 20% mais antigos)
  - Fallback para armazenamento local se R2 não estiver configurado

- **Outros**:
  - Histórico completo com filtros
  - Gerenciamento de unidades e telefones
  - Reenvio de notificação WhatsApp a qualquer momento
  - Interface simples, responsiva e otimizada para setor de entregas

## Como Executar

### No mesmo computador (desenvolvimento)

1. Instale o Python 3.12 ou superior em [https://python.org](https://python.org) marcando a opção **"Add python.exe to PATH"**.

2. Abra o PowerShell ou Prompt de Comando dentro da pasta do projeto.

3. Execute o script pronto:
   ```powershell
   python app.py
   ```

### Configuração do Cloudflare R2 (Opcional mas Recomendado)

1. **Crie uma conta no Cloudflare** (gratuita):
   - Acesse https://dash.cloudflare.com
   - Crie sua conta gratuita

2. **Configure o R2**:
   - No painel, vá em **R2** > **Overview**
   - Anote seu **Account ID**
   - Clique em **"Manage R2 API Tokens"**
   - Crie um token com permissões de **Read** e **Write**
   - Anote o **Access Key ID** e **Secret Access Key**

3. **Crie um bucket**:
   - No R2, clique em **"Create bucket"**
   - Nome: `encomendas-fotos` (ou outro nome de sua preferência)
   - Escolha a localização mais próxima

4. **Configure as variáveis de ambiente**:
   - Copie o arquivo `.env.example` para `.env`
   - Preencha com suas credenciais:
     ```env
     R2_ACCOUNT_ID=seu-account-id
     R2_ACCESS_KEY_ID=seu-access-key-id
     R2_SECRET_ACCESS_KEY=seu-secret-access-key
     R2_BUCKET_NAME=encomendas-fotos
     ```

5. **Instale as dependências**:
   ```powershell
   pip install -r requirements.txt
   ```

6. **Execute o sistema**:
   ```powershell
   python app.py
   ```

### Como rodar em outro computador

1. **Copie os arquivos**
   - Compacte a pasta inteira `Encomendas-Mirantes-R2` em um arquivo `.zip`
   - **Importante**: Exclua a pasta `venv` antes de zipar
   - Copie o zip para o outro computador

2. **No outro computador**:
   - Descompacte o arquivo
   - Instale o Python 3.12 ou 3.13 (marque "Add to PATH")
   - Instale as dependências: `pip install -r requirements.txt`
   - (Opcional) Configure o `.env` com credenciais do R2
   - Execute: `python app.py`

3. Acesse: **http://127.0.0.1:5000**

### Acessando de outros computadores da rede (condomínio)

1. No computador que está rodando o programa, abra o CMD e digite:
   ```cmd
   ipconfig
   ```
   Anote o endereço **IPv4 Address** (ex: 192.168.1.105)

2. Em outro computador da mesma rede Wi-Fi, acesse:
   ```
   http://192.168.1.105:5000
   ```

## Fluxo de Uso (Passo a Passo)

### Receber uma encomenda
1. No painel principal, preencha:
   - Unidade
   - Descrição (opcional)
   - Foto do pacote (será compactada automaticamente)
2. Clique em **Registrar Encomenda + Enviar Aviso**
3. O sistema gera o código e mostra o botão para **Abrir WhatsApp**
4. Clique no botão para enviar a mensagem com o código para o morador

### Entregar a encomenda
1. O morador chega e informa o código
2. Na seção "Entregar Encomenda", digite o código e clique em **Confirmar Entrega**
3. Ou clique em "Verificar Código" primeiro para ver os detalhes e foto
4. Confirme. A encomenda é dada como **entregue** e o código fica registrado como assinatura

### Reenviar aviso
- Na lista de pendentes, clique em **Reenviar WhatsApp**

### Gerenciar unidades
- Acesse o menu **Unidades**
- Cadastre novas unidades com telefone (formato: 5511987654321)
- Edite ou remova unidades

### Importar lista de contatos do WhatsApp
- Vá em **Unidades** → **Importar do WhatsApp / CSV**
- Envie um arquivo CSV ou cole a lista de contatos
- O sistema extrai automaticamente nome, bloco, apartamento e telefone
- Revise e importe com um clique

## Monitoramento do Armazenamento

O sistema monitora automaticamente o espaço do bucket R2:

- **0% - 80%**: Funcionamento normal
- **80% - 100%**: Alerta e limpeza automática dos 20% mais antigos
- **Logs**: Verifique o console para mensagens de status do R2

### Comandos úteis

Ver estatísticas do bucket (adicionar ao código ou criar endpoint):
```python
from cloudflare_r2 import get_bucket_stats
stats = get_bucket_stats()
print(f"Espaço usado: {stats['espaco_usado_gb']:.2f} GB de {stats['espaco_limite_gb']} GB")
```

## Dicas Importantes

- O código só é conhecido pelo morador (recebido via WhatsApp)
- **A atendente NUNCA vê o código** em nenhuma tela do sistema
- Após o cadastro, o código não aparece em flash, histórico, lista de pendentes ou qualquer outra tela
- O morador informa o código verbalmente no momento da retirada
- A foto serve como prova de recebimento
- Use o histórico para consultar tudo que já foi entregue
- **Imagens são compactadas automaticamente** para economizar espaço (qualidade 75%, max 1920px)
- **Sem R2 configurado**: o sistema usa armazenamento local (funciona normalmente, mas dados podem ser perdidos)

## Personalização

- Para mudar o nome do condomínio, edite o arquivo `templates/base.html`
- Para alterar a senha do setor de entregas, configure `ADMIN_PASSWORD` no `.env`
- Para ajustar o limite de armazenamento, altere `STORAGE_LIMIT_GB` no `.env`
- Para alterar o percentual de limpeza, altere `STORAGE_WARNING_THRESHOLD` no `.env`
- Para adicionar autenticação mais robusta, pode ser implementado posteriormente
- Para integração automática com WhatsApp oficial (sem precisar clicar), pode-se integrar com:
  - WhatsApp Business API (Meta)
  - Twilio
  - Evolution API (self-hosted)

## Estrutura de Arquivos

```
Encomendas-Mirantes-R2/
├── app.py                 # Aplicação Flask principal
├── cloudflare_r2.py       # Módulo de integração com Cloudflare R2
├── requirements.txt       # Dependências Python
├── .env.example           # Exemplo de configuração
├── encomendas.db          # Banco de dados SQLite (criado automaticamente)
├── static/
│   └── uploads/           # Fotos das encomendas (fallback local)
├── templates/
│   ├── base.html
│   ├── index.html         # Painel do setor de entregas
│   ├── unidades.html
│   ├── historico.html
│   └── importar.html
└── README.md
```

## Diferenças da Versão com Supabase

| Recurso | Versão Supabase | Versão R2 |
|---------|----------------|-----------|
| Banco de dados | Supabase (PostgreSQL) | SQLite (local) |
| Armazenamento de fotos | Supabase Storage | Cloudflare R2 |
| Limite de armazenamento | 500MB (gratuito) | 10GB (gratuito) |
| Compactação de imagens | ❌ | ✅ Automática |
| Limpeza automática | ❌ | ✅ Aos 80% |
| Custo | Gratuito (limitado) | Gratuito (10GB) |
| Dados na nuvem | ✅ | ❌ (local) |

## Solução de Problemas

### Erro de conexão com R2
- Verifique se as credenciais no `.env` estão corretas
- Confira se o bucket existe no painel do R2
- Verifique se o token tem permissões de leitura e escrita

### Imagens não aparecem
- Verifique se o bucket está configurado como público
- Confira se a URL do R2 está correta
- Verifique os logs do console para erros de upload

### Espaço cheio
- O sistema limpa automaticamente os 20% mais antigos aos 80%
- Para limpar manualmente, delete arquivos no painel do R2
- Aumente o limite em `STORAGE_LIMIT_GB` no `.env`

## Licença

Desenvolvido para uso prático em setor de entregas de condomínios.

---

**Versão**: 2.0 (Cloudflare R2)  
**Data**: 2026  
**Desenvolvido para**: UBS Pium / Condomínio Mirantes