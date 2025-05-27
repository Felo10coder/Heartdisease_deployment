import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
st.set_page_config(
    page_title= "Home Page",
    page_icon= "🏘️",
    layout= "wide"
) 

with open ('./config.yaml') as file:
    config = yaml.load(file,Loader=SafeLoader)
    
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
     
)


# Call login (do not unpack)
authenticator.login(location='sidebar')

# Access session state safely
auth_status = st.session_state.get("authentication_status", None)
username = st.session_state.get("username", None)
name = st.session_state.get("name", None)

# Main app logic
if auth_status:
    authenticator.logout(location='sidebar')
    st.markdown('<h1 style="text-align: center;"><u><i><b> HEART DISEASE PREDICTOR</b></i></u></h1>', unsafe_allow_html=True)
    st.sidebar.success("Select a page above")
    st.subheader("🏥 Heart Disease Analysis Prediction !🏥 ")
    
    st.subheader("*Introduction*")
    st.write("""Heart disease remains one of the leading causes of death worldwide, 
                 placing a significant burden on healthcare systems and affecting quality of life. 
                 Early and accurate diagnosis can lead to better treatment and prevention strategies. 
                 This project leverages machine learning to aid in predicting heart disease, providing 
                 healthcare professionals with a valuable tool to assess patient risk. 
                 By identifying high-risk individuals early, this model can support decision-making,
                 improve patient outcomes, and potentially reduce healthcare costs associated with advanced-stage 
                 treatments. """)
    st.write(""" ### *1.Business Objectives*
**Goal:** The primary objective is to create a predictive model that can identify individuals at high risk of heart disease, assisting healthcare providers in proactive, data-driven interventions.

**Business Success Criteria:** Success in this project means improving the accuracy and efficiency of heart disease screening, thereby reducing diagnosis time, improving patient outcomes, and lowering healthcare costs associated with heart disease management.

### *2.Assess Situation*
**Resources:** Identify available resources, such as heart disease datasets, data storage, processing capabilities, and team expertise in machine learning.

**Requirements:** Gather project requirements, such as data privacy standards, ethical guidelines, and necessary compliance with healthcare regulations.

**Risks and Contingencies:** Potential risks include data quality issues, model overfitting, or inadequate interpretability for medical professionals. Mitigating these risks involves thorough data preprocessing, validation, and choosing interpretable algorithms.

**Cost-Benefit Analysis:** Compare the anticipated costs (time, technology, and labor) against the potential benefits, such as improved diagnostic efficiency, reduced hospital readmissions, and better patient health outcomes.

### *3.Determine Data Mining Goals*
**Technical Success Criteria:** The technical objective is to build a machine learning model that achieves high predictive accuracy and interpretability, allowing healthcare providers to understand and trust the model’s predictions. Key performance indicators (KPIs) include metrics like accuracy, recall, precision, and F1-score.

### *4.Project Plan*

**Technologies and Tools:** Select tools such as Python, Scikit-Learn, and Jupyter Notebooks for data analysis, model building, and testing.

**Detailed Plan for Phases:** Outline each phase—data collection, data preprocessing, model training, evaluation, and deployment—along with specific tasks, timelines, and dependencies to ensure the project stays on track and meets all objectives.""")
    
     # Image 
    image_url = "https://images.pexels.com/photos/4225880/pexels-photo-4225880.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    st.markdown(f'<img src="{image_url}" alt="Telecommunication Networks" width="800" height="700">', unsafe_allow_html=True)


    ##footer
    st.subheader("Contacts")
    st.write("""**Email**: felixkwemoi7@gmail.com """)
    st.write("**Linkedin**: [linkedin](https://www.linkedin.com/in/felixkwemoi)")
    st.write("**Github Repository**: [Github](https://github.com/Felo10coder/Heartdisease_deployment)")
    
    
    
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

    


