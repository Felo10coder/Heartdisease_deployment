import streamlit as st 
from streamlit_option_menu import option_menu 
import streamlit_authenticator as stauth 
import pandas as pd
import yaml 
from yaml.loader import SafeLoader

## Page config
st.set_page_config(
    page_title="Data Page",
    page_icon="📊",
    layout="wide"
)

with open ('./config.yaml') as file:
    config = yaml.load(file,Loader=SafeLoader)
    
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)
## log in side bar
authenticator.login(location='sidebar')

## acccess sessionstate
auth_status = st.session_state.get('authentication_status',None)
username = st.session_state.get('username',None)
name = st.session_state.get('name',None)

## main app logic
if auth_status:
    authenticator.logout(location='sidebar')
    st.sidebar.success("select a page above")
    st.markdown('<h1 style="text-align: center;"><u><i><b> DATA PAGE </b></i></u></h1>', unsafe_allow_html=True)
    st.write("Welcome to the Data Page. Here, you'll find an overview of the dataset used in this heart disease prediction project and description of the features.")

    st.write("""
This project is built on a medical dataset containing health records of patients evaluated for heart disease.  
It includes various clinical features that are known to influence the risk of heart-related conditions.  
Below is a summary of the key features in the dataset.
""")
    
    st.markdown("""
| **Feature**  | **Description**                                                                                       |
|--------------|-------------------------------------------------------------------------------------------------------|
| **age**      | Age of the patient (in years).                                                                        |
| **sex**      | Sex of the patient (1 = male, 0 = female).                                                            |
| **cp**       | Chest pain type: <br> 0: Typical angina <br> 1: Atypical angina <br> 2: Non-anginal pain <br> 3: Asymptomatic |
| **trestbps** | Resting blood pressure (in mm Hg on admission to the hospital).                                       |
| **chol**     | Serum cholesterol in mg/dL.                                                                           |
| **fbs**      | Fasting blood sugar > 120 mg/dL (1 = true; 0 = false).                                               |
| **restecg**  | Resting electrocardiographic results: <br> 0: Normal <br> 1: ST-T wave abnormality <br> 2: Left ventricular hypertrophy  |
| **thalach**  | Maximum heart rate achieved.                                                                           |
| **exang**    | Exercise-induced angina (1 = yes; 0 = no).                                                            |
| **oldpeak**  | ST depression induced by exercise relative to rest.                                                  |
| **slope**    | Slope of the peak exercise ST segment: <br> 0: Upsloping <br> 1: Flat <br> 2: Downsloping            |
| **ca**       | Number of major vessels (0-3) colored by fluoroscopy.                                                 |
| **thal**     | Thalassemia status: <br> 1: Normal <br> 2: Fixed defect <br> 3: Reversible defect                     |
| **target**   | Target variable indicating the presence of heart disease (1 = presence, 0 = absence).                 |
""")
    
    st.write("Below is the data that was used in this project:"
             )
    df = pd.read_csv("Data\heart.csv")
    st.dataframe(df, use_container_width=True)
    st.write("To download the data set, please hit the button below 👇")
    @st.cache_data
    def convert_df_to_csv(data):
        return data.to_csv(index=False).encode('utf-8')

    csv = convert_df_to_csv(df)
    st.download_button(
        label="📥 Download Dataset as CSV",
        data=csv,
        file_name='heart_disease_data.csv',
        mime='text/csv',
)
    
    
    
elif auth_status is False:
    st.error('Username/password is incorrect')

elif auth_status is None:
    st.info('Log in to access the page')
    st.code("""
username: felixkwemoi
password: Heart_Disease#0
username: DonFelo
password: Heart_Disease#1
""")
