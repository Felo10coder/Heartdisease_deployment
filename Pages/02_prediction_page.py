### importing the necessary libraries
import streamlit as st 
import streamlit_authenticator as stauth
import streamlit_option_menu as option_menu
import pandas as pd
import sklearn
import xgboost as xgb
import os
import datetime
import joblib
import yaml
from yaml.loader import SafeLoader 

## page configuration
st.set_page_config(
    page_title= "Prediction Page",
    page_icon = "🚀",
    layout= "wide"
)

##encryption
with open ('./config.yaml')as file:
    config= yaml.load(file, Loader=SafeLoader)
    
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']    
)

### log in side bar
authenticator.login(location="sidebar")

## accessing session state
auth_status = st.session_state.get("authentication_status",None)
username = st.session_state.get("username",None)
name = st.session_state.get("name",None)

if auth_status:
    authenticator.logout(location="sidebar")
    st.sidebar.success("select a page above")
    st.markdown('<h1 style="text-align: center;"><u><i><b> PREDICTION PAGE </b></i></u></h1>', unsafe_allow_html=True)
    st.write ("""
              Welcome to the Heart Disease Prediction Tool. This application allows you to assess the likelihood of a patient developing heart disease based on key health indicators.

You can choose between two models — XGBoost and Logistic Regression — for making predictions. Simply select your preferred model, enter the required patient details, and click Submit to view the prediction outcome.

⚠️ Note: This tool is for educational and informational purposes only and should not replace professional medical advice.""")
    
    ### loading models
    st.cache_resource(show_spinner='modelsloading....')
    def select_model():
        col1,col2 = st.columns(2)
        with col1:
            st.selectbox('***Select a model***', options=['xgb','logistic_regression'], key='selected_model')
    
        with col2:
            pass
        
        if st.session_state['selected_model'] == 'Xgb':
            pipeline = joblib.load('./Models/xgb.joblib')
        else:
            pipeline = joblib.load('./Models/logistic_regression.joblib')
            
        return pipeline
        
        

    def make_prediction(pipeline):
        age = st.session_state['age']
        sex = st.session_state['sex']
        cp = st.session_state['cp']
        trestbps = st.session_state['trestbps']
        chol = st.session_state['chol']
        fbs = st.session_state['fbs']
        restecg = st.session_state['restecg']
        thalach = st.session_state['thalach']
        exang = st.session_state['exang']
        oldpeak = st.session_state['oldpeak']
        slope = st.session_state['slope']
        ca = st.session_state['ca']
        thal = st.session_state['thal']
        
        data = {'age':[age], 'sex':[sex], 'cp':[cp], 'trestbps':[trestbps], 'chol':[chol], 'fbs':[fbs],
                'restecg':[restecg], 'thalach':[thalach], 'exang':[exang], 'oldpeak':[oldpeak],
                'slope':[slope], 'ca':[ca], 'thal':[thal]}    
        df = pd.DataFrame(data)
        
        ## make predictions
        pred = pipeline.predict(df)
        #pred_int = int(pred[0])
        
        probability = pipeline.predict_proba(df)
        
        st.session_state['pred'] = pred
        st.session_state['probability'] = probability[0]
        
        ## adding new columns for recording the predictions
        df['prediction'] = pred
        df['prob_0'] = round(probability[0][0], 2)
        df['prob_1'] = round(probability[0][1], 2)
        
        df['time_of_prediction'] = datetime.date.today()
        df['model_used'] = st.session_state['selected_model']
        
        df.to_csv('./data/history_data.csv',mode='a',header=not os.path.exists('./data/history_data.csv'))
        return pred, probability[0]
    
    if 'pred' not in st.session_state:
        st.session_state['pred']= None
    
    if 'probability' not in st.session_state:
        st.session_state['probability']=None 
        
    def display_form():
        pipeline = select_model()
        with st.form('input-features'):
            col1,col2,col3,col4 = st.columns(4)
            with col1:
                st.write('personal details 🙂‍')
                st.number_input('Enter your Age',key = 'age', max_value=77 ,min_value=27, step=1 )
                st.selectbox('Select your gender Male: 1 ,Female: 2', options=['1','2'], key='sex')
                st.number_input('Chest pain', key='cp',max_value=3, min_value=0, step=1)
            with col2:
                st.write('Blood Test 💉')
                st.number_input('Resting Blood Pressure', key='trestbps', max_value=200, min_value=94,step=1)
                st.number_input('serum cholestrol',key='chol',max_value=564 ,min_value=126 ,step=1)
                st.number_input('fasting blood sugar',key='fbs', max_value=1, min_value=0, step=1)
            with col3:
                st.write("heart Infections ❤️")
                st.number_input('resting electrocardiographic resutls', key='restecg', max_value=2, min_value=0, step=1)
                st.number_input('Maximum heart rate achieved', key='thalach', max_value=202, min_value=71, step=1)
                st.number_input('Exercised induced angina',key='exang',max_value=1,min_value=0,step=1)
            with col4:
                st.write('Other Metrics 🩺')
                st.number_input('depression induced by exercise',key='oldpeak',max_value=6.5,min_value=0.0,step=0.1)
                st.number_input('slope of peak exercise',key='slope',max_value=2, min_value=0, step=1)
                st.number_input('number of major vessels',key='ca',max_value=4,min_value=0,step=1)
                st.number_input('Thalassium status',key='thal',max_value=3,min_value=0,step=1)
            
            st.form_submit_button('submit', on_click = make_prediction, kwargs = dict(pipeline=pipeline))
    
    
    if __name__ == '__main__':
        display_form()
    
        final_prediction = st.session_state['pred']
        final_probability = st.session_state['probability']
        if st.session_state['pred'] == None:
            st.write('PREDICTION HERE')
        else:
            col1,col2=st.columns(2)
            with col1:
                if final_prediction == 1:
                    st.write(f'#### *WILL YOU DEVELOP A HEART DISEASE ?  YES*')
                else:
                    st.write(f'#### *WILL YOU DEVELOP A HEART DISEASE ?  NO*')
            with col2:
                if final_prediction == 1:
                    st.write(f'#### *The probablity of developing a heart disease is {final_probability[1]*100:.2f}%*')
                else:
                    st.write(f'#### *The probablity of not developing a heart disease is {final_probability[0]*100:.2f}%*')
    
    
        
    
    
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
