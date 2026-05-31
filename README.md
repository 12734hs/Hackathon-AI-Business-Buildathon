# 🤝 PeerMatch AI

> Hackathon MVP — AI-powered peer matching for developers, students, and tech communities

**🔗 Live Demo:** [peermatch-ai.up.railway.app](https://peermatch-ai.up.railway.app/)  
**📁 GitHub:** [github.com/12734hs/Hackathon-AI-Business-Buildathon](https://github.com/12734hs/Hackathon-AI-Business-Buildathon)

---

## 🧩 Problem

In hackathons, bootcamps, universities, and tech communities, people often struggle to find the right teammates.

Some need a frontend developer, others need a backend engineer, a designer, or someone who can pitch. **PeerMatch AI** solves this by recommending people who are similar to you or complement your skills.

---

## 💡 Solution

PeerMatch AI uses a matching algorithm combined with AI-generated analysis.

**The algorithm compares profiles by:**
- skills
- interests
- hobbies
- languages
- education
- career goals

**AI generates an explanation:**
- why these people are a good match
- how they can help each other
- what they can build together

---

## 🔄 Main Flow

```
Sign up / Sign in
        ↓
Create a profile
        ↓
Backend compares profile with other users
        ↓
AI generates match analysis
        ↓
User sees recommended peers
        ↓
Connect via Discord
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 Auth | Sign up and sign in with cookie-based sessions |
| 👤 Profile | Setup page with live profile preview |
| 🤖 AI Analysis | Match explanations generated via Groq API |
| 📊 Match Score | Numeric compatibility rating |
| 🔗 Discord | One-click connect button to reach a peer |
| 🔍 Search | Search and refresh the matches list |
| 🌱 Demo Data | Seed users for quick testing |
| 📬 Telegram Bot | Submit support applications directly via Telegram |

---

## 🏗️ Project Structure

```
project/
  backend/
    app.py              # Flask app and API routes
    helpers.py          # Peer matching algorithm
    ai.py               # Groq AI integration
    requirements.txt    # Python dependencies
    .env                # Environment variables
    data/
      users.json        # Users database
      profiles.json     # Profiles database

  frontend/
    peermatch_connected.html   # Main UI file

  telegram_bot/
    bot.py              # Telegram bot — support application handler
    .env                # Bot environment variables
```

---

## 🛠️ Tech Stack

### Frontend
- HTML / CSS / Vanilla JavaScript

### Backend
- Python + Flask
- Flask-CORS, Flask Sessions
- JSON files as database
- Groq API for AI analysis

### Telegram Bot
- Python + pyTelegramBotAPI
- Step-by-step conversation flow
- Forwards user applications to a private team channel

---

## 📡 API Endpoints

### Auth
```http
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/me
```

### Profile
```http
GET /api/profile/me
PUT /api/profile/me
```

### Matches
```http
GET /api/matches
```

### Utilities
```http
POST /api/seed     # Add demo users
GET  /api/health   # Health check
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/12734hs/Hackathon-AI-Business-Buildathon.git
cd Hackathon-AI-Business-Buildathon
```

### 2. Start the backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Backend will be available at `http://localhost:5000`

### 3. Start the frontend

```bash
cd frontend
python3 -m http.server 5173
```

Open in browser: `http://localhost:5173/index.html`

> ⚠️ Always open via `http://`, not `file://` — cookies and sessions only work over HTTP.

### 4. Seed demo users

```bash
curl -X POST http://localhost:5000/api/seed
```

### 5. Start the Telegram bot (optional)

```bash
cd telegram_bot
pip install pyTelegramBotAPI python-dotenv
python bot.py
```

> Requires `TELEGRAM_BOT_TOKEN` and `CHANNEL_ID` set in `telegram_bot/.env`

---

## 🔑 Environment Variables

### Backend — `backend/.env`

```env
SECRET_KEY=your-secret-key
GROQ_API_KEY=your-groq-api-key
```

> If `GROQ_API_KEY` is missing or the API fails, the backend returns a fallback analysis — the demo won't break.

### Telegram Bot — `telegram_bot/.env`

```env
TELEGRAM_BOT_TOKEN=your-bot-token
CHANNEL_ID=your-telegram-channel-id
```

> Get `TELEGRAM_BOT_TOKEN` from [@BotFather](https://t.me/BotFather). The bot must be an admin of the target channel.

---

## 🤖 Telegram Bot

PeerMatch AI includes a Telegram bot that lets users submit support applications directly in Telegram.

### Bot Commands

| Command | Description |
|---|---|
| `/start` | Start the bot and begin a new application |
| `/new` | Submit another application |

### How It Works

1. User sends `/start`
2. Bot greets the user by Telegram username
3. Bot asks for the **subject** of the application
4. Bot asks for the **main text**
5. Application is formatted with a unique ID and forwarded to the team's private Telegram channel
6. User receives a confirmation message

---

## 👤 Example Profile

```json
{
  "fullName": "Sabir Safarav",
  "education": "Holberton School Azerbaijan",
  "skills": ["Python", "Flask", "Backend", "AI"],
  "interests": ["AI", "Hackathons", "Web Development"],
  "hobbies": ["F1", "Volunteering"],
  "careerGoal": "Backend Developer",
  "languages": ["English", "Russian", "Azerbaijani"],
  "bio": "Junior developer interested in AI products and backend development.",
  "discordUsername": "sabir.dev",
  "discordLink": "https://discord.com/users/example"
}
```

---

## 🎯 Who Is This For

- Hackathons
- Coding schools and bootcamps
- Universities
- Student communities
- Startup events
- Volunteer and tech communities

---

## 🔮 Future Improvements

- [ ] Real database instead of JSON files
- [ ] AI matching with embeddings
- [ ] Discord OAuth integration
- [ ] Team formation mode
- [ ] Profile photos
- [ ] Group recommendations for hackathon teams
- [ ] Telegram bot notifications for new peer matches
- [ ] Deploy to Vercel + Railway

---

## 👥 Team

This is a hackathon MVP. The goal is to demonstrate a working product idea:

```
profile → algorithm → AI analysis → recommendation
```
