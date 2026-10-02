const $ = (id) => document.getElementById(id);
let students = [];

async function api(path, options = {}) {
  const res = await fetch(path, {headers: {"Content-Type":"application/json", ...(options.headers||{})}, ...options});
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || `Request failed (${res.status})`);
  return data;
}

function showView(view){
  document.querySelectorAll(".view").forEach(v=>v.classList.add("hidden"));
  $(`${view}View`).classList.remove("hidden");
  document.querySelectorAll(".nav-item").forEach(b=>b.classList.toggle("active", b.dataset.view===view));
  const titles={dashboard:"Good day 👋",students:"Student records",add:"Add a student",chat:"AI Assistant"};
  $("pageTitle").textContent=titles[view];
  if(view==="students") renderStudents();
  if(view==="dashboard") renderDashboard();
}
document.querySelectorAll(".nav-item").forEach(b=>b.addEventListener("click",()=>showView(b.dataset.view)));
$("quickAdd").onclick=()=>showView("add");
$("heroStudents").onclick=()=>showView("students");
$("allStudents").onclick=()=>showView("students");
$("cancelForm").onclick=()=>showView("dashboard");

function initials(name){ return (name||"?").split(" ").map(x=>x[0]).slice(0,2).join("").toUpperCase(); }
function skillPills(skills){
  return (skills||"").split(",").filter(Boolean).map(s=>`<span class="pill">${s.trim()}</span>`).join("");
}
function studentCell(s){
  return `<div class="student-name">${escapeHtml(s.name)}</div><div class="student-email">${escapeHtml(s.email)}</div>`;
}
function escapeHtml(s){return String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]));}

function renderDashboard(){
  $("totalStudents").textContent=students.length;
  $("branchCount").textContent=new Set(students.map(s=>s.branch).filter(Boolean)).size;
  $("yearCount").textContent=new Set(students.map(s=>s.year).filter(Boolean)).size;
  $("recentTable").innerHTML=students.slice(0,5).map(s=>`<tr><td>${studentCell(s)}</td><td>${escapeHtml(s.college)}</td><td>${escapeHtml(s.branch)}</td><td>${escapeHtml(s.year)}</td><td>${skillPills(s.skills)}</td></tr>`).join("") || `<tr><td colspan="5">No students yet.</td></tr>`;
}
function renderStudents(){
  const q=($("searchInput").value||"").toLowerCase();
  const list=students.filter(s=>JSON.stringify(s).toLowerCase().includes(q));
  $("studentsTable").innerHTML=list.map(s=>`<tr><td>${studentCell(s)}</td><td>${escapeHtml(s.email)}</td><td>${escapeHtml(s.college)}</td><td>${escapeHtml(s.branch)}</td><td>${escapeHtml(s.year)}</td><td><button class="action-btn" onclick="deleteStudent(${s.id})">Delete</button></td></tr>`).join("") || `<tr><td colspan="6">No matching records.</td></tr>`;
}
async function loadStudents(){
  try{students=await api("/students/");renderDashboard();renderStudents();}
  catch(e){console.error(e);$("recentTable").innerHTML=`<tr><td colspan="5">Could not load students: ${escapeHtml(e.message)}</td></tr>`;}
}
$("searchInput").addEventListener("input",renderStudents);

$("studentForm").addEventListener("submit",async e=>{
  e.preventDefault();
  const f=new FormData(e.target);
  const payload=Object.fromEntries(f.entries());
  payload.year=Number(payload.year);
  try{
    await api("/students/",{method:"POST",body:JSON.stringify(payload)});
    $("formMessage").textContent="Student saved successfully.";
    e.target.reset(); await loadStudents(); setTimeout(()=>showView("students"),500);
  }catch(err){$("formMessage").textContent=err.message;}
});
async function deleteStudent(id){
  if(!confirm("Delete this student record?")) return;
  try{await api(`/students/${id}`,{method:"DELETE"});await loadStudents();}catch(e){alert(e.message);}
}

document.querySelectorAll(".example-prompts button").forEach(b=>b.onclick=()=>{$("chatInput").value=b.textContent;$("chatInput").focus();});
$("chatForm").addEventListener("submit",async e=>{
  e.preventDefault();
  const input=$("chatInput"), q=input.value.trim(); if(!q)return;
  addChat(q,"user"); input.value="";
  addChat("Thinking…","assistant");
  const last=$("chatMessages").lastElementChild;
  try{
    const data=await api("/chatbot/ask",{method:"POST",body:JSON.stringify({question:q})});
    last.textContent=data.answer || "No answer returned.";
  }catch(err){last.textContent=`Chatbot error: ${err.message}`;}
});
function addChat(text,type){
  const div=document.createElement("div");div.className=`chat-bubble ${type}`;div.textContent=text;$("chatMessages").appendChild(div);$("chatMessages").scrollTop=$("chatMessages").scrollHeight;
}
loadStudents();
