from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import time
from scipy import stats


'''energy e loudness bem correlacionadas '''


start = time.time()



#este é o meu token de acesso para poder utilizar a api do spotify
spot = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id="4122b8a894694d3e8cf1d8a19cf93aec", client_secret="665e23d198b1458f8a4ce02303100b3d"))

#no spotify, cada artista tem uma id para poder reconhecê-lo no sistema
artist_id = '0du5cEVh5yTK9QJze8zA0C'
    
#devolve um dicionário com a id do album e o nome dele para cada album do artista
def get_all_albuns(id_artista):
    albuns_do_artista = spot.artist_albums(id_artista, album_type='album')
    albuns = {}
    for i in range(len(albuns_do_artista['items'])):
        id = albuns_do_artista['items'][i]['id']
        name = albuns_do_artista['items'][i]['name']
        albuns[id] = name
    return albuns


#a função retorna todas as músicas do albúm com as informações requisitadas de cada uma em um data frame
def get_album_data(album_id, album_name):
    tuple_index = []
    data = []
    tracks = spot.album_tracks(album_id)
    for n in range(len(tracks['items'])):
        id_track = tracks['items'][n]['id']
        track = spot.track(id_track)
        audio_features = spot.audio_features(id_track)[0]
    
        #construindo o data frame
        tuple_index.append((album_name, track['name']))
        data.append([int(round(track['duration_ms']/1000, 0)), track['popularity'], audio_features['danceability'], audio_features['energy'], audio_features['key'],
        audio_features['loudness'], audio_features['mode'], audio_features['speechiness'], audio_features['acousticness'],audio_features['instrumentalness'], 
        audio_features['liveness'], audio_features['valence'], audio_features['tempo']])

    index = pd.MultiIndex.from_tuples(tuple_index, names=("Álbuns", "Músicas"))

    return pd.DataFrame(data, columns =['duração(seg)','popularidade', 'danceability', 'energy', 'key', 'loudness', 
    'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'], index=index)

#A url segue o seguinte padrão: "https://genius.com/nome-do-artista-nome-da-música-lyrics"
def formatar_para_url(nome_da_musica):
    
    # algumas musicas do album "An evening with silk sonic" do Bruno Mars
    # aparecem no genius como musicas do silk song
    chave = 0
    if nome_da_musica in ['Silk Sonic Intro', 'Leave The Door Open', 'Fly As Me', 'After Last Night (with Thundercat & Bootsy Collins)',
                            'Smokin Out The Window', 'Put On A Smile', '777', 'Skate', 'Blast Off']:
        chave = 1
    
    #este trecho limpa pedaços como (feat. Damian Marley), deixando apenas o nome da musica
    nome_da_musica = re.sub("\(.*?\)","",nome_da_musica)
    
    nome_da_musica = nome_da_musica.replace("&", "and").replace(" ", "-").lower().replace("'", "")
    if nome_da_musica[-1] == '-':
        nome_da_musica = nome_da_musica[:-1]
    
    if chave == 1:
        return f'https://genius.com/Silk-sonic-{nome_da_musica}-lyrics'
    return f'https://genius.com/Bruno-mars-{nome_da_musica}-lyrics'

def get_lyrics(url):
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
    letra=''
    for tag in soup.select('div[class^="Lyrics__Container"], .song_body-lyrics p'):
        t = tag.get_text(strip=True, separator='\n')
        if t:
            letra+=t
    letra = letra.replace("\n", " ")
    letra = re.sub("\[.*?\]", "", letra)
    
    return letra


#cria um dataframe com todas as informações de todas as musicas
def create_dataframe():
    albuns = get_all_albuns(artist_id)
    dfs ={}
    for id, nome in albuns.items():
        dfs[nome]= get_album_data(id, nome)
    df = pd.concat(dfs.values())

    #tirando essa delux edition para nao ter músicas repetidas
    df.drop('Unorthodox Jukebox (Deluxe Edition)', axis=0, level=0, inplace= True)
    df.index = df.index.remove_unused_levels()

    #adicionando a coluna prêmios pos música.Como são poucos prêmios, pegamos manualmente
    df["prêmios"] = np.array([0,0,0,0,0,0,0,0,0,0,2,0,0,5,0,0,0,1,0,0,2,0,1,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0])

    #df.to_excel(r'dataframe.xlsx')
    return df

#cria um json com a letra de todas as músicas
def get_all_lyrics():
    df = create_dataframe()
    dic = {}
    lista = []
    for i in df.index.values:
        url = formatar_para_url(i[1])
        letra = get_lyrics(url)
        dic = dict(album = f'{i[0]}', musica = f'{i[1]}', letra = f'{letra}')
        lista.append(dic)
    with open("musicas.json", "w") as outfile:
        json.dump(lista, outfile)

#retorna um pd.series com as palavras mais comuns dada uma lista com palavras
def count_freq(lista):
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

#retorna as palvras mais comuns por álbum
def palavras_comuns(album):
    freq = pd.Series(0)
    with open('musicas.json') as file:
        all_musics = json.load(file)
        for dicionario in all_musics:
            if dicionario['album'] == album:
                freq = freq.add(count_freq([dicionario['letra']]), fill_value=0)
    return freq.sort_values(ascending=False)


#essa função plota graficos do tipo: mostre o maior tal e menor tal...
def plot_mais_e_menos(df, lista):
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
            print(f'O máximo em {coluna} no álbum {album} é {max_album}')
            print(f'O mínimo em {coluna} no álbum {album} é {min_album}\n')
            for musica in musicas:
                if musica == min_album:
                    custom_palette.append('y')
                elif musica == max_album:
                    custom_palette.append('r')
                else:
                    custom_palette.append('k')
            sns.set(style = 'whitegrid')
            sns.barplot(x = np.array(musicas), y = df.loc[album, coluna], data=df, palette=custom_palette)
            plt.xticks(fontsize=7, rotation=80)
            plt.title(f'{coluna} em: {album}', fontsize=15)
            plt.ylabel(f'{coluna}', fontsize=10)
            plt.show()

#plotando o gráfico dos albuns mais premiados
def plot_premiados(df):
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
    print("O álbum com mais prêmios é: ",max(res, key=res.get), "\n")

def plot_relacao_um(df):
    sns.lmplot(x="popularidade", y="duração(seg)", data=df)
    r = stats.pearsonr(df['popularidade'], df['duração(seg)'])[0]
    p = stats.pearsonr(df['popularidade'], df['duração(seg)'])[1]
    plt.legend(['R={:f}, p-value={:f}'.format(r,p)])
    plt.show()

def grupo_tres(df, lista):
    #há relação entre as colunas energy e loudness?
    sns.lmplot(x="energy", y="loudness", data=df)
    r = stats.pearsonr(df['energy'], df['loudness'])[0]
    p = stats.pearsonr(df['energy'], df['loudness'])[1]
    plt.legend(['R={:f}, p-value={:f}'.format(r,p)])
    plt.show()

    #quais são os tons (baseados em Pitch class) mais frequentes nas músicas?
    counts = df['key'].value_counts().to_dict()
    k, v = [], []
    for key, value in counts.items():
        k.append(key)
        v.append(value)
    custom_palette = []
    max_value = max(counts, key=counts.get)
    min_value = min(counts, key=counts.get)
    for i in sorted(k, key=int):
        if i == max_value:
            custom_palette.append("b")
        elif i == min_value:
            custom_palette.append("g")
        else:
            custom_palette.append("k")
    sns.set(style = 'whitegrid')
    sns.barplot(x = k, y = v, data=df, palette=custom_palette)
    plt.xticks(fontsize=7)
    plt.title("Frequência dos tons", fontsize=15)
    plt.ylabel("Frequência", fontsize=10)
    plt.xlabel("Tons", fontsize=10)
    plt.show()

    #quais são as músicas consideradas com maior 'danceability' por álbum?
    for coluna in lista:
        tuples = df.index.values
        dict_albuns = {}
        for (key, value) in tuples:
            dict_albuns.setdefault(key, []).append(value)

        for album, musicas in dict_albuns.items():
            custom_palette = []
            max_album = df.loc[album].idxmax()[coluna]
            min_album = df.loc[album].idxmin()[coluna]
            print(f'O máximo em {coluna} no álbum {album} é {max_album}')
            print(f'O mínimo em {coluna} no álbum {album} é {min_album}\n')
            for musica in musicas:
                if musica == min_album:
                    custom_palette.append('y')
                elif musica == max_album:
                    custom_palette.append('r')
                else:
                    custom_palette.append('k')
            sns.set(style = 'whitegrid')
            sns.barplot(x = np.array(musicas), y = df.loc[album, coluna], data=df, palette=custom_palette)
            plt.xticks(fontsize=7, rotation=80)
            plt.title(f'{coluna} em: {album}', fontsize=15)
            plt.ylabel(f'{coluna}', fontsize=10)
            plt.show()

end = time.time()
print("\n\nThe time of execution of above program is :", end-start)
