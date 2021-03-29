# -*- coding: utf-8 -*-
"""limpando_banco_bianca.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DO8rD2BuUHzAIOZCd-A7TcP0LS9AbFix
"""

import pandas as pd
import numpy as np
df = pd.read_csv("banco_de_imoveis.csv")

df.head()

df.duplicated()

# Quantidades de linhas únicas que estão repetidas
sum(df.duplicated())

# Removendo as repetidas mantendo apenas a primeira de cada repetição
df = df.drop_duplicates(keep="first", subset=[coluna for coluna in df.columns if coluna!="crawled_at"]).reset_index(drop=True)

df[df["id"]=="1037345211"]

df

# Cria uma lista com True caso o id seja numérico e False caso não seja
filtro_de_anuncios = [_id.isnumeric() for _id in df["id"]]

# Usamos o filtro para pegar apenas as linhas onde o id é numérico
df = df[filtro_de_anuncios].reset_index(drop=True)

df.shape

# Verificamos os valores únicos
set(df["rooms"])

# Fazemos o split no espaço, pegamos a primeira parte. Depois substituimos o __ por 0.
# Ex: "1 Quartos".split(" ") = [1, Quartos]
# Pegamos a primeira parte: [1]
# Substituimos "--" por 0. Como não tem fica 1 mesmo.
set(df["rooms"].str.split(" ").str[0].str.replace("--","0"))

df["rooms_limpo"] = (df["rooms"]
                     .str.split(" ")
                     .str[0]
                     .str.replace("--","0")
                     .astype(int))

# Exatamente igual rooms
set(df["bathrooms"])

df["bathrooms_limpo"] = (df["bathrooms"]
                         .str.split(" ")
                         .str[0]
                         .str.replace("--","0")
                         .astype(int))

# Exatamente igual rooms
set(df["garages"])

df["garages_limpo"] = (df["garages"]
                       .str.split(" ")
                       .str[0]
                       .str.replace("--","0")
                       .astype(int))

set(df["garages_limpo"])

set(df["price"])

# Fazemos o split no "R$ ", pegamos o segundo elemento, 
# substituimos o . por nada e transformamos em int
# Ex: "R$ 824.200".split("R$ ") = ["R$ ", "824.200"]
# segundo elemento "824.200"
# "824.200".replace(".", "") = "824200"
# int("824200") = 824200 (passando de string para int)

df["price_limpo"] = [int(w.split("R$ ")[1].replace(".","")) for w in df["price"]]

# Passamos os na para a string "MISSING"
df["condo"] = df["condo"].fillna("MISSING")

# Fazemos semelhante ao price mas com a condicional de apenas para os que não não "MISSING".
# Os que são missing vamos substituir por np.nan
df["condo_limpo"] = [int(w.split("R$ ")[1].replace(".","")) if w!="MISSING" else np.nan for w in df["condo"]]

# Area já está limpo, é só passar para in
df["area_limpo"] = df["area"].astype(int)

# Crawled at já está limpo, é só passar para datetime
df["crawled_at"] = pd.to_datetime(df["crawled_at"], format="%Y-%m-%d %H:%M")

# Removendo colunas antigas
df = df.drop(columns=["area", "rooms", "bathrooms", "garages", "price", "condo"])