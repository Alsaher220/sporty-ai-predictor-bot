import os
import requests
import openai
from telegram import Update
from telegram.ext import ContextTypes

# Load API keys
API_FOOTBALL_KEY = os.getenv("FOOTBALL_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

HEADERS = {
    "x-apisports-key": API_FOOTBALL_KEY
}

# Fetch recent match stats for a team
def get_team_stats(team_name):
    search_url = f"https://v3.football.api-sports.io/teams?search={team_name}"
    response = requests.get(search_url, headers=HEADERS).json()

    if not response['response']:
        return None

    team_id = response['response'][0]['team']['id']
    fixtures_url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&last=5"
    fix_response = requests.get(fixtures_url, headers=HEADERS).json()

    matches = fix_response['response']
    if not matches:
        return None

    summary = f"{team_name} - Last 5 Matches:\n"
    for match in matches:
        home = match['teams']['home']['name']
        away = match['teams']['away']['name']
        score_home = match['goals']['home']
        score_away = match['goals']['away']
        summary += f"- {home} {score_home} : {score_away} {away}\n"

    return summary

# /predict command
async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 3 or 'vs' not in context.args:
            await update.message.reply_text("⚠️ Usage: /predict Team1 vs Team2")
            return

        team1, team2 = map(str.strip, ' '.join(context.args).split('vs'))

        stats1 = get_team_stats(team1)
        stats2 = get_team_stats(team2)

        if not stats1 or not stats2:
            await update.message.reply_text("❌ Couldn’t fetch stats for one or both teams.")
            return

        prompt = (
            f"Based on the recent performances of these teams, predict the winner.\n\n"
            f"{stats1}\n\n{stats2}\n\n"
            "Give a final score prediction and a 2-sentence explanation."
        )

        ai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )

        prediction = ai_response['choices'][0]['message']['content']
        await update.message.reply_text(f"🔮 AI Prediction:\n{prediction}")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error occurred: {str(e)}")
