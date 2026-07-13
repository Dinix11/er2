import re

path = r'c:\Users\Diniz\Encomendas-Mirantes\app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove o filtro problemático no servidor
content = re.sub(
    r'            if filtro:\s+# Supabase doesn.*?query = query\.or_\(.*?\n\s+if status == \'pendente\':',
    '            if status == \'pendente\':',
    content,
    flags=re.DOTALL
)

# Adiciona o filtro client-side após a normalização das fotos
content = content.replace(
    '                else:\n                    e["foto_path"] = None\n        except Exception as ex:',
    '''                else:\n                    e["foto_path"] = None\n\n            # Filtro client-side (Supabase nao faz OR ilike facil em joins)\n            if filtro:\n                f = filtro.lower()\n                encomendas = [\n                    e for e in encomendas\n                    if f in (e.get("descricao") or \'\').lower()\n                    or f in (e.get("numero") or \'\').lower()\n                    or f in (e.get("nome_residente") or \'\').lower()\n                ]\n        except Exception as ex:'''
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('OK')
