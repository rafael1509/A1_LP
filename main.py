from multiprocessing.resource_sharer import stop
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
#df = musics.create_dataframe()

#diminui tempo de execução ao usar df vindo do csv
df = pd.read_csv('dataframe.csv', index_col=0, encoding='utf-8-sig', sep='\s*,\s*', engine='python').reset_index()
df = df.set_index(['Álbuns', 'Músicas'])
albuns = df.index.levels[0].values




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
            min_album = df.loc[album].idxmin()[coluna]
            for musica in musicas:
                if musica == max_album:
                    print("max", coluna, album,":",)
                    custom_palette.append('r')
                elif musica == min_album:
                    custom_palette.append('b')
                else:
                    custom_palette.append('k')
            sns.set(style = 'whitegrid')
            sns.barplot(x = np.array(musicas), y = df.loc[album, coluna], data=df, palette=custom_palette)
            plt.xticks(fontsize=7, rotation=80)
            plt.title(f'{coluna} em: {album}', fontsize=15)
            plt.ylabel(f'{coluna}', fontsize=10)
            plt.show()
    #plotando o gráfico dos prêmios
    tuples = df.index.values
    dict_albuns = {}
    albuns = []
    premios = []
    res = {}
    for key in albuns:
        for value in premios:
            res[key] = value
            premios.remove(value)
            break  
    for (key, value) in tuples:
        dict_albuns.setdefault(key, []).append(df.loc[key].iloc[:, 13].sum())
    for album in dict_albuns: 
        albuns.append(album)
    for p in dict_albuns.values():
        premios.append(p[0])
    sns.set(style = 'whitegrid')
    sns.barplot(x = albuns, y = premios, data=df)
    plt.xticks(fontsize=7)
    plt.title("Prêmios por álbuns", fontsize=15)
    plt.ylabel("Prêmios", fontsize=10)
    plt.show()
    res = {}
    for key in albuns:
        for value in premios:
            res[key] = value
            premios.remove(value)
            break  
    print(max(res, key=res.get))
