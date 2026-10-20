const KEY = "taskpilot_tasks";

function load() {
  return JSON.parse(localStorage.getItem(KEY) || "[]");
}

function save(tasks) {
  localStorage.setItem(KEY, JSON.stringify(tasks));
}

const api = {
  listTasks({ status, search } = {}) {
    let tasks = load();
    if (status === "done") tasks = tasks.filter((t) => t.done);
    if (status === "pending") tasks = tasks.filter((t) => !t.done);
    if (search) {
      tasks = tasks.filter((t) => t.title.toLowerCase().includes(search.toLowerCase()));
    }
    const order = { high: 0, medium: 1, low: 2 };
    return tasks.sort((a, b) => (order[a.priority] ?? 1) - (order[b.priority] ?? 1));
  },
  addTask(title, priority = "medium", due = null) {
    const tasks = load();
    const id = tasks.reduce((max, t) => Math.max(max, t.id), 0) + 1;
    const task = { id, title, done: false, priority, due };
    tasks.push(task);
    save(tasks);
    return task;
  },
  completeTask(id) {
    const tasks = load();
    const t = tasks.find((x) => x.id === id);
    if (!t) return false;
    t.done = !t.done;
    save(tasks);
    return true;
  },
  deleteTask(id) {
    const tasks = load();
    const rest = tasks.filter((x) => x.id !== id);
    if (rest.length === tasks.length) return false;
    save(rest);
    return true;
  },
};