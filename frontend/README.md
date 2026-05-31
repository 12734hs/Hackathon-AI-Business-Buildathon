# 🎨 Frontend — PeerMatch AI

The client-side of PeerMatch AI. Built with plain HTML, CSS, and Vanilla JavaScript — no frameworks.

---

## 📁 Folder Structure

```
frontend/
  index.html   # The one and only HTML file of the app
  index.css   # The one and only HTML file of the app
  index.js   # The one and only HTML file of the app

```

---

## 🖥️ What's Inside

### `peermatch_connected.html`

A single file that contains the entire UI of the application:

| Section | Description |
|---|---|
| 🔐 Sign In / Sign Up | Form for creating an account or logging in |
| 👤 Profile Page | Form to fill in skills, interests, hobbies, goals, Discord, etc. |
| 👁️ Live Profile Preview | Profile card updates in real time as you type |
| 🤝 Matches Page | List of recommended peers with AI analysis |
| 🃏 Peer Cards | Show name, skills, interests, match score, and AI explanation |
| 🔗 Discord Button | Direct link to connect with a peer |
| 🔍 Search & Refresh | Search through matches and reload the list |

### JavaScript Logic (inside the HTML file)

- State management: auth, profile, matches
- All backend requests via `fetch` with `credentials: "include"`
- Dynamic rendering of peer cards from JSON responses
- Error handling and fallback states

---

## 🚀 Running the App

### Step 1 — Make sure the backend is running

The frontend needs the backend to be up first.

```bash
# Inside the backend/ folder
pip install -r requirements.txt
python app.py
```

Backend will be available at: `http://localhost:5000`

Verify it's working:
```bash
curl http://localhost:5000/api/health
# Expected: { "status": "ok" }
```

---

### Step 2 — Start the frontend

```bash
cd frontend
python3 -m http.server 5173
```

Open in browser:

```
http://localhost:5173/index.html
```

> ⚠️ **Important:** Always open via `http://localhost:5173`, not `file://`.  
> Sessions and cookies only work over HTTP.

---

### Step 3 — Add demo users (optional)

To instantly see peer matches, seed the database with test users:

```bash
curl -X POST http://localhost:5000/api/seed
```

Demo profiles added:
- Frontend Developer
- Backend Developer
- UI/UX Designer
- AI Engineer
- Data Analyst
- Mobile Developer
- Cybersecurity Student
- Marketing / Pitch Person

---

## 🔗 Backend Communication

All frontend requests go to `http://localhost:5000`.

```javascript
// Example request with cookie session
fetch("http://localhost:5000/api/matches", {
  method: "GET",
  credentials: "include"  // required for sessions
})
```

Endpoints used by the frontend:

```
POST /api/auth/register   — sign up
POST /api/auth/login      — sign in
POST /api/auth/logout     — sign out
GET  /api/auth/me         — get current user
GET  /api/profile/me      — get profile
PUT  /api/profile/me      — update profile
GET  /api/matches         — get peer matches
```

---

## 🛠️ Technologies

| Technology | Purpose |
|---|---|
| HTML5 | Page structure |
| CSS3 | Styles and animations |
| Vanilla JavaScript | Logic, API requests, dynamic rendering |

No frameworks. Everything runs from a single file — intentional for hackathon MVP simplicity.

---

## 📝 Notes

- All styles and scripts are inside `peermatch_connected.html`
- For cookies to work, backend CORS must be configured with `supports_credentials=True`
- No bundlers (Webpack, Vite, etc.) — runs directly from the file server
