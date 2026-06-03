from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import psycopg2
import os

app = FastAPI()

# ✅ STATIC FILES
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")

def get_database_url():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise Exception("DATABASE_URL no definida")
    return db_url

def get_connection():
    return psycopg2.connect(get_database_url(), sslmode="require")

# ✅ TEST DB
@app.get("/test-db")
def test_db():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT NOW()")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return {"ok": True, "server_time": str(result)}
    except Exception as e:
        return {"ok": False, "error": str(e)}

# ✅ SETUP
@app.get("/setup")
def setup():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS demo_records (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100),
        email VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    cur.close()
    conn.close()

    return {"ok": True}

# ✅ CREATE (POST real)
@app.post("/records")
def create_record(data: dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO demo_records (nombre, email)
    VALUES (%s, %s)
    RETURNING id;
    """, (data["nombre"], data["email"]))

    new_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return {"id": new_id}

# ✅ READ
@app.get("/records")
def get_records():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM demo_records ORDER BY id DESC")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows

# ✅ UPDATE
@app.put("/records/{id}")
def update_record(id: int, data: dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    UPDATE demo_records
    SET nombre=%s, email=%s
    WHERE id=%s
    """, (data["nombre"], data["email"], id))

    conn.commit()

    cur.close()
    conn.close()

    return {"ok": True}

# ✅ DELETE
@app.delete("/records/{id}")
def delete_record(id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM demo_records WHERE id=%s", (id,))
    conn.commit()

    cur.close()
    conn.close()

    return {"ok": True}