from textwrap import fill
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re

#este é o meu token de acesso para poder utilizar a api do spotify
spot = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id="4122b8a894694d3e8cf1d8a19cf93aec", client_secret="665e23d198b1458f8a4ce02303100b3d"))

'''
esta linha linha de código talvez seja útil depois:

artist_top_tracks(artist_id, country='US')'''

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
    
        #construindo o data frame
        tuple_index.append((album_name, track['name']))
        data.append([int(round(track['duration_ms']/1000, 0)), track['popularity']])

    index = pd.MultiIndex.from_tuples(tuple_index, names=("Álbuns", "Músicas"))
    return pd.DataFrame(data, columns =['duração(seg)','popularidade'], index=index)

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
    return re.sub(r'\[[^)]*\]', "", letra).replace("(\n", "(").replace("\n)", ")")



#criar um dataframe com todas as informações de todas as musicas
def create_dataframe():
    albuns = get_all_albuns(artist_id)
    dfs ={}
    for id, nome in albuns.items():
        dfs[nome]= get_album_data(id, nome)
    df = pd.concat(dfs.values())

    #tirando essa delux edition para nao ter músicas repetidas
    df.drop('Unorthodox Jukebox (Deluxe Edition)', axis=0, level=0, inplace= True)
    df.index = df.index.remove_unused_levels()
    
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

#retorna um pd.series com as palavras mais comuns
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


# palavras mais comuns nas letras das musicas por album
def palavras_comuns():
    freq_total = pd.Series(0)
    freq_album = pd.Series(0)
    with open('musicas.json') as file:
        all_musics = json.load(file)
        album_atual = all_musics[0]['album']
        for dicionario in all_musics:
            if dicionario['album'] != album_atual or dicionario['musica'] == "Count on Me":
                print(f"\nPalavras mais frequentes em: {album_atual}\n",freq_album.sort_values(ascending=False).head(3), sep="")
                album_atual = dicionario['album']
                freq_album = pd.Series(0)
            freq_total = freq_total.add(count_freq([dicionario['letra']]), fill_value=0)
            freq_album = freq_album.add(count_freq([dicionario['letra']]), fill_value=0)

        print("\nPalavras mais comuns nas letras das músicas em toda a discografia:\n",freq_total.sort_values(ascending=False).head(3), sep="")
        

#frequencia das palavras nos albuns
#print(count_freq(df.index.levels[0].values).head(3))

#frequencia das palavras nos titulos das musicas
# print(count_freq(df.index.levels[1].values))

#df = create_dataframe()
#albuns = df.index.levels[0].values
