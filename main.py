"""
Script de Cruzamento de Dados Geopolíticos (TSE x IBGE).

Este script realiza a leitura de dados eleitorais (locais de votação do TSE) 
e cruza espacialmente com a malha de bairros do IBGE utilizando GeoPandas.
O objetivo é associar cada seção eleitoral ao seu respectivo bairro para 
análises demográficas e geopolíticas posteriores.
"""

import pandas as pd
import geopandas as gpd
import os

CIDADES_PARA_ANALISAR = [
    {'NOME': 'Rio de Janeiro', 'TSE_CODE': 60011, 'IBGE_CODE': 3304557},
    {'NOME': 'Campos dos Goytacazes', 'TSE_CODE': 58130, 'IBGE_CODE': 3301009},
    {'NOME': 'Niterói', 'TSE_CODE': 58874, 'IBGE_CODE': 3303302}
]
ARQUIVO_TSE_CSV = 'eleitorado_local_votacao_2022.csv'
ARQUIVO_BAIRROS_SHP = 'BR_bairros_CD2022.shp'
ARQUIVO_FINAL_SECOES = 'resultado_secoes_multiplas_cidades.csv'
ARQUIVO_FINAL_BAIRROS = 'resultado_catalogo_bairros_multiplas_cidades.csv'

COLUNA_MUNICIPIO_TSE = 'CD_MUNICIPIO'
COLUNA_SECAO_TSE = 'NR_SECAO'
COLUNA_ZONA_TSE = 'NR_ZONA'
COLUNA_LATITUDE_TSE = 'NR_LATITUDE' 
COLUNA_LONGITUDE_TSE = 'NR_LONGITUDE'
COLUNA_UF_TSE = 'SG_UF' 

COLUNA_IBGE_ID_BAIRRO = 'CD_BAIRRO'
COLUNA_IBGE_NOME_BAIRRO = 'NM_BAIRRO'
COLUNA_IBGE_ID_MUNICIPIO = 'CD_MUN'
COLUNA_IBGE_UF = 'NM_UF'


def main():
    print("--- INICIANDO ANÁLISE (MODO DIAGNÓSTICO) ---")

    print("\n[PASSO 1/3] Carregando dados...")
    try:
        df_tse = pd.read_csv(ARQUIVO_TSE_CSV, sep=';', encoding='latin1', low_memory=False)
        gdf_bairros = gpd.read_file(ARQUIVO_BAIRROS_SHP)
        print(f"✔ Dados carregados com sucesso. Total de {len(df_tse)} seções no arquivo do TSE.")
    except Exception as e:
        print(f"ERRO ao carregar arquivos: {e}")
        return

    print(f"\nFiltrando seções para as cidades selecionadas...")
    
    codigos_tse_para_filtrar = [cidade['TSE_CODE'] for cidade in CIDADES_PARA_ANALISAR]
    
    df_tse[COLUNA_MUNICIPIO_TSE] = pd.to_numeric(df_tse[COLUNA_MUNICIPIO_TSE], errors='coerce')
    df_tse_filtrado = df_tse[df_tse[COLUNA_MUNICIPIO_TSE].isin(codigos_tse_para_filtrar)].copy()
    
    if df_tse_filtrado.empty:
        print("\nERRO CRÍTICO: Nenhuma seção encontrada para as cidades especificadas.")
        return 
    else:
        print(f"✔ CHECKPOINT 1: Após o filtro, restaram {len(df_tse_filtrado)} seções.")

    print("\n[PASSO 2/3] Preparando e cruzando dados geográficos...")

    df_tse_filtrado['latitude'] = pd.to_numeric(df_tse_filtrado[COLUNA_LATITUDE_TSE].astype(str).str.replace(',', '.'), errors='coerce')
    df_tse_filtrado['longitude'] = pd.to_numeric(df_tse_filtrado[COLUNA_LONGITUDE_TSE].astype(str).str.replace(',', '.'), errors='coerce')
    
    linhas_antes_dropna = len(df_tse_filtrado)
    df_tse_filtrado.dropna(subset=['latitude', 'longitude'], inplace=True)
    linhas_depois_dropna = len(df_tse_filtrado)
    print(f"✔ CHECKPOINT 2: Após remover seções sem coordenadas, restaram {linhas_depois_dropna} seções (Perda de {linhas_antes_dropna - linhas_depois_dropna} linhas).")

    gdf_secoes = gpd.GeoDataFrame(
        df_tse_filtrado, 
        geometry=gpd.points_from_xy(df_tse_filtrado.longitude, df_tse_filtrado.latitude),
        crs="EPSG:4326"
    )
    
    gdf_final = gpd.sjoin(gdf_secoes, gdf_bairros.to_crs(gdf_secoes.crs), how="left", predicate="within")
    print(f"✔ CHECKPOINT 3: Após a junção espacial, a tabela final tem {len(gdf_final)} linhas.")
    
    bairros_encontrados = gdf_final[COLUNA_IBGE_ID_BAIRRO].notna().sum()
    print(f"✔ Junção espacial concluída! {bairros_encontrados} seções foram associadas a um bairro.")

    print(f"\n[PASSO 3/3] Formatando e salvando arquivos...")
    
    gdf_final = gdf_final.rename(columns={
        COLUNA_IBGE_ID_BAIRRO: 'bairro_id',
        COLUNA_SECAO_TSE: 'secao',
        COLUNA_ZONA_TSE: 'zona',
        COLUNA_MUNICIPIO_TSE: 'municipio_id'
    })
    
    gdf_final['ano'] = 2022
    gdf_final['id_unico_secao'] = range(1, len(gdf_final) + 1)
    gdf_final['bairro_id'] = gdf_final['bairro_id'].fillna('N/A')
    
    colunas_finais = ['ano', 'secao', 'zona', 'id_unico_secao', 'bairro_id', 'municipio_id']
    resultado_df_secoes = gdf_final[colunas_finais]
    print(f"✔ CHECKPOINT 4: A tabela de seções final a ser salva tem {len(resultado_df_secoes)} linhas.")
    
    resultado_df_secoes.to_csv(ARQUIVO_FINAL_SECOES, index=False, sep=';', encoding='utf-8-sig')
    print(f"🎉 Tabela de seções salva como: {os.path.abspath(ARQUIVO_FINAL_SECOES)}")

    codigos_ibge_para_filtrar = [cidade['IBGE_CODE'] for cidade in CIDADES_PARA_ANALISAR]
    gdf_bairros[COLUNA_IBGE_ID_MUNICIPIO] = pd.to_numeric(gdf_bairros[COLUNA_IBGE_ID_MUNICIPIO], errors='coerce')
    gdf_bairros_filtrado = gdf_bairros[gdf_bairros[COLUNA_IBGE_ID_MUNICIPIO].isin(codigos_ibge_para_filtrar)]
    
    if gdf_bairros_filtrado.empty:
        print(f"AVISO: Nenhum bairro encontrado para os códigos IBGE especificados no arquivo de mapa.")
        cabecalho_bairros = ['bairro_id', 'nome_bairro', 'municipio_id', 'sigla_uf', 'geom']
        pd.DataFrame(columns=cabecalho_bairros).to_csv(ARQUIVO_FINAL_BAIRROS, index=False, sep=';', encoding='utf-8-sig')
    else:
        catalogo_bairros = gdf_bairros_filtrado.rename(columns={
            COLUNA_IBGE_ID_BAIRRO: 'bairro_id',
            COLUNA_IBGE_NOME_BAIRRO: 'nome_bairro',
            COLUNA_IBGE_ID_MUNICIPIO: 'municipio_id',
            COLUNA_IBGE_UF: 'sigla_uf',
            'geometry': 'geom'
        })
        colunas_catalogo = ['bairro_id', 'nome_bairro', 'municipio_id', 'sigla_uf', 'geom']
        catalogo_bairros = catalogo_bairros[colunas_catalogo]
        catalogo_bairros['geom'] = catalogo_bairros['geom'].apply(lambda x: x.wkt)
        catalogo_bairros.to_csv(ARQUIVO_FINAL_BAIRROS, index=False, sep=';', encoding='utf-8-sig')
    
    print(f"🎉 Tabela de bairros salva como: {os.path.abspath(ARQUIVO_FINAL_BAIRROS)}")
    
    print("\n--- PROCESSO CONCLUÍDO! ---")

if __name__ == "__main__":
    main()