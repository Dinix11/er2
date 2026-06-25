# Sistema de Recebimento, Aviso e Entrega de Encomendas

Sistema completo para condomínios gerenciar o fluxo de encomendas no setor de entregas.

## Funcionalidades

- **Recebimento pela atendente**:
  - Selecionar unidade
  - Inserir descrição
  - Anexar **foto obrigatória** da encomenda
  - Geração automática de **código único** (6 caracteres alfanuméricos)

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

   - Duplo clique em `run.bat`, ou
   - No PowerShell:
     ```powershell
     .\run.ps1
     ```

O sistema vai criar o ambiente virtual automaticamente na primeira execução.

### Como rodar em outro computador (muito importante)

Siga estes passos **exatamente**:

1. **Copie os arquivos**
   - Compacte a pasta inteira `condominio-encomendas` em um arquivo `.zip`
   - **Importante**: Exclua a pasta `venv` antes de zipar (ela é específica de cada máquina).
   - Copie o zip para o outro computador (pendrive, rede, Google Drive, etc.).

2. **No outro computador**:
   - Descompacte o arquivo em qualquer lugar (ex: `Documentos` ou `Área de Trabalho`).
   - Instale o Python 3.12 ou 3.13 em [python.org](https://python.org) (marque "Add to PATH").

3. **Execute o programa**:
   - Entre na pasta descompactada.
   - Dê **duplo clique** no arquivo `run.bat`

   Ou manualmente no PowerShell:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python app.py
   ```

4. Abra o navegador e acesse:
   **http://127.0.0.1:5000**

### Acessando de outros computadores da rede (condomínio)

O sistema já está configurado para aceitar conexões da rede.

1. No computador que está rodando o programa, abra o CMD e digite:
   ```cmd
   ipconfig
   ```
   Anote o endereço **IPv4 Address** (ex: 192.168.1.105)

2. Em outro computador da mesma rede Wi-Fi, abra o navegador e acesse:
   ```
   http://192.168.1.105:5000
   ```
   (substitua pelo IP real que você anotou)

**Possível problema de firewall**:
- Se não conseguir acessar, abra o Windows Defender Firewall → "Permitir um app ou recurso".
- Adicione o Python ou libere a porta 5000.

### Executando automaticamente quando o computador ligar

- Crie um atalho do `run.bat` e coloque na pasta de Inicialização do Windows:
  Pressione `Win + R` → digite `shell:startup` → cole o atalho.

## Fluxo de Uso (Passo a Passo)

### Receber uma encomenda
1. No painel principal, preencha:
   - Unidade
   - Descrição (opcional)
   - Foto do pacote
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

## Dicas Importantes

- O código só é conhecido pelo morador (recebido via WhatsApp)
- **A atendente NUNCA vê o código** em nenhuma tela do sistema
- Após o cadastro, o código não aparece em flash, histórico, lista de pendentes ou qualquer outra tela
- O morador informa o código verbalmente no momento da retirada
- A foto serve como prova de recebimento
- Use o histórico para consultar tudo que já foi entregue

## Personalização

- Para mudar o nome do condomínio, edite o arquivo `templates/base.html`
- Para adicionar autenticação simples (senha do setor de entregas), pode ser implementado posteriormente
- Para integração automática com WhatsApp oficial (sem precisar clicar), pode-se integrar com:
  - WhatsApp Business API (Meta)
  - Twilio
  - Evolution API (self-hosted)

## Estrutura de Arquivos

```
condominio-encomendas/
├── app.py                 # Aplicação Flask principal
├── requirements.txt
├── encomendas.db          # Banco de dados SQLite (criado automaticamente)
├── static/
│   └── uploads/           # Fotos das encomendas
├── templates/
│   ├── base.html
│   ├── index.html         # Painel do setor de entregas
│   ├── unidades.html
│   └── historico.html
└── README.md
```

---

Desenvolvido para uso prático em setor de entregas de condomínios.
