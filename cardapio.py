import sqlite3
import customtkinter as ctk
from tkinter import ttk, messagebox

# ---------------- CONFIGURAÇÃO ----------------
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("dark-blue")
janela = ctk.CTk()
janela.title("Cardápio Digital")
janela.geometry("850x600")
# ---------------- BANCO ----------------

conexao = sqlite3.connect("cardapio.db")
cursor = conexao.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS pratos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    ingredientes TEXT,
    preco REAL,
    disponibilidade TEXT
)
""")

conexao.commit()
id_atual = None

# ---------------- FUNÇÕES ----------------
def mostrar():
    tabela.delete(*tabela.get_children())

    cursor.execute("SELECT * FROM pratos")

    for linha in cursor.fetchall():
        tabela.insert("", "end", values=linha)


def limpar():
    global id_atual

    nome.delete(0, "end")
    ingredientes.delete(0, "end")
    preco.delete(0, "end")
    disponibilidade.set("Disponível")
    id_atual = None


def salvar():
    cursor.execute("""
    INSERT INTO pratos(nome, ingredientes, preco, disponibilidade)
    VALUES(?,?,?,?)
    """, (
        nome.get(),
        ingredientes.get(),
        preco.get(),
        disponibilidade.get()
    ))
    conexao.commit()

    mostrar()
    limpar()


def selecionar(event):
    global id_atual
    item = tabela.focus()
    if item == "":
        return

    dados = tabela.item(item)["values"]
    limpar()
    id_atual = dados[0]

    nome.insert(0, dados[1])
    ingredientes.insert(0, dados[2])
    preco.insert(0, dados[3])
    disponibilidade.set(dados[4])


def atualizar():
    if id_atual is None:
        messagebox.showwarning("Aviso", "Selecione um prato.")
        return

    cursor.execute("""
    UPDATE pratos
    SET nome=?, ingredientes=?, preco=?, disponibilidade=?
    WHERE id=?
    """, (
        nome.get(),
        ingredientes.get(),
        preco.get(),
        disponibilidade.get(),
        id_atual
    ))
    conexao.commit()

    mostrar()
    limpar()


def excluir():
    if id_atual is None:
        messagebox.showwarning("Aviso", "Selecione um prato.")
        return

    cursor.execute("DELETE FROM pratos WHERE id=?", (id_atual,))
    conexao.commit()

    mostrar()
    limpar()

def buscar():
    tabela.delete(*tabela.get_children())

    cursor.execute(
        "SELECT * FROM pratos WHERE nome LIKE ?",
        ("%" + pesquisa.get() + "%",)
    )
    for linha in cursor.fetchall():
        tabela.insert("", "end", values=linha)

# ---------------- TÍTULO ----------------
titulo = ctk.CTkLabel(
    janela,
    text="🍽️ CARDÁPIO DIGITAL",
    font=("Arial", 28, "bold"),
    text_color="#f6b06b"
)
titulo.pack(pady=(0, 10))
# ---------------- FORMULÁRIO ----------------

frame = ctk.CTkFrame(janela, fg_color="#ffefd0")
frame.pack(padx=20, fill="x")

ctk.CTkLabel(frame,text="🍝 Prato").grid(row=0,column=0,padx=10,pady=8)
nome = ctk.CTkEntry(frame,width=250, border_color="#f6b06b", fg_color="white")
nome.grid(row=0,column=1)

ctk.CTkLabel(frame,text="🥗 Ingredientes").grid(row=1,column=0,padx=10,pady=8)
ingredientes = ctk.CTkEntry(frame,width=250, border_color="#f6b06b", fg_color="white")
ingredientes.grid(row=1,column=1)

ctk.CTkLabel(frame,text="💰 Preço").grid(row=2,column=0,padx=10,pady=8)
preco = ctk.CTkEntry(frame,width=150, border_color="#f6b06b", fg_color="white")
preco.grid(row=2,column=1)

ctk.CTkLabel(frame,text="📦 Disponibilidade").grid(row=3,column=0,padx=10,pady=8)

disponibilidade = ctk.CTkComboBox(
    frame, values=["Disponível","Indisponível"], button_color="#ffd2a2", button_hover_color="#f6b06b", border_color="#ffd2a2", text_color="#000")
disponibilidade.grid(row=3,column=1)
disponibilidade.set("Disponível")

# ---------------- BOTÕES ----------------
botoes = ctk.CTkFrame(janela, fg_color="#ffefd0")
botoes.pack(pady=15)

ctk.CTkButton(botoes,text="💾 Salvar",command=salvar, fg_color="#ffd2a2", hover_color="#f6b06b", text_color="#000").grid(row=0,column=0,padx=5)
ctk.CTkButton(botoes,text="✏️ Atualizar",command=atualizar, fg_color="#ffd2a2", hover_color="#f6b06b", text_color="#000").grid(row=0,column=1,padx=5)
ctk.CTkButton(botoes,text="🗑️ Excluir",command=excluir, fg_color="#ffd2a2", hover_color="#f6b06b", text_color="#000").grid(row=0,column=2,padx=5)
ctk.CTkButton(botoes,text="🧹 Limpar",command=limpar, fg_color="#ffd2a2", hover_color="#f6b06b", text_color="#000").grid(row=0,column=3,padx=5)
# ---------------- BUSCA ----------------

busca = ctk.CTkFrame(janela,fg_color="#ffefd0")
busca.pack(fill="x",padx=20)

pesquisa = ctk.CTkEntry(busca,width=250,placeholder_text="Buscar prato")
pesquisa.grid(row=0,column=0,padx=10,pady=10)

ctk.CTkButton(busca,text="🔍 Buscar",command=buscar, fg_color="#ffd2a2", hover_color="#f6b06b", text_color="#000").grid(row=0,column=1,padx=5)
ctk.CTkButton(busca,text="📋 Mostrar Todos",command=mostrar, fg_color="#ffd2a2", hover_color="#f6b06b", text_color="#000").grid(row=0,column=2,padx=5)

# ---------------- TABELA ----------------
colunas = ("ID","Prato","Ingredientes","Preço","Disponibilidade")

tabela = ttk.Treeview(janela, columns=colunas, show="headings",height=12)

for coluna in colunas:
    tabela.heading(coluna,text=coluna)
tabela.pack(fill="both",expand=True,padx=20,pady=15)
tabela.bind("<<TreeviewSelect>>", selecionar)
mostrar()

janela.mainloop()
