# ⚙️ Backend — PeerMatch AI

The server-side of PeerMatch AI. Built with Python and Flask. Provides the API for authentication, profiles, peer matching algorithm, and AI analysis.

---

## 📁 Folder Structure

```
backend/
  app.py              # Entry point: Flask app and all API routes
  helpers.py          # Peer matching algorithm and score calculation
  ai.py               # Groq API integration for AI-generated analysis
  requirements.txt    # Python dependencies
  .env                # Environment variables (do not commit to git!)
  data/
    users.json        # Users "database" (login / hashed password)
    profiles.json     # User profiles "database"
```

---

## 📄 File Descriptions

### `app.py`
Main Flask application file. Contains:
- App initialization and CORS setup
- All API routes (auth, profile, matches, seed, health)
- Session management via Flask sessions (cookie-based)
- Response assembly logic for `/api/matches`

### `helpers.py`
Peer matching algorithm. Contains:
- Function to compare two profiles
- `matchScore` calculation based on skills, interests, hobbies, languages, education, and career goals
- Detection of `commonPoints` (shared traits) and `complementaryPoints` (skills that complement each other)

### `ai.py`
Groq API integration. Contains:
- Prompt construction based on two user profiles
- Groq API request to generate: why they match, how they can help each other, what they can build together
- Fallback response if the API is unavailable or the key is not set

### `data/users.json`
JSON file storing user accounts:
```json
[
  {
    "id": 1,
    "email": "user@example.com",
    "password": "<hashed>"
  }
]
```

### `data/profiles.json`
JSON file storing user profiles:
```json
[
  {
    "userId": 1,
    "fullName": "Sabir Safarav",
    "skills": ["Python", "Flask"],
    "interests": ["AI", "Hackathons"],
    "hobbies": ["F1"],
    "careerGoal": "Backend Developer",
    "languages": ["English", "Azerbaijani"],
    "education": "Holberton School Azerbaijan",
    "discordUsername": "sabir.dev",
    "discordLink": "https://discord.com/users/example"
  }
]
```

---

## 🚀 Running the Backend

### Step 1 — Navigate to the backend folder

```bash
cd backend
```

### Step 2 — Create the `.env` file

```bash
touch .env
```

Add the following to `.env`:

```env
SECRET_KEY=your-secret-key
GROQ_API_KEY=your-groq-api-key
```

> Get your `GROQ_API_KEY` at [console.groq.com](https://console.groq.com)  
> If the key is not set, the backend returns a fallback response — the demo won't break.

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Start the server

```bash
python app.py
```

Backend will be available at:
```
http://localhost:5000
```

### Step 5 — Verify it's working

```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{ "status": "ok" }
```

---

## 🌱 Seed Demo Users

```bash
curl -X POST http://localhost:5000/api/seed
```

Adds the following demo profiles:
- Frontend Developer
- Backend Developer
- UI/UX Designer
- AI Engineer
- Data Analyst
- Mobile Developer
- Cybersecurity Student
- Marketing / Pitch Person

---

## 📡 API Endpoints

### Auth

| Method | Route | Description |
|---|---|---|
| `POST` | `/api/auth/register` | Register a new user |
| `POST` | `/api/auth/login` | Log in |
| `POST` | `/api/auth/logout` | Log out |
| `GET` | `/api/auth/me` | Get current user data |

### Profile

| Method | Route | Description |
|---|---|---|
| `GET` | `/api/profile/me` | Get current user's profile |
| `PUT` | `/api/profile/me` | Update current user's profile |

### Matches

| Method | Route | Description |
|---|---|---|
| `GET` | `/api/matches` | Get recommended peers with AI analysis |

### Utilities

| Method | Route | Description |
|---|---|---|
| `POST` | `/api/seed` | Populate the database with demo users |
| `GET` | `/api/health` | Server health check |

---

## 🤖 How AI Analysis Works

1. Backend calculates `matchScore` via `helpers.py` (no AI involved)
2. For each match, `ai.py` builds a prompt using both user profiles
3. Groq API returns a JSON with:
   - `whyMatch` — why these people are a good match
   - `howYouCanHelpEachOther` — how they can support each other
   - `whatYouCanDoTogether` — list of project ideas they could work on
4. If Groq is unavailable — a pre-written fallback response is returned

---

## 🔗 CORS Configuration

Backend allows requests from the frontend origin:

```python
CORS(app, supports_credentials=True, origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://0.0.0.0:5173"
])
```

> All frontend requests must include `credentials: "include"` — required for Flask session cookies to work.

---

## 📦 Dependencies (`requirements.txt`)

```
flask
flask-cors
python-dotenv
requests
```

---

## 🛠️ Technologies

| Technology | Purpose |
|---|---|
| Python | Core language |
| Flask | Web framework and routing |
| Flask-CORS | Cross-origin request handling |
| Flask Sessions | Cookie-based authentication |
| JSON files | Simple database (MVP) |
| Groq API | AI match analysis generation |
| python-dotenv | Load variables from `.env` |

---

## 📝 Notes

- JSON files are used instead of a real database intentionally — for hackathon simplicity
- Sessions are stored in cookies — no JWT needed
- The `.env` file must never be committed to git (add it to `.gitignore`)
- In the future, JSON can be replaced with PostgreSQL or SQLite without changing the API
