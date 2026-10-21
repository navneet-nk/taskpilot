const form = document.getElementById("add-form");
const input = document.getElementById("title");
const priorityInput = document.getElementById("priority");
const dueInput = document.getElementById("due");
const searchInput = document.getElementById("search");
const statusSelect = document.getElementById("status");
const list = document.getElementById("task-list");
const empty = document.getElementById("empty");

async function render() {
  let tasks;
  try {
    tasks = await api.listTasks({
      status: statusSelect.value,
      search: searchInput.value,
    });
  } catch (err) {
    list.innerHTML = "";
    empty.style.display = "block";
    empty.textContent = "Server se connect nahi ho paaya. Kya API chal rahi hai?";
    return;
  }

  list.innerHTML = "";
  empty.textContent = "No tasks yet.";
  empty.style.display = tasks.length ? "none" : "block";

  tasks.forEach((t) => {
    const li = document.createElement("li");
    li.className = "task" + (t.done ? " done" : "");

    const check = document.createElement("input");
    check.type = "checkbox";
    check.checked = t.done;
    check.addEventListener("change", async () => {
      await api.completeTask(t.id, check.checked);
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
    del.addEventListener("click", async () => {
      await api.deleteTask(t.id);
      render();
    });

    li.append(check, span, badge, dueText, del);
    list.append(li);
  });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = input.value.trim();
  if (!title) return;
  await api.addTask(title, priorityInput.value, dueInput.value || null);
  input.value = "";
  dueInput.value = "";
  render();
});

searchInput.addEventListener("input", render);
statusSelect.addEventListener("change", render);

render();