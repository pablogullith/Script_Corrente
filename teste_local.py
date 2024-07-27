import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
from sqlalchemy import create_engine

# Configuração do banco de dados SQLite local
sqlite_db = 'dados_corrente.db'
engine = create_engine(f'sqlite:///{sqlite_db}', echo=False)

# Função para carregar dados do banco de dados remoto
def carregar_dados_do_bd_remoto():
    try:
        with engine.connect() as conn_remote:
            query = "SELECT timestamp, current FROM dados_corrente"
            dados = pd.read_sql_query(query, conn_remote)
        return dados
    except Exception as e:
        print(f"Erro ao carregar dados do banco de dados remoto: {e}")
        return None

# Função para salvar dados no banco de dados SQLite local
def salvar_dados_no_bd_local(dados):
    try:
        dados['timestamp'] = pd.to_datetime(dados['timestamp'])
        dados.to_sql('corrente', engine, if_exists='replace', index=False)
        print("Dados salvos localmente com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar dados no banco de dados local: {e}")

# Função para carregar dados do banco de dados SQLite local
def carregar_dados_do_bd_local():
    try:
        conn_local = sqlite3.connect(sqlite_db)
        query = "SELECT * FROM corrente"
        df = pd.read_sql_query(query, conn_local)
        conn_local.close()
        return df
    except Exception as e:
        print(f"Erro ao carregar dados do banco de dados local: {e}")
        return None

# Função para plotar o gráfico
def plotar_grafico(df):
    try:
        plt.figure(figsize=(10, 6))
        plt.plot(df['timestamp'], df['current'], marker='o', linestyle='-', color='b')
        plt.title('Corrente Elétrica ao Longo do Tempo')
        plt.xlabel('Hora')
        plt.ylabel('Valor da Corrente Elétrica')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Erro ao plotar gráfico: {e}")

# Função principal para executar o script
def main():
    try:
        # Carregar dados do banco de dados remoto
        dados_remotos = carregar_dados_do_bd_remoto()

        if dados_remotos is not None:
            # Salvar dados no banco de dados SQLite local
            salvar_dados_no_bd_local(dados_remotos)

            # Carregar dados do banco de dados SQLite local
            dados_carregados = carregar_dados_do_bd_local()

            if dados_carregados is not None:
                # Plotar o gráfico
                plotar_grafico(dados_carregados)
    except Exception as e:
        print(f"Erro no script principal: {e}")

if __name__ == '__main__':
    main()
