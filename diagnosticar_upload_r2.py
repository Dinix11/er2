#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico completo do upload R2
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

print("="*60)
print("DIAGNÓSTICO DE UPLOAD CLOUDFLARE R2")
print("="*60)

# 1. Verificar variáveis de ambiente
print("\n1. VARIÁVEIS DE AMBIENTE:")
print("-" * 60)

r2_account = os.getenv('R2_ACCOUNT_ID')
r2_key = os.getenv('R2_ACCESS_KEY_ID')
r2_secret = os.getenv('R2_SECRET_ACCESS_KEY')
r2_bucket = os.getenv('R2_BUCKET_NAME')
R2_ENDPOINT_URL = f"https://{r2_account}.r2.cloudflarestorage.com" if r2_account else None

print(f"R2_ACCOUNT_ID: {'✅ Presente' if r2_account else '❌ AUSENTE'} | {str(r2_account)[:30] if r2_account else 'None'}")
print(f"R2_ACCESS_KEY_ID: {'✅ Presente' if r2_key else '❌ AUSENTE'} | {str(r2_key)[:20] if r2_key else 'None'}")
print(f"R2_SECRET_ACCESS_KEY: {'✅ Presente' if r2_secret else '❌ AUSENTE'} | {str(r2_secret)[:20] if r2_secret else 'None'}")
print(f"R2_BUCKET_NAME: {'✅ Presente' if r2_bucket else '❌ AUSENTE'} | {r2_bucket or 'None'}")

if not all([r2_account, r2_key, r2_secret, r2_bucket]):
    print("\n❌ ERRO: Variáveis de ambiente incompletas!")
    print("Configure no arquivo .env:")
    print("  R2_ACCOUNT_ID=seu-account-id")
    print("  R2_ACCESS_KEY_ID=sua-access-key")
    print("  R2_SECRET_ACCESS_KEY=sua-secret-key")
    print("  R2_BUCKET_NAME=encomendas-fotos")
    sys.exit(1)

# 2. Verificar dependências
print("\n2. DEPENDÊNCIAS:")
print("-" * 60)

try:
    import boto3
    print("✅ boto3: Instalado")
except ImportError:
    print("❌ boto3: NÃO INSTALADO")
    print("   Execute: pip install boto3")
    sys.exit(1)

try:
    from PIL import Image
    print("✅ Pillow: Instalado")
except ImportError:
    print("❌ Pillow: NÃO INSTALADO")
    print("   Execute: pip install Pillow")
    sys.exit(1)

# 3. Testar conexão com R2
print("\n3. TESTE DE CONEXÃO:")
print("-" * 60)

try:
    from botocore.client import Config
    
    print(f"\n   Criando cliente com:")
    print(f"   - Endpoint: {R2_ENDPOINT_URL}")
    print(f"   - Access Key: {r2_key[:20]}...")
    print(f"   - Secret Key: {r2_secret[:20]}...")
    print(f"   - Bucket: {r2_bucket}")
    
    # Criar cliente diretamente para debug
    client = boto3.client(
        's3',
        endpoint_url=R2_ENDPOINT_URL,
        aws_access_key_id=r2_key,
        aws_secret_access_key=r2_secret,
        config=Config(signature_version='s3v4'),
        region_name='auto'
    )
    
    print("✅ Cliente R2 criado com sucesso")
    
    # Testar listagem de objetos
    print("\n4. TESTE DE ACESSO AO BUCKET:")
    print("-" * 60)
    
    try:
        print(f"   Endpoint: {client._endpoint}")
        print(f"   Region: {client.meta.region_name}")
        
        # Testar listagem de buckets primeiro
        print("\n   Testando listagem de buckets...")
        try:
            buckets = client.list_buckets()
            print(f"   ✅ Conexão OK! Buckets encontrados: {len(buckets.get('Buckets', []))}")
            if buckets.get('Buckets'):
                for bucket in buckets['Buckets'][:5]:
                    print(f"      - {bucket['Name']}")
        except Exception as e:
            print(f"   ⚠️  Erro ao listar buckets: {e}")
        
        # Verificar se o bucket existe
        print(f"\n   Verificando se bucket '{r2_bucket}' existe...")
        try:
            client.head_bucket(Bucket=r2_bucket)
            print(f"   ✅ Bucket '{r2_bucket}' existe e é acessível")
        except Exception as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            if error_code == '404':
                print(f"   ❌ Bucket '{r2_bucket}' NÃO EXISTE")
                print(f"\n   ⚠️  AÇÃO NECESSÁRIA:")
                print(f"   1. Acesse https://dash.cloudflare.com")
                print(f"   2. Vá em R2 > Overview")
                print(f"   3. Clique em 'Create bucket'")
                print(f"   4. Nome: {r2_bucket}")
                print(f"   5. Escolha a localização mais próxima")
                print(f"   6. Clique em 'Create bucket'")
                print(f"\n   Após criar o bucket, execute este diagnóstico novamente.")
            elif error_code == '403':
                print(f"   ❌ Bucket '{r2_bucket}' existe mas SEM PERMISSÃO")
                print(f"\n   ⚠️  PROBLEMA: O token não tem permissão para acessar este bucket")
                print(f"   SOLUÇÕES:")
                print(f"   1. Verifique se o bucket está na conta correta (Account ID: {r2_account})")
                print(f"   2. Verifique se o token tem permissões de 'Object Read & Write'")
                print(f"   3. Tente criar um novo token com permissões totais")
            else:
                print(f"   ❌ Erro ao acessar bucket: {e}")
            sys.exit(1)
        
        print(f"\n   Tentando acessar objetos do bucket: {r2_bucket}")
        response = client.list_objects_v2(Bucket=r2_bucket, MaxKeys=5)
        print(f"✅ Bucket '{r2_bucket}' acessível")
        
        if 'Contents' in response:
            print(f"   Objetos encontrados: {len(response['Contents'])}")
            for obj in response['Contents'][:3]:
                print(f"   - {obj['Key']} ({obj['Size']} bytes)")
        else:
            print("   Bucket vazio")
            
    except Exception as e:
        print(f"❌ ERRO ao acessar bucket: {e}")
        if "SignatureDoesNotMatch" in str(e):
            print("\n   ⚠️  ERRO DE ASSINATURA: As credenciais estão incorretas!")
            print("   Verifique no painel Cloudflare:")
            print("   1. Vá em R2 > Overview")
            print("   2. Clique em 'Manage R2 API Tokens'")
            print("   3. Verifique se o token está ativo e tem permissões de leitura/escrita")
            print("   4. Confira se a Secret Access Key está correta")
        else:
            print("   Verifique se o bucket existe e se as credenciais têm permissão")
        sys.exit(1)
    
    # 5. Teste de upload
    print("\n5. TESTE DE UPLOAD:")
    print("-" * 60)
    
    import io
    
    # Criar imagem de teste
    image = Image.new('RGB', (100, 100), color='red')
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    buffer.seek(0)
    
    test_filename = f"teste_{os.getpid()}.jpg"
    test_path = f"encomendas/teste/{test_filename}"
    
    try:
        client.upload_fileobj(
            buffer,
            r2_bucket,
            test_path,
            ExtraArgs={
                'ContentType': 'image/jpeg',
                'ACL': 'public-read'
            }
        )
        print(f"✅ Upload de teste bem-sucedido!")
        print(f"   Arquivo: {test_path}")
        
        # Gerar URL pública
        public_url = f"https://{r2_account}.r2.cloudflarestorage.com/{r2_bucket}/{test_path}"
        print(f"   URL: {public_url}")
        
        # Limpar arquivo de teste
        try:
            client.delete_object(Bucket=r2_bucket, Key=test_path)
            print(f"✅ Arquivo de teste removido")
        except:
            pass
        
    except Exception as e:
        print(f"❌ ERRO no upload: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "="*60)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("="*60)
    print("\nO R2 está configurado corretamente.")
    print("Se as fotos ainda não estão sendo enviadas, verifique:")
    print("1. Se o servidor está rodando")
    print("2. Se há erros no log do servidor")
    print("3. Se o arquivo de foto é válido")
    
except Exception as e:
    print(f"❌ ERRO inesperado: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)