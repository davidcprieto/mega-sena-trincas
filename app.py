import streamlit as st
import pandas as pd
from itertools import combinations

st.title("Análise Estatística da Mega-Sena por Trincas")

uploaded_file = st.file_uploader("Faça o upload da planilha da Mega-Sena (.csv)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    dezenas_cols = ['Dezena 1', 'Dezena 2', 'Dezena 3', 'Dezena 4', 'Dezena 5', 'Dezena 6']
    df_valid = df.dropna(subset=dezenas_cols).copy()
    df_valid[dezenas_cols] = df_valid[dezenas_cols].astype(int)

    ultimo_concurso = df_valid.iloc[0]
    numeros_ultimo_concurso = ultimo_concurso[dezenas_cols].tolist()
    trincas = list(combinations(sorted(numeros_ultimo_concurso), 3))

    st.subheader(f"Último concurso completo: {int(ultimo_concurso['Concurso'])}")
    st.write("Números sorteados:", numeros_ultimo_concurso)
    st.write("Trincas geradas:", trincas)

    historico = df_valid.iloc[1:].reset_index(drop=True)
    numeros_pos_trinca = []
    for trinca in trincas:
        trinca_set = set(trinca)
        for idx in range(len(historico) - 1):
            dezenas_concurso = set(historico.loc[idx, dezenas_cols])
            if trinca_set.issubset(dezenas_concurso):
                numeros_seguinte = historico.loc[idx + 1, dezenas_cols].tolist()
                numeros_pos_trinca.extend(numeros_seguinte)

    if numeros_pos_trinca:
        frequencia = pd.Series(numeros_pos_trinca).value_counts().sort_values(ascending=False)
        aposta_principal = sorted(frequencia.head(6).index.tolist())
        variacoes_possiveis = sorted(frequencia.iloc[6:10].index.tolist())

        st.subheader("Resultado da Análise")
        st.markdown("**Aposta Principal (6 mais frequentes):**")
        st.write(aposta_principal)
        st.markdown("**Variações Possíveis (4 seguintes mais frequentes):**")
        st.write(variacoes_possiveis)
    else:
        st.warning("Nenhuma trinca encontrada no histórico anterior.")
