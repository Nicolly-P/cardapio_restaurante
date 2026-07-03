from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def conectar():
    return sqlite3.connect("cardapio.db")

@app.route("/")
def inicio():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM pratos")
    pratos = cursor.fetchall()
    conexao.close()
    return render_template("index.html", pratos=pratos)

@app.route("/adicionar", methods=["POST"])
def adicionar():
    nome = request.form["nome"]
    ingredientes = request.form["ingredientes"]
    preco = request.form["preco"]
    disponibilidade = request.form["disponibilidade"]
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
    INSERT INTO pratos(nome, ingredientes, preco, disponibilidade)
    VALUES(?,?,?,?)
    """, (nome, ingredientes, preco, disponibilidade))
    conexao.commit()
    conexao.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
