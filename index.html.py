from flask import Flask, request, jsonify, render_template
import random
import re

app = Flask(__name__)

historico_respostas = {
    "saudacoes": [],
    "despedidas": [],
    "IA": [],
    "azar": [],
    "piadas": []
}

def escolher_resposta(categoria: str, respostas_lista: list) -> str:
    usadas = historico_respostas[categoria]
    disponiveis = [r for r in respostas_lista if r not in usadas]

    if not disponiveis:  
        historico_respostas[categoria] = []
        disponiveis = respostas_lista

    resposta = random.choice(disponiveis)
    historico_respostas[categoria].append(resposta)
    return resposta

def obter_resposta_bot(mensagem: str) -> str:
    def contem_expressao(expressao: str) -> bool:
        padrao = rf"(?<!\w){re.escape(expressao)}(?!\w)"
        return re.search(padrao, mensagem, flags=re.IGNORECASE) is not None

    saudacoes = ['oi', 'ola', 'olá', 'opa', 'bom', 'bão', 'bao']
    despedidas = ["tchau", "adeus", "falou", 'fui', 'até mais', 'até logo']
    azar = ['impacta', 'impacto', 'importância', 'importante', 'desafio', 'contras']
    IAs = ['ia', 'ai', 'artificial', 'artificiais']
    comedias = ['piada', 'piadas', 'humor']
    politicas = ['guerra', 'presidente', 'eleições', 'eleiçoes', 'voto', 'vota']

    respostas_saudacoes = ['Oi, tudo bem?', 'Oi, como vai?', 'Olá, como posso ajudá-lo?', 'Opa! No que posso ajudar?']
    respostas_despedidas = ['Tchau', 'Adeus', 'Adios, mi amigo', 'Tchauzinho', 'Falou, rapá!']
    respostas_IA = ['Segundo a PUCRS, a IA em sua essência é a capacidade das máquinas de pensar como seres humanos. Ou seja, aprender, perceber e decidir quais caminhos seguir, de forma racional, diante de determinadas situações.',
        'Segundo a AMAZON, a Inteligência Artificial (IA) é uma tecnologia transformadora que permite que as máquinas realizem tarefas de resolução de problemas semelhantes às humanas. Desde o reconhecimento de imagens e a geração de conteúdo criativo até a realização de previsões orientadas por dados, a IA permite que as empresas tomem decisões mais inteligentes em grande escala.'    
    ]
    respostas_azar = ['Segundo o SENAC, o  desafio que a IA nos traz é a sua aplicação em áreas sensíveis da vida, como Saúde, Segurança e Finanças. Em alguns casos, a IA recebe certas responsabilidades que precisariam de intervenção humana, como uma tomada de decisão sobre um empréstimo ou a identificação de um possível delito.',
        'Segundo o SENAC, Um dos principais desafios que a IA nos impõe é o descompasso considerável entre o avanço tecnológico e a nossa capacidade de avaliar novas tecnologias.'   
    ]
    respostas_piadas = ['Sabe por que a galinha atravessou a rua? Para ver a missa do galo!(e todos riem)',
                        'Um empregado falou para o chefe: "É melhor o senhor me dar um aumento logo, pois saiba o senhor que tem três empresas atrás de mim", então o chefe perguntou: "Que empresas?". Duas horas depois, o funcionário estava na rua por ter respondido "A CEMIG, a COPASA e a TIM"',
                        'Fiquei confuso depois da aula de inglês. Se “car” significa carro e “men” significa “homens”, então minha tia Carmen é um Transformer?',
                        'Um caipira chega à casa de um amigo que estava vendo TV e pergunta: E aí, firme? O outro responde: Não, futebor!',
                        '"Alô, eu gostaria de falar com o João, por favor.". "É o próprio.". "Oi, é o Próprio falando?". "Sim!". "Passa pro João, por favor.".',
                        'Tinha dois caminhões voando. Um deles caiu. Por que o outro continuou voando? Porque era caminhão-pipa.',
                        'O bêbado atravessa a rua fora da faixa e um carro buzina para ele: “Bi-bi!”. O bêbado responde: “Eu também bibi, e não foi pouco não”.',
                        'Por que a aranha é o animal mais carente do mundo? Porque ela é um aracneedyou (kitunts).'
    ]
        
    

    if any(contem_expressao(s) for s in saudacoes):
        return escolher_resposta('saudacoes', respostas_saudacoes)
    elif any(contem_expressao(d) for d in despedidas):
        return escolher_resposta('despedidas', respostas_despedidas)
    elif any(contem_expressao(i) for i in IAs):
        return escolher_resposta('IA', respostas_IA)
    elif any(contem_expressao(a) for a in azar):
        return escolher_resposta('azar', respostas_azar)
    elif any(contem_expressao(c) for c in comedias):
        return escolher_resposta('piadas', respostas_piadas)
    elif any(contem_expressao(p) for p in politicas):
        return "Prefiro não me meter nesse assunto. Que tal perguntar sobre IAs?"

    elif contem_expressao == "outra":
        return historico_respostas
        
    return "Não tenho acervo suficiente para responder essa pergunta. Por favor, faça perguntas abrangentes sobre o tema do trabalho."

@app.route("/", methods=['GET'])
def index():
    return render_template("buttons.html")

@app.route("/ia", methods=['GET'])
def home():
   return render_template("AI.html")

@app.route("/blog", methods=['POST'])
def chat():
    dados = request.get_json()
    
    if not dados or "mensagem" not in dados:
        return jsonify({"erro": "Por favor, digite algo na propriedade 'mensagem'."}), 400
        
    mensagem_usuario = dados["mensagem"]
    resposta_ia = obter_resposta_bot(mensagem_usuario)
    
    return jsonify({"resposta": resposta_ia})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
