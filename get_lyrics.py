import create_dataframe as create
import requests
from bs4 import BeautifulSoup
import json
import re


# A url do genius segue o seguinte padrão: "https://genius.com/nome-do-artista-nome-da-música-lyrics". 
# A função retornará a url de uma música específca ao receber o nome da música
def formatar_para_url(nome_da_musica):
    """Recebe o nome de uma música e retorna sua url específica.
    
    :param nome_da_musica: nome da música escolhida.
    :type nome_da_musica: str
    :return: a url de acesso da música escolhida.
    :rtype: str
    """
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


# Devolve a letra de uma música específica
def get_lyrics(url):
    """Recebe a url de uma música e retorna sua letra.
    
    :param url: url da música escolhida.
    :type url: str
    :return: letra completa da música escolhida.
    :rtype: str
    """
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
    letra=''
    for tag in soup.select('div[class^="Lyrics__Container"], .song_body-lyrics p'):
        t = tag.get_text(strip=True, separator='\n')
        if t:
            letra+=t
    letra = letra.replace("\n", " ")
    letra = re.sub("\[.*?\]", "", letra)
    return letra

#cria um json com a letra de todas as músicas
def get_all_lyrics():
    """Essa função não recebe parâmetros.

        Essa função cria um json com a letra de todas as músicas.

    """
    df = create.create_dataframe()
    dic = {}
    lista = []
    for i in create.df.index.values:
        url = formatar_para_url(i[1])
        letra = get_lyrics(url)
        dic = dict(album = f'{i[0]}', musica = f'{i[1]}', letra = f'{letra}')
        lista.append(dic)
    with open("musicas.json", "w") as outfile:
        json.dump(lista, outfile)
