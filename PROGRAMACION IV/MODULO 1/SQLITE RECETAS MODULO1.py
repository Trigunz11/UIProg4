import sqlite3
import os

APP_PATH = os.getcwd()
DB_PATH = os.path.join(APP_PATH, 'recipes.db')

con = sqlite3.connect(DB_PATH)
cursor = con.cursor()

def crear_tabla():
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS recetas(
            ID            INTEGER         PRIMARY KEY     AUTOINCREMENT,
            NOMBRE        TEXT                           NOT NULL,
            INSTRUCCIONES TEXT                           NOT NULL
            )
            """
    )
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingredientes(
            ID            INTEGER         PRIMARY KEY     AUTOINCREMENT,
            RECETA_ID     INTEGER                         NOT NULL,
            INGREDIENTE   TEXT                           NOT NULL,
            FOREIGN KEY (RECETA_ID) REFERENCES recetas(ID)
            )
            """
    )

def agregar_receta(nombre, instrucciones, ingredientes):
    cursor.execute("INSERT INTO recetas(nombre, instrucciones) VALUES (?, ?)", (nombre, instrucciones))
    receta_id = cursor.lastrowid
    for ingrediente in ingredientes:
        cursor.execute("INSERT INTO ingredientes(receta_id, ingrediente) VALUES (?, ?)", (receta_id, ingrediente))
    con.commit()

def editar_receta(nombre, nuevas_instrucciones, nuevos_ingredientes):
    cursor.execute("UPDATE recetas SET instrucciones = ? WHERE nombre = ?", (nuevas_instrucciones, nombre))
    receta_id = cursor.execute("SELECT ID FROM recetas WHERE nombre = ?", (nombre,)).fetchone()[0]
    cursor.execute("DELETE FROM ingredientes WHERE receta_id = ?", (receta_id,))
    for ingrediente in nuevos_ingredientes:
        cursor.execute("INSERT INTO ingredientes(receta_id, ingrediente) VALUES (?, ?)", (receta_id, ingrediente))
    con.commit()

def eliminar_receta(nombre):
    receta_id = cursor.execute("SELECT ID FROM recetas WHERE nombre = ?", (nombre,)).fetchone()[0]
    cursor.execute("DELETE FROM recetas WHERE nombre = ?", (nombre,))
    cursor.execute("DELETE FROM ingredientes WHERE receta_id = ?", (receta_id,))
    con.commit()

def obtener_recetas(): 
    cursor.execute("SELECT nombre FROM recetas")
    return cursor.fetchall()

def buscar_receta(nombre):
    receta = cursor.execute("SELECT instrucciones FROM recetas WHERE nombre = ?", (nombre,)).fetchone()
    ingredientes = cursor.execute("SELECT ingrediente FROM ingredientes WHERE receta_id = (SELECT ID FROM recetas WHERE nombre = ?)", (nombre,)).fetchall()
    if receta:
        return receta[0], [ingrediente[0] for ingrediente in ingredientes]
    return None

def principal():
    crear_tabla()
    menu = """
 === Bienvenido al libro de recetas ===
 a) Agregar nueva receta
 b) Editar receta existente
 c) Eliminar receta existente 
 d) Ver listado de recetas
 e) Buscar receta 
 f) Salir 
 Elige: """

    while True:
        eleccion = input(menu)
        if eleccion == "a":
            nombre = input("Ingresa el nombre de la receta: ")
            posible_receta = buscar_receta(nombre)
            if posible_receta:
                print("La receta\t" + nombre + "\tya existe")
            else:
                instrucciones = input("Ingrese las instrucciones: ")
                ingredientes = input("Ingrese los ingredientes separados por comas: ").split(',')
                agregar_receta(nombre, instrucciones, [ing.strip() for ing in ingredientes])
                print("Receta agregada")
        elif eleccion == "b":
            nombre = input("Ingresar el nombre de la receta que deseas editar: ")
            nuevas_instrucciones = input("Ingresar nuevas instrucciones: ")
            nuevos_ingredientes = input("Ingresar nuevos ingredientes separados por comas: ").split(',')
            editar_receta(nombre, nuevas_instrucciones, [ing.strip() for ing in nuevos_ingredientes])
            print("Receta actualizada")
        elif eleccion == "c":
            nombre = input("Ingresar el nombre de la receta que desea eliminar: ")
            eliminar_receta(nombre)
            print("La receta\t" + nombre + "\tha sido eliminada")
        elif eleccion == "d":
            recetas = obtener_recetas()
            print("=== Listado de recetas ===")
            for receta in recetas:
                print(receta[0])
        elif eleccion == "e":
            nombre = input("Introduzca el nombre de la receta que desea buscar: ")
            resultado = buscar_receta(nombre)
            if resultado:
                instrucciones, ingredientes = resultado
                print(f"Receta: {nombre}\nInstrucciones: {instrucciones}\nIngredientes: {', '.join(ingredientes)}")
            else:
                print(f"Receta\t" + nombre + "\tno encontrada")
        elif eleccion == "f":
            print("Saliste del libro de recetas")
            break
        else:
            print("Elección inválida")

    con.close()

if __name__ == "__main__":
    principal()
