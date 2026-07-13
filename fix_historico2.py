path = r'c:\Users\Diniz\Encomendas-Mirantes\app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '''            if filtro:
                # Supabase doesn't do easy OR ilike on joined easily, do client-side filter or broad
                query = query.or_(f"descricao.ilike.%{filtro}%,unidades.numero.ilike.%{filtro}%,unidades.nome_residente.ilike.%{filtro}%")
            if status == 'pendente':
                query = query.eq("status", "pendente")
            elif status == 'entregue':
                query = query.eq("status", "entregue")
            res = query.order("data_recebimento", desc=True).execute()
            encomendas = res.data or []

            # Normalize for template compatibility
            for e in encomendas:
                u = e.get("unidades") or {}
                e["numero"] = u.get("numero")
                e["nome_residente"] = u.get("nome_residente")
                e["bloco"] = u.get("bloco")
                foto_raw = e.get("foto_url") or e.get("foto_path")
                if foto_raw:
                    s = str(foto_raw)
                    if s.startswith(('http://', 'https://')):
                        e["foto_path"] = s
                    elif s.startswith('/foto/'):
                        e["foto_path"] = s[len('/foto/'):]
                    else:
                        e["foto_path"] = s
                else:
                    e["foto_path"] = None
        except Exception as ex:
            print("Erro Supabase no histÃ³rico:", ex)
            encomendas = []'''

new = '''            if status == 'pendente':
                query = query.eq("status", "pendente")
            elif status == 'entregue':
                query = query.eq("status", "entregue")
            res = query.order("data_recebimento", desc=True).execute()
            encomendas = res.data or []

            # Normalize for template compatibility
            for e in encomendas:
                u = e.get("unidades") or {}
                e["numero"] = u.get("numero")
                e["nome_residente"] = u.get("nome_residente")
                e["bloco"] = u.get("bloco")
                foto_raw = e.get("foto_url") or e.get("foto_path")
                if foto_raw:
                    s = str(foto_raw)
                    if s.startswith(('http://', 'https://')):
                        e["foto_path"] = s
                    elif s.startswith('/foto/'):
                        e["foto_path"] = s[len('/foto/'):]
                    else:
                        e["foto_path"] = s
                else:
                    e["foto_path"] = None

            # Filtro client-side (Supabase nao faz OR ilike facil em joins)
            if filtro:
                f = filtro.lower()
                encomendas = [
                    e for e in encomendas
                    if f in (e.get("descricao") or '').lower()
                    or f in (e.get("numero") or '').lower()
                    or f in (e.get("nome_residente") or '').lower()
                ]
        except Exception as ex:
            print("Erro Supabase no histÃ³rico:", ex)
            encomendas = []'''

if old not in content:
    print('OLD TEXT NOT FOUND')
    exit(1)

content = content.replace(old, new)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('OK')
