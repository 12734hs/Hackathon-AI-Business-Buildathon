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
