# 📤 Como Enviar Código para o GitHub pelo Terminal

## 🎯 Comandos Rápidos:

```bash
# 1. Entre na pasta do projeto
cd ../Encomendas-Mirantes-R2

# 2. Adicione todos os arquivos modificados
git add .

# 3. Faça o commit
git commit -m "Descrição da mudança"

# 4. Envie para o GitHub
git push
```

---

## 📋 Passo a Passo Detalhado:

### PASSO 1: Abrir Terminal no VS Code

1. No VS Code, vá em **Terminal** → **New Terminal**
2. Ou pressione: `` Ctrl + ` `` (crase)

### PASSO 2: Navegar até a pasta do projeto

```bash
cd ../Encomendas-Mirantes-R2
```

### PASSO 3: Verificar status

```bash
git status
```

Você verá os arquivos modificados em vermelho.

### PASSO 4: Adicionar arquivos

```bash
git add .
```

Ou adicione arquivos específicos:
```bash
git add app.py
git add .env
```

### PASSO 5: Fazer commit

```bash
git commit -m "Descrição da sua mudança"
```

Exemplos:
```bash
git commit -m "Fix: Corrigir upload de fotos no R2"
git commit -m "Update: Atualizar credenciais do R2"
git commit -m "Feat: Adicionar nova funcionalidade"
```

### PASSO 6: Enviar para GitHub

```bash
git push
```

---

## 🔄 Comandos Úteis:

### Ver histórico de commits:
```bash
git log --oneline
```

### Ver status atual:
```bash
git status
```

### Ver diferenças:
```bash
git diff
```

### Desfazer mudanças (CUIDADO!):
```bash
git checkout -- arquivo.py
```

---

## ⚠️ Se der erro:

### Erro: "fatal: not a git repository"
```bash
# Inicialize o git:
git init
git remote add origin https://github.com/Dinix11/Encomendas-Mirantes.git
```

### Erro: "Authentication failed"
```bash
# Use token de acesso pessoal:
# 1. Acesse: https://github.com/settings/tokens
# 2. Generate new token
# 3. Use o token como senha
```

### Erro: "Everything up-to-date"
```bash
# Não há mudanças para enviar
# Verifique: git status
```

---

## 🎯 Exemplo Prático:

```bash
# 1. Navegar
cd ../Encomendas-Mirantes-R2

# 2. Verificar mudanças
git status

# 3. Adicionar
git add .

# 4. Commit
git commit -m "Fix: Corrigir problema de templates no Render"

# 5. Enviar
git push
```

---

## 💡 Dica:

Sempre faça `git status` antes de `git add` para ver o que vai ser enviado!

---

## 📝 Comandos que já usamos:

```bash
# Enviar correção de templates:
git add app.py
git commit -m "Fix: Adicionar caminhos explícitos de templates e static para Render"
git push
```

---

**Pronto! Seu código está no GitHub!** 🎉