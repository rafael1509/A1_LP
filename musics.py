from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd

#este é o meu token de acesso para poder utilizar a api do spotify
spot = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id="4122b8a894694d3e8cf1d8a19cf93aec", client_secret="665e23d198b1458f8a4ce02303100b3d"))

'''
esta linha linha de código talvez seja útil depois:

artist_top_tracks(artist_id, country='US')'''

#no spotify, cada artista tem uma id para poder reconhecê-lo no sistema
artist_id = '3ZHU5AKrUmIPnCFfr82QER'
    
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
    tuple_columns = []
    duracao = []
    popularidade = []
    data = [duracao, popularidade]
    tracks = spot.album_tracks(album_id)
    for n in range(len(tracks['items'])):
        id_track = tracks['items'][n]['id']
        track = spot.track(id_track)
        
        #construindo o data frame
        tuple_columns.append((album_name, track['name']))
        duracao.append(int(round(track['duration_ms']/1000, 0)))
        popularidade.append(track['popularity'])

    colunas = pd.MultiIndex.from_tuples(tuple_columns)
    return pd.DataFrame(data, columns =colunas, index=['duração(seg)','popularidade'])

albuns = get_all_albuns('5j4HeCoUlzhfWtjAfM1acR')
dfs ={}
for id, nome in albuns.items():
    dfs[nome]= get_album_data(id, nome)
print(pd.concat(dfs.values(), axis=1))
