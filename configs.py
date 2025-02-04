import streamlit as st

MODEL_NAME = 'gpt-3.5-turbo-0125'
RETRIEVAL_SEARCH_TYPE = 'mmr'
RETRIEVAL_KWARGS = {"k": 5, "fetch_k": 20}
PROMPT = '''Responda a pergunta do usuário com base no contexto abaixo:

Contexto:
{context}

Conversa atual:
{chat_history}
Human: {question}
AI: '''

# Dicionário de respostas fixas
RESPOSTAS_FIXAS = {
    "Qual foi o mês com maior despesa assistencial no ano de 2024?": """
    O mês com maior despesa assistencial em 2024 foi julho, com um total de R$ 272.189.212.

    Esse valor representa um aumento de +14,82% em relação à média dos meses anteriores 
    (janeiro a maio/2024) e um crescimento de +26,69% em comparação ao mesmo mês de 
    2023. Em termos absolutos, o aumento foi de R$ 35 milhões na primeira comparação e de 
    R$ 57 milhões na segunda.

    Além disso, os dados revelam uma tendência recorrente ao longo do ano, com um padrão 
    de alta em um mês seguida por duas quedas nos meses subsequentes. Essa tendência se 
    estabiliza a partir de setembro/2024, quando as despesas permanecem lineares até 
    dezembro de 2024, que registra o segundo menor valor do ano. Esse comportamento 
    pode estar relacionado ao período de férias, quando há menor utilização dos planos de 
    saúde, ou à postergação de despesas assistenciais para outros períodos.
   
    """,
    
    "Quais foram os maiores ofensores desse valor?": """
    Os 20 beneficiários com maior impacto nas despesas estão representados no gráfico 
    abaixo. O beneficiário com maior utilização (0064.XXXX.XXXXX-XX) consumiu R$ 
    467.820, o que corresponde a 8,10% do total acumulado pelos 20 principais 
    beneficiários. Os 7 primeiros beneficiários apresentam despesas acima da média, que é 
    de R$ 288.605,50.

    Vale destacar que esse mesmo beneficiário acumula R$ 1,85M em custo assistencial ao 
    longo de 2024, enquanto sua contribuição em faturamento bruto foi de apenas R$ 4.857. 

    Os 20 prestadores com maior impacto nas despesas também estão representados no 
    gráfico abaixo. O principal prestador, CEU, gerou um total de R$ 16,26M em despesas, 
    representando 15,55% do total dos 20 maiores. Entre eles, os 6 primeiros prestadores 
    apresentaram despesas superiores à média dos demais, que é de R$ 5,27M. 
    
    """,

    "Quais foram os principais procedimentos envolvidos?": """
    Para o beneficiário 0064.XXXX.XXXXX-XX, o total de despesas foi de R$ 467.820, sendo 
    que o procedimento ENHERTU 100 MG PO LIOF SOL INJ IV (MG) foi o maior responsável, 
    representando 28,78% do total. Este medicamento é utilizado no tratamento de câncer. 

    Outro fator relevante está relacionado ao Home Care Liminar, possivelmente decorrente 
    de uma decisão judicial que garantiu atendimento domiciliar dedicado. Além disso, 
    despesas significativas também foram observadas com diárias de UTI/Privativo ao 
    analisar os 20 beneficiários mais custosos. 

    Ao considerar os 20 procedimentos com maior impacto no mês de julho/2024, destaca-
    se um total de R$ 30 milhões em consultas e mais de R$ 5 milhões relacionados a 
    diárias de UTI. Outro item que merece atenção são as terapias especiais, que somaram 
    R$ 3,8 milhões no mesmo período. 

    Esses dados demonstram os principais fatores que impulsionaram os custos 
    assistenciais e destacam áreas críticas para análise e possíveis intervenções.
    """
}

def get_config(config_name):
    if config_name.lower() in st.session_state:
        return st.session_state[config_name.lower()]
    elif config_name.lower() == 'model_name':
        return MODEL_NAME
    elif config_name.lower() == 'retrieval_search_type':
        return RETRIEVAL_SEARCH_TYPE
    elif config_name.lower() == 'retrieval_kwargs':
        return RETRIEVAL_KWARGS
    elif config_name.lower() == 'prompt':
        return PROMPT
    elif config_name.lower() == 'respostas_fixas':
        return RESPOSTAS_FIXAS  # Retorna o dicionário de respostas fixas
