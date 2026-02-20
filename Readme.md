🏏 IPL Match Win Predictor
A Machine Learning-based web application that predicts the real-time win probability of the chasing team in an IPL match using ball-by-ball historical data.

🚀 Project Overview
The IPL Match Win Predictor estimates the winning probability of a team during the second innings of a match based on live match conditions such as:
Runs left
Balls left
Wickets remaining
Current Run Rate (CRR)
Required Run Rate (RRR)
Target score
City / venue
The model is trained using historical IPL ball-by-ball data and deployed using Streamlit for interactive predictions.

🧠 Machine Learning Approach
Type: Supervised Learning (Classification)
Algorithm Used: Random Forest Classifier
Feature Engineering:
Runs Left
Balls Left
Wickets Left
Current Run Rate
Required Run Rate
Data Split: Train/Test split
Library: Scikit-learn
Random Forest was chosen because it handles non-linear tabular data well and reduces overfitting using ensemble learning.

🛠️ Tech Stack
Languages
Python
Libraries
Pandas
NumPy
Scikit-learn
Streamlit
Tools
Git
VS Code

📊 Dataset
The model is trained on:
IPL Matches dataset
IPL Deliveries (ball-by-ball) dataset
Features were engineered from second innings chase situations only.

💻 Features of the Web App
Select batting and bowling teams
Select venue (city-based mapping)
Enter:
Target
Current score
Overs completed
Wickets down

Real-time win probability calculation
Cricket-based rule adjustments for realistic predictions
Clean and interactive UI

▶️ How to Run the Project
Clone the repository
git clone https://github.com/yourusername/ipl-win-predictor.git
cd ipl-win-predictor
Install dependencies
pip install -r requirements.txt
Run the Streamlit app
streamlit run app.py

📈 Future Improvements
Improve probability calibration
Add first innings prediction
Deploy on cloud (Render / Streamlit Cloud)
Add live API integration
Improve UI/UX design

🎯 Learning Outcomes
Applied machine learning to real-world sports data
Implemented feature engineering for classification problems
Built and deployed an ML web application
Improved understanding of probability-based predictions

📬 Contact
Mayank Maurya
GitHub: https://github.com/Mayank-Maurya975
LinkedIn: https://linkedin.com/in/Mayank-Maurya975
