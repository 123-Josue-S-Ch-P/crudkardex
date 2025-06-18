from flask import Flask, request, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)

# Conexion a la base de datos
def get_db_connection():
    conn = sqlite3.connect("bd_kardex.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS personal(
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            fecha_nac DATE NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

# Crear la tabla en la base de datos
init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/personal")
def personal():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personal")
    personal = cursor.fetchall()
    return render_template("personal.html", personal=personal)

@app.route("/personal/nuevo", methods=['GET', 'POST'])
def nuevo_personal():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        fecha_nac = request.form['fecha_nac']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO personal (nombre, telefono, fecha_nac) VALUES (?, ?, ?)",
                       (nombre, telefono, fecha_nac))
        conn.commit()
        conn.close()
        return redirect(url_for('personal'))
    return render_template('form_personal.html')

# EDITAR PERSONA
@app.route("/personal/edit/<int:id>", methods=['GET', 'POST'])
def persona_edit(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personal WHERE id = ?", (id,))
    personal = cursor.fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        fecha_nac = request.form['fecha_nac']
        cursor.execute("UPDATE personal SET nombre = ?, telefono = ?, fecha_nac = ? WHERE id = ?",
                       (nombre, telefono, fecha_nac, id))
        conn.commit()
        return redirect(url_for('personal'))

    conn.close()
    return render_template("edit.html", personal=personal)

# ELIMINAR REGISTRO
@app.route("/personal/delete/<int:id>")
def personas_delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personal WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/personal')

if __name__ == '__main__':
    app.run(debug=True)
