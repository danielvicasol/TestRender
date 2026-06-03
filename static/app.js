async function load(){
 const res = await fetch('/records');
 const data = await res.json();
 const t = document.getElementById('table');
 t.innerHTML='';
 data.forEach(r=>{
  t.innerHTML += `<tr>
   <td>${r[0]}</td>
   <td><input value="${r[1]}" id="n${r[0]}"></td>
   <td><input value="${r[2]}" id="e${r[0]}"></td>
   <td>
    <button onclick="update(${r[0]})">Guardar</button>
    <button onclick="del(${r[0]})">Eliminar</button>
   </td>
  </tr>`;
 });
}

async function create(){
 const nombre=document.getElementById('nombre').value;
 const email=document.getElementById('email').value;
 await fetch('/records',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({nombre,email})});
 load();
}

async function update(id){
 const nombre=document.getElementById('n'+id).value;
 const email=document.getElementById('e'+id).value;
 await fetch('/records/'+id,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({nombre,email})});
 load();
}

async function del(id){
 await fetch('/records/'+id,{method:'DELETE'});
 load();
}

async function setup(){
 await fetch('/setup');
 alert('BD lista');
}
