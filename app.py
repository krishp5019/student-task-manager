from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("task.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            priority TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

@app.route('/', methods=['GET','POST'])
def home():
    
    if request.method == "POST":
        task = request.form["task"]
        priority = request.form["priority"]
        if not task.strip():
            return redirect("/")
        
        conn = get_db_connection()
        conn.execute("INSERT INTO tasks(task,priority) values (?,?)",(task,priority))
        conn.commit()
        print("Task saved!")
        conn.close()

    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks WHERE completed=0").fetchall()
    #print(tasks)
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>", methods=["POST"])
def delete_task(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id=?",(id,))

    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit_task(id):
    if request.method == "POST":
        task = request.form['task']
        priority = request.form['priority']

        conn = get_db_connection()
        conn.execute("UPDATE tasks SET task= ?, priority = ? WHERE id=?",(task,priority,id))
        conn.commit()
        conn.close()

        return redirect("/" )

    conn = get_db_connection()
    task = conn.execute("SELECT * FROM tasks WHERE id=?",(id,)).fetchone()

    conn.close()
    return render_template("edit.html", task=task)

@app.route("/completed/<int:id>", methods=["POST"])
def completed_task(id):
    conn = get_db_connection()
    conn.execute(
        "UPDATE tasks SET completed = 1 WHERE id = ?",
        (id,)
    )
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/comp_tasks", methods=["GET"])
def show_comp_tasks():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks WHERE completed=1").fetchall()
    conn.close()
    return render_template("comp_tasks.html",tasks = tasks)


if __name__ == "__main__":  
    init_db()
    app.run(debug=True)