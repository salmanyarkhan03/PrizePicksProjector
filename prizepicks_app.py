import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

# Load dataset
DATA_PATH = "/Users/User/database_24_25.csv"  # Update the path
df = pd.read_csv(DATA_PATH)

# Helper functions
def preprocess_player_data(player_name, stat):
    player_data = df[df["Player"] == player_name].copy()
    player_data[f"{stat}_5GameAvg"] = player_data[stat].rolling(window=5).mean()
    player_data[f"{stat}_5GameStd"] = player_data[stat].rolling(window=5).std()
    return player_data.dropna(subset=[f"{stat}_5GameAvg", f"{stat}_5GameStd"])

def train_model(player_data, stat, line):
    player_data["Higher"] = (player_data[stat] > line).astype(int)
    features = [f"{stat}_5GameAvg", f"{stat}_5GameStd"]
    X = player_data[features]
    y = player_data["Higher"]
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    return model

def predict_higher_lower(player_name, stat, line, opponent):
    try:
        player_data = preprocess_player_data(player_name, stat)
        if player_data.empty:
            return "Not enough data for prediction.", None

        latest_game = player_data.iloc[-1][[f"{stat}_5GameAvg", f"{stat}_5GameStd"]].values.reshape(1, -1)
        model = train_model(player_data, stat, line)
        prediction = model.predict(latest_game)[0]

        if len(model.classes_) == 2:
            probabilities = model.predict_proba(latest_game)[0]
            confidence = probabilities[prediction] * 100
        else:
            confidence = 100.0

        return "Higher" if prediction == 1 else "Lower", confidence
    except Exception as e:
        return f"Error during prediction: {str(e)}", None

# Streamlit UI
st.markdown(
    """
    <div style="text-align: center;">
        <h1>🏀 PrizePicks Prediction Tool 🏀</h1>
        <p>Analyze and predict player performance with confidence.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Tabs for features
tab1, tab2, tab3 = st.tabs(["🔮 Prediction", "📊 Player Comparison", "📈 Recent Performance"])

# Tab 1: Prediction
with tab1:
    player_name = st.selectbox("Select Player:", options=df["Player"].unique(), key="player_select")
    stat = st.selectbox(
        "Select Stat:",
        options=[
            "PTS: Points",
            "AST: Assists",
            "TRB: Total Rebounds",
            "STL: Steals",
            "BLK: Blocks",
            "FG: Field Goals",
            "FGA: Field Goal Attempts",
            "FG%: Field Goal Percentage",
            "3P: Three-Point Field Goals",
            "3PA: Three-Point Attempts",
            "3P%: Three-Point Percentage",
            "FT: Free Throws",
            "FTA: Free Throw Attempts",
            "FT%: Free Throw Percentage",
            "ORB: Offensive Rebounds",
            "DRB: Defensive Rebounds",
            "TOV: Turnovers",
        ],
        key="stat_select",
    )
    line = st.number_input("Enter PrizePicks Line for the Stat:", value=10.5, step=0.5, format="%.1f", key="line_input")
    opponent = st.selectbox(
        "Select Opponent Team:",
        options=[
           "ATL: Atlanta Hawks",
    "BOS: Boston Celtics",
    "BKN: Brooklyn Nets",
    "CHA: Charlotte Hornets",
    "CHI: Chicago Bulls",
    "CLE: Cleveland Cavaliers",
    "DAL: Dallas Mavericks",
    "DEN: Denver Nuggets",
    "DET: Detroit Pistons",
    "GSW: Golden State Warriors",
    "HOU: Houston Rockets",
    "IND: Indiana Pacers",
    "LAC: Los Angeles Clippers",
    "LAL: Los Angeles Lakers",
    "MEM: Memphis Grizzlies",
    "MIA: Miami Heat",
    "MIL: Milwaukee Bucks",
    "MIN: Minnesota Timberwolves",
    "NOP: New Orleans Pelicans",
    "NYK: New York Knicks",
    "OKC: Oklahoma City Thunder",
    "ORL: Orlando Magic",
    "PHI: Philadelphia 76ers",
    "PHX: Phoenix Suns",
    "POR: Portland Trail Blazers",
    "SAC: Sacramento Kings",
    "SAS: San Antonio Spurs",
    "TOR: Toronto Raptors",
    "UTA: Utah Jazz",
    "WAS: Washington Wizards",
        ],
        key="opponent_select",
    )
    if st.button("Predict", key="predict_button"):
        result, confidence = predict_higher_lower(
            player_name=player_name,
            stat=stat.split(":")[0],
            line=line,
            opponent=opponent.split(":")[0],
        )
        if confidence is not None:
            color = "green" if result == "Higher" else "red"
            st.markdown(
                f"### 🎯 Prediction: <span style='color: {color}; font-weight: bold;'>{result}</span> with {confidence:.2f}% confidence.",
                unsafe_allow_html=True,
            )
            # Plotting the chart below the prediction result
            st.subheader("Recent Performance Chart")
            player_data = preprocess_player_data(player_name, stat.split(":")[0])
            if not player_data.empty:
                fig, ax = plt.subplots(figsize=(10, 6))

                # Prepare chart data
                stats = player_data.tail(10)[stat.split(":")[0]]
                games = [f"Game {i}" for i in range(1, len(stats) + 1)]
                colors = ["green" if value > line else "red" for value in stats]

                # Create vertical bar chart
                ax.bar(games, stats, color=colors, edgecolor="white", linewidth=1.2)
                ax.axhline(y=line, color="blue", linestyle="--", linewidth=2, label=f"Line: {line}")

                # Customize chart aesthetics
                ax.set_facecolor("#2b2b2b")  # Dark background for the plot area
                fig.patch.set_facecolor("#1e1e1e")  # Dark background for the figure
                ax.spines["bottom"].set_color("white")
                ax.spines["left"].set_color("white")
                ax.tick_params(colors="white", labelsize=12)
                ax.yaxis.label.set_color("white")
                ax.xaxis.label.set_color("white")
                ax.title.set_color("white")
                ax.legend(loc="upper right", fontsize=12, facecolor="#2b2b2b", edgecolor="white")

                # Add chart labels
                ax.set_title(f"Recent Performance for {player_name} ({stat})", fontsize=16, color="white")
                ax.set_xlabel("Games", fontsize=14, color="white")
                ax.set_ylabel(f"{stat.split(':')[0]} Values", fontsize=14, color="white")
                ax.grid(axis="y", linestyle="--", alpha=0.5, color="white")

                # Display chart
                st.pyplot(fig)
            else:
                st.write("No recent performance data available.")
        else:
            st.error(result)


# Tab 2: Player Comparison
with tab2:
    st.subheader("Compare Two Players")
    player1 = st.selectbox("Select Player 1:", options=df["Player"].unique(), key="player1_select")
    player2 = st.selectbox("Select Player 2:", options=df["Player"].unique(), key="player2_select")
    stat_comp = st.selectbox("Select Stat for Comparison:", options=["PTS", "AST", "TRB"], key="stat_comp_select")

    if st.button("Compare Players"):
        comparison_data = df[df["Player"].isin([player1, player2])][["Player", stat_comp]]
        st.write(comparison_data)









    
    