const BASE_URL = "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const res = await fetch(BASE_URL + path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error("Request failed: " + res.status);
  return res.status === 204 ? null : res.json();
}

const api = {
  listTasks({ status, search } = {}) {
    const params = new URLSearchParams();
    if (status) params.set("status", status);
    if (search) params.set("search", search);
    const qs = params.toString();
    return request("/tasks" + (qs ? "?" + qs : ""));
  },
  addTask(title, priority = "medium", due = null) {
    return request("/tasks", {
      method: "POST",
      body: JSON.stringify({ title, priority, due }),
    });
  },
  completeTask(id, done) {
    return request("/tasks/" + id, {
      method: "PATCH",
      body: JSON.stringify({ done }),
    });
  },
  deleteTask(id) {
    return request("/tasks/" + id, { method: "DELETE" });
  },
};