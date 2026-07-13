import sqlite3

conn = sqlite3.connect('encomendas.db')
cursor = conn.cursor()

# Verificar estrutura da tabela
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='unidades'")
schema = cursor.fetchone()[0]
print("Schema da tabela unidades:")
print(schema)
print()

# Verificar constraints
cursor.execute("PRAGMA table_info(unidades)")
columns = cursor.fetchall()
print("Colunas:")
for col in columns:
    print(f"  {col}")

conn.close()