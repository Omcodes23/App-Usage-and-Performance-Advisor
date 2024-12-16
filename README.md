# App Usage and Performance Advisor

This Streamlit application provides users with insights into their app usage and performance, offering detailed metrics and analysis. The app allows users to view performance data for single or multiple users, generate visualizations, estimate goal achievement using fuzzy logic, and interact with a virtual project manager for advice.

## Features

- **Single User or Multiple Users Analysis**: Allows users to analyze performance metrics for one or more users.
- **Goal Completion Accuracy**: Visualizes goal completion accuracy with various chart types such as bar charts, line charts, area charts, pie charts, scatter charts, and radar charts.
- **Goal Achievement Estimation**: Uses fuzzy logic to estimate goal achievement based on goal completion accuracy and time spent on the app.
- **Virtual Project Manager Chat**: Interact with a virtual project manager to get advice, sentiment analysis of your input, and data-driven suggestions.
- **Export to PDF**: Export performance data and analysis to a PDF report.

## Installation

To run this project locally, you need to install the required dependencies. Follow these steps:

1. Clone this repository:

    ```bash
    git clone https://github.com/your-repository/app-usage-performance-advisor.git
    cd app-usage-performance-advisor
    ```

2. Create a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Ensure you have the `fine_tuning_params.txt` and `app_usage_data.json` files in your project directory.

5. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

## Files

- **app.py**: The main Streamlit app file that contains all the logic for user selection, data analysis, visualizations, and PDF export.
- **fine_tuning_params.txt**: A text file containing parameters for fine-tuning the model.
- **app_usage_data.json**: The dataset file in JSON format containing app usage and performance data.

## Dataset

The app uses a JSON file (`app_usage_data.json`) containing user-specific performance data, including:

- `user`: The name of the user.
- `date`: The date of the data entry.
- `active_time_on_app`: The time spent by the user on the app (in minutes).
- `goal_completion_accuracy`: The accuracy with which the user completes their goals (percentage).
- `goals_completed_on_time`: The number of goals completed on time.
- `avg_task_completion_time`: The average time taken to complete a task (in minutes).
- `success_rate`: The percentage of successful tasks completed.

### Example JSON format:

```json
[
  {
    "user": "User1",
    "data": [
      {
        "date": "2024-01-01",
        "active_time_on_app": 120,
        "goal_completion_accuracy": 85,
        "goals_completed_on_time": 10,
        "avg_task_completion_time": 30,
        "success_rate": 90
      },
      {
        "date": "2024-01-02",
        "active_time_on_app": 150,
        "goal_completion_accuracy": 88,
        "goals_completed_on_time": 12,
        "avg_task_completion_time": 25,
        "success_rate": 92
      }
    ]
  }
]
