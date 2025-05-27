import flet as ft
import requests
from html import unescape
from random import randint
import sqlite3

#Parametro de requisição da API de perguntas; 
#Token é gerado automaticamente ao iniciar o jogo
token = ''
parametro = 'https://opentdb.com/api.php?amount=10'

#Configurações iniciais
questao_num = 0
numero_a_exibir = 0
dados = []
loop = 0
pontuacao = 0
erros = 0
nome = ''

correto = ''

categoria_selecionada = ''
dificuldade = ''
tipo_de_pergunta = ''

game_mode = 0
#GAME MODE 1 = INFINITO
#GAME MODE 2 = 10 perguntas

cursor = ''

def main(page: ft.Page):
    global pontuacao
    global token
    global cursor

    con = sqlite3.connect('trivia.db')
    cur = con.cursor()
    cursor = cur
    
    questao_atual = ft.Text(key='questao_atual')
    questao_tipo = ft.Text(key='questao_atual1')
    questao_dificuldade = ft.Text(key='questao_atual2')
    questao_categoria = ft.Text(key='questao_atual3')
    questao_body = ft.Text(key='questao_atual4')
    pontuacao_txt = ft.Text(key='questao_atual5')
    erros_exibicao = ft.Text(key='questao_atual6')

    resultado = ft.Text(key="texto_resultado")

    nome_input = ft.TextField(label="Seu nome (até 3 letras)", max_length=3, width=150, key="input_nome")


    global token
    token_req = requests.get('https://opentdb.com/api_token.php?command=request')
    token = f"&token={token_req.json()['token']}"

    def iniciar_jogo_inf(e):
        global categoria_selecionada
        global dificuldade
        global tipo_de_pergunta
        global parametro
        global token
        global nome

        #Procura as opções selecionadas pelo jogador e as adiciona ao parametro de requisição
        if categoria_selecionada:
            if categoria_selecionada != 'Qualquer':
                parametro +=f'&category={categoria_selecionada}'
        if dificuldade:
            if dificuldade != 'Qualquer dificuldade':
                parametro+=f'&difficulty={dificuldade}'
        if tipo_de_pergunta:
            if tipo_de_pergunta != 'Qualquer tipo':
                parametro+=f'&type={tipo_de_pergunta}'

        nome = encontrar_ctr("input_nome").value
        
        #Adiciona o token a requisição e limpa as campos de questao atual e tipo
        parametro+=token
        questao_atual.value = ''
        questao_tipo.value = ''
        buscar_dados(0, 1)

    #Duas versões da mesma função porém com game_mode diferente
    #Isso foi feito para conseguir rodar essas funções em uma função lambda sem parametros
    def iniciar_jogo_normal(e):
        global categoria_selecionada
        global dificuldade
        global tipo_de_pergunta
        global parametro
        global token
        global nome
        if categoria_selecionada:
            if categoria_selecionada != 'Qualquer':
                parametro +=f'&category={categoria_selecionada}'
        if dificuldade:
            if dificuldade != 'Qualquer Dificuldade':
                parametro+=f'&difficulty={dificuldade}'
        if tipo_de_pergunta:
            if tipo_de_pergunta != 'Qualquer Tipo':
                parametro+=f'&type={tipo_de_pergunta}'

        campo_nome = encontrar_ctr("input_nome")
        if campo_nome.value:
            nome = campo_nome.value
        else:
            nome = '???'
        
        parametro+=token
        questao_atual.value = ''
        questao_tipo.value = ''
        buscar_dados(0, 2)


    #Configuração dos Dropdowns
    opcoes_tipos = []

    opcoes_tipos.append(ft.DropdownOption(key='Qualquer Tipo', content=ft.Text(value='Qualquer tipo')))
    opcoes_tipos.append(ft.DropdownOption(key='boolean', content=ft.Text(value='Verdadeiro ou Falso')))
    opcoes_tipos.append(ft.DropdownOption(key='multiple', content=ft.Text(value='Múltipla escolha')))

    dificuldades = []

    dificuldades.append(ft.DropdownOption(key='Qualquer Dificuldade', content=ft.Text(value='Qualquer dificuldade')))
    dificuldades.append(ft.DropdownOption(key='easy', content=ft.Text(value='Fácil')))
    dificuldades.append(ft.DropdownOption(key='medium', content=ft.Text(value='Médio')))
    dificuldades.append(ft.DropdownOption(key='hard', content=ft.Text(value='Difícil')))

    categorias = [{'id':'Qualquer','name':'Qualquer Categoria'},{"id":9,"name":"Conhecimento Geral"},{"id":10,"name":"Livros"},{"id":11,"name":"Filmes"},{"id":12,"name":"Música"},{"id":13,"name":"Teatro e Musicais"},{"id":14,"name":"Televisão"},{"id":15,"name":"Video Games"},{"id":16,"name":"Jogos de Tabuleiro"},{"id":17,"name":"Ciências e Natureza"},{"id":18,"name":"Computadores"},{"id":19,"name":"Matemática"},{"id":20,"name":"Mitologias"},{"id":21,"name":"Esportes"},{"id":22,"name":"Geografia"},{"id":23,"name":"História"},{"id":24,"name":"Politica"},{"id":25,"name":"Arte"},{"id":26,"name":"Celebridades"},{"id":27,"name":"Animais"},{"id":28,"name":"Veiculos"},{"id":29,"name":"Quadrinhos"},{"id":30,"name":"Ferramentas"},{"id":31,"name":"Anime e Mangá"},{"id":32,"name":"Desenhos e Animações"}]

    def categorias_func():
        categorias_dd = []
        for categoria in categorias:
            categorias_dd.append(
                ft.DropdownOption(
                    key=categoria['name'],
                    data=categoria['id'],
                    content=ft.Text(
                        value=categoria['name'],
                    ),
                )
            )
        return categorias_dd

    def dropdown_changed(e):
        e.control.color = e.control.data
        global categoria_selecionada
        categoria_selecionada = encontrar_id_categoria(page.controls[0].value)
        page.update()

    def dropdown_changed2(e):
        e.control.color = e.control.data
        global dificuldade
        dificuldade = page.controls[1].value
        page.update()

    def dropdown_changed3(e):
        e.control.color = e.control.data
        global tipo_de_pergunta
        tipo_de_pergunta = page.controls[2].value
        page.update()

    dd = ft.Dropdown(
        editable=True,
        label="Categorias",
        options=categorias_func(),
        on_change=dropdown_changed,
        key='dd'
    )

    dd2 = ft.Dropdown(
        editable=True,
        label="Dificuldade",
        options=dificuldades,
        on_change=dropdown_changed2,
        key='dd2'
    )

    dd3 = ft.Dropdown(
        editable=True,
        label="Tipos de pergunta",
        options=opcoes_tipos,
        on_change=dropdown_changed3,
        key='dd3'
    )

    page.controls.append(dd)
    page.controls.append(dd2)
    page.controls.append(dd3)
    page.update()

    def inicio(e=0,vitoria=False):
        #Função que recria a tela inicial do jogo ao ganhar/perder e exibe uma mensagem e leaderboard
        global token
        global game_mode
        #Reseta o token para que as perguntas sejam resetadas
        requests.get(f'https://opentdb.com/api_token.php?command=reset&token={token}')
        if vitoria:
            questao_atual = ft.Text('VOCE VENCEU !!!!!!!!!!', key='questao_atual')
        else:
            questao_atual = ft.Text('VOCE PERDEU !!!!!!!', key='questao_atual')

        #Busca leaderboard do banco de dados do modo de jogo selecionado
        if game_mode == 2:
            scoreboard = cursor.execute("SELECT nome, pontuacao FROM recordes_fin ORDER BY pontuacao DESC LIMIT 5")
            #lst_scoreboard = scoreboard.fetchall()
            #questao_tipo = ft.Text(str(lst_scoreboard), key='questao_atual1')
            questao_tipo = ft.Text("Pontuação           Nome\n\n", key='questao_atual1')
            for row in scoreboard:
                nome, pont = row
                questao_tipo.value+=f"      {pont}                     {nome}\n\n"
        elif game_mode == 1:
            scoreboard = cursor.execute("SELECT nome, pontuacao FROM recordes_inf ORDER BY pontuacao DESC LIMIT 5")
            #lst_scoreboard = scoreboard.fetchall()
            #questao_tipo = ft.Text('str(lst_scoreboard)', key='questao_atual1')
            questao_tipo = ft.Text("Pontuação           Nome\n\n", key='questao_atual1')
            for row in scoreboard:
                nome, pont = row
                questao_tipo.value+=f"      {pont}                     {nome}\n\n"
        game_mode = 0
        botao3 = ft.ElevatedButton("Iniciar Infinito", on_click=iniciar_jogo_inf, key='botao_inicio_inf')
        botao4_ = ft.ElevatedButton("Iniciar Finito", on_click=iniciar_jogo_normal, key='botao_inicio_fin')

        a =[dd, dd2, dd3, nome_input, botao3, botao4_, pontuacao_txt, questao_atual, questao_tipo, questao_dificuldade, questao_categoria, questao_body, resultado, erros_exibicao]
        for i in a:
            page.controls.append(i)

        # print("\n\n\n\n\n\nINICIO ATIVADO")
        # print(page.controls)
        page.update()


    def reset(e=0,vitoria=False):
        #Reseta todos os padroes aos iniciais e apaga todos elementos da tela
        global questao_num
        global dados
        global numero_a_exibir
        global loop
        global pontuacao
        global erros
        global parametro

        questao_num = 0
        numero_a_exibir = 0
        dados = []
        loop = 0
        pontuacao = 0
        erros = 0
        parametro = 'https://opentdb.com/api.php?amount=10'
        for ctr in page.controls:
            if 'questao_atual' in ctr.key:
                #print(ctr.value)
                ctr.value = ''
                

        page.controls.clear()


        # remover = []
        # for ctr in page.controls:
        #     print(ctr)
        #     print(isinstance(ctr, ft.ElevatedButton))
        #     print(isinstance(ctr, ft.Dropdown))
        #     if 'questao_atual' not in ctr.key:
        #         remover.append(ctr)
        #     else:
        #         ctr.value = ''

        # for i in remover:
        #     page.controls.remove(i)

        # print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nRESET ATIVADO')
        # print(page.controls)
        inicio(0,vitoria)

    def buscar_dados(e, modo=game_mode, new_game=True):
        #Usa os parametros definidos anteriormente para fazer o request de perguntas e retorna-las
        global questao_num
        global dados
        global numero_a_exibir
        global loop
        global game_mode
        global parametro
        game_mode = modo

        remover = []
        for ctr in page.controls:
            if(isinstance(ctr, ft.ElevatedButton)):
                if 'botao_inicio' in ctr.key:
                    remover.append(ctr)
            elif(isinstance(ctr, ft.Dropdown)):
                remover.append(ctr)
            elif(isinstance(ctr, ft.TextField)):
                remover.append(ctr)
            #elif ctr.key == "texto_resultado":
                #remover.append(ctr)

        for i in remover:
            page.controls.remove(i)

        page.update()

        if new_game == True or questao_num == 10:
            if questao_num ==10:
                loop+=1
            response = requests.get(parametro)
            #print(len(response.json()['results']))
            questao_num = 0
            dados = response.json()['results']
        else:
            response = dados

        if response.status_code == 200:
            if response.json()['response_code'] == 0:
                game_loop(game_mode)
        else:
            resultado.value = "Erro"
            print("ERRO")
        page.update()

    def responder(selecionada, correta):
        resultado.value = "Correto" if selecionada == correta else "Errado"
        resultado.size = 20

        if resultado.value == "Correto":
            global pontuacao
            pontuacao +=1
            pontuacao_txt.value = f'Pontuação: {pontuacao}'
        elif resultado.value == 'Errado':
            global erros
            if type(erros_exibicao.value) != str:
                erros+=1
                erros_exibicao.value ='❌'
            else:
                erros+=1
                erros_exibicao.value += '❌'
               
        page.update()
        global game_mode
        game_loop(game_mode)
        #buscar_dados(0,game_mode,False)

    #def next():

    def game_loop(game_mode):
        #Loop de gameplay do jogo
        #Pega as perguntas do request e as traduz
        #Exibe as perguntas, cria os botões de resposta, tudo traduzido
        global questao_num
        global numero_a_exibir
        global loop
        global erros
        global dados
        global pontuacao
        global nome

        for ctr in page.controls:
            if ctr.key =='questao_atual':
                questao_atual = ctr
            if ctr.key =='questao_atual1':
                questao_tipo = ctr

        if game_mode!=0:
        #MODO NORMAL
            resultado.value = ''

            if questao_num == 11 and game_mode==1:
                buscar_dados(0, game_mode, False)
            elif questao_num == 10 and game_mode==2:
                if not nome:
                    nome = "???"
                elif len(nome) > 3:
                    nome = nome[:3]
                dados_bd = [nome, pontuacao]

                if game_mode == 2:
                    cursor.execute("INSERT INTO recordes_fin VALUES (?, ?)", dados_bd)
                    con.commit()
                elif game_mode == 1:
                    cursor.execute("INSERT INTO recordes_inf VALUES (?, ?)", dados_bd)
                    con.commit()
                reset(0,True)
                return

            if erros == 3:
                if not nome:
                    nome = "???"
                elif len(nome) > 3:
                    nome = nome[:3]
                dados_bd = [nome, pontuacao]

                if game_mode == 2:
                    cursor.execute("INSERT INTO recordes_fin VALUES (?, ?)", dados_bd)
                    con.commit()
                elif game_mode == 1:
                    cursor.execute("INSERT INTO recordes_inf VALUES (?, ?)", dados_bd)
                    con.commit()
                reset()
                return
            

            response = dados
            data = response[questao_num-1]
            #print(data)
            respostas = [unescape(x) for x in data['incorrect_answers']]
            respostas.append(unescape(data['correct_answer']))
            respostas_str = ''

            #Junta a pegunta e opções para criar uma unica frase com todos elementos permitindo fazer toda a tradução com uma unica query/request
            #Separa a pergunta e opções com um / para evitar erro em separações com virgula
            for x in respostas:
                respostas_str+=x+'/ '

            q = (respostas_str+unescape(data['question'])).split('/ ')

            try:
                lbt_response = requests.post(
                        "http://localhost:5000/translate",
                        headers={ "Content-Type": "application/json" },
                        json={
                            "q": (respostas_str+unescape(data['question'])).split('/ '),
                            "source": "en",
                            "target": "pb",
                            "format": "text",
                            "alternatives": 2
                            }
                    )
                if lbt_response.status_code == 200:
                    print("TRADUZIDO")
                    traducao = lbt_response.json()["translatedText"]
                    
                    #print(len(traducao))
                    
                    if unescape(data['type'])== 'boolean':
                        wrong = traducao[0]
                        right = traducao[1] 
                        question = ' '.join(traducao[2:])
                    else:
                        wrong = traducao[:3]
                        right = traducao[3]
                        question = ' '.join(traducao[4:])

                    questao_body.value = question
                    #print(traducao)
                else:
                    print("ERRO AO TRADUZIR")
                    #print(lbt_response.text)

            except Exception as e:
                print(e)
                print("ERRO NA REQUISIÇÃO")

                traducao = q

                if unescape(data['type'])== 'boolean':
                    wrong = traducao[0]
                    right = traducao[1] 
                    question = ' '.join(traducao[2:])
                else:
                    wrong = traducao[:3]
                    right = traducao[3]
                    question = ' '.join(traducao[4:])

                questao_body.value = question
            
            questao_tipo.value = unescape(data['type'])
            questao_dificuldade.value = unescape(data['difficulty'])
            questao_categoria.value = unescape(data['category'])
            
            pontuacao_txt.value = f'Pontuação: {pontuacao}'
            
            i = 1
            num_rnd = randint(1,4)

            page.controls = [ctrl for ctrl in page.controls if not (isinstance(ctrl, ft.ElevatedButton) and ctrl.key and ctrl.key.startswith("botao_erro"))]
            page.controls = [ctrl for ctrl in page.controls if not (isinstance(ctrl, ft.ElevatedButton) and ctrl.key and ctrl.key.startswith("RESPOSTA_CORRETA"))]
            
            # for ctr in page.controls:
            #     print(ctr)
            if unescape(data['type']) != 'boolean':
                for resposta in wrong:
                    if i == num_rnd:
                        botao1 = ft.ElevatedButton(right, key="RESPOSTA_CORRETA", on_click=lambda e: responder(right,right))
                        page.controls.append(botao1)

                    botao_novo = ft.ElevatedButton(unescape(resposta), on_click=lambda e: responder(resposta,right), key=f'botao_erro1')
                    i+=1
                    page.controls.append(botao_novo)

                if not encontrar_ctr("RESPOSTA_CORRETA"):
                        botao1 = ft.ElevatedButton(right, key="RESPOSTA_CORRETA", on_click=lambda e: responder(right,right))
                        page.controls.append(botao1)

            else:
                opcoes = [ft.ElevatedButton(right, key="RESPOSTA_CORRETA", on_click=lambda e: responder(right,right)), ft.ElevatedButton(wrong, on_click=lambda e: responder(wrong,right), key=f'botao_erro1')]
                botao_2 = opcoes.pop(randint(0,1))
                page.controls.append(botao_2)

                page.controls.append(opcoes[0])
            encontrar_ctr("RESPOSTA_CORRETA")

            questao_num+=1
            numero_a_exibir = questao_num + loop*10
            questao_atual.value = f"Questão {numero_a_exibir}"
            page.update()

    def encontrar_ctr(key):
        for ctr in page.controls:
            if(isinstance(ctr, ft.ElevatedButton)):
                if(ctr.key) == key:
                    global correto
                    correto = ctr
                    return ctr
                
            elif(isinstance(ctr, ft.TextField)):
                if ctr.key == key:
                    return ctr
        return False
    
    def encontrar_id_categoria(name):
        global categoria_selecionada
        for i in categorias:
            if i['name'] == name:
                return i['id']
    
    botao = ft.ElevatedButton("Iniciar Infinito", on_click=iniciar_jogo_inf, key='botao_inicio_inf')
    botao_ = ft.ElevatedButton("Iniciar Finito", on_click=iniciar_jogo_normal, key='botao_inicio_fin')

    page.add(nome_input, botao, botao_, pontuacao_txt, questao_atual, questao_tipo, questao_dificuldade, questao_categoria, questao_body, resultado, erros_exibicao)

ft.app(main)