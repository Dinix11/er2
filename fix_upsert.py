path = r'c:\Users\Diniz\Encomendas-Mirantes\app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '''        file_options = {
            "contentType": getattr(file, "content_type", None) or "image/jpeg",
            "upsert": True,
        }'''

new = '''        file_options = {
            "contentType": getattr(file, "content_type", None) or "image/jpeg",
            "upsert": "true",  # string, não bool — headers HTTP devem ser str/bytes
        }'''

if old not in content:
    print('OLD TEXT NOT FOUND')
    exit(1)

content = content.replace(old, new)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('OK')
