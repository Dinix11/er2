import sqlite3

conn = sqlite3.connect('encomendas.db')
cursor = conn.cursor()

print("🔧 Removendo constraint UNIQUE do campo 'numero'...")

# Criar nova tabela sem UNIQUE
cursor.execute('''
    CREATE TABLE IF NOT EXISTS unidades_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero TEXT NOT NULL,
        telefone TEXT NOT NULL,
        nome_residente TEXT,
        bloco TEXT,
        criado_em TEXT DEFAULT CURRENT_TIMESTAMP
    )
''')

# Copiar dados
cursor.execute('''
    INSERT INTO unidades_new (id, numero, telefone, nome_residente, bloco, criado_em)
    SELECT id, numero, telefone, nome_residente, bloco, criado_em FROM unidades
''')

# Deletar tabela antiga
cursor.execute('DROP TABLE unidades')

# Renomear nova tabela
cursor.execute('ALTER TABLE unidades_new RENAME TO unidades')

conn.commit()
conn.close()

print("✅ Constraint UNIQUE removida com sucesso!")
print("   Agora é possível cadastrar unidades com mesmo número em blocos diferentes.")