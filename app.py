import scipy.stats
import streamlit as st
import time

st.header('Lanzar una moneda')

chart = st.line_chart([0.5])

def toss_coin(n): #funcion que emula el lanzamiento de la moneda
    trial_outcomes = scipy.stats.bernoilli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count+=1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(0.05)
    return mean
    
number_of_trials = st.slider('Numero de intentos?', 1, 1000, 10)
start_button = st.button('Ejecutar')

if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')


st.write('Esta aplicacion aun no funciona. En construccion.')
