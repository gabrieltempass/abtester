import random
import math
import numpy as np
import pandas as pd
import statsmodels.stats.api as sms
import streamlit as st

# Set browser tab title, favicon and link to get help
st.set_page_config(
    page_title='A/B Tester',
    # page_icon=':heart:',
    menu_items={
        'Get help': None,
        'Report a bug': 'https://github.com/gabrieltempass/ab-tester/issues/new?title=Your%20issue%20title%20here&body=Your%20issue%20description%20here.',
        'About': 'This app was made by Gabriel Tem Pass. You can check the source code at [https://github.com/gabrieltempass/ab-tester](https://github.com/gabrieltempass/ab-tester).'
    }
)

# Hide top right menu and "Made with Streamlit" footer
hide_menu_style = '''
	<style>
	MainMenu {visibility: hidden; }
	footer {visibility: hidden;}
	</style>
'''
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.title('A/B Tester')
option = st.selectbox(
    'What do you want to do?',
    ('Select an option',
     'Calculate the minimum sample size',
     'Evaluate the statistical significance'))

if option == 'Calculate the minimum sample size':
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

	alternative = st.radio(
	    label='Hypothesis',
	    options=('One-sided', 'Two-sided'),
	    index=1,
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

	# Format the variables according to the function requirements
	control_conversion = control_conversion/100
	sensitivity = sensitivity/100
	treatment_conversion = control_conversion*(1 + sensitivity)
	if alternative == 'One-sided':
		alternative = 'smaller'
	else:
		alternative = 'two-sided'
	confidence_level = confidence_level/100
	alpha = 1 - confidence_level
	power = power/100

	if not(st.button('Calculate')):
		st.stop()

	effect_size = sms.proportion_effectsize(control_conversion,
										   treatment_conversion)
	analysis = sms.TTestIndPower()
	min_sample = math.ceil(analysis.solve_power(effect_size,
												power=power,
												alpha=alpha,
												ratio=1,
												alternative=alternative))

	st.subheader(min_sample)

	code = f'''
# Import the libraries
import math
import statsmodels.stats.api as sms

# Define the parameters
control_conversion = {control_conversion}
sensitivity = {sensitivity}
treatment_conversion = control_conversion*(1 + sensitivity)
alternative = '{alternative}'
confidence_level = {confidence_level}
alpha = 1 - confidence_level
power = {power}

# Calculate the minimum sample
effect_size = sms.proportion_effectsize(
    control_conversion,
    treatment_conversion
)
analysis = sms.TTestIndPower()
min_sample = math.ceil(analysis.solve_power(
    effect_size,
    power=power,
    alpha=alpha,
    ratio=1,
    alternative=alternative
))

# Show the result
print(min_sample)
	'''

	with st.expander('Show the code'):
		st.code(code, language='python')

if option == 'Evaluate the statistical significance':
	st.header('Statistical significance')

	def perm_fun(x, nA, nB):
	    n = nA + nB
	    idx_A = set(random.sample(range(n), nB))
	    idx_B = set(range(n)) - idx_A
	    return x.loc[idx_B].mean() - x.loc[idx_A].mean()

	test = st.radio(
	    label='Test',
	    options=('Proportions', 'Means'),
	    index=0)

	if test == 'Proportions':

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

		control_conversions = st.number_input(
			label='Conversions from the control',
			min_value=0,
			value=1219,
			step=1)

		treatment_conversions = st.number_input(
			label='Conversions from the treatment',
			min_value=0,
			value=1247,
			step=1)

		confidence_level = st.slider(
		    label='Confidence level',
		    min_value=70,
		    max_value=99,
		    value=95,
		    format='%d%%',
		    key='post-test')

		confidence_level = confidence_level/100
		alpha = 1 - confidence_level

		if not(st.button('Calculate')):
			st.stop()

		control_effect = control_conversions/control_users
		treatment_effect = treatment_conversions/treatment_users
		observed_diff = treatment_effect - control_effect

		conversion = [0]*(control_users + treatment_users)
		conversion.extend([1]*(control_conversions + treatment_conversions))
		conversion = pd.Series(conversion)

		perm_diffs = []
		i = 100
		my_bar = st.progress(0)
		for percent_complete in range(i):
			perm_diffs.append(perm_fun(
				conversion,
				control_users + control_conversions,
				treatment_users + treatment_conversions))
			my_bar.progress((percent_complete + 1)/i)

		p_value = np.mean([diff > observed_diff for diff in perm_diffs])

		st.subheader('Result')
		if p_value <= alpha:
			st.success('The difference is statistically significant')
		else:
			st.error('The difference is not statistically significant')
		st.write(f'Control conversion: {control_effect:.2%}')
		st.write(f'Treatment conversion: {treatment_effect:.2%}')
		st.write(f'Observed difference: {observed_diff*100:+.2f} p.p. ({observed_diff/control_effect:+.2%})')
		st.write(f'p-value: {p_value:.2f}')

		code = f'''
# Import the libraries
import random
import numpy as np
import pandas as pd

# Declare the permutation function
def perm_fun(x, nA, nB):
    n = nA + nB
    idx_A = set(random.sample(range(n), nB))
    idx_B = set(range(n)) - idx_A
    return x.loc[idx_B].mean() - x.loc[idx_A].mean()

# Define the parameters
control_users = {control_users}
treatment_users = {treatment_users}
control_conversions = {control_conversions}
treatment_conversions = {treatment_conversions}
confidence_level = {confidence_level}
alpha = 1 - confidence_level

# Calculate the observed difference
control_effect = control_conversions/control_users
treatment_effect = treatment_conversions/treatment_users
observed_diff = treatment_effect - control_effect

# Create the pool to draw the samples
conversion = [0]*(control_users + treatment_users)
conversion.extend([1]*(control_conversions + treatment_conversions))
conversion = pd.Series(conversion)

# Execute the permutation test
perm_diffs = []
for _ in range(1000):
    perm_diffs.append(perm_fun(
        conversion,
        control_users + control_conversions,
        treatment_users + treatment_conversions))

# Calculate the p-value
p_value = np.mean([diff > observed_diff for diff in perm_diffs])

# Show the result
if p_value <= alpha:
    print(f'The difference is statistically significant')
else:
    print(f'The difference is not statistically significant')
print(f'Control conversion: {{control_effect:.2%}}')
print(f'Treatment conversion: {{treatment_effect:.2%}}')
print(f'Observed difference: {{observed_diff*100:+.2f}} p.p. ({{observed_diff/control_effect:+.2%}})')
print(f'p-value: {{p_value:.2f}}')
		'''

		with st.expander('Show the code'):
			st.code(code, language='python')

	else:

		uploaded_file = st.file_uploader("Choose a file")
		if uploaded_file is not None:
		    dataframe = pd.read_csv(uploaded_file)
		    st.write('File uploaded. Preview of the first 10 rows:')
		    st.dataframe(dataframe.head(10), height=1000)
		else:
			st.write('The file must have each row with a unique user. One column named "group", with the user classification as "control" or "treatment". And one column named "measurement", with the value of the metric for the respective user. Below is an example of how the file should look like:')
			sample = pd.read_csv('data_sample.csv')
			st.dataframe(sample, height=1000)

		confidence_level = st.slider(
		    label='Confidence level',
		    min_value=70,
		    max_value=99,
		    value=95,
		    format='%d%%',
		    key='post-test')

		confidence_level = confidence_level/100
		alpha = 1 - confidence_level

		if not(st.button('Calculate')):
			st.stop()

		measurements = dataframe['measurement']
		control_users = dataframe[dataframe['group'] == 'control'].shape[0]
		treatment_users = dataframe[dataframe['group'] == 'treatment'].shape[0]

		control_mean = dataframe[dataframe['group'] == 'control']['measurement'].mean()
		treatment_mean = dataframe[dataframe['group'] == 'treatment']['measurement'].mean()
		observed_diff = treatment_mean - control_mean

		perm_diffs = []
		i = 100
		my_bar = st.progress(0)
		for percent_complete in range(i):
			perm_diffs.append(perm_fun(
				measurements,
				control_users,
				treatment_users))
			my_bar.progress((percent_complete + 1)/i)

		p_value = np.mean(perm_diffs > observed_diff)

		st.subheader('Result')
		if p_value <= alpha:
			st.success('The difference is statistically significant')
		else:
			st.error('The difference is not statistically significant')
		st.write(f'Control mean: {control_mean:.2f}')
		st.write(f'Treatment mean: {treatment_mean:.2f}')
		st.write(f'Observed difference: {observed_diff/control_mean:+.2%}')
		st.write(f'p-value: {p_value:.2f}')

		code = f'''
# Import the libraries
import random
import numpy as np
import pandas as pd

# Declare the permutation function
def perm_fun(x, nA, nB):
    n = nA + nB
    idx_A = set(random.sample(range(n), nB))
    idx_B = set(range(n)) - idx_A
    return x.loc[idx_B].mean() - x.loc[idx_A].mean()

# Define the parameters
confidence_level = {confidence_level}
alpha = 1 - confidence_level

# Get the measurements and count the users
measurements = dataframe['measurement']
control_users = dataframe[dataframe['group'] == 'control'].shape[0]
treatment_users = dataframe[dataframe['group'] == 'treatment'].shape[0]

# Calculate the observed difference
control_mean = dataframe[dataframe['group'] == 'control']['measurement'].mean()
treatment_mean = dataframe[dataframe['group'] == 'treatment']['measurement'].mean()
observed_diff = treatment_mean - control_mean

# Execute the permutation test
perm_diffs = []
for _ in range(1000):
    perm_diffs.append(perm_fun(
        measurements,
        control_users,
        treatment_users))

# Calculate the p-value
p_value = np.mean(perm_diffs > observed_diff)

# Show the result
if p_value <= alpha:
    print('The difference is statistically significant')
else:
    print('The difference is not statistically significant')
print(f'Control mean: {{control_mean:.2f}}')
print(f'Treatment mean: {{treatment_mean:.2f}}')
print(f'Observed difference: {{observed_diff/control_mean:+.2%}}')
print(f'p-value: {{p_value:.2f}}')
		'''

		with st.expander('Show the code'):
			st.code(code, language='python')