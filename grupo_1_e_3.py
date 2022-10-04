import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


# Essa função plota graficos do tipo: mostre o maior tal e menor tal POR ÁLBUM
def plot_mais_e_menos_por_album(df, coluna):
    """Recebe o dataframe das músicas e o nome das colunas escolhidas para extração de informação.

       Essa função plota graficos e responde as perguntas do tipo: mostre o maior tal e menor tal POR ÁLBUM.
    
    :param df: dataframe com todas as informações das músicas.
    :param coluna: nome(s) das coluna(s) requisitadas para obter informações.
    :type df: object
    :type coluna: (str or tuple(str))
    """
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
        print(f'O máximo em {coluna} no álbum {album} é {max_album}')
        print(f'O mínimo em {coluna} no álbum {album} é {min_album}\n')
        for musica in musicas:
            if musica == min_album or musica == max_album:
                custom_palette.append('#25316D')
            else:
                custom_palette.append('#97D2EC')
        sns.set(style = 'whitegrid')
        sns.barplot(x = np.array(musicas), y = df.loc[album, coluna], data=df, palette=custom_palette)
        plt.xticks(fontsize=7, rotation=80)
        plt.title(f'{coluna} em: {album}', fontsize=15)
        plt.ylabel(f'{coluna}', fontsize=10)
        plt.show()


# essa função plota graficos do tipo: mostre o maior tal e menor tal EM TODA DISCOGRAFIA
def plot_mais_e_menos_geral(df, coluna):
    """Recebe o dataframe das músicas e o nome das colunas escolhidas para extração de informação.
    
       Essa função plota graficos e responde as perguntas do tipo: mostre o maior tal e menor tal EM TODA DISCOGRAFIA.
    
    :param df: dataframe com todas as informações das músicas.
    :param coluna: nome(s) das coluna(s) requisitadas para obter informações.
    :type df: object
    :type coluna: (str or tuple(str))
    """
    custom_palette = []
    musicas = []
    maximo = df.idxmax()[coluna][1]
    minimo = df.idxmin()[coluna][1]
    print(f'O máximo em {coluna} em toda discografia é {maximo}')
    print(f'O mínimo em {coluna} em toda discografia é {minimo}\n')
    for i in df.index.values:
        musicas.append(i[1])
        if i[1] == maximo or i[1] == minimo:
            custom_palette.append('#3CCF4E')
        else:
            custom_palette.append('#ADDDD0')
    sns.set(style = 'whitegrid')
    sns.barplot(x = np.array(musicas), y = df[coluna], data=df, palette=custom_palette)
    plt.xticks(fontsize=7, rotation=80)
    plt.title(f'{coluna} em: toda discografia', fontsize=15)
    plt.ylabel(f'{coluna}', fontsize=10)
    plt.show()


#plotando o gráfico dos albuns mais premiados
def plot_premiados(df):
    """Recebe o dataframe das músicas.
    
       Essa função plota o gráfico com as premiações de cada álbum e responde o álbum com mais prêmios.
       (Foram considerados os somatórios dos prêmios de cada música de cada álbum como premiação total do álbum.)
    
    :param df: dataframe com todas as informações das músicas.
    :type df: object
    """
    tuples = df.index.values
    dict_albuns = {}
    albuns = []
    premios = []
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
    print("O álbum com mais prêmios é: ",max(res, key=res.get))
    print("O álbum com menos prêmios é: ",min(res, key=res.get))


# Calcula a correlação entre duas colunas do dataframe. Essas colunas são informadas em uma tupla
def plot_correlacao(df, tupla):
    """Recebe o dataframe das músicas e o nome das colunas escolhidas para extração de informação.
    
       Essa função plota graficos de correlação entre duas informações escolhidas.
    
    :param df: dataframe com todas as informações das músicas.
    :param tupla: nomes das colunas requisitadas para obter informações.
    :type df: object
    :type coluna: tuple(str)
    """
    sns.lmplot(x=tupla[0], y=tupla[1], data=df)
    r = stats.pearsonr(df[tupla[0]], df[tupla[1]])[0]
    p = stats.pearsonr(df[tupla[0]], df[tupla[1]])[1]
    plt.legend(['R={:f}, p-value={:f}'.format(r,p)])
    plt.show()

#quais são os tons (baseados em Pitch class) mais frequentes nas músicas?
def plot_tom_mais_frequente(df):
    """Recebe o dataframe das músicas.
    
       Essa função plota o gráfico e responde qual o tom mais frequente nas músicas.
    
    :param df: dataframe com todas as informações das músicas.
    :type df: object
    """
    counts = df['key'].value_counts().to_dict()
    k, v = [], []
    for key, value in counts.items():
        k.append(key)
        v.append(value)
    custom_palette = []
    max_value = max(counts, key=counts.get)
    min_value = min(counts, key=counts.get)
    print("O tom mais frequente é: ", max_value)
    print("O tom menos frequente é: ", min_value)
    for i in sorted(k, key=int):
        if i == max_value or i == min_value:
            custom_palette.append("#820000")
        else:
            custom_palette.append("#FF9494")
    sns.set(style = 'whitegrid')
    sns.barplot(x = k, y = v, data=df, palette=custom_palette)
    plt.xticks(fontsize=7)
    plt.title("Frequência dos tons", fontsize=15)
    plt.ylabel("Frequência", fontsize=10)
    plt.xlabel("Tons", fontsize=10)
    plt.show()
