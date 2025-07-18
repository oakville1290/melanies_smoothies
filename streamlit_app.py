# Import python packages
import streamlit as st

import requests
#from snowflake.snowpark.context import get_active_session
#streamlit.title('My Parents New Healthy Diner')
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)


name_on_order =st.text_input('Name on Smoothies:')
st.write('The name on your Smoothie will be:',name_on_order)

from snowflake.snowpark.functions import col
#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
pd_df=my_dataframe.to_pandas()
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
ingredients_list = st.multiselect('Choose up to 5 ingredients:',my_dataframe)
if ingredients_list:
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://www.fruityvice.com/api/fruit/" + search_on)
        fv_df= st.dataframe(data=fruityvice_response.json(),use_container_width=True)
        #smoothiefroot_response = requests.get("https://www.fruityvice.com/api/fruit/watermelon")
        #sf_df= st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)


                    
