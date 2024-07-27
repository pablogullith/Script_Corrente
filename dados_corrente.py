import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Gerar dados fictícios com menos pontos
def gerar_dados_ficticios(num_pontos=20):
    timestamps = [datetime.now() - timedelta(minutes=10*i) for i in range(num_pontos)]
    current_values = np.random.rand(num_pontos) * 10  # Valores aleatórios de corrente entre 0 e 10
    return list(zip(timestamps, current_values))

# Inserir dados no banco de dados SQLite
def inserir_dados_no_sqlite(dados, db_name='dados_corrente.db'):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Criar tabela se não existir
        cursor.execute('''CREATE TABLE IF NOT EXISTS dados_corrente
                          (timestamp TEXT, current REAL)''')

        # Inserir dados
        cursor.executemany("INSERT INTO dados_corrente (timestamp, current) VALUES (?, ?)", dados)
        conn.commit()
        conn.close()
        print("Dados inseridos com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir dados no banco de dados: {e}")

# Função principal para gerar e inserir dados
def main():
    dados_ficticios = gerar_dados_ficticios()
    inserir_dados_no_sqlite(dados_ficticios)

if __name__ == '__main__':
    main()
