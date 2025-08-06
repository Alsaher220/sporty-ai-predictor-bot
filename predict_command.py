import os
import requests
import openai
from telegram import Update
from telegram.ext import ContextTypes

# Load your API keys from Render environment variables
API_FOOTBALL_KEY = os.getenv("FOOTBALL_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

HEADERS = {
    "x-apisports-key": API_FOOTBALL_KEY
}

# Get last 5 matches of a team
def get_team_stats(team_name):
    url = f"https://v3.football.api-sports.io/teams?search={team_name}"
    res = requests.get(url, headers=HEADERS).json()

    if not res['response']:
        return None

    team_id = res['response'][0]['team']['id']
    fixtures_url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&last=5"
    fix_res = requests.get(fixtures_url, headers=HEADERS).json()

    matches = fix_res['response']
    summary = f"{team_name} - Last 5 matches:\n"
    for match in matches:
        home = match['teams']['home']['name']
        away = match['teams']['away']['name']
        goals = match['goals']
        summary += f"- {home} {goals['home']} - {goals['away']} {away}\n"
    return summary

# /predict command function
async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 3 or 'vs' not in context.args:
            await update.message.reply_text("⚠️ Usage: /predict Team1 vs Team2")
            return

        team1, team2 = map(str.strip, ' '.join(context.args).split('vs'))

        stats1 = get_team_stats(team1)
        stats2 = get_team_stats(team2)

        if not stats1 or not stats2:
            await update.message.reply_text("❌ Could not find stats for one or both teams.")
            return

        prompt = (
            f"Predict the outcome of the match between {team1} and {team2} based on the recent form below.\n\n"
            f"{stats1}\n\n{stats2}\n\n"
            "Give a final score prediction and a short explanation."
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=250
        )

        prediction = response['choices'][0]['message']['content']
        await update.message.reply_text(f"🔮 AI Prediction:\n{prediction}")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")
