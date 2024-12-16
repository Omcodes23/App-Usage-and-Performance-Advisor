import pandas as pd
import streamlit as st
import json
from transformers import pipeline
from fpdf import FPDF
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import skfuzzy as fuzz
import skfuzzy.control as ctrl

st.set_page_config(
    page_title="App Usage and Performance Advisor",  # Title for the browser tab
    page_icon="📊",  # Optional: Add an icon
    layout="centered",  # Optional: Use 'centered' or 'wide'
    initial_sidebar_state="expanded"  # Optional: Initial sidebar state
)

# Load the Fine-Tuning Parameters
# FINE_TUNING_FILE = "fine_tuning_params.txt"
# with open(FINE_TUNING_FILE, "r") as file:
#     fine_tuning_params = file.read()

# Path to your JSON file
DATASET_FILE = "app_usage_data.json"

# Load the JSON dataset into a pandas DataFrame
with open(DATASET_FILE, "r") as file:
    data = json.load(file)

# Flatten the JSON structure into a pandas DataFrame
users_data = []
for user in data:
    user_name = user["user"]
    for entry in user["data"]:
        users_data.append({
            "user": user_name,
            "date": entry["date"],
            "active_time_on_app": entry["active_time_on_app"],
            "goal_completion_accuracy": entry["goal_completion_accuracy"],
            "goals_completed_on_time": entry["goals_completed_on_time"],
            "avg_task_completion_time": entry["avg_task_completion_time"],
            "success_rate": entry["success_rate"]
        })

# Create DataFrame
df = pd.DataFrame(users_data)

# Load Hugging Face pipelines
sentiment_pipe = pipeline("sentiment-analysis")
text_gen_pipe = pipeline("text2text-generation", model="google/flan-t5-base")
# text_gen_pipe = pipeline("text-generation", model="meta-llama/Llama-3.2-1B")

# Fuzzy Logic for Goal Achievement Estimation
goal_accuracy = ctrl.Antecedent(np.arange(0, 101, 1), 'goal_accuracy')
time_spent = ctrl.Antecedent(np.arange(0, 101, 1), 'time_spent')
achievement = ctrl.Consequent(np.arange(0, 101, 1), 'achievement')

goal_accuracy.automf(3)
time_spent.automf(3)
achievement.automf(3)

rule1 = ctrl.Rule(goal_accuracy['poor'] & time_spent['poor'], achievement['poor'])
rule2 = ctrl.Rule(goal_accuracy['average'] & time_spent['average'], achievement['average'])
rule3 = ctrl.Rule(goal_accuracy['good'] & time_spent['good'], achievement['good'])

achievement_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
achievement_sim = ctrl.ControlSystemSimulation(achievement_ctrl)

# Streamlit App
st.title("App Usage and Performance Advisor")

# User Selection for Single or Multiple Users
user_selection = st.selectbox("Select User(s) for Analysis", ["Single User", "Multiple Users"])

# If Single User is selected, show the data for that user
if user_selection == "Single User":
    user_name = st.selectbox("Select a User", df["user"].unique())
    user_data = df[df["user"] == user_name]
    st.subheader(f"Performance Metrics for {user_name}")
    st.dataframe(user_data)

    # Visualization for Single User
    st.subheader(f"Goal Completion Accuracy for {user_name}")
    chart_option = st.selectbox("Choose chart type", ["Bar Chart", "Line Chart", "Area Chart", "Pie Chart", "Scatter Chart", "Radar Chart"])
    
    if chart_option == "Bar Chart":
        st.bar_chart(user_data.set_index("date")["goal_completion_accuracy"])
    elif chart_option == "Line Chart":
        st.line_chart(user_data.set_index("date")["goal_completion_accuracy"])
    elif chart_option == "Area Chart":
        st.area_chart(user_data.set_index("date")["goal_completion_accuracy"])
    elif chart_option == "Pie Chart":
        pie_data = user_data.groupby("user")["goal_completion_accuracy"].mean()
        st.pyplot(pie_data.plot(kind="pie", autopct="%1.1f%%").get_figure())
    elif chart_option == "Scatter Chart":
        fig, ax = plt.subplots()
        ax.scatter(user_data["active_time_on_app"], user_data["goal_completion_accuracy"])
        ax.set_xlabel('Active Time on App (mins)')
        ax.set_ylabel('Goal Completion Accuracy (%)')
        st.pyplot(fig)
    elif chart_option == "Radar Chart":
        labels = user_data.columns[3:]
        values = user_data.iloc[0, 3:].values
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.plot(labels, values, linewidth=2, linestyle='solid')
        ax.fill(labels, values, alpha=0.25)
        st.pyplot(fig)

    # Fuzzy Logic for Goal Achievement Estimation
    achievement_sim.input['goal_accuracy'] = user_data["goal_completion_accuracy"].mean()
    achievement_sim.input['time_spent'] = user_data["active_time_on_app"].mean()
    achievement_sim.compute()
    st.write(f"Estimated Goal Achievement: {achievement_sim.output['achievement']:.2f}%")

else:
    # Show data for multiple users and compare them
    st.subheader("Performance Metrics for Multiple Users")
    selected_users = st.multiselect("Select Users", df["user"].unique())
    if selected_users:
        selected_data = df[df["user"].isin(selected_users)]
        st.dataframe(selected_data)

        # Visualization for Multiple Users Comparison
        st.subheader("Goal Completion Accuracy Comparison")
        chart_option = st.selectbox("Choose chart type for multiple users", ["Bar Chart", "Line Chart", "Area Chart", "Pie Chart", "Scatter Chart", "Radar Chart"])
        if chart_option == "Bar Chart":
            st.bar_chart(selected_data.set_index("user")["goal_completion_accuracy"])
        elif chart_option == "Line Chart":
            st.line_chart(selected_data.set_index("user")["goal_completion_accuracy"])
        elif chart_option == "Area Chart":
            st.area_chart(selected_data.set_index("user")["goal_completion_accuracy"])
        elif chart_option == "Pie Chart":
            pie_data = selected_data.groupby("user")["goal_completion_accuracy"].mean()
            st.pyplot(pie_data.plot(kind="pie", autopct="%1.1f%%").get_figure())
        elif chart_option == "Scatter Chart":
            fig, ax = plt.subplots()
            ax.scatter(selected_data["active_time_on_app"], selected_data["goal_completion_accuracy"])
            ax.set_xlabel('Active Time on App (mins)')
            ax.set_ylabel('Goal Completion Accuracy (%)')
            st.pyplot(fig)
        elif chart_option == "Radar Chart":
            labels = selected_data.columns[3:]
            values = selected_data.iloc[0, 3:].values
            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            ax.set_theta_offset(np.pi / 2)
            ax.set_theta_direction(-1)
            ax.plot(labels, values, linewidth=2, linestyle='solid')
            ax.fill(labels, values, alpha=0.25)
            st.pyplot(fig)

# Chat Simulation for Virtual Project Manager
st.subheader("Chat with the Virtual Project Manager")
user_input = st.text_input("Ask for advice or share your thoughts:")

if user_input:
    # Sentiment Analysis
    sentiment_result = sentiment_pipe(user_input)[0]
    st.write(f"Sentiment: {sentiment_result['label']}")
    st.write(f"Confidence: {sentiment_result['score']:.2f}")

    # Process queries related to the dataset
    if "tell me about" in user_input.lower():
        # Extract user name from the query
        user_name = user_input.lower().replace("tell me about", "").strip()
        user_name = user_name.title()  # Ensure capitalization matches the dataset
        if user_name in df["user"].unique():
            # Fetch user-specific data
            user_data = df[df["user"] == user_name]
            response = f"""
            Here is what I found about {user_name}:
            - Average Active Time on App: {user_data['active_time_on_app'].mean():.2f} minutes
            - Goal Completion Accuracy: {user_data['goal_completion_accuracy'].mean():.2f}%
            - Goals Completed On Time: {user_data['goals_completed_on_time'].mean():.2f}
            - Success Rate: {user_data['success_rate'].mean():.2f}%
            """
        else:
            response = f"I couldn't find any information about {user_name} in the dataset. Please check the name and try again."
        st.write(f"Advisor: {response}")

    elif "improve" in user_input.lower() or "performance" in user_input.lower():
        # Provide general improvement suggestions based on dataset insights
        avg_accuracy = df["goal_completion_accuracy"].mean()
        avg_active_time = df["active_time_on_app"].mean()
        response = f"""
        To improve performance:
        - The average goal completion accuracy across users is {avg_accuracy:.2f}%. Encourage users to aim higher.
        - Average active time on the app is {avg_active_time:.2f} minutes. Increasing engagement time may lead to better outcomes.
        - Focus on completing goals on time and reducing task completion times.
        """
        st.write(f"Advisor: {response}")

    else:
        # Handle general queries or unsupported inputs
        st.write("Advisor: I'm here to help with questions about the app usage and dataset. Try asking about a user or how to improve performance.")

# Export as PDF
st.subheader("Export Data and Results")
if st.button("Export to PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add content to PDF based on User Selection
    pdf.cell(200, 10, txt="App Usage and Performance Metrics", ln=True, align="C")
    pdf.ln(10)

    if user_selection == "Single User":
        pdf.cell(200, 10, txt=f"Data for User: {user_name}", ln=True)
        for i, row in user_data.iterrows():
            pdf.cell(200, 10, txt=f"{row['date']}: Time on App={row['active_time_on_app']} mins, Goal Completion Accuracy={row['goal_completion_accuracy']}%, Goals On Time={row['goals_completed_on_time']}", ln=True)
    else:
        pdf.cell(200, 10, txt="Data for Multiple Users", ln=True)
        for i, row in selected_data.iterrows():
            pdf.cell(200, 10, txt=f"{row['user']} - {row['date']}: Time on App={row['active_time_on_app']} mins, Goal Completion Accuracy={row['goal_completion_accuracy']}%, Goals On Time={row['goals_completed_on_time']}", ln=True)

    # Add Average Goal Completion Accuracy
    avg_goal_completion_accuracy = df["goal_completion_accuracy"].mean()
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Average Goal Completion Accuracy: {avg_goal_completion_accuracy:.2f}%", ln=True)

    # Save PDF and send to browser
    pdf_file = "performance_report.pdf"
    pdf.output(pdf_file)
    
    with open(pdf_file, "rb") as file:
        st.download_button("Download PDF", file, file_name=pdf_file)