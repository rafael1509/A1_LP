import pandas as pd
import grupo_1_e_3 as g13
import grupo_2 as g2


global df, albuns

#df = musics.create_dataframe()

#diminui tempo de execução ao usar df vindo do csv
df = pd.read_csv('dataframe.csv', index_col=0, encoding='utf-8-sig', sep='\s*,\s*', engine='python').reset_index()
df = df.set_index(['Albuns', 'Musics'])

albuns = df.index.levels[0].values



def grupo_um():
    # item i
    g13.plot_mais_e_menos_por_album(df, 'popularity')

    # item ii
    # g13.plot_mais_e_menos_por_album(df, 'duration (sec)')

    # item iii
    # g13.plot_mais_e_menos_geral(df, 'popularity')

    # item iv
    # g13.plot_mais_e_menos_geral(df, 'duration (sec)')

    # item v
    # g13.plot_premiados(df)

    # item vi
    # g13.plot_correlacao(df, ('duration (sec)', 'popularity'))
# grupo_um()


def grupo_dois():
    # item i
    # g2.frequencia_dos_titulos_dos_albuns(df)

    # item ii
    # g2.frequencia_dos_titulos_das_musicas(df)

    # item iii
    # g2.palavras_comuns_albuns(albuns)

    # item iv
    # g2.palavras_comuns_discografia(albuns)

    # item v
    # print(g2.titulo_albuns_nas_letras(albuns))

    # item vi
    print(g2.titulo_musica_na_letra())
grupo_dois()

def grupo_tres():    
    # Há relação entre as colunas energy e loudness?
    g13.plot_correlacao(df, ('energy', 'loudness'))

    # Quais são os tons (baseados em Pitch class) mais frequentes nas músicas?
    g13.plot_tom_mais_frequente(df)

    # Quais são as músicas consideradas com maior 'danceability' por álbum e em toda discografia?
    g13.plot_mais_e_menos_por_album(df, ['danceability'])
    g13.plot_mais_e_menos_geral(df, ['danceability'])
