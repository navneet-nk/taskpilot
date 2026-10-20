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
  addTask(title) {
    const tasks = load();
    const id = tasks.reduce((max, t) => Math.max(max, t.id), 0) + 1;
    const task = { id, title, done: false };
    tasks.push(task);
    save(tasks);
    return task;
  },
};