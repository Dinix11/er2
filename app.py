#!/usr/bin/env python3
"""
Sistema de Recebimento, Aviso e Entrega de Encomendas
Condomínio - Setor de Entregas
"""

import os
import sqlite3
import secrets
import string
from datetime import datetime
from urllib.parse import quote
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, session
from functools import wraps
import re
import csv
from io import StringIO
from supabase import create_client, Client
import requests  # para upload se necessário
from dotenv import load_dotenv
load_dotenv()  # carrega variáveis do .env para desenvolvimento local

# Configuração
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
DATABASE = os.path.join(BASE_DIR, 'encomendas.db')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.secret_key = os.environ.get('SECRET_KEY', 'condominio-encomendas-dev-key-2026')

# Senha simples para proteção (configure ADMIN_PASSWORD nas variáveis de ambiente no Render)
# MUDE ESSA SENHA! Nunca use o valor padrão em produção.
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'setordentregas123')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Proteção por senha simples
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def require_login():
    # Permite acesso a login, logout e arquivos estáticos sem autenticação
    if request.endpoint in ('login', 'logout') or (request.endpoint and request.endpoint.startswith('static')):
        return None
    if not session.get('logged_in'):
        return redirect(url_for('login'))

# Supabase (nuvem gratuita)
supabase: Client = None

def get_supabase() -> Client | None:
    global supabase
    if supabase is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if url and key:
            supabase = create_client(url, key)
        else:
            print("Usando SQLite local (Supabase não configurado)")
    return supabase


def _row_to_dict(row):
    """Convert sqlite3.Row or Supabase dict to regular dict"""
    if row is None:
        return None
    if isinstance(row, dict):
        return row
    try:
        return dict(row)
    except:
        return row


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    # Tabela de unidades
    c.execute('''
        CREATE TABLE IF NOT EXISTS unidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT NOT NULL UNIQUE,
            telefone TEXT NOT NULL,
            nome_residente TEXT,
            bloco TEXT,
            criado_em TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabela de encomendas
    # Nota: codigo NÃO é UNIQUE para permitir múltiplas encomendas com o mesmo código de lote
    c.execute('''
        CREATE TABLE IF NOT EXISTS encomendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unidade_id INTEGER NOT NULL,
            data_recebimento TEXT NOT NULL,
            descricao TEXT,
            foto_path TEXT,
            codigo TEXT NOT NULL,
            status TEXT DEFAULT 'pendente',
            data_entrega TEXT,
            entregue_por TEXT,
            FOREIGN KEY (unidade_id) REFERENCES unidades (id)
        )
    ''')

    # Tabela simples de log de notificações (auditoria)
    c.execute('''
        CREATE TABLE IF NOT EXISTS notificacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            encomenda_id INTEGER,
            telefone TEXT,
            mensagem TEXT,
            link_whatsapp TEXT,
            enviado_em TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (encomenda_id) REFERENCES encomendas (id)
        )
    ''')

    conn.commit()

    # Migração: remover UNIQUE do campo codigo (para suportar lotes com código único)
    try:
        # Verifica se existe constraint unique no schema
        schema = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='encomendas'").fetchone()
        if schema and 'UNIQUE' in (schema[0] or '').upper():
            c.execute('''
                CREATE TABLE IF NOT EXISTS encomendas_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    unidade_id INTEGER NOT NULL,
                    data_recebimento TEXT NOT NULL,
                    descricao TEXT,
                    foto_path TEXT,
                    codigo TEXT NOT NULL,
                    status TEXT DEFAULT 'pendente',
                    data_entrega TEXT,
                    entregue_por TEXT,
                    FOREIGN KEY (unidade_id) REFERENCES unidades (id)
                )
            ''')
            c.execute('''
                INSERT INTO encomendas_new (id, unidade_id, data_recebimento, descricao, foto_path, codigo, status, data_entrega, entregue_por)
                SELECT id, unidade_id, data_recebimento, descricao, foto_path, codigo, status, data_entrega, entregue_por FROM encomendas
            ''')
            c.execute("DROP TABLE encomendas")
            c.execute("ALTER TABLE encomendas_new RENAME TO encomendas")
            print("Migração: removida restrição UNIQUE do código para suportar lotes.")
    except Exception as e:
        print("Aviso na migração do código:", e)

    # Seed inicial de unidades (se vazio)
    c.execute("SELECT COUNT(*) FROM unidades")
    if c.fetchone()[0] == 0:
        unidades_seed = [
            ("101", "5511987654321", "João Silva", "Bloco A"),
            ("102", "5511987654322", "Maria Souza", "Bloco A"),
            ("201", "5511976543210", "Carlos Pereira", "Bloco B"),
            ("202", "5511991234567", "Ana Costa", "Bloco B"),
            ("301", "5511965432109", "Pedro Oliveira", "Bloco C"),
        ]
        c.executemany(
            "INSERT INTO unidades (numero, telefone, nome_residente, bloco) VALUES (?, ?, ?, ?)",
            unidades_seed
        )
        conn.commit()
        print("Unidades iniciais cadastradas.")

    conn.close()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def gerar_codigo(tamanho=6):
    """Gera código alfanumérico único e fácil de falar"""
    alfabeto = string.ascii_uppercase + string.digits
    for _ in range(20):  # tenta até 20 vezes
        codigo = ''.join(secrets.choice(alfabeto) for _ in range(tamanho))
        conn = get_db()
        existe = conn.execute("SELECT 1 FROM encomendas WHERE codigo = ?", (codigo,)).fetchone()
        conn.close()
        if not existe:
            return codigo
    # fallback bem improvável
    return secrets.token_hex(4).upper()


def limpar_telefone(tel):
    """Remove tudo que não é dígito e garante prefixo Brasil"""
    digits = ''.join(filter(str.isdigit, tel or ''))
    if not digits:
        return ''
    if digits.startswith('0'):
        digits = digits[1:]
    if not digits.startswith('55'):
        digits = '55' + digits
    return digits


def parse_contato_linha(linha):
    """Extrai nome, bloco, número e telefone de uma linha de contato (WhatsApp ou lista)"""
    if not linha or not linha.strip():
        return None
    original = linha.strip()

    # 1. Procurar telefone de forma mais inteligente
    telefone = ''
    # Encontra sequências de dígitos que parecem telefones (com ou sem separadores)
    # Prioriza números com 11 dígitos (DDD + 9 dígitos)
    candidates = re.findall(r'\b(?:\+?55)?\s*[\(\-]?(\d{2})\s*[\)\-]?[\s\-]?(\d{4,5})[\s\-]?(\d{4})\b', original)
    if candidates:
        for ddd, meio, fim in candidates:
            full = ddd + meio + fim
            if 10 <= len(full) <= 13:
                telefone = limpar_telefone(full)
                break
    if not telefone:
        # Fallback: maior sequência pura de dígitos entre 8 e 13
        all_digits = re.findall(r'\d{8,13}', original)
        if all_digits:
            best = max(all_digits, key=lambda x: (10 <= len(x) <= 13, len(x)))
            telefone = limpar_telefone(best)

    # 2. Remover telefone da linha para análise
    linha_sem_tel = re.sub(r'[\+]?[\d\s\(\)\-\.]{8,}', '', original).strip(' -:,;|\t')

    # 3. Bloco
    bloco = ''
    m_bloco = re.search(r'(?i)(?:bloco|bl\.?|bl)\s*[:\-]?\s*([A-Za-z])', linha_sem_tel)
    if m_bloco:
        bloco = m_bloco.group(1).upper()

    # 4. Número do apartamento
    numero = ''
    m_num = re.search(r'(?i)(?:apto|apt\.?|apartamento|ap\.?|unidade|unid\.?)\s*[:\-]?\s*([A-Za-z]?\d{1,4}[A-Za-z]?)', linha_sem_tel)
    if m_num:
        numero = m_num.group(1).strip()
    else:
        nums = re.findall(r'\b([A-Z]?\d{2,4}[A-Z]?)\b', linha_sem_tel)
        for n in nums:
            if not re.match(r'20\d{2}', n):
                numero = n
                break
        if not numero and nums:
            numero = nums[-1]

    # Se temos bloco e um número logo após ele na linha original, usar como apartamento
    if bloco and not numero:
        m_after_bloco = re.search(r'(?i)(?:bloco|bl\.?|bl)\s*' + re.escape(bloco) + r'\s*([A-Z]?\d{1,4}[A-Z]?)', original)
        if m_after_bloco:
            numero = m_after_bloco.group(1)

    # 5. Nome
    nome = linha_sem_tel
    nome = re.sub(r'(?i)(bloco|bl\.?|bl|apto|apt\.?|apartamento|ap\.?|unidade|unid\.?)\s*[:\-]?\s*[A-Za-z]?\d{0,4}[A-Za-z]?', '', nome)
    nome = re.sub(r'\s+', ' ', nome).strip(' -:,|;')

    if not nome or len(nome) < 2:
        parts = re.split(r'[-–—|;\t,]', original)
        nome = parts[0].strip()

    return {
        'nome': nome[:80].strip(),
        'bloco': bloco,
        'numero': numero,
        'telefone': telefone
    }


def processar_lista_contatos(file_storage=None, texto=''):
    """Processa arquivo CSV/TXT ou texto colado e retorna lista de contatos"""
    contatos = []

    if file_storage and file_storage.filename:
        filename = file_storage.filename.lower()
        try:
            raw = file_storage.read()
            content = raw.decode('utf-8', errors='ignore')
        except:
            content = ''

        if filename.endswith('.csv'):
            # CSV com cabeçalhos flexíveis
            try:
                reader = csv.DictReader(StringIO(content))
                for row in reader:
                    nome = (row.get('nome') or row.get('name') or row.get('Nome') or row.get('Name') or
                            row.get('proprietario') or row.get('Proprietário') or '')
                    bloco = (row.get('bloco') or row.get('block') or row.get('Bloco') or '')
                    apt = (row.get('apartamento') or row.get('numero') or row.get('apto') or
                           row.get('apt') or row.get('Apartamento') or row.get('Numero') or
                           row.get('Unidade') or '')
                    tel = (row.get('telefone') or row.get('phone') or row.get('celular') or
                           row.get('Telefone') or row.get('WhatsApp') or row.get('telefone whatsapp') or '')

                    c = {
                        'nome': str(nome).strip(),
                        'bloco': str(bloco).strip(),
                        'numero': str(apt).strip(),
                        'telefone': limpar_telefone(tel)
                    }
                    if c['telefone'] or c['numero']:
                        contatos.append(c)
                return contatos
            except Exception as e:
                print("Erro CSV:", e)

        # Texto simples (linhas)
        linhas = content.splitlines()
    else:
        linhas = texto.splitlines()

    for linha in linhas:
        parsed = parse_contato_linha(linha)
        if parsed and (parsed['telefone'] or parsed['numero']):
            contatos.append(parsed)

    return contatos


def obter_unidade(unidade_id):
    conn = get_db()
    unidade = conn.execute("SELECT * FROM unidades WHERE id = ?", (unidade_id,)).fetchone()
    conn.close()
    return unidade


def registrar_notificacao(encomenda_id, telefone, mensagem, link):
    sb = get_supabase()
    if sb:
        try:
            sb.table("notificacoes").insert({
                "encomenda_id": encomenda_id,
                "telefone": telefone,
                "mensagem": mensagem,
                "link_whatsapp": link
            }).execute()
        except Exception as e:
            print("Erro Supabase notificação:", e)
    else:
        conn = get_db()
        conn.execute(
            "INSERT INTO notificacoes (encomenda_id, telefone, mensagem, link_whatsapp) VALUES (?, ?, ?, ?)",
            (encomenda_id, telefone, mensagem, link)
        )
        conn.commit()
        conn.close()

def upload_foto_supabase(file, filename: str) -> str | None:
    """Upload foto para Supabase Storage e retorna URL pública"""
    sb = get_supabase()
    if not sb:
        return None
    try:
        bucket = "fotos"
        path = f"encomendas/{datetime.now().strftime('%Y%m%d')}/{filename}"
        # Lê o conteúdo
        content = file.read()
        # Upload
        sb.storage.from_(bucket).upload(path, content, {"content-type": file.content_type or "image/jpeg"})
        # URL pública (assumindo bucket público)
        public_url = sb.storage.from_(bucket).get_public_url(path)
        return public_url
    except Exception as e:
        print("Erro upload Supabase:", e)
        return None


def gerar_qr_code(codigo: str) -> str:
    """Gera um QR Code para o código. Tenta Supabase Storage, fallback para gerador público."""
    sb = get_supabase()
    if sb:
        try:
            import qrcode
            from io import BytesIO

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(codigo)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            bucket = "fotos"
            path = f"qrcodes/{codigo}.png"
            content = buffer.getvalue()

            sb.storage.from_(bucket).upload(
                path, 
                content, 
                {"content-type": "image/png", "upsert": True}
            )
            public_url = sb.storage.from_(bucket).get_public_url(path)
            return public_url
        except Exception as e:
            print("Erro ao gerar/upload QR no Supabase:", e)
            # Fallback para gerador público

    # Fallback público (funciona sem Supabase)
    from urllib.parse import quote
    return f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={quote(codigo)}"


@app.route('/')
def index():
    conn = get_db()

    # Estatísticas
    pendentes = conn.execute(
        "SELECT COUNT(*) FROM encomendas WHERE status = 'pendente'"
    ).fetchone()[0]

    entregues_hoje = conn.execute(
        "SELECT COUNT(*) FROM encomendas WHERE status = 'entregue' AND date(data_entrega) = date('now', 'localtime')"
    ).fetchone()[0]

    # Lista de unidades para o formulário
    sb = get_supabase()
    if sb:
        try:
            u_res = sb.table("unidades").select("*").order("bloco").order("numero").execute()
            unidades = u_res.data or []
            p_res = sb.table("encomendas").select("*, unidades!inner(numero, nome_residente, bloco)").eq("status", "pendente").order("data_recebimento", desc=True).execute()
            pendentes_lista = p_res.data or []
            # normalizar
            for p in pendentes_lista:
                u = p.get("unidades", {})
                p["numero"] = u.get("numero")
                p["nome_residente"] = u.get("nome_residente")
                p["bloco"] = u.get("bloco")
                p["foto_path"] = p.get("foto_url") or p.get("foto_path")
        except:
            unidades = []
            pendentes_lista = []
    else:
        unidades = conn.execute(
            "SELECT * FROM unidades ORDER BY bloco, numero"
        ).fetchall()
        pendentes_lista = conn.execute('''
            SELECT e.*, u.numero, u.nome_residente, u.bloco
            FROM encomendas e
            JOIN unidades u ON e.unidade_id = u.id
            WHERE e.status = 'pendente'
            ORDER BY e.data_recebimento DESC
        ''').fetchall()

    # Últimas entregas (para preview)
    ultimas = conn.execute('''
        SELECT e.*, u.numero, u.nome_residente, u.bloco
        FROM encomendas e
        JOIN unidades u ON e.unidade_id = u.id
        WHERE e.status = 'entregue'
        ORDER BY e.data_entrega DESC
        LIMIT 5
    ''').fetchall()

    conn.close()

    return render_template(
        'index.html',
        pendentes=pendentes,
        entregues_hoje=entregues_hoje,
        unidades=unidades,
        pendentes_lista=pendentes_lista,
        ultimas=ultimas
    )


@app.route('/receber', methods=['POST'])
def receber():
    """Recebe encomendas. Suporta lote com 1 código. Usa Supabase (nuvem gratuita) se configurado."""
    sb = get_supabase()
    data_receb = datetime.now().isoformat(sep=' ', timespec='seconds')

    unidades_ids = request.form.getlist('unidade_id')
    descricoes = request.form.getlist('descricao')
    fotos = request.files.getlist('foto')

    if not unidades_ids:
        single_unidade = request.form.get('unidade_id')
        if single_unidade:
            unidades_ids = [single_unidade]
            descricoes = [request.form.get('descricao', '').strip()]
            fotos = [request.files.get('foto')]

    if not unidades_ids or not unidades_ids[0]:
        flash('Selecione pelo menos uma unidade.', 'danger')
        return redirect(url_for('index'))

    codigo = gerar_codigo()

    ids_inseridos = []
    itens_descricao = []
    primeira_unidade = None

    for i, uid in enumerate(unidades_ids):
        if not uid:
            continue

        descricao = descricoes[i].strip() if i < len(descricoes) else ''
        foto = fotos[i] if i < len(fotos) else None

        if not foto or foto.filename == '' or not allowed_file(foto.filename):
            flash(f'Foto obrigatória para a encomenda #{i+1}.', 'danger')
            return redirect(url_for('index'))

        filename = secure_filename(foto.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        safe_name = f"{timestamp}_{i}_{filename}"

        # Foto
        foto_url = None
        if sb:
            foto.seek(0)  # reset
            foto_url = upload_foto_supabase(foto, safe_name)
            if not foto_url:
                # fallback local se falhar
                caminho = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)
                foto.seek(0)
                foto.save(caminho)
                foto_url = f"/foto/{safe_name}"
        else:
            caminho = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)
            foto.save(caminho)
            foto_url = f"/foto/{safe_name}"

        # Inserir
        if sb:
            try:
                res = sb.table("encomendas").insert({
                    "unidade_id": int(uid),
                    "data_recebimento": data_receb,
                    "descricao": descricao,
                    "foto_url": foto_url,
                    "codigo": codigo,
                    "status": "pendente"
                }).execute()
                inserted = res.data[0] if res.data else {}
                ids_inseridos.append(inserted.get("id"))
            except Exception as e:
                print("Erro insert Supabase:", e)
                flash("Erro ao salvar no banco nuvem.", "danger")
                return redirect(url_for('index'))
        else:
            conn = get_db()
            cur = conn.execute('''
                INSERT INTO encomendas (unidade_id, data_recebimento, descricao, foto_path, codigo, status)
                VALUES (?, ?, ?, ?, ?, 'pendente')
            ''', (uid, data_receb, descricao, safe_name if not foto_url.startswith('http') else foto_url, codigo))
            ids_inseridos.append(cur.lastrowid)
            conn.commit()
            conn.close()

        # Info para mensagem
        if sb:
            u_res = sb.table("unidades").select("*").eq("id", uid).execute()
            unidade = u_res.data[0] if u_res.data else None
        else:
            conn = get_db()
            row = conn.execute("SELECT * FROM unidades WHERE id = ?", (uid,)).fetchone()
            conn.close()
            unidade = dict(row) if row else None

        if unidade:
            u_label = f"{unidade.get('bloco') or ''} {unidade.get('numero')}".strip()
            itens_descricao.append({
                'unidade': u_label,
                'nome': unidade.get('nome_residente') or '',
                'descricao': descricao or 'Encomenda',
                'foto_url': foto_url
            })
            if primeira_unidade is None:
                primeira_unidade = unidade

    if not ids_inseridos:
        flash('Nenhuma encomenda válida foi registrada.', 'danger')
        return redirect(url_for('index'))

    # Gera QR Code para o lote (em vez de código textual)
    qr_url = gerar_qr_code(codigo)

    # Notificação WhatsApp
    wa_link = None
    if primeira_unidade:
        tel = primeira_unidade.get('telefone') if isinstance(primeira_unidade, dict) else primeira_unidade['telefone']
        telefone = limpar_telefone(tel)
        unidades_unicas = set(item['unidade'] for item in itens_descricao)
        if len(unidades_unicas) == 1:
            unidade_label = list(unidades_unicas)[0]
            nome = primeira_unidade.get('nome_residente') if isinstance(primeira_unidade, dict) else primeira_unidade['nome_residente']
            intro = f"Olá {nome or ''}!\n\nVocê recebeu as seguintes encomendas no condomínio para a unidade {unidade_label}:"
        else:
            intro = "Olá!\n\nVocê recebeu as seguintes encomendas no condomínio:"

        # Monta descrições
        descricoes_lista = "\n".join(f"• {item['descricao']} (Unidade {item['unidade']})" for item in itens_descricao)

        # Monta links das fotos (somente URLs públicas completas do Supabase)
        fotos_links = []
        for i, item in enumerate(itens_descricao, 1):
            fu = item.get('foto_url')
            if fu and str(fu).startswith('http'):
                fotos_links.append(f"Foto {i}: {fu}")

        qr_text = qr_url or "QR Code disponível no sistema"

        fotos_part = ""
        if fotos_links:
            fotos_part = "\n\nFotos do(s) pacote(s):\n" + "\n".join(fotos_links)

        msg = (
            f"{intro}\n\n"
            f"{descricoes_lista}"
            f"{fotos_part}\n\n"
            f"Recebido em: {data_receb[:16]}\n\n"
            f"🔐 Escaneie o QR Code abaixo para retirar suas encomendas no setor de entregas:\n{qr_text}\n\n"
            f"Toque nos links para abrir as fotos e o QR Code."
        )
        wa_link = f"https://wa.me/{telefone}?text={quote(msg)}"
        registrar_notificacao(ids_inseridos[0], telefone, msg, wa_link)

    qtd = len(ids_inseridos)
    msg_flash = f'{qtd} encomendas registradas com sucesso! O QR Code foi enviado ao morador via WhatsApp.'
    flash(msg_flash, 'success')

    return redirect(url_for('index', wa_link=wa_link))


@app.route('/entregar', methods=['POST'])
def entregar():
    codigo = request.form.get('codigo', '').strip().upper()

    if not codigo:
        flash('Informe o código de retirada.', 'danger')
        return redirect(url_for('index'))

    sb = get_supabase()
    data_entrega = datetime.now().isoformat(sep=' ', timespec='seconds')

    if sb:
        try:
            # Buscar pendentes
            res = sb.table("encomendas").select("*, unidades!inner(numero, bloco)").eq("codigo", codigo).eq("status", "pendente").execute()
            pendentes = res.data or []
            if not pendentes:
                flash('Código inválido ou encomenda já foi entregue.', 'danger')
                return redirect(url_for('index'))

            # Atualizar todas
            sb.table("encomendas").update({
                "status": "entregue",
                "data_entrega": data_entrega,
                "entregue_por": "Setor de Entregas"
            }).eq("codigo", codigo).eq("status", "pendente").execute()

            qtd = len(pendentes)
            u = pendentes[0].get("unidades", {})
            unidade_label = f"{u.get('bloco') or ''} {u.get('numero')}".strip()

            if qtd == 1:
                flash(f'Encomenda entregue com sucesso para a unidade {unidade_label}! O código informado foi registrado como assinatura.', 'success')
            else:
                flash(f'{qtd} encomendas entregues com sucesso (lote) para a unidade {unidade_label}!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            print("Erro Supabase entregar:", e)
            flash('Erro ao dar baixa no banco nuvem.', 'danger')
            return redirect(url_for('index'))
    else:
        # SQLite fallback
        conn = get_db()
        pendentes = conn.execute('''
            SELECT e.*, u.numero, u.nome_residente, u.bloco
            FROM encomendas e
            JOIN unidades u ON e.unidade_id = u.id
            WHERE e.codigo = ? AND e.status = 'pendente'
        ''', (codigo,)).fetchall()

        if not pendentes:
            conn.close()
            flash('Código inválido ou encomenda já foi entregue.', 'danger')
            return redirect(url_for('index'))

        conn.execute('''
            UPDATE encomendas 
            SET status = 'entregue', data_entrega = ?, entregue_por = ?
            WHERE codigo = ? AND status = 'pendente'
        ''', (data_entrega, 'Setor de Entregas', codigo))
        conn.commit()

        qtd = len(pendentes)
        unidade_label = f"{pendentes[0]['bloco'] or ''} {pendentes[0]['numero']}".strip()
        conn.close()

        if qtd == 1:
            flash(f'Encomenda entregue com sucesso para a unidade {unidade_label}! O código informado foi registrado como assinatura.', 'success')
        else:
            flash(f'{qtd} encomendas entregues com sucesso para a unidade {unidade_label}!', 'success')
        return redirect(url_for('index'))


@app.route('/verificar_codigo')
def verificar_codigo():
    """AJAX: Verifica um código e retorna as encomendas (Supabase ou local)"""
    codigo = request.args.get('codigo', '').strip().upper()
    if not codigo:
        return jsonify({'valido': False})

    sb = get_supabase()
    if sb:
        try:
            res = sb.table("encomendas").select("*, unidades!inner(numero, nome_residente, bloco)").eq("codigo", codigo).eq("status", "pendente").order("id").execute()
            rows = res.data or []
        except Exception as e:
            print("Erro Supabase verificar:", e)
            rows = []
    else:
        conn = get_db()
        rows = conn.execute('''
            SELECT e.*, u.numero, u.nome_residente, u.bloco
            FROM encomendas e
            JOIN unidades u ON e.unidade_id = u.id
            WHERE e.codigo = ? AND e.status = 'pendente'
            ORDER BY e.id
        ''', (codigo,)).fetchall()
        conn.close()
        rows = [dict(r) for r in rows] if rows else []

    if not rows:
        return jsonify({'valido': False})

    itens = []
    for enc in rows:
        u = enc.get('unidades', {}) if isinstance(enc.get('unidades'), dict) else enc
        unidade_label = f"{u.get('bloco') or ''} {u.get('numero')}".strip()
        foto = enc.get('foto_url') or enc.get('foto_path') or ''
        itens.append({
            'id': enc.get('id'),
            'unidade': unidade_label,
            'nome': u.get('nome_residente') or enc.get('nome_residente'),
            'descricao': enc.get('descricao') or 'Sem descrição',
            'data_recebimento': str(enc.get('data_recebimento', ''))[:16],
            'foto': foto
        })

    primeiro = itens[0]
    return jsonify({
        'valido': True,
        'quantidade': len(itens),
        'itens': itens,
        'id': primeiro['id'],
        'unidade': primeiro['unidade'],
        'nome': primeiro['nome'],
        'descricao': primeiro['descricao'],
        'data_recebimento': primeiro['data_recebimento'],
        'foto': primeiro['foto']
    })


@app.route('/unidades')
def unidades():
    sb = get_supabase()
    if sb:
        try:
            u_res = sb.table("unidades").select("*").order("bloco").order("numero").execute()
            lista = u_res.data or []

            p_res = sb.table("encomendas").select("unidade_id").eq("status", "pendente").execute()
            pend_counts = {}
            for p in (p_res.data or []):
                uid = p["unidade_id"]
                pend_counts[uid] = pend_counts.get(uid, 0) + 1
        except Exception as e:
            print("Erro Supabase unidades:", e)
            lista = []
            pend_counts = {}
    else:
        conn = get_db()
        lista = conn.execute("SELECT * FROM unidades ORDER BY bloco, numero").fetchall()
        pendentes = conn.execute('''
            SELECT unidade_id, COUNT(*) as qtd
            FROM encomendas
            WHERE status = 'pendente'
            GROUP BY unidade_id
        ''').fetchall()
        pend_counts = {p['unidade_id']: p['qtd'] for p in pendentes}
        conn.close()

    return render_template('unidades.html', unidades=lista, pend_map=pend_counts)


@app.route('/unidades/adicionar', methods=['POST'])
def adicionar_unidade():
    numero = request.form.get('numero', '').strip()
    telefone = request.form.get('telefone', '').strip()
    nome = request.form.get('nome_residente', '').strip()
    bloco = request.form.get('bloco', '').strip() or None

    if not numero or not telefone:
        flash('Número da unidade e telefone são obrigatórios.', 'danger')
        return redirect(url_for('unidades'))

    sb = get_supabase()
    if sb:
        try:
            sb.table("unidades").insert({
                "numero": numero,
                "telefone": telefone,
                "nome_residente": nome or None,
                "bloco": bloco
            }).execute()
            flash('Unidade cadastrada com sucesso!', 'success')
        except Exception as e:
            print("Erro Supabase add unidade:", e)
            flash('Já existe uma unidade com esse número ou erro no banco nuvem.', 'danger')
    else:
        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO unidades (numero, telefone, nome_residente, bloco) VALUES (?, ?, ?, ?)",
                (numero, telefone, nome or None, bloco)
            )
            conn.commit()
            flash('Unidade cadastrada com sucesso!', 'success')
        except sqlite3.IntegrityError:
            flash('Já existe uma unidade com esse número.', 'danger')
        finally:
            conn.close()

    return redirect(url_for('unidades'))


@app.route('/unidades/editar/<int:unidade_id>', methods=['POST'])
def editar_unidade(unidade_id):
    numero = request.form.get('numero', '').strip()
    telefone = request.form.get('telefone', '').strip()
    nome = request.form.get('nome_residente', '').strip()
    bloco = request.form.get('bloco', '').strip() or None

    if not numero or not telefone:
        flash('Número da unidade e telefone são obrigatórios.', 'danger')
        return redirect(url_for('unidades'))

    conn = get_db()
    conn.execute('''
        UPDATE unidades SET numero=?, telefone=?, nome_residente=?, bloco=?
        WHERE id=?
    ''', (numero, telefone, nome or None, bloco, unidade_id))
    conn.commit()
    conn.close()

    flash('Unidade atualizada!', 'success')
    return redirect(url_for('unidades'))


@app.route('/unidades/excluir/<int:unidade_id>', methods=['POST'])
def excluir_unidade(unidade_id):
    conn = get_db()
    # Só exclui se não tiver encomendas
    tem = conn.execute(
        "SELECT COUNT(*) FROM encomendas WHERE unidade_id = ?", (unidade_id,)
    ).fetchone()[0]

    if tem > 0:
        flash('Não é possível excluir: existem encomendas vinculadas a esta unidade.', 'danger')
    else:
        conn.execute("DELETE FROM unidades WHERE id = ?", (unidade_id,))
        conn.commit()
        flash('Unidade removida.', 'success')

    conn.close()
    return redirect(url_for('unidades'))


@app.route('/unidades/importar', methods=['GET', 'POST'])
def importar_unidades():
    """Importa unidades a partir de lista de contatos (CSV, TXT ou texto colado do WhatsApp)"""
    preview = []

    if request.method == 'POST':
        arquivo = request.files.get('arquivo')
        texto_colado = request.form.get('texto', '').strip()
        acao = request.form.get('acao', 'preview')

        if acao == 'preview':
            if arquivo and arquivo.filename:
                preview = processar_lista_contatos(file_storage=arquivo)
            elif texto_colado:
                preview = processar_lista_contatos(texto=texto_colado)

            if not preview:
                flash('Nenhum contato válido encontrado. Verifique o arquivo ou o texto colado.', 'warning')
            return render_template('importar.html', preview=preview)

        elif acao == 'importar':
            # Importar os itens selecionados (vêm do formulário da preview)
            indices = request.form.getlist('indices')
            imported = 0
            updated = 0
            skipped = 0

            conn = get_db()
            for i in indices:
                nome = request.form.get(f'nome_{i}', '').strip()
                bloco = request.form.get(f'bloco_{i}', '').strip() or None
                numero = request.form.get(f'numero_{i}', '').strip()
                telefone = limpar_telefone(request.form.get(f'telefone_{i}', ''))

                if not numero or not telefone:
                    skipped += 1
                    continue

                try:
                    existente = conn.execute(
                        "SELECT id FROM unidades WHERE numero = ?",
                        (numero,)
                    ).fetchone()

                    if existente:
                        conn.execute('''
                            UPDATE unidades 
                            SET nome_residente = ?, bloco = ?, telefone = ?
                            WHERE id = ?
                        ''', (nome or None, bloco, telefone, existente['id']))
                        updated += 1
                    else:
                        conn.execute('''
                            INSERT INTO unidades (numero, telefone, nome_residente, bloco)
                            VALUES (?, ?, ?, ?)
                        ''', (numero, telefone, nome or None, bloco))
                        imported += 1
                except sqlite3.IntegrityError:
                    skipped += 1

            conn.commit()
            conn.close()

            msg = f'{imported} unidades novas importadas'
            if updated:
                msg += f', {updated} atualizadas'
            if skipped:
                msg += f', {skipped} ignoradas'
            flash(msg + '.', 'success')
            return redirect(url_for('unidades'))

    return render_template('importar.html', preview=preview)


@app.route('/historico')
def historico():
    conn = get_db()
    filtro = request.args.get('filtro', '').strip()
    status = request.args.get('status', 'todas')

    query = '''
        SELECT e.*, u.numero, u.nome_residente, u.bloco
        FROM encomendas e
        JOIN unidades u ON e.unidade_id = u.id
    '''
    params = []

    where = []
    if filtro:
        where.append("(u.numero LIKE ? OR u.nome_residente LIKE ? OR e.descricao LIKE ?)")
        params.extend([f'%{filtro}%'] * 3)

    if status == 'pendente':
        where.append("e.status = 'pendente'")
    elif status == 'entregue':
        where.append("e.status = 'entregue'")

    if where:
        query += " WHERE " + " AND ".join(where)

    query += " ORDER BY e.data_recebimento DESC"

    encomendas = conn.execute(query, params).fetchall()
    conn.close()

    return render_template('historico.html', encomendas=encomendas, filtro=filtro, status=status)


@app.route('/foto/<path:filename>')
def foto(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/reenviar/<int:encomenda_id>')
def reenviar(encomenda_id):
    """Gera novamente o link do WhatsApp para reenvio"""
    sb = get_supabase()
    if sb:
        try:
            res = sb.table("encomendas").select("*, unidades!inner(numero, nome_residente, bloco, telefone)").eq("id", encomenda_id).execute()
            row = res.data[0] if res.data else None
        except Exception as e:
            print("Erro Supabase reenviar:", e)
            row = None
    else:
        conn = get_db()
        row = conn.execute('''
            SELECT e.*, u.numero, u.nome_residente, u.bloco, u.telefone
            FROM encomendas e
            JOIN unidades u ON e.unidade_id = u.id
            WHERE e.id = ?
        ''', (encomenda_id,)).fetchone()
        conn.close()
        if row:
            row = dict(row)

    if not row:
        flash('Encomenda não encontrada.', 'danger')
        return redirect(url_for('index'))

    row = _row_to_dict(row)
    if row is None:
        row = {}

    telefone = limpar_telefone(row.get('telefone') or (row.get('unidades') or {}).get('telefone'))
    u = row.get('unidades') or row
    unidade_label = f"{u.get('bloco') or ''} {u.get('numero')}".strip()
    nome = u.get('nome_residente') or row.get('nome_residente') or ''

    msg = (
        f"Olá {nome}!\n\n"
        f"Você tem uma encomenda pendente no condomínio.\n"
        f"Unidade: {unidade_label}\n"
        f"Descrição: {row.get('descricao') or 'Encomenda'}\n"
        f"Recebido em: {str(row.get('data_recebimento', ''))[:16]}\n"
    )
    foto = row.get('foto_url') or row.get('foto_path')
    if not foto and isinstance(row.get('unidades'), dict):
        foto = row.get('unidades').get('foto_url') or row.get('unidades').get('foto_path')  # unlikely
    if foto and str(foto).startswith('http'):
        msg += f"Foto: {foto}\n"
    qr = gerar_qr_code(row.get('codigo'))
    msg += (
        f"\n🔐 Escaneie este QR Code para retirar sua encomenda:\n{qr or 'QR indisponível'}\n\n"
        f"Apresente o QR Code no setor de entregas para retirar."
    )

    wa_link = f"https://wa.me/{telefone}?text={quote(msg)}"
    flash('Link gerado para reenvio.', 'info')
    return redirect(url_for('index', wa_link=wa_link, reenviar=1))


@app.route('/api/unidades')
def api_unidades():
    conn = get_db()
    unidades = conn.execute("SELECT id, numero, nome_residente, bloco FROM unidades ORDER BY bloco, numero").fetchall()
    conn.close()
    return jsonify([dict(u) for u in unidades])


# ==================== LOGIN SIMPLES COM SENHA ====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Senha incorreta.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    init_db()
    print("\n" + "="*60)
    print("  SISTEMA DE ENCOMENDAS - CONDOMÍNIO")
    print("  Acesse no navegador: http://127.0.0.1:5000")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
