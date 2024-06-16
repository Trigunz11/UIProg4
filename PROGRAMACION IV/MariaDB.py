import mysql.connector
from mysql.connector import Error

# ejemplo de como seria conectar la bd, necesitariamos asignar los puertos, el host, user y password.
# DB_HOST = 'localhost'
# DB_USER = 'your_username'
# DB_PASSWORD = 'your_password'
# DB_NAME = 'recipes_db'


# def connect_to_db():
    # try:
        # con = mysql.connector.connect(
            # host=DB_HOST,
            # user=DB_USER,
            # password=DB_PASSWORD,
            # database=DB_NAME
        # )
        # return con
    # except Error as e:
        # print(f"Error: {e}")
        # return None


def crear_tabla():
    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recetas(
        ID            INT AUTO_INCREMENT PRIMARY KEY,
        NOMBRE        VARCHAR(255) NOT NULL,
        INSTRUCCIONES TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredientes(
        ID            INT AUTO_INCREMENT PRIMARY KEY,
        RECETA_ID     INT NOT NULL,
        INGREDIENTE   VARCHAR(255) NOT NULL,
        FOREIGN KEY (RECETA_ID) REFERENCES recetas(ID)
        )
    """)
    con.close()


def agregar_receta(nombre, instrucciones, ingredientes):
    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute("INSERT INTO recetas (nombre, instrucciones) VALUES (%s, %s)", (nombre, instrucciones))
    receta_id = cursor.lastrowid
    for ingrediente in ingredientes:
        cursor.execute("INSERT INTO ingredientes (receta_id, ingrediente) VALUES (%s, %s)", (receta_id, ingrediente))
    con.commit()
    con.close()

def editar_receta(nombre, nuevas_instrucciones, nuevos_ingredientes):
    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute("UPDATE recetas SET instrucciones = %s WHERE nombre = %s", (nuevas_instrucciones, nombre))
    cursor.execute("SELECT ID FROM recetas WHERE nombre = %s", (nombre,))
    receta_id = cursor.fetchone()[0]
    cursor.execute("DELETE FROM ingredientes WHERE receta_id = %s", (receta_id,))
    for ingrediente in nuevos_ingredientes:
        cursor.execute("INSERT INTO ingredientes (receta_id, ingrediente) VALUES (%s, %s)", (receta_id, ingrediente))
    con.commit()
    con.close()


def eliminar_receta(nombre):
    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute("SELECT ID FROM recetas WHERE nombre = %s", (nombre,))
    receta_id = cursor.fetchone()[0]
    cursor.execute("DELETE FROM recetas WHERE nombre = %s", (nombre,))
    cursor.execute("DELETE FROM ingredientes WHERE receta_id = %s", (receta_id,))
    con.commit()
    con.close()


def obtener_recetas():
    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute("SELECT nombre FROM recetas")
    recetas = cursor.fetchall()
    con.close()
    return recetas


def buscar_receta(nombre):
    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute("SELECT instrucciones FROM recetas WHERE nombre = %s", (nombre,))
    receta = cursor.fetchone()
    cursor.execute("SELECT ingrediente FROM ingredientes WHERE receta_id = (SELECT ID FROM recetas WHERE nombre = %s)", (nombre,))
    ingredientes = cursor.fetchall()
    con.close()
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

if __name__ == "__main__":
    principal()
