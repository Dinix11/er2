#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para cadastrar todas as unidades do condomínio
67 blocos × 16 unidades = 1.072 unidades
"""
import sqlite3
import os

# Caminho do banco de dados
DATABASE = os.path.join(os.path.dirname(__file__), 'encomendas.db')

# Configuração
NUMERO_BLOCOS = 67
UNIDADES_POR_BLOCO = [101, 102, 103, 104, 201, 202, 203, 204, 301, 302, 303, 304, 401, 402, 403, 404]
TELEFONE_PADRAO = "5511999999999"  # Telefone padrão (será atualizado depois)

def cadastrar_unidades():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Verificar se já existem unidades
    cursor.execute("SELECT COUNT(*) FROM unidades")
    count = cursor.fetchone()[0]
    
    if count > 0:
        print(f"⚠️  Já existem {count} unidades cadastradas.")
        print("🗑️  Limpando tabela de unidades...")
        cursor.execute("DELETE FROM unidades")
        conn.commit()
    
    print(f"🏢 Cadastrando {NUMERO_BLOCOS} blocos com {len(UNIDADES_POR_BLOCO)} unidades cada...")
    print(f"📊 Total: {NUMERO_BLOCOS * len(UNIDADES_POR_BLOCO)} unidades")
    
    cadastrados = 0
    erros = 0
    
    for bloco in range(1, NUMERO_BLOCOS + 1):
        bloco_nome = f"Bloco {bloco:02d}"
        
        for unidade_num in UNIDADES_POR_BLOCO:
            try:
                cursor.execute(
                    "INSERT INTO unidades (numero, telefone, nome_residente, bloco) VALUES (?, ?, ?, ?)",
                    (str(unidade_num), TELEFONE_PADRAO, f"Morador {unidade_num}", bloco_nome)
                )
                cadastrados += 1
                
                # Mostrar progresso a cada 100 unidades
                if cadastrados % 100 == 0:
                    print(f"   ✅ {cadastrados} unidades cadastradas...")
                    
            except sqlite3.IntegrityError:
                erros += 1
                if erros <= 5:  # Mostrar apenas os primeiros 5 erros
                    print(f"   ⚠️  Unidade {unidade_num} do {bloco_nome} já existe")
    
    conn.commit()
    conn.close()
    
    print("\n" + "="*60)
    print(f"✅ CADASTRO CONCLUÍDO!")
    print(f"   📊 Total cadastradas: {cadastrados}")
    print(f"   ⚠️  Erros (já existiam): {erros}")
    print("="*60)
    
    # Mostrar algumas unidades de exemplo
    print("\n📋 Exemplos de unidades cadastradas:")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM unidades ORDER BY bloco, numero LIMIT 10")
    unidades = cursor.fetchall()
    for u in unidades:
        print(f"   {u[4]} - Unidade {u[1]} - {u[3]}")
    conn.close()

if __name__ == '__main__':
    cadastrar_unidades()