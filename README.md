<h1>A1_LP</h1>

Nesse repositório, feito para a avaliação de Linguagem de Programação, encontram-se os códigos feitos para a extração e visualização de dados de um determinado artista ou banda, por meio da API do Spotify. Para essa avaliação, escolhemos o artista ``Bruno Mars``.

<h2>Índice:</h2>

   * [Requisitos](#requisitos)
   * [Uso](#uso)
   * [Visualizações](#visualizacoes)
   * [Documentação](#docs)
   * [Colaboradores](#equipe)

<h2 id=requisitos>Requisitos:</h2>

Use o pacote [pip](https://pip.pypa.io/en/stable/) para instalar as bibliotecas necessárias:

```bash
pip install pandas
pip install numpy
pip install spotipy
pip install bs4
pip install json
pip install re
pip install seaborn
pip install matplotlib
pip install requests
pip install scipy
pip install nltk
pip install wordcloud
```

<h2 id=uso>Uso:</h2>

Após instalar todas as bibliotecas, para o uso desse repositório e ver seu funcionamento, basta cloná-lo e seguir a seguinte linha de comando:

```bash
python main.py
```

⚠️ Atenção: Esses códigos estão analisando os dados do artista ``Bruno Mars``, por isso as ``ids`` do artista e dos álbuns e os arquivos no repositório se referenciam a esse artista no spotify. Caso você queria usar os códigos com outro artista ou banda, será necessário a troca das ``ids`` e alguns ajustes nas linhas de códigos, como a troca manual da coluna ``premios`` e outros ajustes que fizemos especificamente para o artista escolhido.

<h2 id=visualizacoes>Visualizações:</h2>

As visualizações, feitas através da Seaborn e da WordCloud, podem ser todas encontradas na pasta ``visualizacoes`` em .png, e, também nessa pasta, encontra-se um PDF de nome ``Relatório_A1_LP.pdf`` com cada visualização em seu respectivo grupo de perguntas, na sequência que aparecem ao usar a ``main.py``.


<h2 id=docs>Documentação:</h2>

Toda a documentação está comentada em cada função de cada módulo de código. Para uma rápida visualização, basta acessar o link https://joaopereiraoliveira.github.io/A1_LP/, feito com a biblioteca Sphinx e gerado o html pelo ```Pages``` do Github. Para gerar essa página de documentação, foi criado a branch ```gh-pages``` no respositório, onde pode-se ver todos os html gerados a partir da Sphinx.



<h2 id=equipe>Colaboradores:</h2>
  
  * [João Oliveira](https://github.com/JoaoPereiraOliveira)
  
  * [Rafael dos Santos](https://github.com/rafael1509)
