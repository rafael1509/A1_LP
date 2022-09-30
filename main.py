import matplotlib.pyplot as plt
from wordcloud import WordCloud
import musics
import pandas as pd
import numpy as np
import json
import re
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from nltk.corpus import stopwords

global df, albuns
# df = musics.create_dataframe()

#diminui tempo de execução ao usar df vindo do csv
df = pd.read_csv('dataframe.csv', index_col=0, encoding='utf-8-sig', sep='\s*,\s*', engine='python').reset_index()
df = df.set_index(['Álbuns', 'Músicas'])


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
    v = df3["prêmios"].idxmax()
    print("Álbum com mais premiações:", v)


#palavras mais comuns nas letras das musicas por album e em toda discografia
def palavras_comuns_musicas():
    freq_total = pd.Series(0)
    for album in albuns:
        serie = musics.palavras_comuns(album)
        print(f"\nPalavras mais frequentes em: {album}\n", serie.head(3), sep="")

        #nuvem de palavras por álbum
        wordcloud = WordCloud(background_color="white", colormap='Dark2')
        wordcloud.generate_from_frequencies(frequencies=serie)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title(f"Palavras mais frequentes em: {album}")
        plt.show()

        freq_total = freq_total.add(serie, fill_value=0)

    print("\nPalavras mais comuns nas letras das músicas em toda a discografia:\n", freq_total.sort_values(ascending=False).head(3),sep="")
    wordcloud = WordCloud(background_color="white", colormap='PuRd_r')
    wordcloud.generate_from_frequencies(frequencies=freq_total)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title('Palavras mais comuns nas letras das músicas em toda a discografia')
    plt.show()


# frequencia das palavras nos títulos dos albuns
def frequencia_dos_titulos_dos_albuns():
    print(musics.count_freq(df.index.levels[0].values).head(3))
    wordcloud = WordCloud(background_color="white", colormap='Dark2')
    wordcloud.generate_from_frequencies(frequencies=musics.count_freq(df.index.levels[1].values))
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title('Palavras mais comuns nos títulos dos álbuns')
    plt.show()


# frequencia das palavras nos titulos das musicas
def frequencia_dos_titulos_das_musicas():
    print(musics.count_freq(df.index.levels[1].values))
    wordcloud = WordCloud(background_color="white", colormap='Dark2')
    wordcloud.generate_from_frequencies(frequencies=musics.count_freq(df.index.levels[1].values))
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title('Palavras mais comuns nos títulos das músicas')
    plt.show()


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


# o titulo de uma música é tema recorrente nas letras? A função retorna o número total de vezes que
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


#plotar gráficos referentes ao grupo 1
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

#essa função plota graficos do tipo: mostre o maior tal e menor tal...
def plot_mais_e_menos():
    lista = ['duração(seg)', 'popularidade']#se quiser mais alguma informação, adicionar aqui
    for coluna in lista:
        # Criando um dicionario em que a chave é o nome do álbum e o valor é uma lista com as musicas dele.
        # Isso irá ajudar para plotar um gráfico por álbum
        tuples = df.index.values
        dict_albuns = {}
        for (key, value) in tuples:
            dict_albuns.setdefault(key, []).append(value)

        #plotando os gráficos para cada álbum
        for album, musicas in dict_albuns.items():
            custom_palette = []
            max_album = df.loc[album].idxmax()[coluna]
            for musica in musicas:

                if musica == max_album:
                    custom_palette.append('r')
                else:
                    custom_palette.append('k')
            sns.set(style = 'whitegrid')
            sns.barplot(x = np.array(musicas), y = df.loc[album, coluna], data=df, palette=custom_palette)
            plt.xticks(fontsize=7, rotation=80)
            plt.title(f'{coluna} em: {album}', fontsize=15)
            plt.ylabel(f'{coluna}', fontsize=10)
            plt.show()
print(plot_mais_e_menos())
