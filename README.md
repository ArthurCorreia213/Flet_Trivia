# Jogo de Trivia feito em Flet

## Como executar:

1. Clone o Repositorio
```
git clone 'https://github.com/ArthurCorreia213/Flet_Trivia'
cd Flet_Trivia
python -m venv .venv
.venv\Scripts\activate
```
2. Instale os requisitos
```
pip install -r requirements.txt
```
3. Inicialize o servidor de tradução
### Se é sua primeira vez rodando o programa:
```
libretranslate --port 5000
```
### Se você ja instalou os pacotes de tradução antes:
```
libretranslate --load-only en,pt-BR --port 5000
```
### PS: O servidor de tradução deve ficar aberto para a aplicação funcionar
4. Rode a aplicação Flet
```
flet run
```