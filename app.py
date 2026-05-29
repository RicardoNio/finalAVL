"""
app.py — Servidor Flask que expone el DatabaseManager original como API REST.
NO modifica ningún archivo del proyecto original.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

# ── Importamos exactamente el código original del proyecto ──
from database_manager import DatabaseManager
from exceptions import (
    DatabaseError,
    DuplicateKeyError,
    KeyNotFoundError,
    DatabaseCorruptionError,
    ValidationError,
)

app = Flask(__name__, static_folder="static")
CORS(app)  # Permite que el HTML llame a la API aunque esté en otro puerto

# ── Inicializamos la base de datos original ──
DB_PATH = "data/database.json"
try:
    db = DatabaseManager(DB_PATH)
    print(f"[OK] DatabaseManager inicializado → {DB_PATH}")
except DatabaseCorruptionError as e:
    print(f"[ERROR CRÍTICO] Base de datos corrupta: {e}")
    db = None
except Exception as e:
    print(f"[ERROR INESPERADO] {e}")
    db = None


# ── Helper: convierte excepciones a respuestas JSON ──
def err(msg: str, code: int = 400):
    return jsonify({"ok": False, "error": msg}), code


def ok(data=None, msg: str = None):
    payload = {"ok": True}
    if data is not None:
        payload["data"] = data
    if msg:
        payload["message"] = msg
    return jsonify(payload)


def check_db():
    if db is None:
        return err("La base de datos no está disponible.", 503)
    return None


# ══════════════════════════════════════════════════════════
#  ENDPOINTS
# ══════════════════════════════════════════════════════════

# ── GET /api/records → listar todos (inorder AVL) ──
@app.route("/api/records", methods=["GET"])
def list_records():
    if (e := check_db()):
        return e
    try:
        registros = db.get_all_sorted()
        return ok(registros)
    except DatabaseError as e:
        return err(str(e))


# ── POST /api/records → insertar ──
@app.route("/api/records", methods=["POST"])
def insert_record():
    if (e := check_db()):
        return e
    body = request.get_json(silent=True)
    if not body:
        return err("El cuerpo de la solicitud debe ser JSON.")
    try:
        # Convierte id a int por si viene como string desde el formulario
        if "id" in body:
            body["id"] = int(body["id"])
        db.save_record(body)
        return ok(msg=f"Registro con ID {body['id']} guardado correctamente."), 201
    except (DuplicateKeyError, ValidationError) as e:
        return err(str(e))
    except ValueError:
        return err("El ID debe ser un número entero válido.")
    except DatabaseError as e:
        return err(str(e), 500)


# ── GET /api/records/<id> → buscar por ID (O log n) ──
@app.route("/api/records/<int:record_id>", methods=["GET"])
def get_record(record_id):
    if (e := check_db()):
        return e
    try:
        registro = db.find_by_id(record_id)
        return ok(registro)
    except KeyNotFoundError as e:
        return err(str(e), 404)
    except ValidationError as e:
        return err(str(e))


# ── PUT /api/records/<id> → actualizar ──
@app.route("/api/records/<int:record_id>", methods=["PUT"])
def update_record(record_id):
    if (e := check_db()):
        return e
    body = request.get_json(silent=True)
    if not body:
        return err("El cuerpo de la solicitud debe ser JSON.")
    try:
        body["id"] = record_id  # forzamos el id de la URL
        db.update_record(body)
        return ok(msg=f"Registro con ID {record_id} actualizado correctamente.")
    except KeyNotFoundError as e:
        return err(str(e), 404)
    except (ValidationError, DatabaseError) as e:
        return err(str(e))


# ── DELETE /api/records/<id> → eliminar ──
@app.route("/api/records/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    if (e := check_db()):
        return e
    try:
        db.delete_record(record_id)
        return ok(msg=f"Registro {record_id} eliminado correctamente.")
    except KeyNotFoundError as e:
        return err(str(e), 404)
    except (ValidationError, DatabaseError) as e:
        return err(str(e))


# ── GET /api/search?field=categoria&value=Electronica ──
@app.route("/api/search", methods=["GET"])
def search_by_criteria():
    if (e := check_db()):
        return e
    field = request.args.get("field", "").strip()
    value = request.args.get("value", "").strip()
    if not field or not value:
        return err("Se requieren los parámetros 'field' y 'value'.")
    try:
        resultados = db.find_by_criteria(field, value)
        return ok(resultados)
    except DatabaseError as e:
        return err(str(e))


# ── GET /api/tree → estructura del árbol para visualización ──
@app.route("/api/tree", methods=["GET"])
def get_tree_structure():
    if (e := check_db()):
        return e
    estructura = db.tree.get_structure_dict(db.root)
    altura     = db.tree.get_height(db.root)
    total      = len(db.get_all_sorted())
    return ok({"structure": estructura, "height": altura, "total": total})


# ── Sirve el frontend (index.html) desde /static ──
@app.route("/")
def index():
    return send_from_directory("static", "index.html")


if __name__ == "__main__":
    print("\n" + "="*55)
    print("  GESTOR AVL — Servidor Flask")
    print("  http://localhost:5000")
    print("="*55 + "\n")
    app.run(debug=True, port=5000)
