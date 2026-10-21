const API_URL = "http://127.0.0.1:8000";

function getToken() {
  return localStorage.getItem("taskpilot_token");
}

function getUsername() {
  return localStorage.getItem("taskpilot_user");
}

function saveSession(token, username) {
  localStorage.setItem("taskpilot_token", token);
  localStorage.setItem("taskpilot_user", username);
}

function clearSession() {
  localStorage.removeItem("taskpilot_token");
  localStorage.removeItem("taskpilot_user");
}

async function authRequest(path, username, password) {
  let res;
  try {
    res = await fetch(API_URL + path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
  } catch (err) {
    throw new Error("Server se connect nahi ho paaya. Kya API chal rahi hai?");
  }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    if (typeof data.detail === "string") throw new Error(data.detail);
    throw new Error("Username kam se kam 3 aur password kam se kam 6 characters ka hona chahiye.");
  }
  return data;
}