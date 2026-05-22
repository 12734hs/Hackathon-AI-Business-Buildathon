  const API_BASE = "http://localhost:5000";
  let currentUser = null;
  let allMatches = [];

  async function apiRequest(path, options = {}) {
    const response = await fetch(`${API_BASE}${path}`, {
      credentials: "include",
      headers: { "Content-Type": "application/json", ...(options.headers || {}) },
      ...options
    });

    let data = null;
    try { data = await response.json(); } catch (_) { data = {}; }

    if (!response.ok) {
      throw new Error(data.error || data.message || "Request failed");
    }
    return data;
  }

  function showMessage(id, text, type = "error") {
    const el = document.getElementById(id);
    if (!el) return;
    if (!text) { el.innerHTML = ""; return; }
    el.innerHTML = `<div class="message ${type}">${escapeHtml(text)}</div>`;
  }

  function escapeHtml(value = "") {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function toArray(value) {
    if (Array.isArray(value)) return value;
    return String(value || "")
      .split(",")
      .map(item => item.trim())
      .filter(Boolean);
  }

  function arrToInput(value) {
    return Array.isArray(value) ? value.join(", ") : (value || "");
  }

  async function getMe() {
    try {
      const data = await apiRequest("/api/auth/me");
      currentUser = data.user || null;
      return currentUser;
    } catch (err) {
      currentUser = null;
      return null;
    }
  }

  async function showPage(name) {
    if ((name === "profile" || name === "matches") && !currentUser) {
      const user = await getMe();
      if (!user) {
        openAuth("signin");
        return;
      }
    }

    if (name === "landing" && currentUser) {
      name = "profile";
    }

    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    const target = document.getElementById('page-' + name);
    if (target) {
      target.classList.add('active');
      window.scrollTo(0, 0);
    }

    if (name === "profile") loadProfile();
    if (name === "matches") loadMatches();
  }

  function openAuth(mode = "signin") {
    showPage("auth");
    toggleAuthTab(mode);
  }

  function toggleAuthTab(tab) {
    const signin = document.getElementById('form-signin');
    const signup = document.getElementById('form-signup');
    const tabSignin = document.getElementById('tab-signin');
    const tabSignup = document.getElementById('tab-signup');
    showMessage("signin-message", "");
    showMessage("signup-message", "");

    if (tab === 'signin') {
      signin.classList.remove('hidden');
      signup.classList.add('hidden');
      tabSignin.classList.add('active');
      tabSignup.classList.remove('active');
    } else {
      signup.classList.remove('hidden');
      signin.classList.add('hidden');
      tabSignup.classList.add('active');
      tabSignin.classList.remove('active');
    }
  }

  async function loginUser() {
    const email = document.getElementById("signin-email").value.trim();
    const password = document.getElementById("signin-password").value.trim();
    if (!email || !password) return showMessage("signin-message", "Email and password are required.");

    try {
      showMessage("signin-message", "Signing in...", "success");
      const data = await apiRequest("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password })
      });
      currentUser = data.user;
      showPage("profile");
    } catch (err) {
      showMessage("signin-message", err.message);
    }
  }

  async function registerUser() {
    const fullName = document.getElementById("signup-name").value.trim();
    const email = document.getElementById("signup-email").value.trim();
    const password = document.getElementById("signup-password").value.trim();
    const confirm = document.getElementById("signup-confirm").value.trim();

    if (!fullName || !email || !password || !confirm) return showMessage("signup-message", "All fields are required.");
    if (!email.includes("@")) return showMessage("signup-message", "Enter a valid email.");
    if (password !== confirm) return showMessage("signup-message", "Passwords do not match.");

    try {
      showMessage("signup-message", "Creating account...", "success");
      const data = await apiRequest("/api/auth/register", {
        method: "POST",
        body: JSON.stringify({ fullName, email, password })
      });
      currentUser = data.user;
      showPage("profile");
    } catch (err) {
      showMessage("signup-message", err.message);
    }
  }

  async function logoutUser() {
    try { await apiRequest("/api/auth/logout", { method: "POST" }); } catch (_) {}
    currentUser = null;
    showPage("landing");
  }

  async function loadProfile() {
    try {
      showMessage("profile-message", "Loading profile...", "success");
      const data = await apiRequest("/api/profile/me");
      const p = data.profile || {};
      document.getElementById("p-name").value = p.fullName || currentUser?.fullName || "";
      document.getElementById("p-edu").value = p.education || "";
      document.getElementById("p-skills").value = arrToInput(p.skills);
      document.getElementById("p-interests").value = arrToInput(p.interests);
      document.getElementById("p-hobbies").value = arrToInput(p.hobbies);
      document.getElementById("p-languages").value = arrToInput(p.languages);
      document.getElementById("p-goal").value = p.careerGoal || "";
      document.getElementById("p-bio").value = p.bio || "";
      document.getElementById("p-discord").value = p.discordUsername || "";
      document.getElementById("p-discord-link").value = p.discordLink || "";
      showMessage("profile-message", "");
      updatePreview();
    } catch (err) {
      showMessage("profile-message", err.message);
    }
  }

  function getProfileFormData() {
    return {
      fullName: document.getElementById("p-name").value.trim(),
      education: document.getElementById("p-edu").value.trim(),
      skills: toArray(document.getElementById("p-skills").value),
      interests: toArray(document.getElementById("p-interests").value),
      hobbies: toArray(document.getElementById("p-hobbies").value),
      careerGoal: document.getElementById("p-goal").value.trim(),
      languages: toArray(document.getElementById("p-languages").value),
      bio: document.getElementById("p-bio").value.trim(),
      discordUsername: document.getElementById("p-discord").value.trim(),
      discordLink: document.getElementById("p-discord-link").value.trim()
    };
  }

  async function saveProfile(goToMatches = false) {
    try {
      showMessage("profile-message", "Saving profile...", "success");
      const profile = getProfileFormData();
      await apiRequest("/api/profile/me", {
        method: "PUT",
        body: JSON.stringify(profile)
      });
      showMessage("profile-message", "Profile saved successfully.", "success");
      if (goToMatches) showPage("matches");
    } catch (err) {
      showMessage("profile-message", err.message);
    }
  }

  function updatePreview() {
    const name = document.getElementById('p-name')?.value || 'John Doe';
    const edu  = document.getElementById('p-edu')?.value || 'MIT | Computer Science';
    const skills = document.getElementById('p-skills')?.value || 'Python, React, PyTorch';
    const interests = document.getElementById('p-interests')?.value || 'AI Safety, Robotics';
    const goal = document.getElementById('p-goal')?.value || 'Aspiring to build scalable ML systems at OpenAI.';
    const bio  = document.getElementById('p-bio')?.value || 'Passionate about the intersection of AI and engineering.';
    const discord = document.getElementById('p-discord')?.value || 'johndoe#1234';

    document.getElementById('prev-name').textContent = name;
    document.getElementById('prev-edu').textContent = edu.replace(',', ' |');
    document.getElementById('prev-goal').textContent = '"' + goal + '"';
    document.getElementById('prev-bio').textContent = bio;
    document.getElementById('prev-interests').textContent = interests;
    document.getElementById('prev-discord').textContent = '💬 ' + discord;

    const skillTags = document.getElementById('prev-skills');
    skillTags.innerHTML = '';
    skills.split(',').map(s => s.trim()).filter(Boolean).forEach(s => {
      const span = document.createElement('span');
      span.className = 'tag';
      span.textContent = s.toUpperCase();
      skillTags.appendChild(span);
    });
  }

  async function loadMatches() {
    const grid = document.getElementById("matchesGrid");
    if (!grid) return;
    grid.innerHTML = `<div class="small-loading">Loading matches...</div>`;

    try {
      allMatches = await apiRequest("/api/matches");
      renderMatches(allMatches);
    } catch (err) {
      grid.innerHTML = `<div class="message error">${escapeHtml(err.message)}</div>`;
    }
  }

  function renderMatches(matches) {
    const grid = document.getElementById("matchesGrid");
    if (!matches || matches.length === 0) {
      grid.innerHTML = `<div class="message">No matches found. Complete your profile and refresh matches.</div>`;
      return;
    }

    grid.innerHTML = matches.map(match => {
      const ai = match.aiAnalysis || {};
      const ideas = Array.isArray(ai.whatYouCanDoTogether) ? ai.whatYouCanDoTogether : [];
      return `
        <div class="match-card animate">
          <div class="match-card-top">
            <div class="match-header">
              <div class="match-identity">
                <div class="match-avatar">${escapeHtml((match.name || '?')[0])}</div>
                <div>
                  <div class="match-name">${escapeHtml(match.name || 'Unknown')}</div>
                  <div class="match-role">${escapeHtml(match.education || 'No education info')}</div>
                </div>
              </div>
              <div class="match-score-block">
                <div class="match-score">${escapeHtml(match.matchScore || 0)}%</div>
                <div class="match-score-label">MATCH SCORE</div>
              </div>
            </div>

            <div class="match-common-label">COMMON POINTS</div>
            <div class="tag-group">${tagsHtml(match.commonPoints)}</div>

            <hr class="match-divider">

            <div class="match-common-label">COMPLEMENTARY POINTS</div>
            <div class="tag-group">${tagsHtml(match.complementaryPoints)}</div>

            <hr class="match-divider">

            <div class="match-stats-row">
              <div>
                <div class="match-stat-label">Skills</div>
                <div class="match-stat-value">${escapeHtml((match.skills || []).join(', '))}</div>
              </div>
              <div>
                <div class="match-stat-label">Interests</div>
                <div class="match-stat-value">${escapeHtml((match.interests || []).join(', '))}</div>
              </div>
            </div>
          </div>

          <div class="match-card-reason">
            <div class="match-reason-icon">✦</div>
            <div class="match-reason-text">
              <strong>Why match:</strong> ${escapeHtml(ai.whyMatch || 'AI analysis is not available.')}<br><br>
              <strong>How you can help:</strong> ${escapeHtml(ai.howYouCanHelpEachOther || '')}
              ${ideas.length ? `<ul class="match-ai-list">${ideas.map(i => `<li>${escapeHtml(i)}</li>`).join('')}</ul>` : ''}
            </div>
          </div>

          <div class="match-card-footer">
            <div class="match-discord-tag">
              <span class="match-discord-hash">#</span>
              <span class="mono">${escapeHtml(match.discordUsername || 'No Discord username')}</span>
            </div>
            <button class="btn btn-primary btn-full" onclick="connectDiscord('${escapeHtml(match.discordLink || '')}', '${escapeHtml(match.discordUsername || '')}')">CONNECT ON DISCORD</button>
          </div>
        </div>
      `;
    }).join('');
  }

  function tagsHtml(items) {
    if (!items || items.length === 0) return `<span class="tag">NONE</span>`;
    return items.map(item => `<span class="tag">${escapeHtml(item)}</span>`).join('');
  }
