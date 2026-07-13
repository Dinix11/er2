#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para diagnosticar problemas com Cloudflare R2
"""
import os
from dotenv import load_dotenv
from cloudflare_r2 import get_r2_client, get_bucket_stats

load_dotenv()

print("="*60)
print("DIAGNÓSTICO DO CLOUDFLARE R2")
print("="*60)

# Verificar variáveis de ambiente
print("\n1. VERIFICANDO VARIÁVEIS DE AMBIENTE:")
print(f"   R2_ACCOUNT_ID: {'✅ Presente' if os.getenv('R2_ACCOUNT_ID') else '❌ Ausente'}")
print(f"   R2_ACCESS_KEY_ID: {'✅ Presente' if os.getenv('R2_ACCESS_KEY_ID') else '❌ Ausente'}")
print(f"   R2_SECRET_ACCESS_KEY: {'✅ Presente' if os.getenv('R2_SECRET_ACCESS_KEY') else '❌ Ausente'}")
print(f"   R2_BUCKET_NAME: {os.getenv('R2_BUCKET_NAME', '❌ Não definido')}")

# Testar conexão
print("\n2. TESTANDO CONEXÃO COM R2:")
client = get_r2_client()
if client:
    print("   ✅ Cliente R2 criado com sucesso")
else:
    print("   ❌ Falha ao criar cliente R2")
    print("   Verifique se as credenciais estão corretas")
    exit(1)

# Testar listagem de objetos
print("\n3. TESTANDO LISTAGEM DE OBJETOS:")
try:
    stats = get_bucket_stats()
    if stats:
        print(f"   ✅ Bucket acessível")
        print(f"   📊 Estatísticas:")
        print(f"      - Arquivos: {stats['total_arquivos']}")
        print(f"      - Espaço usado: {stats['espaco_usado_gb']:.2f} GB")
        print(f"      - Limite: {stats['espaco_limite_gb']} GB")
        print(f"      - Uso: {stats['porcentagem_uso']:.1f}%")
        if stats['alerta']:
            print("      ⚠️  ALERTA: Bucket acima de 80%!")
    else:
        print("   ❌ Não foi possível obter estatísticas")
except Exception as e:
    print(f"   ❌ Erro ao acessar bucket: {e}")

# Testar upload
print("\n4. TESTANDO UPLOAD:")
try:
    import io
    from PIL import Image
    
    # Criar imagem de teste
    test_image = Image.new('RGB', (100, 100), color='red')
    buffer = io.BytesIO()
    test_image.save(buffer, format='JPEG', quality=75)
    buffer.seek(0)
    
    # Tentar upload
    test_path = f"teste_{os.getenv('R2_BUCKET_NAME')}.jpg"
    client.upload_fileobj(
        buffer,
        os.getenv('R2_BUCKET_NAME'),
        test_path,
        ExtraArgs={
            'ContentType': 'image/jpeg',
            'ACL': 'public-read'
        }
    )
    
    print(f"   ✅ Upload de teste bem-sucedido!")
    print(f"   📁 Arquivo: {test_path}")
    
    # Remover arquivo de teste
    client.delete_object(Bucket=os.getenv('R2_BUCKET_NAME'), Key=test_path)
    print(f"   🗑️  Arquivo de teste removido")
    
except Exception as e:
    print(f"   ❌ ERRO NO UPLOAD: {e}")
    print("\n   POSSÍVEIS CAUSAS:")
    print("   1. Token sem permissão de escrita (Edit)")
    print("   2. Bucket não existe")
    print("   3. Credenciais incorretas")
    print("\n   SOLUÇÃO:")
    print("   1. Acesse: https://dash.cloudflare.com")
    print("   2. Vá em R2 → Manage R2 API Tokens")
    print("   3. Crie um novo token com permissões:")
    print("      ✅ Account > Cloudflare R2 > Edit")
    print("      ✅ Account > Cloudflare R2 > Read")
    print("   4. Atualize o arquivo .env com as novas credenciais")

print("\n" + "="*60)
print("DIAGNÓSTICO CONCLUÍDO")
print("="*60)