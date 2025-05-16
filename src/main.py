import flet as ft
import requests
from html import unescape
from random import randint

questao_num=0
numero_a_exibir = 0
dados = []
loop = 0
pontuacao = 0

def main(page: ft.Page):
    global pontuacao

    questao_atual = ft.Text()
    questao_tipo = ft.Text()
    questao_dificuldade = ft.Text()
    questao_categoria = ft.Text()
    questao_body = ft.Text()
    pontuacao_txt = ft.Text(str(pontuacao))

    resultado = ft.Text(key="texto_resultado")

    def buscar_dados(e,new_game=True):
        global questao_num
        global dados
        global numero_a_exibir
        global loop

        if new_game == True or questao_num == 10:
            if questao_num ==10:
                loop+=1
            response = requests.get("https://opentdb.com/api.php?amount=10")
            print(len(response.json()['results']))
            questao_num = 0
            dados = response
        else:
            response = dados

        if response.status_code == 200:
            if response.json()['response_code'] == 0:
                data = response.json()['results'][questao_num-1]
                questao_tipo.value = unescape(data['type'])
                questao_dificuldade.value = unescape(data['difficulty'])
                questao_categoria.value = unescape(data['category'])
                questao_body.value = unescape(data['question'])
                
                i = 1
                num_rnd = randint(1,4)

                # if numero_a_exibir>0:
                #     #print(page.controls[-4:-1])
                #     while len(page.controls) >7:
                #         if not page.controls[-1].key == 'texto_resultado':
                #             page.controls.remove(page.controls[-1])

                # Remover apenas botões de resposta (ElevatedButton com chave específica)
                # for ctr in page.controls:
                #     print(ctr)

                page.controls = [ctrl for ctrl in page.controls if not (isinstance(ctrl, ft.ElevatedButton) and ctrl.key and ctrl.key.startswith("botao_erro"))]
                page.controls = [ctrl for ctrl in page.controls if not (isinstance(ctrl, ft.ElevatedButton) and ctrl.key and ctrl.key.startswith("RESPOSTA_CORRETA"))]
                
                # for ctr in page.controls:
                #     print(ctr)

                for resposta in data['incorrect_answers']:
                    if i == num_rnd:
                        botao1 = ft.ElevatedButton(unescape(data['correct_answer']), key="RESPOSTA_CORRETA", on_click=lambda e: responder(unescape(data['correct_answer']),unescape(data['correct_answer'])))
                        page.add(botao1)

                    botao_novo = ft.ElevatedButton(unescape(resposta), on_click=lambda e: responder(unescape(resposta),unescape(data['correct_answer'])), key=f'botao_erro1')
                    i+=1
                    page.controls.append(botao_novo)

                if not encontrar_ctr("RESPOSTA_CORRETA"):
                        print("ADICIONADO")
                        botao1 = ft.ElevatedButton(unescape(data['correct_answer']), key="RESPOSTA_CORRETA", on_click=lambda e: responder(unescape(data['correct_answer']),unescape(data['correct_answer'])))
                        page.controls.append(botao1)
                    #print(page.get_control(botao1.uid))
                #print(ft.ElevatedButton(unescape(data['correct_answer']), on_click=lambda e: responder(unescape(data['correct_answer']),unescape(data['correct_answer']))) in page.controls)

            questao_num+=1
            numero_a_exibir = questao_num + loop*10
            questao_atual.value = f"Questão {numero_a_exibir}"
        else:
            resultado.value = "Erro"
        page.update()

    def responder(selecionada, correta):
        resultado.value = "Correto" if selecionada == correta else "Errado"
        resultado.size = 20

        if resultado.value == "Correto":
            global pontuacao
            pontuacao +=1
            pontuacao_txt.value = f'Pontuação: {pontuacao}'
        
            
        page.update()
        buscar_dados(0,False)

    def encontrar_ctr(key):
        for ctr in page.controls:
            if(isinstance(ctr, ft.ElevatedButton)):
                if(ctr.key) == key:
                    return ctr
        return False
    botao = ft.ElevatedButton("Gerar questão", on_click=buscar_dados)

    page.add(botao, pontuacao_txt, questao_atual, questao_tipo, questao_dificuldade, questao_categoria, questao_body, resultado)

ft.app(main)
