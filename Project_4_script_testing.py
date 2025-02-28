import streamlit
import pandas as pd 
import numpy as np
import joblib

model = joblib.load('random_forest_model.pkl')
onehot_encoder = joblib.load('onehot_encoder.pkl')

streamlit.title("Lunge Cancer Survival App")
streamlit.write("Enter Patient Detail to Predict Survival")

col0, col1 = streamlit.columns(2)

#collect input data
with col0 :
    age = streamlit.number_input('Age', min_value=4, max_value=104, value=45 )
    gender = streamlit.selectbox('Gender', ['Male', 'Female'])
    country = streamlit.selectbox('Contry', ['Sweden', 'Netherlands', 'Hungary', 'Belgium', 'Luxembourg', 'Italy', 'Croatia',
                                             'Denmark', 'Malta', 'Germany', 'Poland', 'Ireland', 'Romania', 'Spain', 'Greece', 
                                             'Estonia', 'Cyprus', 'France', 'Slovenia', 'Latvia', 'Portugal', 'Austria',
                                             'Czech Republic', 'Finland', 'Lithuania', 'Slovakia', 'Bulgaria'])
    cancer_stage = streamlit.selectbox('Cancer Stage', ['Stage I', 'Stage II', 'Stage III', 'Stage IV'] )
    family_history = streamlit.selectbox('Family History', ['Yes' ,'No'])
    smoking_status = streamlit.selectbox('Smoking Status', ['Passive Smoker', 'Former Smoker', 'Never Smoked', 'Current Smoker'])
    bmi = streamlit.number_input('BMI', min_value = 16, max_value=45, value=24)
    
with col1:
    cholesterol_level = streamlit.number_input('Cholesterol Level', min_value=150, max_value=300 , value =200)
    hypertension = streamlit.selectbox('Hypertension', [0, 1])
    asthma = streamlit.selectbox('Asthma', [0, 1])
    cirrhosis = streamlit.selectbox('Cirrhosis', [0, 1])
    other_cancer = streamlit.selectbox('Other Cancer', [0, 1])
    treatment_type = streamlit.selectbox('Treatment Type', ['Chemotherapy', 'Surgery', 'Combined', 'Radiation'])

#create datafram for input
input_data = pd.DataFrame([[age, gender, country, cancer_stage, family_history, smoking_status, bmi, 
                            cholesterol_level, hypertension, asthma, cirrhosis, other_cancer, treatment_type]], 
                          columns=['age', 'gender', 'country', 'cancer_stage', 'family_history', 'smoking_status', 'bmi', 'cholesterol_level', 
                                   'hypertension', 'asthma', 'cirrhosis', 'other_cancer', 'treatment_type'])



# One-Hot Encode user inputs
categorical_col = ['gender', 'country', 'cancer_stage', 'family_history', 'smoking_status', 'treatment_type']
encoded_input = onehot_encoder.transform(input_data[categorical_col])
encoded_df = pd.DataFrame(encoded_input, columns=onehot_encoder.get_feature_names_out(categorical_col))
input_data = pd.concat([input_data.drop(columns=categorical_col), encoded_df], axis=1)


if streamlit.button('Prediction Survival'):
    prediction = model.predict(input_data)[0]
    if prediction == 1:
        streamlit.success('The patient is likely to survive.')
    else:
        streamlit.error('The patient is not likely to survive.')
