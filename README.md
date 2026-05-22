# PeerMatch AI

**PeerMatch AI** is a hackathon MVP that helps students, developers, and community members find relevant peers based on their profile, skills, interests, goals, and background.

The platform allows a user to create a profile, receive AI-powered peer recommendations, and connect with recommended peers through Discord.

---

## Problem

In hackathons, bootcamps, universities, and tech communities, people often struggle to find the right teammates or peers.

Some people need a frontend teammate, some need a backend developer, some need a designer, and others need someone who can pitch or analyze data.

PeerMatch AI solves this by recommending people who are either similar or complementary.

---

## Solution

PeerMatch AI uses a simple matching algorithm plus AI-generated analysis.

The backend compares user profiles by:

- skills
- interests
- hobbies
- languages
- education
- career goals

Then AI generates a useful explanation:

- why these people match
- how they can help each other
- what they can build together

---

## Main Flow

```text
User signs up / signs in
        ↓
User creates profile
        ↓
Backend compares profile with other peers
        ↓
AI generates match analysis
        ↓
User sees recommended peers
        ↓
User connects through Discord
```

---

## Features

- Sign up and sign in
- Cookie-based session authentication
- Profile setup page
- Live profile preview
- AI-powered peer match analysis
- Match score calculation
- Common points and complementary points
- Peer cards with skills, interests, and explanation
- Discord connect button
- Search and refresh matches
- Demo seed users for testing

---

## Tech Stack

### Frontend

- HTML
- CSS
- Vanilla JavaScript

### Backend

- Python
- Flask
- Flask-CORS
- Flask sessions
- JSON files as database
- Groq API for AI analysis

### Database

The project uses simple JSON files:

```text
data/users.json
data/profiles.json
```

This keeps the MVP simple and easy to run during a hackathon.

---

## Project Structure

```text
project/
  backend/
    app.py
    helpers.py
    ai.py
    requirements.txt
    .env
    data/
      users.json
      profiles.json

  frontend/
    peermatch_connected.html
```

---

## Backend API

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

### Demo Data

```http
POST /api/seed
```

### Health Check

```http
GET /api/health
```

---

## Environment Variables

Create a `.env` file inside the backend folder:

```env
SECRET_KEY=your-secret-key
GROQ_API_KEY=your-groq-api-key
```

`GROQ_API_KEY` is used for AI-generated peer analysis.

If the AI key is missing or the API fails, the backend returns fallback analysis so the demo does not break.

---

## How to Run Backend

Go to the backend folder:

```bash
cd backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Flask server:

```bash
python app.py
```

Backend will run on:

```text
http://localhost:5000
```

Check if backend is working:

```bash
curl http://localhost:5000/api/health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

## How to Seed Demo Users

Run:

```bash
curl -X POST http://localhost:5000/api/seed
```

This adds demo users such as:

- frontend developer
- backend developer
- UI/UX designer
- AI engineer
- data analyst
- mobile developer
- cybersecurity student
- marketing / pitch person

---

## How to Run Frontend

Go to the frontend folder:

```bash
cd frontend
```

Run a simple local server:

```bash
python3 -m http.server 5173
```

Open:

```text
http://localhost:5173/index.html
```

Important: do not open the HTML file directly with `file://`.

Use `http://localhost:5173` so cookies and sessions work correctly.

---

## CORS Setup

The backend should allow the frontend origin:

```python
CORS(app, supports_credentials=True, origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://0.0.0.0:5173"
])
```

Frontend requests must use:

```js
credentials: "include"
```

This is required because the project uses Flask sessions instead of JWT.

---

## Example User Profile

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

## Example Match Response

```json
{
  "id": 1,
  "name": "Leyla Mammadova",
  "education": "Holberton School Azerbaijan",
  "matchScore": 45,
  "commonPoints": ["Startups", "Hackathons"],
  "complementaryPoints": ["Flask + JavaScript"],
  "skills": ["JavaScript", "React", "CSS", "HTML", "Figma"],
  "interests": ["AI Products", "Startups", "Hackathons"],
  "aiAnalysis": {
    "whyMatch": "These users are a good match because they share interests in startups and hackathons.",
    "howYouCanHelpEachOther": "One user can work on backend APIs while the other can build the frontend interface.",
    "whatYouCanDoTogether": [
      "Build a full-stack AI web app",
      "Create a hackathon MVP together",
      "Develop an AI product prototype"
    ]
  },
  "discordUsername": "leyla.dev",
  "discordLink": "https://discord.com/users/leyla"
}
```

---

## AI Usage

The project uses AI only for final peer analysis.

The match score is calculated by the backend algorithm.

AI is used to generate:

1. why the users match
2. how they can help each other
3. what they can build together

This makes the system stable and explainable while still being AI-powered.

---

## Demo Scenario

1. Open the landing page.
2. Create an account.
3. Fill in your profile.
4. Save the profile.
5. Open peer matches.
6. See AI-generated recommendations.
7. Click “Connect on Discord”.

---

## Why This Project Matters

PeerMatch AI helps people find the right peers faster.

It is useful for:

- hackathons
- coding schools
- universities
- student communities
- startup events
- volunteer communities
- tech bootcamps

Instead of random networking, users get structured and explainable peer recommendations.

---

## Team Notes

This is a hackathon MVP.

The goal is not to build a production-level system, but to show a working product idea:

```text
profile input → backend matching → AI analysis → peer recommendation
```

---

## Future Improvements

- Real database instead of JSON files
- Better AI matching with embeddings
- Discord OAuth integration
- Team formation mode
- Admin dashboard for communities
- User profile photos
- Better scoring algorithm
- Deployment to Vercel and Railway
- Group recommendations for hackathon teams
