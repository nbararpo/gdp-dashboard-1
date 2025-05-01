import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Healthcare Data Analytics Dashboard",
    page_icon="🏥",  # Medical building icon
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and description
st.title("🏥 Healthcare Data Analytics Platform")
st.markdown("Upload, visualize, and model your healthcare data for better clinical insights")

# Create sidebar for navigation
st.sidebar.image("https://img.icons8.com/color/96/000000/healthcare.png", width=100)
st.sidebar.title("Navigation")

# Navigation options
page = st.sidebar.radio(
    "Select a Page",
    ["Home", "Patient Demographics", "Clinical Analytics", "Predictive Modeling"]
)

# Function to load data
@st.cache_data
def load_data(file):
    if file is not None:
        if file.name.endswith('.csv'):
            data = pd.read_csv(file)
        elif file.name.endswith(('.xlsx', '.xls')):
            data = pd.read_excel(file)
        return data
    return None

# File upload section in sidebar
st.sidebar.header("Data Input")
uploaded_file = st.sidebar.file_uploader("Upload your health dataset", type=["csv", "xlsx"])

# Demo dataset options
st.sidebar.markdown("### Or use a demo dataset")
dataset_option = st.sidebar.selectbox(
    "Choose a dataset",
    ["None", "Patient Satisfaction", "Clinical Outcomes", "Healthcare Costs"]
)

# Function to load demo data
@st.cache_data
def get_demo_data(option):
    if option == "Patient Satisfaction":
        # Sample patient satisfaction data
        data = pd.DataFrame({
            'PatientID': range(1, 101),
            'Age': np.random.randint(18, 85, 100),
            'Gender': np.random.choice(['Male', 'Female'], 100),
            'Department': np.random.choice(['Cardiology', 'Neurology', 'Oncology', 'Orthopedics', 'Pediatrics'], 100),
            'WaitTime': np.random.randint(5, 120, 100),  # in minutes
            'ConsultationTime': np.random.randint(10, 60, 100),  # in minutes
            'StaffCourtesy': np.random.randint(1, 6, 100),  # 1-5 rating
            'DoctorCommunication': np.random.randint(1, 6, 100),  # 1-5 rating
            'FacilityCleanness': np.random.randint(1, 6, 100),  # 1-5 rating
            'OverallSatisfaction': np.random.randint(1, 6, 100),  # 1-5 rating
            'FollowUpScheduled': np.random.choice([True, False], 100),
            'Readmission': np.random.choice([True, False], 100, p=[0.15, 0.85]),
            'Date': pd.date_range(start='2023-01-01', periods=100)
        })
        return data
    
    elif option == "Clinical Outcomes":
        # Sample clinical outcomes data
        data = pd.DataFrame({
            'PatientID': range(1, 101),
            'Age': np.random.randint(18, 85, 100),
            'Gender': np.random.choice(['Male', 'Female'], 100),
            'Diagnosis': np.random.choice(['Hypertension', 'Diabetes', 'Heart Disease', 'COPD', 'Cancer'], 100),
            'LengthOfStay': np.random.randint(1, 30, 100),  # in days
            'Readmitted30Days': np.random.choice([True, False], 100, p=[0.2, 0.8]),
            'MortalityRisk': np.random.uniform(0, 1, 100),
            'Complications': np.random.choice([True, False], 100, p=[0.25, 0.75]),
            'FunctionalStatus': np.random.randint(1, 6, 100),  # 1-5 scale
            'PainScore': np.random.randint(0, 11, 100),  # 0-10 scale
            'Treatment': np.random.choice(['Medication', 'Surgery', 'Therapy', 'Combined'], 100),
            'AdmissionDate': pd.date_range(start='2023-01-01', periods=100)
        })
        return data
    
    elif option == "Healthcare Costs":
        # Sample healthcare costs data
        data = pd.DataFrame({
            'PatientID': range(1, 101),
            'Age': np.random.randint(18, 85, 100),
            'Gender': np.random.choice(['Male', 'Female'], 100),
            'InsuranceType': np.random.choice(['Medicare', 'Medicaid', 'Private', 'Uninsured'], 100),
            'TotalCost': np.random.uniform(500, 50000, 100),
            'MedicationCost': np.random.uniform(100, 5000, 100),
            'ProcedureCost': np.random.uniform(0, 20000, 100),
            'RoomCost': np.random.uniform(300, 10000, 100),
            'LengthOfStay': np.random.randint(1, 30, 100),
            'Diagnosis': np.random.choice(['Hypertension', 'Diabetes', 'Heart Disease', 'COPD', 'Cancer'], 100),
            'EmergencyAdmission': np.random.choice([True, False], 100),
            'ReadmissionCost': np.random.uniform(0, 10000, 100),
            'ServiceDate': pd.date_range(start='2023-01-01', periods=100)
        })
        return data
    
    return None

# Load data (from upload or demo)
if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.sidebar.success("Uploaded data loaded successfully!")
elif dataset_option != "None":
    df = get_demo_data(dataset_option)
    st.sidebar.success(f"Demo dataset '{dataset_option}' loaded!")
else:
    df = None

# HOME PAGE
if page == "Home" and df is None:
    st.header("Welcome to the Healthcare Data Analytics Platform")
    st.write("This interactive dashboard helps healthcare providers analyze patient data, clinical outcomes, and healthcare costs.")
    
    st.info("Please upload a dataset or select a demo dataset from the sidebar to get started.")
    
    # Feature highlights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📊 Patient Demographics")
        st.write("Analyze patient population by age, gender, diagnosis, and more.")
        
    with col2:
        st.subheader("🏆 Clinical Analytics")
        st.write("Track clinical outcomes, readmission rates, and patient satisfaction.")
        
    with col3:
        st.subheader("🧠 Predictive Modeling")
        st.write("Build models to predict patient outcomes, costs, and readmission risks.")

elif page == "Home" and df is not None:
    st.header("Dataset Overview")
    
    # Display basic dataset info
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dataset Preview")
        st.dataframe(df.head())
    
    with col2:
        st.subheader("Dataset Summary")
        st.write(f"Total records: {len(df)}")
        st.write(f"Total features: {len(df.columns)}")
        
        # Identify categorical and numerical columns
        categorical_cols = df.select_dtypes(include=['object', 'bool']).columns.tolist()
        numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        
        st.write(f"Categorical features: {len(categorical_cols)}")
        st.write(f"Numerical features: {len(numerical_cols)}")
    
    # Show key metrics
    st.subheader("Key Metrics")
    
    metric_cols = st.columns(4)
    
    # Customize metrics based on dataset type
    if dataset_option == "Patient Satisfaction":
        avg_satisfaction = round(df['OverallSatisfaction'].mean(), 2)
        avg_wait_time = round(df['WaitTime'].mean(), 2)
        readmission_rate = round(df['Readmission'].mean() * 100, 2)
        followup_rate = round(df['FollowUpScheduled'].mean() * 100, 2)
        
        metric_cols[0].metric("Avg Satisfaction Score", f"{avg_satisfaction}/5")
        metric_cols[1].metric("Avg Wait Time", f"{avg_wait_time} min")
        metric_cols[2].metric("Readmission Rate", f"{readmission_rate}%")
        metric_cols[3].metric("Follow-up Rate", f"{followup_rate}%")
    
    elif dataset_option == "Clinical Outcomes":
        avg_stay = round(df['LengthOfStay'].mean(), 2)
        readmit_rate = round(df['Readmitted30Days'].mean() * 100, 2)
        complication_rate = round(df['Complications'].mean() * 100, 2)
        avg_pain = round(df['PainScore'].mean(), 2)
        
        metric_cols[0].metric("Avg Length of Stay", f"{avg_stay} days")
        metric_cols[1].metric("30-Day Readmission", f"{readmit_rate}%")
        metric_cols[2].metric("Complication Rate", f"{complication_rate}%")
        metric_cols[3].metric("Avg Pain Score", f"{avg_pain}/10")
    
    elif dataset_option == "Healthcare Costs":
        avg_total = round(df['TotalCost'].mean(), 2)
        avg_los = round(df['LengthOfStay'].mean(), 2)
        cost_per_day = round(avg_total / avg_los, 2)
        emergency_rate = round(df['EmergencyAdmission'].mean() * 100, 2)
        
        metric_cols[0].metric("Avg Total Cost", f"${avg_total:.2f}")
        metric_cols[1].metric("Avg Length of Stay", f"{avg_los} days")
        metric_cols[2].metric("Cost per Day", f"${cost_per_day:.2f}")
        metric_cols[3].metric("Emergency Rate", f"{emergency_rate}%")

# PATIENT DEMOGRAPHICS PAGE
elif page == "Patient Demographics" and df is not None:
    st.header("Patient Demographics")
    
    # Check if necessary columns exist
    demo_cols = ['Age', 'Gender']
    if not all(col in df.columns for col in demo_cols):
        st.warning("This dataset doesn't have the required demographic columns (Age, Gender).")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Age Distribution")
            fig = px.histogram(
                df, 
                x='Age', 
                nbins=20,
                title="Distribution of Patient Ages",
                color_discrete_sequence=['#3a86ff']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Gender Distribution")
            fig = px.pie(
                df, 
                names='Gender', 
                title="Patient Gender Distribution",
                color_discrete_sequence=['#3a86ff', '#ff006e']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Additional demographics if available
        if 'Diagnosis' in df.columns:
            st.subheader("Diagnosis Distribution")
            fig = px.bar(
                df['Diagnosis'].value_counts().reset_index(),
                x='index',
                y='Diagnosis',
                labels={'index': 'Diagnosis', 'Diagnosis': 'Number of Patients'},
                title="Distribution of Patient Diagnoses",
                color='Diagnosis',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, use_container_width=True)
        
        if 'Department' in df.columns and 'Gender' in df.columns:
            st.subheader("Department by Gender")
            dept_gender = pd.crosstab(df['Department'], df['Gender'])
            fig = px.bar(
                dept_gender,
                barmode='group',
                labels={'value': 'Number of Patients', 'Department': 'Department'},
                title="Department Distribution by Gender",
                color_discrete_sequence=['#3a86ff', '#ff006e']
            )
            st.plotly_chart(fig, use_container_width=True)

# CLINICAL ANALYTICS PAGE
elif page == "Clinical Analytics" and df is not None:
    st.header("Clinical Analytics")
    
    # Check dataset type and show relevant analytics
    if dataset_option == "Patient Satisfaction":
        st.subheader("Patient Satisfaction Metrics")
        
        # Satisfaction by Department
        if 'Department' in df.columns and 'OverallSatisfaction' in df.columns:
            dept_sat = df.groupby('Department')['OverallSatisfaction'].mean().reset_index()
            fig = px.bar(
                dept_sat,
                x='Department',
                y='OverallSatisfaction',
                title="Average Patient Satisfaction by Department",
                color='Department',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Correlation between wait time and satisfaction
        if 'WaitTime' in df.columns and 'OverallSatisfaction' in df.columns:
            st.subheader("Wait Time vs. Satisfaction")
            fig = px.scatter(
                df,
                x='WaitTime',
                y='OverallSatisfaction',
                trendline="ols",
                labels={'WaitTime': 'Wait Time (minutes)', 'OverallSatisfaction': 'Overall Satisfaction'},
                title="Relationship Between Wait Time and Patient Satisfaction"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed satisfaction metrics
        sat_cols = ['StaffCourtesy', 'DoctorCommunication', 'FacilityCleanness', 'OverallSatisfaction']
        if all(col in df.columns for col in sat_cols):
            st.subheader("Satisfaction Components")
            
            sat_data = pd.DataFrame({
                'Category': ['Staff Courtesy', 'Doctor Communication', 'Facility Cleanness', 'Overall'],
                'Average Rating': [
                    df['StaffCourtesy'].mean(),
                    df['DoctorCommunication'].mean(),
                    df['FacilityCleanness'].mean(),
                    df['OverallSatisfaction'].mean()
                ]
            })
            
            fig = px.bar(
                sat_data,
                x='Category',
                y='Average Rating',
                title="Average Ratings Across Different Satisfaction Components",
                color='Category',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig, use_container_width=True)
    
    elif dataset_option == "Clinical Outcomes":
        st.subheader("Clinical Outcome Metrics")
        
        # Length of stay by diagnosis
        if 'Diagnosis' in df.columns and 'LengthOfStay' in df.columns:
            los_diag = df.groupby('Diagnosis')['LengthOfStay'].mean().reset_index()
            fig = px.bar(
                los_diag,
                x='Diagnosis',
                y='LengthOfStay',
                title="Average Length of Stay by Diagnosis",
                color='Diagnosis',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Readmission by age group
        if 'Age' in df.columns and 'Readmitted30Days' in df.columns:
            df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 30, 45, 60, 75, 100], 
                                    labels=['<30', '30-45', '46-60', '61-75', '>75'])
            readmit_age = df.groupby('AgeGroup')['Readmitted30Days'].mean().reset_index()
            
            fig = px.bar(
                readmit_age,
                x='AgeGroup',
                y='Readmitted30Days',
                title="30-Day Readmission Rate by Age Group",
                labels={'Readmitted30Days': 'Readmission Rate', 'AgeGroup': 'Age Group'},
                color='AgeGroup',
                color_discrete_sequence=px.colors.sequential.Viridis
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Pain score vs functional status
        if 'PainScore' in df.columns and 'FunctionalStatus' in df.columns:
            st.subheader("Pain Score vs. Functional Status")
            fig = px.scatter(
                df,
                x='PainScore',
                y='FunctionalStatus',
                trendline="ols",
                labels={'PainScore': 'Pain Score (0-10)', 'FunctionalStatus': 'Functional Status (1-5)'},
                title="Relationship Between Pain Score and Functional Status"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    elif dataset_option == "Healthcare Costs":
        st.subheader("Healthcare Cost Analysis")
        
        # Cost breakdown
        cost_cols = ['MedicationCost', 'ProcedureCost', 'RoomCost', 'ReadmissionCost']
        if all(col in df.columns for col in cost_cols):
            cost_data = pd.DataFrame({
                'Category': ['Medication', 'Procedures', 'Room & Board', 'Readmissions'],
                'Average Cost': [
                    df['MedicationCost'].mean(),
                    df['ProcedureCost'].mean(),
                    df['RoomCost'].mean(),
                    df['ReadmissionCost'].mean()
                ]
            })
            
            fig = px.pie(
                cost_data,
                values='Average Cost',
                names='Category',
                title="Healthcare Cost Breakdown",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Costs by diagnosis
        if 'Diagnosis' in df.columns and 'TotalCost' in df.columns:
            cost_diag = df.groupby('Diagnosis')['TotalCost'].mean().reset_index()
            fig = px.bar(
                cost_diag,
                x='Diagnosis',
                y='TotalCost',
                title="Average Total Cost by Diagnosis",
                labels={'TotalCost': 'Average Cost ($)', 'Diagnosis': 'Diagnosis'},
                color='Diagnosis',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Length of stay vs. total cost
        if 'LengthOfStay' in df.columns and 'TotalCost' in df.columns:
            st.subheader("Length of Stay vs. Total Cost")
            fig = px.scatter(
                df,
                x='LengthOfStay',
                y='TotalCost',
                trendline="ols",
                labels={'LengthOfStay': 'Length of Stay (days)', 'TotalCost': 'Total Cost ($)'},
                title="Relationship Between Length of Stay and Total Cost"
            )
            st.plotly_chart(fig, use_container_width=True)

# PREDICTIVE MODELING PAGE
elif page == "Predictive Modeling" and df is not None:
    st.header("Predictive Modeling")
    
    # Identify numerical and categorical columns
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'bool']).columns.tolist()
    
    # Remove ID columns and date columns
    id_cols = [col for col in numerical_cols if 'id' in col.lower() or 'patient' in col.lower()]
    numerical_cols = [col for col in numerical_cols if col not in id_cols]
    date_cols = [col for col in df.columns if 'date' in col.lower()]
    
    # Model configuration
    st.subheader("Model Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Target selection
        available_targets = numerical_cols + categorical_cols
        target_variable = st.selectbox("Select target variable", available_targets)
        
        # Determine modeling task type
        is_classification = target_variable in categorical_cols or df[target_variable].nunique() < 10
        
        # Feature selection
        feature_options = [col for col in numerical_cols + categorical_cols 
                          if col != target_variable 
                          and col not in id_cols + date_cols]
        
        selected_features = st.multiselect(
            "Select features for modeling", 
            feature_options,
            default=feature_options[:min(5, len(feature_options))]
        )
        
        # Model selection
        if is_classification:
            model_type = st.selectbox(
                "Select model type",
                ["Logistic Regression", "Random Forest Classifier"]
            )
        else:
            model_type = st.selectbox(
                "Select model type",
                ["Linear Regression", "Random Forest Regressor"]
            )
        
        # Train/test split
        test_size = st.slider("Test data size (%)", 10, 50, 20) / 100
        
        # Model training button
        train_model_button = st.button("Train Model")
    
    with col2:
        st.subheader("Model Results")
        
        if train_model_button and selected_features:
            # Prepare X data (features)
            X = df[selected_features].copy()
            
            # Handle categorical features
            for col in X.select_dtypes(include=['object', 'bool']).columns:
                X = pd.get_dummies(X, columns=[col], drop_first=True)
            
            # Prepare y data (target)
            y = df[target_variable]
            
            # Convert boolean target to int for classification
            if is_classification and y.dtype == bool:
                y = y.astype(int)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42
            )
            
            # Create and train model
            if is_classification:
                if model_type == "Logistic Regression":
                    model = LogisticRegression(max_iter=1000, random_state=42)
                else:  # Random Forest
                    model = RandomForestClassifier(n_estimators=100, random_state=42)
            else:
                if model_type == "Linear Regression":
                    model = LinearRegression()
                else:  # Random Forest
                    model = RandomForestRegressor(n_estimators=100, random_state=42)
            
            model.fit(X_train, y_train)
            
            # Evaluate model
            train_score = model.score(X_train, y_train)
            test_score = model.score(X_test, y_test)
            
            # Display metrics
            if is_classification:
                st.metric("Training Accuracy", f"{train_score:.4f}")
                st.metric("Testing Accuracy", f"{test_score:.4f}")
            else:
                st.metric("Training R² Score", f"{train_score:.4f}")
                st.metric("Testing R² Score", f"{test_score:.4f}")
            
            # Feature importance
            if "Random Forest" in model_type:
                importances = model.feature_importances_
                importance_df = pd.DataFrame({
                    'Feature': X.columns,
                    'Importance': importances
                }).sort_values('Importance', ascending=False)
                
                fig = px.bar(
                    importance_df,
                    x='Importance',
                    y='Feature',
                    orientation='h',
                    title='Feature Importance',
                    color='Importance',
                    color_continuous_scale='Viridis'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Coefficients for Linear/Logistic Regression
            elif "Regression" in model_type:
                coef_df = pd.DataFrame({
                    'Feature': X.columns,
                    'Coefficient': model.coef_ if len(model.coef_.shape) == 1 else model.coef_[0]
                }).sort_values('Coefficient', ascending=False)
                
                fig = px.bar(
                    coef_df,
                    x='Coefficient',
                    y='Feature',
                    orientation='h',
                    title='Feature Coefficients',
                    color='Coefficient',
                    color_continuous_scale='RdBu'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Add prediction interface if model is trained
            st.subheader("Make Predictions")
            
            # Create input fields for each feature
            prediction_inputs = {}
            for feature in selected_features:
                # Skip one-hot encoded features
                if feature not in X.columns:
                    continue
                
                # For categorical features
                if feature in categorical_cols:
                    unique_values = df[feature].unique().tolist()
                    prediction_inputs[feature] = st.selectbox(
                        f"Select {feature}",
                        unique_values
                    )
                # For numerical features
                else:
                    min_val = float(df[feature].min())
                    max_val = float(df[feature].max())
                    mean_val = float(df[feature].mean())
                    
                    prediction_inputs[feature] = st.slider(
                        f"{feature}",
                        min_val,
                        max_val,
                        mean_val,
                        step=(max_val - min_val) / 100
                    )
            
            # Make prediction button
            predict_button = st.button("Predict")
            
            if predict_button:
                # Create input dataframe
                input_df = pd.DataFrame([prediction_inputs])
                
                # Handle categorical features in input
                for col in input_df.select_dtypes(include=['object', 'bool']).columns:
                    input_df = pd.get_dummies(input_df, columns=[col], drop_first=True)
                
                # Ensure all columns from training are present
                for col in X.columns:
                    if col not in input_df.columns:
                        input_df[col] = 0
                
                # Ensure columns are in same order as training
                input_df = input_df[X.columns]
                
                # Make prediction
                prediction = model.predict(input_df)[0]
                
                # Display prediction
                if is_classification:
                    # For classification, show prediction and probability
                    st.success(f"Predicted {target_variable}: {prediction}")
                    if hasattr(model, 'predict_proba'):
                        proba = model.predict_proba(input_df)[0]
                        st.write(f"Prediction Probability: {max(proba):.2f}")
                else:
                    # For regression, show predicted value
                    st.success(f"Predicted {target_variable}: {prediction:.4f}")

# Show a message if data isn't loaded
elif df is None and page != "Home":
    st.info("Please upload a dataset or select a demo dataset from the sidebar to proceed.")

# Footer
st.markdown("---")
st.markdown(
    """
    **About this dashboard:** This healthcare analytics platform helps clinical teams analyze patient data, 
    monitor clinical outcomes, and build predictive models to improve healthcare delivery.
    """
)
