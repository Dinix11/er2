import os
import sqlite3

print('DB exists:', os.path.exists('encomendas.db'))
conn = sqlite3.connect('encomendas.db')
cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]
print('Tables:', tables)

# Check if moradores table exists
if 'moradores' in tables:
    print('✅ Tabela moradores existe')
    cursor = conn.execute("SELECT COUNT(*) FROM moradores")
    count = cursor.fetchone()[0]
    print(f'   Moradores cadastrados: {count}')
else:
    print('❌ Tabela moradores NÃO existe - será criada na inicialização')

conn.close()