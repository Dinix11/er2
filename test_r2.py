#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar a integração com Cloudflare R2
"""
import os
import sys
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

print("="*60)
print("TESTE DE INTEGRAÇÃO CLOUDFLARE R2")
print("="*60)

# Verifica dependências
print("\n1. Verificando dependências...")
try:
    import boto3
    from PIL import Image
    import io
    print("   ✅ boto3 instalado")
    print("   ✅ Pillow instalado")
except ImportError as e:
    print(f"   ❌ Erro: {e}")
    print("   Execute: pip install boto3 Pillow")
    sys.exit(1)

# Verifica variáveis de ambiente
print("\n2. Verificando variáveis de ambiente...")
r2_account = os.getenv('R2_ACCOUNT_ID')
r2_key = os.getenv('R2_ACCESS_KEY_ID')
r2_secret = os.getenv('R2_SECRET_ACCESS_KEY')
r2_bucket = os.getenv('R2_BUCKET_NAME')

if not r2_account:
    print("   ⚠️  R2_ACCOUNT_ID não configurado")
else:
    print(f"   ✅ R2_ACCOUNT_ID: {r2_account[:20]}...")

if not r2_key:
    print("   ⚠️  R2_ACCESS_KEY_ID não configurado")
else:
    print(f"   ✅ R2_ACCESS_KEY_ID: {r2_key[:10]}...")

if not r2_secret:
    print("   ⚠️  R2_SECRET_ACCESS_KEY não configurado")
else:
    print("   ✅ R2_SECRET_ACCESS_KEY: ***")

if not r2_bucket:
    print("   ⚠️  R2_BUCKET_NAME não configurado (usará padrão: encomendas-fotos)")
    r2_bucket = 'encomendas-fotos'
else:
    print(f"   ✅ R2_BUCKET_NAME: {r2_bucket}")

# Testa conexão com R2
print("\n3. Testando conexão com Cloudflare R2...")
try:
    from cloudflare_r2 import get_r2_client, get_bucket_stats, upload_foto_r2
    
    client = get_r2_client()
    if not client:
        print("   ❌ Não foi possível conectar ao R2")
        print("   Verifique as credenciais no arquivo .env")
        sys.exit(1)
    
    print("   ✅ Conexão com R2 estabelecida")
    
    # Testa listagem de objetos
    print("\n4. Verificando bucket...")
    stats = get_bucket_stats()
    if stats:
        print(f"   ✅ Bucket: {stats['total_arquivos']} arquivos")
        print(f"   📊 Espaço usado: {stats['espaco_usado_gb']:.2f} GB de {stats['espaco_limite_gb']} GB")
        print(f"   📈 Porcentagem: {stats['porcentagem_uso']:.1f}%")
        if stats['alerta']:
            print("   ⚠️  ATENÇÃO: Bucket acima de 80%!")
        else:
            print("   ✅ Espaço OK")
    else:
        print("   ⚠️  Não foi possível obter estatísticas (bucket pode não existir)")
    
    # Testa upload de imagem
    print("\n5. Testando upload de imagem...")
    
    # Cria uma imagem de teste
    test_image = Image.new('RGB', (800, 600), color='red')
    buffer = io.BytesIO()
    test_image.save(buffer, format='JPEG', quality=75)
    buffer.seek(0)
    
    # Simula upload
    class FakeFile:
        def __init__(self, data):
            self.data = data
            self.content_type = 'image/jpeg'
        def read(self):
            return self.data
        def seek(self, pos):
            pass
    
    fake_file = FakeFile(buffer.getvalue())
    test_filename = f"test_{os.urandom(4).hex()}.jpg"
    
    url = upload_foto_r2(fake_file, test_filename)
    if url:
        print(f"   ✅ Upload realizado com sucesso!")
        print(f"   🔗 URL: {url[:80]}...")
        
        # Limpa arquivo de teste
        print("\n6. Limpando arquivo de teste...")
        from cloudflare_r2 import delete_foto_r2
        if delete_foto_r2(url):
            print("   ✅ Arquivo de teste removido")
        else:
            print("   ⚠️  Não foi possível remover arquivo de teste (remova manualmente)")
    else:
        print("   ❌ Falha no upload")
        print("   Verifique se o bucket existe e tem permissões de escrita")
    
except Exception as e:
    print(f"   ❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*60)
print("✅ TESTE CONCLUÍDO COM SUCESSO!")
print("="*60)
print("\nPróximos passos:")
print("1. Configure o .env com suas credenciais")
print("2. Crie o bucket no Cloudflare R2")
print("3. Execute: python app.py")
print("="*60)