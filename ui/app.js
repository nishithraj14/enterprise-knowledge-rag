const API_BASE = "http://localhost:8000";

let selectedDocument = null;

// -----------------------------
// Load documents
// -----------------------------
async function loadDocuments() {
  const res = await fetch(`${API_BASE}/documents`);
  const data = await res.json();

  const list = document.getElementById("docList");
  list.innerHTML = "";

  data.documents.forEach(doc => {
    const li = document.createElement("li");
    li.textContent = doc;

    li.onclick = () => {
      document.querySelectorAll(".sidebar li").forEach(x => x.classList.remove("active"));
      li.classList.add("active");
      selectedDocument = doc;
    };

    list.appendChild(li);
  });
}

// -----------------------------
// Upload
// -----------------------------
async function upload() {
  const files = document.getElementById("fileUpload").files;
  if (!files.length) return;

  const form = new FormData();
  for (const f of files) form.append("files", f);

  await fetch(`${API_BASE}/ingest`, { method: "POST", body: form });
  await loadDocuments();
}

// -----------------------------
// Ask
// -----------------------------
async function ask() {
  const question = document.getElementById("question").value.trim();
  if (!question) return;

  const mode = document.querySelector('input[name="mode"]:checked').value;

  const payload = {
    question,
    source: mode === "selected" ? selectedDocument : null
  };

  const res = await fetch(`${API_BASE}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  const data = await res.json();
  document.getElementById("response").textContent = data.answer;
}

loadDocuments();
