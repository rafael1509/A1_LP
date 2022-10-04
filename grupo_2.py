import re
import pandas as pd
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns


def count_freq(lista):
    """   
    :param lista: lista com strings.
    :type lista: list
    :return: um pd.Series com a frequência de cada palavra da lista.
    :rtype: object
    """
    
    words = []
    for item in lista:
        item = re.subn('[(,),&,!,:,?]', "", item)#re.subn devolve uma tupla, oq impede o uso do replace
        item = item[0].replace("\n", " ").replace('"', "").lower()
        if " " in item:
            for palavra in item.split():
                words.append(palavra)
        else:
            words.append(item)
    freq = pd.value_counts(words)

    #tirando stopwords
    stops = list(stopwords.words('english'))
    for palavra, repeticoes in freq.items():
        if palavra in stops:
            freq = freq.drop(palavra)
    return freq


# Quais são as palavras mais comuns nos títulos dos Álbuns?
def frequencia_dos_titulos_dos_albuns(df):
    """
    Essa função responde quais são as palavras mais comuns nos títulos dos álbuns e plota as tag lous.
    
    :param df: dataframe com todas as informações das músicas.
    :type df: object
    """
    print(count_freq(df.index.levels[0].values).head(3))
    wordcloud = WordCloud(background_color="#1B2430", colormap='Blues')
    wordcloud.generate_from_frequencies(frequencies=count_freq(df.index.levels[0].values))
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title('Palavras mais comuns nos títulos dos álbuns')
    plt.show()


# Quais são as palavras mais comuns nos títulos das músicas?
def frequencia_dos_titulos_das_musicas(df):
    """
    Essa função responde quais são as palavras mais comuns nos títulos das músicas e plota as tag clous.
    
    :param df: dataframe com todas as informações das músicas.
    :type df: object
    """
    print(count_freq(df.index.levels[1].values).head(3))
    wordcloud = WordCloud(background_color="#0F0E0E", colormap='GnBu')
    wordcloud.generate_from_frequencies(frequencies=count_freq(df.index.levels[1].values))
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title('Palavras mais comuns nos títulos das músicas')
    plt.show()



def palavras_comuns(album):
    """
    :param album: nome do álbum escolhido.
    :type album: str
    :return: um pd.Series com a frequência de cada palavra que aparece nas músicas de um álbum específico
    :rtype: object
    """
    freq = pd.Series(0)
    with open('musicas.json') as file:
        all_musics = json.load(file)
        for dicionario in all_musics:
            if dicionario['album'] == album:
                freq = freq.add(count_freq([dicionario['letra']]), fill_value=0)
    return freq.sort_values(ascending=False)


# Quais são as palavras mais comuns nas letras das músicas, por Álbum?
def palavras_comuns_albuns(lista_albuns):
    """
    Recebe uma lista com os nomes dos álbuns a serem analisados.
    Responde quais as palavras mais frequentes nas letras das músicas por álbum e plota a tag cloud de CADA ÁLBUM.

    :param lista_albuns: lista com os nomes dos álbuns.
    :type lista_albuns: list[str]
    """
    for album in lista_albuns:
        serie = palavras_comuns(album)
        print(f"\nPalavras mais frequentes em: {album}\n", serie.head(3), sep="")
        wordcloud = WordCloud(colormap='Dark2')
        wordcloud.generate_from_frequencies(frequencies=serie)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title(f"Palavras mais frequentes em: {album}")
        plt.show()


# Quais são as palavras mais comuns nas letras das músicas, em toda a discografia?
def palavras_comuns_discografia(lista_albuns):
    """
    Recebe uma lista com os nomes dos álbuns a serem analisados.
    Responde quais as palavras mais frequentes nas letras das músicas e plota a wordcloud de TODA A DISCOGRAFIA.

    :param lista_albuns: lista com os nomes dos álbuns.
    :type lista_albuns: list[str]
    """
    freq_total = pd.Series(0)
    for album in lista_albuns:
        freq_total = freq_total.add(palavras_comuns(album), fill_value=0)
    print("\nPalavras mais comuns nas letras das músicas em toda a discografia:\n", freq_total.sort_values(ascending=False).head(3),sep="")
    wordcloud = WordCloud(background_color="#0F0E0E", colormap='PuRd_r')
    wordcloud.generate_from_frequencies(frequencies=freq_total)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title('Palavras mais comuns nas letras das músicas em toda a discografia')
    plt.show()


# o titulo do album é tema recorrente nas letras?
def titulo_albuns_nas_letras(albuns):
    """
    Recebe uma lista com os nomes dos álbuns a serem analisados.
    A função plota um gráfico de barras que mostra o número de vezes que o nome do álbum aparece
    nas músicas dele. Contabilizamos uma ocorrência para cada palavra-chave que está presente em uma
    música (palavra-chave seria uma palavra que não está na lista padrão das stopwords da biblioteca NLTK).

    :param albuns: lista com os nomes dos álbuns.
    :type albuns: list[str]
    """
    
    ocorrencias = {}
    for titulo in albuns:
        if titulo not in ocorrencias:
            ocorrencias[titulo]= 0
        titulo_list = re.sub("\(.*?\)","", titulo).replace("&", "").lower().split()
        stops = list(stopwords.words('english'))
        filtered = [palavra for palavra in titulo_list if not palavra.lower() in stops]
        freq = palavras_comuns(titulo)
        for palavra in filtered:
            try:
                ocorrencias[titulo] += freq[palavra]
            except KeyError:
                continue
                #esse é o caso de uma palavra chave do álbum não ter nenhuma ocorrência na letra da música
    keys = list(ocorrencias.keys())
    vals = list(ocorrencias.values())
    sns.set(style = 'whitegrid')
    sns.barplot(x = keys, y = vals)
    plt.xticks(fontsize=7)
    plt.title("Ocorrência do título nas letras das músicas", fontsize=15)
    plt.ylabel("Frequência", fontsize=10)
    plt.show()


# o titulo de uma música é tema recorrente nas letras?
def titulo_musica_na_letra():
    """
    Essa função não recebe parâmetros.
    A função plota um gráfico de barras que mostra o número de vezes que o título da música aparece
    na sua letra. Contabilizamos uma ocorrência para cada palavra-chave que está presente em uma
    música (palavra-chave seria uma palavra que não está na lista padrão das stopwords da biblioteca NLTK).

    """
    
    ocorrencias = {}
    with open("musicas.json") as file:
        all_musics = json.load(file)
        for dicionario in all_musics:
            if dicionario['musica'] not in ocorrencias:
                ocorrencias[dicionario['musica']] = 0
            titulo_list = re.sub("\(.*?\)","", dicionario['musica']).replace("&", "").lower().split()
            stops = list(stopwords.words('english'))
            filtered = [palavra for palavra in titulo_list if not palavra.lower() in stops]
            freq = count_freq([dicionario['letra']])
            for palavra in filtered:
                try:
                    ocorrencias[dicionario['musica']] += freq[palavra]
                except KeyError:
                    continue
                    #esse é o caso de uma palavra chave da música não ter nenhuma ocorrência na letra da música

        custom_palette = []
        posicao = pd.Series(ocorrencias).sort_values(ascending=False)
        for titulo, frequencia in ocorrencias.items():
            if posicao.index.get_loc(titulo) < 13:
                custom_palette.append('#FFC4C4')
            elif posicao.index.get_loc(titulo) < 26:
                custom_palette.append('#EE6983')
            else:
                custom_palette.append('#850E35')
        keys = list(ocorrencias.keys())
        vals = list(ocorrencias.values())
        sns.set(style = 'whitegrid')
        sns.barplot(x = keys, y = vals, palette=custom_palette)
        plt.xticks(fontsize=7, rotation=80)
        plt.title("Ocorrência do título nas letras das músicas", fontsize=15)
        plt.ylabel("Frequência", fontsize=10)
        plt.show()
