import musics
import pandas as pd
import json
import nltk
from nltk.corpus import stopwords
import  re

global df, albuns
df = pd.read_csv('dataframe.csv', index_col=0).reset_index()#manter essa linha se quiser o dataframe vindo do arquivo csv
df = df.set_index(['Álbuns', 'Músicas'])
albuns = df.index.levels[0].values

def grupo_um():
    for album in list(albuns):
        i_max = df.loc[album].idxmax()
        i_min = df.loc[album].idxmin()
        print("Música com mais duração, popularidade e prêmios do álbum ",album,":","\n",i_max,"\n",sep="")
        print("Música com menos duração, popularidade e prêmios do álbum ",album,":","\n",i_min,"\n",sep="")

    ii_max = df.loc[albuns].idxmax()
    print("Música com mais duração, popularidade e prêmios em toda a discografia:", "\n", ii_max, "\n", sep="")
    ii_min = df.loc[albuns].idxmin()
    print("Música com menos duração, popularidade e prêmios em toda a discografia:", "\n", ii_min, "\n", sep="")


# palavras mais comuns nas letras das musicas por album e em toda discografia
def palavras_comuns_musicas():
    freq_total = pd.Series(0)
    for album in albuns:
        print(f"\nPalavras mais frequentes em: {album}\n", musics.palavras_comuns(album).head(3), sep="")
        freq_total.add(musics.palavras_comuns(album), fill_value=0)
    print("\nPalavras mais comuns nas letras das músicas em toda a discografia:\n", freq_total.head(3),sep="")


# frequencia das palavras nos títulos dos albuns
# print(musics.count_freq(df.index.levels[0].values).head(3))


# frequencia das palavras nos titulos das musicas
# print(musics.count_freq(df.index.levels[1].values))


# o titulo do album é tema recorrente nas letras? A função retorna o número total de vezes que
# palavras-chave nos titulos dos albuns estão presentes nas suas músicas
def titulo_albuns_nas_letras():
    ocorrencias = {}
    for titulo in albuns:
        if titulo not in ocorrencias:
            ocorrencias[titulo]= 0
        titulo_list = re.sub("\(.*?\)","", titulo).replace("&", "").lower().split()
        stops = list(stopwords.words('english'))
        filtered = [palavra for palavra in titulo_list if not palavra.lower() in stops]
        freq = musics.palavras_comuns(titulo)
        for palavra in filtered:
            try:
                ocorrencias[titulo] += freq[palavra]
            except KeyError:
                continue
                #esse é o caso de uma palavra chave do álbum não ter nenhuma ocorrência na letra da música
    return ocorrencias


# o titulo de uma é tema recorrente nas letras? A função retorna o número total de vezes que
# palavras-chave nos titulos dos albuns estão presentes nas suas músicas
def titulo_musica_na_letra():
    ocorrencias = {}
    with open("musicas.json") as file:
        all_musics = json.load(file)
        for dicionario in all_musics:
            if dicionario['musica'] not in ocorrencias:
                ocorrencias[dicionario['musica']] = 0
            titulo_list = re.sub("\(.*?\)","", dicionario['musica']).replace("&", "").lower().split()
            stops = list(stopwords.words('english'))
            filtered = [palavra for palavra in titulo_list if not palavra.lower() in stops]
            freq = musics.count_freq([dicionario['letra']])
            for palavra in filtered:
                try:
                    ocorrencias[dicionario['musica']] += freq[palavra]
                except KeyError:
                    continue
                    #esse é o caso de uma palavra chave da música não ter nenhuma ocorrência na letra da música
        return ocorrencias

