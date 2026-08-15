# Jogo de Trivia feito em Flet

 - [Jogue Online clicando aqui](https://flet-trivia.onrender.com)

- Mais de 4000 perguntas
- Tradução em pt-BR (versão local)
- Modo tradicional com 10 perguntas
- Modo infinito
- Placar com as melhores pontuações registradas

## Ferramentas utilizadas

+ Flet - GUI e lógica
+ Open Trivia Database (opentdb.com) - Banco de Dados de perguntas e API
+ LibreTranslate - API de tradução 
+ SQLite - Armazenamento de placar

## Como executar localmente:

### Requisitos:

+ Python 3.10+
+ Git

1. Clone o Repositorio
```
git clone 'https://github.com/ArthurCorreia213/Flet_Trivia' &&
cd Flet_Trivia &&
python -m venv .venv
```
2. Execute o ambiente virtual (opcional)
```
.venv\Scripts\activate
```
3. Instale os requisitos
```
pip install -r requirements.txt
```
4. Inicialize o servidor de tradução (opcional)

```
libretranslate --load-only en,pt-BR --port 5000
```

Em caso de erro pode ser necessário baixar todas linguagens
Para isso:
```
libretranslate --port 5000
```

5. Rode a aplicação Flet
```
cd src &&
flet run
```
