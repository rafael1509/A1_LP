from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re
import numpy as np
import seaborn
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time
import openpyxl


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
    return re.sub("\[.*?\]", "", letra)


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

    #df.to_csv('dataframe.csv')
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
    return pd.value_counts(words)

#retorna as palvras mais comuns por álbum
def palavras_comuns(album):
    freq = pd.Series(0)
    with open('musicas.json') as file:
        all_musics = json.load(file)
        for dicionario in all_musics:
            if dicionario['album'] == album:
                freq = freq.add(count_freq([dicionario['letra']]), fill_value=0)
    return freq.sort_values(ascending=False)


end = time.time()
print("\n\nThe time of execution of above program is :", end-start)

#==============================CONSTRUÇÃO DAS VIZUALIZAÇÕES===========================#
# custom_palette = []
# albuns = df.index.levels[0].values
# for i in df.index.values:
#     if i[0] == albuns[0]:
#         custom_palette.append('k')
#     elif i[0] == albuns[1]:
#         custom_palette.append('y')
#     elif i[0] == albuns[2]:
#         custom_palette.append('g')
#     elif i[0] == albuns[3]:
#         custom_palette.append('r')

# seaborn.set(style = 'whitegrid')
# seaborn.barplot(x = df.index.levels[1].values, y = 'popularidade', data=df, palette=custom_palette)
# plt.xticks(fontsize=7, rotation=80)
# primeiro = mpatches.Patch(color='k', label=albuns[0])
# segundo = mpatches.Patch(color='y', label=albuns[1])
# terceiro = mpatches.Patch(color='g', label=albuns[2])
# quarto = mpatches.Patch(color='r', label=albuns[3])
# plt.legend(handles=[primeiro,segundo,terceiro,quarto])
# plt.show()
#======================================================================================#
