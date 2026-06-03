const API = "";

async function load() {
    const res = await fetch(`${API}/records`);
    const data = await res.json();

    const table = document.getElementById("table");
    table.innerHTML = "";

    data.forEach(r => {
        table.innerHTML += `
        <tr>
            <td>${r[0]}</td>
            <td>${r[1]}</td>
            <td>${r[2]}</td>
            <td>
                <button onclick="del(${r[0]})">Eliminar</button>
            </td>
        </tr>`;
    });
}

async function create() {
    const nombre = document.getElementById("nombre").value;
    const email = document.getElementById("email").value;

    await fetch(`/records`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ nombre, email })
    });

    load();
}

async function del(id) {
    await fetch(`/records/${id}`, { method: "DELETE" });
    load();
}

async function setup() {
    await fetch(`/setup`);
    alert("Tabla creada");
}
``