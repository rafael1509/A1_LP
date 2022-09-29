import musics
import pandas as pd
import json
import re
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

global df, albuns

#diminui tempo de execução ao usar df vindo do cdv
# df = pd.read_csv('dataframe.csv', index_col=0).reset_index()
# df = df.set_index(['Álbuns', 'Músicas'])

df = musics.create_dataframe()

albuns = df.index.levels[0].values

#criando dois novos dataframes para poder pegar a soma das premiações de cada música em cada álbum
df2 = df.iloc[:, 13]
premios = []
for album in list(albuns):
    j = df2.loc[album].sum()
    premios.append([j])
df3 = pd.DataFrame(premios, index=list(albuns), columns=["prêmios"])

def grupo_um():
    #pegando as músicas mais e menos tocadas e com mais e menos duração por álbum
    for album in list(albuns):
        i_max = df.loc[album].idxmax()
        i_min = df.loc[album].idxmin()
        print("Música com mais duração e popularidade do álbum ",album,":","\n",i_max[[0,1]],"\n",sep="")
        print("Música com menos duração e popularidade do álbum ",album,":","\n",i_min[[0,1]],"\n",sep="")
    #pegando as músicas mais e menos tocadas e com mais e menos duração em toda a discografia
    ii_max = df.loc[albuns].idxmax()
    print("Música com mais duração e popularidade em toda a discografia:", "\n", ii_max[[0,1]], "\n", sep="")
    ii_min = df.loc[albuns].idxmin()
    print("Música com menos duração e popularidade em toda a discografia:", "\n", ii_min[[0,1]], "\n", sep="")
    #pegando as premiações por álbum e o álbum mais premiado
    print("Prêmios por álbum: \n", df3, sep="")
    print("\n")
    v = df3["prêmios"].idxmax()
    print("Álbum com mais premiações:", v)

#palavras mais comuns nas letras das musicas por album e em toda discografia
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


def plot():
    #criando uma paleta de cor para usar como diferenciação das músicas por seus respectivos álbuns
    custom_palette = []
    albuns = df.index.levels[0].values
    for i in df.index.values:
        if i[0] == albuns[0]:
            custom_palette.append('k')
        elif i[0] == albuns[1]:
            custom_palette.append('y')
        elif i[0] == albuns[2]:
            custom_palette.append('g')
        elif i[0] == albuns[3]:
            custom_palette.append('r')
    #criando as cores para a legenda dos gráficos
    primeiro = mpatches.Patch(color='k', label=albuns[0])
    segundo = mpatches.Patch(color='y', label=albuns[1])
    terceiro = mpatches.Patch(color='g', label=albuns[2])
    quarto = mpatches.Patch(color='r', label=albuns[3])
    cor_leg = [primeiro, segundo, terceiro, quarto]

    #criação dos gráficos
    sns.set(style = 'whitegrid')

    sns.barplot(x = df.index.levels[1].values, y = 'popularidade', data=df, palette=custom_palette)
    plt.xticks(fontsize=7, rotation=80)
    plt.title('Popularidade das músicas', fontsize=15)
    plt.ylabel('Popularidade', fontsize=10)
    plt.legend(handles=cor_leg)
    plt.show()

    sns.barplot(x = df.index.levels[1].values, y = 'duração(seg)', data=df, palette=custom_palette)
    plt.xticks(fontsize=7, rotation=80)
    plt.title('Durações das músicas', fontsize=15)
    plt.ylabel('Duração(seg)', fontsize=10)
    plt.legend(handles=cor_leg)
    plt.show()

    sns.barplot(data = df3, x = df3.index.values ,y = "prêmios")
    plt.title('Prêmios dos álbuns', fontsize=15)
    plt.xlabel('Álbuns', fontsize=10)
    plt.ylabel('Prêmios', fontsize=10)
    plt.show()
