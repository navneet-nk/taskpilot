if (!getToken()) {
  window.location.href = "login.html";
}

const form = document.getElementById("add-form");
const input = document.getElementById("title");
const priorityInput = document.getElementById("priority");
const dueInput = document.getElementById("due");
const searchInput = document.getElementById("search");
const statusInput = document.getElementById("status");
const statusButtons = document.querySelectorAll(".segmented button");
const list = document.getElementById("task-list");
const empty = document.getElementById("empty");
const summary = document.getElementById("summary");
const toast = document.getElementById("toast");

const TRASH_ICON =
  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 7h16M10 11v6M14 11v6M6 7l1 12a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2l1-12M9 7V4h6v3"/></svg>';

let firstRender = true;
let toastTimer;

// ---------- header ----------

const username = getUsername() || "";
document.getElementById("user").textContent = username;
document.getElementById("logout").addEventListener("click", () => {
  clearSession();
  window.location.href = "login.html";
});

(function setGreeting() {
  const h = new Date().getHours();
  const part = h < 12 ? "Good morning" : h < 17 ? "Good afternoon" : "Good evening";
  document.getElementById("greeting").textContent = username ? part + ", " + username : part;
})();

// ---------- helpers ----------

function todayString() {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, "0");
  return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
}

function formatDue(due) {
  if (!due) return "No date";
  return new Date(due + "T00:00:00").toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
  });
}

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), 3500);
}

async function run(action) {
  let ok = true;
  try {
    await action();
  } catch (err) {
    ok = false;
    if (err.message !== "Session expired") {
      showToast("Couldn't save that change. Check that the API is running.");
    }
  }
  render();
  return ok;
}

function renderSummary(tasks) {
  const today = todayString();
  const done = tasks.filter((t) => t.done).length;
  const open = tasks.length - done;
  const overdue = tasks.filter((t) => !t.done && t.due && t.due < today).length;

  summary.innerHTML = "";
  if (!tasks.length) return;

  const parts = [];
  const openEl = document.createElement("b");
  openEl.textContent = open + " open";
  parts.push(openEl);
  if (overdue) {
    const w = document.createElement("span");
    w.className = "warn";
    w.textContent = overdue + " overdue";
    parts.push(w);
  }
  parts.push(document.createTextNode(done + " done"));

  parts.forEach((p, i) => {
    if (i) summary.append(", ");
    summary.append(p);
  });
}

// ---------- render ----------

async function render() {
  let tasks;
  try {
    tasks = await api.listTasks({
      status: statusInput.value,
      search: searchInput.value,
    });
  } catch (err) {
    list.innerHTML = "";
    summary.innerHTML = "";
    empty.style.display = "block";
    empty.textContent = "Can't reach the server. Start the API and refresh the page.";
    return;
  }

  renderSummary(tasks);
  list.innerHTML = "";

  const filtering = statusInput.value || searchInput.value;
  empty.textContent = filtering
    ? "No tasks match these filters."
    : "No tasks yet. Add your first task above.";
  empty.style.display = tasks.length ? "none" : "block";

  const today = todayString();

  tasks.forEach((t, i) => {
    const priority = t.priority || "medium";
    const overdue = !t.done && t.due && t.due < today;

    const li = document.createElement("li");
    li.className = "task " + priority + (t.done ? " done" : "") + (overdue ? " overdue" : "");
    if (firstRender) {
      li.classList.add("enter");
      li.style.setProperty("--i", Math.min(i, 8));
    }

    const checkCell = document.createElement("div");
    checkCell.className = "check-cell";
    const check = document.createElement("input");
    check.type = "checkbox";
    check.checked = t.done;
    check.setAttribute("aria-label", "Mark \"" + t.title + "\" as done");
    check.addEventListener("change", () => run(() => api.completeTask(t.id, check.checked)));
    checkCell.append(check);

    const title = document.createElement("span");
    title.className = "title";
    title.textContent = t.title;

    const priorityCell = document.createElement("span");
    priorityCell.className = "cell priority";
    priorityCell.textContent = priority;

    const dueCell = document.createElement("span");
    dueCell.className = "cell due";
    dueCell.textContent = (overdue ? "Overdue " : "") + formatDue(t.due);

    const del = document.createElement("button");
    del.type = "button";
    del.className = "remove";
    del.innerHTML = TRASH_ICON;
    del.setAttribute("aria-label", "Delete \"" + t.title + "\"");
    del.addEventListener("click", () => run(() => api.deleteTask(t.id)));

    li.append(checkCell, title, priorityCell, dueCell, del);
    list.append(li);
  });

  firstRender = false;
}

// ---------- events ----------

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = input.value.trim();
  if (!title) return;
  const ok = await run(() => api.addTask(title, priorityInput.value, dueInput.value || null));
  if (ok) {
    input.value = "";
    dueInput.value = "";
  }
  input.focus();
});

searchInput.addEventListener("input", render);

statusButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    statusInput.value = btn.dataset.status;
    statusButtons.forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
    render();
  });
});

render();
