import flet as ft
import requests
from html import unescape

questao_num = 0

def main(page: ft.Page):
    questao_atual = ft.Text()
    questao_tipo = ft.Text()
    questao_dificuldade = ft.Text()
    questao_categoria = ft.Text()
    questao_body = ft.Text()
    questao_correto = ft.Text()
    questao_errados = ft.Text()

    resultado = ft.Text(key="texto_resultado")

    def buscar_dados(e):
        response = requests.get("https://opentdb.com/api.php?amount=1")
        if response.status_code == 200:
            data = response.json()['results'][0]
            questao_tipo.value = unescape(data['type'])
            questao_dificuldade.value = unescape(data['difficulty'])
            questao_categoria.value = unescape(data['category'])
            questao_body.value = unescape(data['question'])

            botao1 = ft.ElevatedButton(unescape(data['correct_answer']), on_click=lambda e: responder(unescape(data['correct_answer']),unescape(data['correct_answer'])))
            page.add(botao1)

            for resposta in data['incorrect_answers']:
                botao_novo = ft.ElevatedButton(unescape(resposta), on_click=lambda e: responder(unescape(resposta),unescape(data['correct_answer'])))
                page.add(botao_novo)
            #questao_correto.value = unescape(data['correct_answer'])
            #questao_errados.value = unescape(data['incorrect_answers'])

            global questao_num
            questao_num +=1
            questao_atual.value = f"Questão {questao_num}"
        else:
            resultado.value = "Erro"
        page.update()

    def responder(selecionada, correta):
        resultado.value = "Correto" if selecionada == correta else "Errado"
        page.update()
        #print(page.controls[-1])
        #print(ft.Text(value='Correto') in page.controls)
        #print(page.get_control("texto_resultado"))
        
        #if page.get_control("texto_resultado"):
        #    page.controls.remove(page.get_control("texto_resultado"))
            

        #if selecionada == correta:
        #    result = ft.Text(value="Correto", key='texto_resultado')
        #else:
         #   result = ft.Text(value="Errado", key='texto_resultado')
        #page.add(result)


    botao = ft.ElevatedButton("Buscar dados da API", on_click=buscar_dados)

    page.add(botao, questao_atual, questao_tipo, questao_dificuldade, questao_categoria, questao_body, questao_correto, questao_errados, resultado)

ft.app(main)
