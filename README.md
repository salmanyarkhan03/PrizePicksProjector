# PrizePicksProjector
PrizePicks Prediction Tool
🏀 is a web-based application built using Streamlit that predicts whether an NBA player's performance will exceed or fall below a specific line for a given statistic. It also visualizes the player's recent game performance with an interactive chart.

Features
Player Performance Prediction:

Predicts whether a player's performance in a given stat (e.g., Points, Assists, Rebounds) will be "Higher" or "Lower" than a user-provided line.
Displays the confidence percentage for the prediction.
Visualizations:

A vertical bar chart of the player's last 10 games with:
Green bars for games where the stat exceeds the line.
Red bars for games where the stat is below the line.
A blue line indicating the user-defined line.
User-Friendly Interface:

Intuitive dropdowns for selecting players, stats, and teams.
Aesthetic design inspired by PrizePicks' branding (purple and light purple theme).
Technology Stack
Frontend: Streamlit
Backend: Python
Libraries:
pandas: For data manipulation.
scikit-learn: For machine learning predictions.
matplotlib: For visualizations.
Setup and Installation
1. Clone the Repository
bash
Copy code
git clone https://github.com/salmanyarkhan03/PrizePicksProjector.git
cd PrizePicksProjector
2. Install Dependencies
Make sure you have Python 3.7+ installed. Then, install the required libraries:

bash
Copy code
pip install -r requirements.txt
3. Run the Application
Run the Streamlit app locally:

bash
Copy code
streamlit run prizepicks_app.py
4. Deploy on Streamlit Cloud
To deploy on Streamlit Cloud:

Push the code to your GitHub repository.
Go to Streamlit Cloud and deploy the app.
Project Structure
plaintext
Copy code
PrizePicksProjector/
├── prizepicks_app.py      # Main Streamlit application file
├── database_24_25.csv     # NBA dataset
├── requirements.txt       # List of dependencies
├── README.md              # Project documentation
Usage
Select a Player: Choose a player from the dropdown.
Select a Stat: Pick a statistic (e.g., Points, Assists, Rebounds).
Enter a Line: Enter the PrizePicks line for the selected stat.
View Prediction:
The app predicts "Higher" or "Lower" and shows the confidence percentage.
The chart below visualizes the player's recent game performance.
Example Screenshots
Home Page
Description of what the home page looks like (replace this text with an actual screenshot).

Prediction Example
Description of what a prediction result looks like (replace this text with an actual screenshot).

Future Enhancements
Add support for live data integration from APIs (e.g., NBA stats API).
Provide more advanced analytics, such as trends and player comparisons.
Enhance UI with more customization options.
Contributing
We welcome contributions! If you'd like to improve this project:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -m "Add feature").
Push the branch (git push origin feature-branch).
Create a Pull Request.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For questions or suggestions, feel free to reach out:

GitHub: salmanyarkhan03
Email: salmanhyarkhan@gmail.com
