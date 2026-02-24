import streamlit as st

from apputil import *

# Load Titanic dataset
df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

st.write(
'''
"Was the term 'save the children' accurate for the Titanic? Or just for the higher classes?"

'''
)
# Generate and display the figure
fig1 = visualize_demographic()
st.plotly_chart(vi, use_container_width=True)

st.write(
'''
"These findings from the last name counts seem odd to me because if there are 25 passengers with a family size of 7+ then how come only 2 last names have 7+ unique people?
How much was first class really on average and how does that compare to the other tickets?"
'''
)
# Generate and display the figure
fig2 = visualize_families()
st.plotly_chart(fig2, use_container_width=True)

st.write(
'''
# Titanic Visualization Bonus
'''
)
# Generate and display the figure
fig3 = visualize_family_size()
st.plotly_chart(fig3, use_container_width=True)
