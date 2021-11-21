from random import random
import math
import statsmodels.stats.api as sms
import streamlit as st

# ability
# abacus

# Set browser tab title, favicon and sidebar initial state
st.set_page_config(
    page_title='A/B Tester',
    # page_icon=':heart:',
    initial_sidebar_state='expanded',
    menu_items={
        'Get help': 'https://im.xiaojukeji.com/channel?uid=74266&token=36cf8a878dfbd9658b08224ad09ded00&id=721670773793655296',
    }
)

# Hide top right menu and "Made with Streamlit" footer
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.title('A/B Tester')
st.header('Sample size')

control_conversion = st.number_input(
	label='Baseline conversion rate (%)',
	min_value=0.0,
	max_value=100.0,
	value=15.0,
	step=0.1,
	format='%.1f')

sensitivity = st.number_input(
	label='Sensitivity (%)',
	min_value=0.0,
	value=10.0,
	step=0.1,
	format='%.1f')

hypothesis = st.radio(
    label='Hypothesis',
    options=('One-sided', 'Two-sided'),
    key='pre-test')

confidence_level = st.slider(
    label='Confidence level',
    min_value=70,
    max_value=99,
    value=95,
    format='%d%%',
    key='pre-test')

power = st.slider(
    label='Power',
    min_value=70, 
    max_value=99,
    value=80,
    format='%d%%')

control_conversion = control_conversion/100
treatment_conversion = control_conversion*(1 + sensitivity/100)
alpha = 1 - confidence_level/100
power = power/100

if not(st.button('Calculate minimum sample size')):
	# st.stop()
	pass

es = sms.proportion_effectsize(control_conversion, treatment_conversion)
min_sample = math.ceil(sms.NormalIndPower().solve_power(es, power=power, alpha=alpha, ratio=1))
st.subheader(min_sample)

st.header('Result')

control_users = st.number_input(
	label='Users in the control',
	min_value=0,
	value=30000,
	step=1)

treatment_users = st.number_input(
	label='Users in the treatment',
	min_value=0,
	value=30000,
	step=1)

control_conversion_2 = st.number_input(
	label='Conversion rate from the control (%)',
	min_value=0.0,
	max_value=100.0,
	value=15.0,
	step=0.1,
	format='%.1f')

treatment_conversion_2 = st.number_input(
	label='Conversion rate from the treatment (%)',
	min_value=0.0,
	max_value=100.0,
	value=17.0,
	step=0.1,
	format='%.1f')

hypothesis2 = st.radio(
    label='Hypothesis',
    options=('One-sided', 'Two-sided'),
    key='post-test')

confidence_level2 = st.slider(
    label='Confidence level',
    min_value=70,
    max_value=99,
    value=95,
    format='%d%%',
    key='post-test')