const form = document.getElementById("add-form");
const input = document.getElementById("title");
const list = document.getElementById("task-list");
const empty = document.getElementById("empty");
const priorityInput = document.getElementById("priority");
const dueInput = document.getElementById("due");

function render() {
  const tasks = api.listTasks();
  list.innerHTML = "";
  empty.style.display = tasks.length ? "none" : "block";

  tasks.forEach((t) => {
    const li = document.createElement("li");
    li.className = "task" + (t.done ? " done" : "");

    const check = document.createElement("input");
    check.type = "checkbox";
    check.checked = t.done;
    check.addEventListener("change", () => {
      api.completeTask(t.id);
      render();
    });

    const span = document.createElement("span");
    span.className = "title";
    span.textContent = t.title;

    const badge = document.createElement("span");
    badge.className = "badge " + (t.priority || "medium");
    badge.textContent = t.priority || "medium";

    const dueText = document.createElement("small");
    dueText.textContent = t.due ? "Due " + t.due : "";

    const del = document.createElement("button");
    del.textContent = "Delete";
    del.addEventListener("click", () => {
      api.deleteTask(t.id);
      render();
    });

    li.append(check, span, badge, dueText, del);
    list.append(li);
  });
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const title = input.value.trim();
  if (!title) return;
  api.addTask(title, priorityInput.value, dueInput.value || null);
  input.value = "";
  dueInput.value = "";
  render();
});

render();