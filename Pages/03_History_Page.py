import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import os
import yaml
from yaml.loader import SafeLoader

st.set_page_config(
    page_title= 'History Page',
    page_icon = '📆',
    layout= 'wide'
)
###### Enryption
with open ('./config.yaml') as file:
    config = yaml.load(file,Loader=SafeLoader)
    
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)
#### log in side bar
authenticator.login(location='sidebar')

## accessing session state
auth_status = st.session_state.get("authentication_status",None)
username = st.session_state.get("username",None)
name = st.session_state.get("name",None)

if auth_status:
    authenticator.logout(location="sidebar")
    st.sidebar.success("select a page above")
    st.markdown('<h1 style="text-align: center;"><u><i><b> HISTORY PAGE </b></i></u></h1>', unsafe_allow_html=True)
    st.write ("""
              Welcome to the History Page. This section displays a record of patients’ data along with their heart disease prediction results.

Each entry includes:

The predicted outcome (whether the patient is likely to develop heart disease or not),

The probability/confidence score of the prediction,

And the date and time the prediction was made.

Use this page to track and review past predictions.
              """)
    def display_historic_data():
        csv_path='./Data/history_data.csv'
        csv_exists=os.path.exists(csv_path)
        if csv_exists:
            historic_data=pd.read_csv(csv_path) 
        return st.dataframe(historic_data)
        

    if __name__ == '__main__':
        display_historic_data() 
    
    
    
    
    
    
    
    
elif auth_status is False:
    st.error('username/password is incorrect')
    
elif auth_status is None:
    st.info("log in to access the page")
    st.code("""
            username: felixkwemoi
            password: Heart_Disease#0
            username: DonFelo
            password: Heart_Disease#1
            """)