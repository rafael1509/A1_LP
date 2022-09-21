from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

#este é o meu token de acesso para poder utilizar a api do spotify
spot = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id="4122b8a894694d3e8cf1d8a19cf93aec", client_secret="665e23d198b1458f8a4ce02303100b3d"))

artista = 'post malone'


'''
esta linha linha de código talvez seja útil depois:

artist_top_tracks(artist_id, country='US')'''



#no spotify, cada artista tem uma id. Essa função retorna a id do artista
def get_artista_por_nome(name):
    busca = spot.search(name)
    items = busca['tracks']['items']
    if len(items) > 0:
        return items[0]['artists'][0]
    else:
        return None
    

info = get_artista_por_nome(artista)
id = info['id']

    
#devolve um dicionário com a id do album e o nome dele para cada album do artista
def get_dados_do_artista(id):
    albuns_do_artista = spot.artist_albums(id, album_type='album')
    albuns = {}
    for i in range(len(albuns_do_artista['items'])):
            id = albuns_do_artista['items'][i]['id']
            name = albuns_do_artista['items'][i]['name']
            albuns[id] = name
    return albuns


#a função retorna todas as músicas do albúm com as informações requisitadas acerca de cada uma
def get_dados_dos_albuns(album_id, album_name):
    spotify_album = {}
    
    tracks = spot.album_tracks(album_id)
    for n in range(len(tracks['items'])):
        id_track = tracks['items'][n]['id']
        track = spot.track(id_track)
        spotify_album[id_track] = {}

        #As variaveis (dados) que estou querendo coletar das músicas
        spotify_album[id_track]['album'] = album_name 
        spotify_album[id_track]['track_number'] = track['track_number'] 
        spotify_album[id_track]['name'] = track['name'] 
        spotify_album[id_track]['popularity'] = track['popularity']
        spotify_album[id_track]['duration_ms'] = track['duration_ms']              
    return spotify_album


#testando a função passando o nome do albúm e sua id
x = get_dados_dos_albuns('31z2OBrrfVwrqU68ouWCwx', 'Stooney')
for k, v in x.items():
    print(k, "--->", v)

