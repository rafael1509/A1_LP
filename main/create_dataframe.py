from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import numpy as np


# este é o meu token de acesso para poder utilizar a api do spotify
spot = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id="4122b8a894694d3e8cf1d8a19cf93aec", client_secret="665e23d198b1458f8a4ce02303100b3d"))

# no spotify, cada artista tem uma id para poder reconhecê-lo no sistema. 
artist_id = '0du5cEVh5yTK9QJze8zA0C' #id do Bruno Mars


def get_all_albuns(id_artista):
    """    
    :param id_artist: id do artista escolhido.
    :type id_artist: str
    :return: um dicionário com a id do album e o nome dele para cada album do artista
    :rtype: dict
    """

    try:
        albuns_do_artista = spot.artist_albums(id_artista, album_type='album')
    except spotipy.exceptions.SpotifyException as error:
        return error
    else:
        albuns = {}
        for i in range(len(albuns_do_artista['items'])):
            id = albuns_do_artista['items'][i]['id']
            name = albuns_do_artista['items'][i]['name']
            albuns[id] = name
        return albuns


def get_album_data(album_id, album_name):
    """
    Cria um dataframe com informações consideradas relevantes sobre cada música de um álbum específico.
    
    :param album_id: id do álbum escolhido.
    :param album_name: nome do álbum escolhido.
    :type album_id: str
    :type album_name: str
    :return: um dataframe com multi-index de álbum e nome das músicas, em que as colunas
    são são informações consideradas relevantes sobre cada música.
    :rtype: object
    """

    try:
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
        
        index = pd.MultiIndex.from_tuples(tuple_index, names=("Albuns", "Musics"))

        return pd.DataFrame(data, columns =['duration (sec)','popularity', 'danceability', 'energy', 'key', 'loudness', 
        'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'], index=index)
    except Exception as error:
        return error


def create_dataframe():
    """Cria um dataframe com informações consideradas relevantes para todas as músicas do artista
    
    :param: None
    :return: um dataframe com multi-index de álbuns e nome das músicas, em que as colunas
    são são informações consideradas relevantes sobre cada música.
    :rtype: object
    """
    
    try:
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

        #df.to_csv(r'dataframe.csv')
        return df
    except Exception as error:
        return error