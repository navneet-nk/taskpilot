const KEY = "taskpilot_tasks";

function load() {
  return JSON.parse(localStorage.getItem(KEY) || "[]");
}

function save(tasks) {
  localStorage.setItem(KEY, JSON.stringify(tasks));
}

const api = {
  listTasks() {
    return load();
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