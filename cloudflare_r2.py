#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de integração com Cloudflare R2
Substitui Supabase por armazenamento R2 com limite de 10GB
"""
import os
import boto3
from botocore.client import Config
from dotenv import load_dotenv
from datetime import datetime
from collections import defaultdict

load_dotenv()

# Configurações do Cloudflare R2
R2_ACCOUNT_ID = os.getenv('R2_ACCOUNT_ID')
R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_BUCKET_NAME = os.getenv('R2_BUCKET_NAME', 'encomendas-fotos')
R2_ENDPOINT_URL = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com" if R2_ACCOUNT_ID else None

# Limites de armazenamento
STORAGE_LIMIT_GB = 10
STORAGE_WARNING_THRESHOLD = 0.80
STORAGE_LIMIT_BYTES = STORAGE_LIMIT_GB * 1024 * 1024 * 1024
STORAGE_WARNING_BYTES = STORAGE_LIMIT_BYTES * STORAGE_WARNING_THRESHOLD

# Cliente S3 para R2
s3_client = None

def get_r2_client():
    """Retorna cliente S3 configurado para R2"""
    global s3_client
    if s3_client is None:
        if not all([R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ENDPOINT_URL]):
            print("⚠️  Cloudflare R2 não configurado. Verifique as variáveis de ambiente.")
            return None
        
        # Cloudflare R2 usa endpoint S3 compatível
        # Região deve ser 'auto' para R2
        s3_client = boto3.client(
            's3',
            endpoint_url=R2_ENDPOINT_URL,
            aws_access_key_id=R2_ACCESS_KEY_ID,
            aws_secret_access_key=R2_SECRET_ACCESS_KEY,
            config=Config(
                signature_version='s3v4',
                s3={'addressing_style': 'path'}  # Usar path-style URLs
            ),
            region_name='auto'
        )
    return s3_client


def upload_foto_r2(file, filename: str) -> str | None:
    """Upload de foto para Cloudflare R2 com compactação"""
    client = get_r2_client()
    if not client:
        return None
    
    try:
        from PIL import Image
        import io
        
        file.seek(0)
        image_data = file.read()
        
        image = Image.open(io.BytesIO(image_data))
        
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        max_size = 1920
        if max(image.size) > max_size:
            ratio = max_size / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        output_buffer = io.BytesIO()
        image.save(output_buffer, format='JPEG', quality=75, optimize=True)
        output_buffer.seek(0)
        
        path = f"encomendas/{datetime.now().strftime('%Y%m%d')}/{filename}"
        
        client.upload_fileobj(
            output_buffer,
            R2_BUCKET_NAME,
            path,
            ExtraArgs={
                'ContentType': 'image/jpeg',
                'ACL': 'public-read'
            }
        )
        
        public_url = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com/{R2_BUCKET_NAME}/{path}"
        
        verificar_espaco_bucket()
        
        return public_url
        
    except Exception as e:
        print(f"[R2] Erro no upload: {repr(e)}")
        import traceback
        traceback.print_exc()
        return None


def verificar_espaco_bucket():
    """Verifica se o bucket está acima de 80% e limpa os 20% mais antigos"""
    try:
        client = get_r2_client()
        if not client:
            return
        
        response = client.list_objects_v2(Bucket=R2_BUCKET_NAME)
        
        if 'Contents' not in response:
            return
        
        objetos = response['Contents']
        total_size = sum(obj['Size'] for obj in objetos)
        
        print(f"[R2] Espaço usado: {total_size / (1024*1024*1024):.2f} GB de {STORAGE_LIMIT_GB} GB")
        
        if total_size > STORAGE_WARNING_BYTES:
            print(f"[R2] ⚠️  Limite de 80% atingido! Iniciando limpeza automática...")
            
            objetos_ordenados = sorted(objetos, key=lambda x: x['LastModified'])
            
            espaco_para_liberar = total_size * 0.20
            espaco_liberado = 0
            objetos_removidos = 0
            
            for obj in objetos_ordenados:
                if espaco_liberado >= espaco_para_liberar:
                    break
                
                try:
                    client.delete_object(Bucket=R2_BUCKET_NAME, Key=obj['Key'])
                    espaco_liberado += obj['Size']
                    objetos_removidos += 1
                except Exception as e:
                    print(f"[R2] Erro ao remover {obj['Key']}: {e}")
            
            print(f"[R2] ✅ Limpeza concluída: {objetos_removidos} arquivos removidos, {espaco_liberado / (1024*1024):.2f} MB liberados")
            
    except Exception as e:
        print(f"[R2] Erro na verificação de espaço: {repr(e)}")


def get_bucket_stats():
    """Retorna estatísticas do bucket"""
    try:
        client = get_r2_client()
        if not client:
            return None
        
        response = client.list_objects_v2(Bucket=R2_BUCKET_NAME)
        
        if 'Contents' not in response:
            return {
                'total_arquivos': 0,
                'espaco_usado_gb': 0,
                'espaco_limite_gb': STORAGE_LIMIT_GB,
                'porcentagem_uso': 0,
                'alerta': False
            }
        
        objetos = response['Contents']
        total_size = sum(obj['Size'] for obj in objetos)
        porcentagem = (total_size / STORAGE_LIMIT_BYTES) * 100
        
        return {
            'total_arquivos': len(objetos),
            'espaco_usado_gb': total_size / (1024*1024*1024),
            'espaco_limite_gb': STORAGE_LIMIT_GB,
            'porcentagem_uso': porcentagem,
            'alerta': porcentagem >= (STORAGE_WARNING_THRESHOLD * 100)
        }
        
    except Exception as e:
        print(f"[R2] Erro ao obter estatísticas: {repr(e)}")
        return None


def delete_foto_r2(filepath: str) -> bool:
    """Remove uma foto do bucket R2"""
    try:
        client = get_r2_client()
        if not client:
            return False
        
        if filepath.startswith('http'):
            parts = filepath.split(f'/{R2_BUCKET_NAME}/')
            if len(parts) > 1:
                filepath = parts[1]
        
        client.delete_object(Bucket=R2_BUCKET_NAME, Key=filepath)
        return True
    except Exception as e:
        print(f"[R2] Erro ao deletar foto: {repr(e)}")
        return False