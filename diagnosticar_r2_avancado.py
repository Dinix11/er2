#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico avançado do R2
"""
import os
from dotenv import load_dotenv
import boto3
from botocore.client import Config

load_dotenv()

print("="*60)
print("DIAGNÓSTICO AVANÇADO DO CLOUDFLARE R2")
print("="*60)

# Mostrar credenciais (parcialmente)
print("\n1. CREDENCIAIS CONFIGURADAS:")
print(f"   R2_ACCOUNT_ID: {os.getenv('R2_ACCOUNT_ID')}")
print(f"   R2_ACCESS_KEY_ID: {os.getenv('R2_ACCESS_KEY_ID')[:10]}...")
print(f"   R2_SECRET_ACCESS_KEY: {os.getenv('R2_SECRET_ACCESS_KEY')[:10]}...")
print(f"   R2_BUCKET_NAME: {os.getenv('R2_BUCKET_NAME')}")
print(f"   R2_ENDPOINT_URL: https://{os.getenv('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com")

# Criar cliente
print("\n2. CRIANDO CLIENTE S3:")
try:
    client = boto3.client(
        's3',
        endpoint_url=f"https://{os.getenv('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com",
        aws_access_key_id=os.getenv('R2_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('R2_SECRET_ACCESS_KEY'),
        config=Config(signature_version='s3v4'),
        region_name='auto'
    )
    print("   ✅ Cliente criado")
except Exception as e:
    print(f"   ❌ Erro ao criar cliente: {e}")
    exit(1)

# Listar buckets
print("\n3. LISTANDO BUCKETS:")
try:
    response = client.list_buckets()
    buckets = [b['Name'] for b in response.get('Buckets', [])]
    print(f"   ✅ Buckets encontrados: {buckets}")
    
    target_bucket = os.getenv('R2_BUCKET_NAME')
    if target_bucket in buckets:
        print(f"   ✅ Bucket '{target_bucket}' EXISTE")
    else:
        print(f"   ❌ Bucket '{target_bucket}' NÃO ENCONTRADO!")
        print(f"   💡 Crie o bucket no Cloudflare Dashboard")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# Testar listagem de objetos no bucket
print(f"\n4. TESTANDO ACESSO AO BUCKET '{os.getenv('R2_BUCKET_NAME')}':")
try:
    response = client.list_objects_v2(Bucket=os.getenv('R2_BUCKET_NAME'))
    count = response.get('KeyCount', 0)
    print(f"   ✅ Bucket acessível")
    print(f"   📊 Objetos no bucket: {count}")
except Exception as e:
    print(f"   ❌ ERRO: {e}")
    print("\n   POSSÍVEIS CAUSAS:")
    print("   1. Bucket não existe")
    print("   2. Nome do bucket incorreto")
    print("   3. Token não tem acesso a este bucket")

# Testar upload
print(f"\n5. TESTANDO UPLOAD NO BUCKET '{os.getenv('R2_BUCKET_NAME')}':")
try:
    import io
    from PIL import Image
    
    # Criar imagem de teste
    test_image = Image.new('RGB', (100, 100), color='red')
    buffer = io.BytesIO()
    test_image.save(buffer, format='JPEG', quality=75)
    buffer.seek(0)
    
    test_path = "teste_diagnostico.jpg"
    
    # Upload
    client.put_object(
        Bucket=os.getenv('R2_BUCKET_NAME'),
        Key=test_path,
        Body=buffer,
        ContentType='image/jpeg',
        ACL='public-read'
    )
    
    print(f"   ✅ Upload BEM-SUCEDIDO!")
    print(f"   📁 Arquivo: {test_path}")
    
    # Verificar se existe
    client.head_object(Bucket=os.getenv('R2_BUCKET_NAME'), Key=test_path)
    print(f"   ✅ Arquivo confirmado no bucket")
    
    # Deletar
    client.delete_object(Bucket=os.getenv('R2_BUCKET_NAME'), Key=test_path)
    print(f"   🗑️  Arquivo de teste removido")
    
except Exception as e:
    print(f"   ❌ ERRO NO UPLOAD: {e}")
    print("\n   🔍 VERIFIQUE:")
    print(f"   1. Bucket '{os.getenv('R2_BUCKET_NAME')}' existe?")
    print(f"   2. Token tem permissão para este bucket?")
    print(f"   3. Nome do bucket está correto no .env?")

print("\n" + "="*60)
print("DIAGNÓSTICO CONCLUÍDO")
print("="*60)