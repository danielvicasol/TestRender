from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

def get_database_url():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise Exception("DATABASE_URL no está definida")
    return db_url

def get_connection():
    return psycopg2.connect(
        get_database_url(),
        sslmode="require"
    )

@app.get("/")
def root():
    return {"status": "API funcionando"}

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

@app.get("/setup")
def setup():
    try:
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

        return {"ok": True, "message": "Tabla creada"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.get("/insert")
def insert():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO demo_records (nombre, email)
        VALUES ('Usuario Render', 'render@test.com')
        RETURNING id;
        """)

        new_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return {"ok": True, "id": new_id}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.get("/records")
def get_records():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM demo_records ORDER BY id DESC")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return {"data": rows}
    except Exception as e:
        return {"ok": False, "error": str(e)}
