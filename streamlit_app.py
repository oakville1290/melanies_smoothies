# Import python packages
import streamlit as st
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

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients:',my_dataframe)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen + ' '
    st.write(ingredients_string)
    my_insert_stmt =""" insert into smoothies.public.orders(ingredients,name_on_order) 
    values ('"""+ ingredients_string +"""','"""+name_on_order+"""')"""
    st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothies is ordered!')

import requests
smoothiefroot_response = requests.get("https://www.fruityvice.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())       
sf_df= st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
                    
