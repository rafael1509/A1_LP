import musics
import pandas as pd
import json

global df, albuns
df= musics.create_dataframe()
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
palavras_comuns_musicas()

# frequencia das palavras nos títulos dos albuns
# print(musics.count_freq(df.index.levels[0].values).head(3))

# frequencia das palavras nos titulos das musicas
# print(musics.count_freq(df.index.levels[1].values))

