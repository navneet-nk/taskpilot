const form = document.getElementById("add-form");
const input = document.getElementById("title");
const list = document.getElementById("task-list");
const empty = document.getElementById("empty");

function render() {
  const tasks = api.listTasks();
  list.innerHTML = "";
  empty.style.display = tasks.length ? "none" : "block";

  tasks.forEach((t) => {
    const li = document.createElement("li");
    li.className = "task" + (t.done ? " done" : "");

    const span = document.createElement("span");
    span.className = "title";
    span.textContent = t.title;

    li.append(span);
    list.append(li);
  });
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const title = input.value.trim();
  if (!title) return;
  api.addTask(title);
  input.value = "";
  render();
});

render();