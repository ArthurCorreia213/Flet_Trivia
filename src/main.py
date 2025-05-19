import flet as ft
import requests
from html import unescape
from random import randint

parametro = 'https://opentdb.com/api.php?amount=10'

questao_num = 0
numero_a_exibir = 0
dados = []
loop = 0
pontuacao = 0
erros = 0

game_mode = 0
#GAME MODE 1 = INFINITO
#GAME MODE 2 = 10 perguntas

def main(page: ft.Page):
    global pontuacao

    questao_atual = ft.Text()
    questao_tipo = ft.Text()
    questao_dificuldade = ft.Text()
    questao_categoria = ft.Text()
    questao_body = ft.Text()
    pontuacao_txt = ft.Text()
    erros_exibicao = ft.Text()

    resultado = ft.Text(key="texto_resultado")

    def iniciar_jogo_inf(e):
        buscar_dados(0, 1)
    def iniciar_jogo_normal(e):
        buscar_dados(0, 2)

    def inicio(e=0):
            questao_atual = ft.Text()
            questao_tipo = ft.Text()
            questao_dificuldade = ft.Text()
            questao_categoria = ft.Text()
            questao_body = ft.Text()
            pontuacao_txt = ft.Text()
            erros_exibicao = ft.Text()
            botao3 = ft.ElevatedButton("Iniciar Infinito", on_click=iniciar_jogo_inf)
            botao4_ = ft.ElevatedButton("Iniciar Finito", on_click=iniciar_jogo_normal)

            a =[botao3, botao4_, pontuacao_txt, questao_atual, questao_tipo, questao_dificuldade, questao_categoria, questao_body, resultado, erros_exibicao]
            for i in a:
                page.controls.append(i)

            print("\n\n\n\n\n\nINICIO ATIVADO")
            print(page.controls)


    def reset(e=0):
        print("EJWQOEWIQJEOWQEIJWQOIE")
        global questao_num
        global dados
        global numero_a_exibir
        global loop
        global game_mode
        global pontuacao
        global erros

        questao_num = 0
        numero_a_exibir = 0
        dados = []
        loop = 0
        pontuacao = 0
        erros = 0
        game_mode = 0

        page.controls.clear()

        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nRESET ATIVADO')
        print(page.controls)
        inicio()

    def buscar_dados(e, modo=game_mode, new_game=True):
        global questao_num
        global dados
        global numero_a_exibir
        global loop
        global game_mode
        global parametro
        print("DJKDSKLAJD")
        game_mode = modo

        resultado.value = ''

        if new_game == True or questao_num == 10:
            if questao_num ==10:
                loop+=1
            response = requests.get(parametro)
            print(len(response.json()['results']))
            questao_num = 0
            dados = response
        else:
            response = dados

        if response.status_code == 200:
            if response.json()['response_code'] == 0:
                game_loop(game_mode, response.json()['results'])

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
        buscar_dados(0,game_mode,False)

    def game_loop(game_mode, dados_):
        global questao_num
        global numero_a_exibir
        global loop
        global erros
        if game_mode !=0:
            #MODO NORMAL

                if questao_num == 10 and game_mode==1:
                    buscar_dados(0, game_mode, False)

                if erros == 3:
                    reset()
                    return
                

                response = dados_
                data = response[questao_num-1]
                print(data)
                respostas = [unescape(x) for x in data['incorrect_answers']]
                respostas.append(unescape(data['correct_answer']))
                respostas_str = ''
                for x in respostas:
                    respostas_str+=x+'/ '
                print((respostas_str+unescape(data['question'])).split('/ '))
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
                        
                        print(len(traducao))
                        
                        if unescape(data['type'])== 'boolean':
                            wrong = traducao[0]
                            right = traducao[1] 
                            question = ' '.join(traducao[2:])
                        else:
                            wrong = traducao[:3]
                            right = traducao[3]
                            question = ' '.join(traducao[4:])

                        questao_body.value = question
                        print(traducao)
                    else:
                        print(unescape(data['question']))
                        print("ERRO AO TRADUZIR")
                        print(lbt_response.text)

                except Exception as e:
                    print(e)
                    print("ERRO NA REQUISIÇÃO")
                    questao_body.value = unescape(data['question'])

                
                questao_tipo.value = unescape(data['type'])
                questao_dificuldade.value = unescape(data['difficulty'])
                questao_categoria.value = unescape(data['category'])
                
                pontuacao_txt.value = str(pontuacao)
                
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
                            print("ADICIONADO")
                            botao1 = ft.ElevatedButton(right, key="RESPOSTA_CORRETA", on_click=lambda e: responder(right,right))
                            page.controls.append(botao1)

                else:
                    opcoes = [ft.ElevatedButton(right, key="RESPOSTA_CORRETA", on_click=lambda e: responder(right,right)), ft.ElevatedButton(wrong, on_click=lambda e: responder(wrong,right), key=f'botao_erro1')]
                    botao_2 = opcoes.pop(randint(0,1))
                    page.controls.append(botao_2)

                    page.controls.append(opcoes[0])


        questao_num+=1
        numero_a_exibir = questao_num + loop*10
        questao_atual.value = f"Questão {numero_a_exibir}"

    def encontrar_ctr(key):
        for ctr in page.controls:
            if(isinstance(ctr, ft.ElevatedButton)):
                if(ctr.key) == key:
                    return ctr
        return False
    
    botao = ft.ElevatedButton("Iniciar Infinito", on_click=iniciar_jogo_inf)
    botao_ = ft.ElevatedButton("Iniciar Finito", on_click=iniciar_jogo_normal)

    page.add(botao, botao_, pontuacao_txt, questao_atual, questao_tipo, questao_dificuldade, questao_categoria, questao_body, resultado, erros_exibicao)

ft.app(main)


#EXEMPLO API COM TODOS PARAMETROS :
#https://opentdb.com/api.php?amount=10&category=27&difficulty=easy&type=multiple