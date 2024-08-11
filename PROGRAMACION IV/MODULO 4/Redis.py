import redis
import json

#para establecer conexion
REDIS_HOST = 'your_host'  # e.g., 'localhost'
REDIS_PORT = 6379  # Default Redis port
REDIS_DB = 0  # Default Redis DB index


def connect_to_db():
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        return r
    except Exception as e:
        print(f"Error: {e}")
        return None


def crear_tabla():
    db = connect_to_db()
    if db is None:
        return


def agregar_receta(nombre, instrucciones, ingredientes):
    db = connect_to_db()
    if db is None:
        return
    receta_key = f"receta:{nombre}"
    ingredientes_key = f"receta:{nombre}:ingredientes"

    db.hset(receta_key, "instrucciones", instrucciones)
    db.delete(ingredientes_key)
    for ingrediente in ingredientes:
        db.rpush(ingredientes_key, ingrediente)


def editar_receta(nombre, nuevas_instrucciones, nuevos_ingredientes):
    db = connect_to_db()
    if db is None:
        return
    receta_key = f"receta:{nombre}"
    ingredientes_key = f"receta:{nombre}:ingredientes"

    db.hset(receta_key, "instrucciones", nuevas_instrucciones)
    db.delete(ingredientes_key)
    for ingrediente in nuevos_ingredientes:
        db.rpush(ingredientes_key, ingrediente)


def eliminar_receta(nombre):
    db = connect_to_db()
    if db is None:
        return
    receta_key = f"receta:{nombre}"
    ingredientes_key = f"receta:{nombre}:ingredientes"

    db.delete(receta_key)
    db.delete(ingredientes_key)


def obtener_recetas():
    db = connect_to_db()
    if db is None:
        return []
    keys = db.keys("receta:*:ingredientes")
    return [key.decode().split(":")[1] for key in keys]


def buscar_receta(nombre):
    db = connect_to_db()
    if db is None:
        return None
    receta_key = f"receta:{nombre}"
    ingredientes_key = f"receta:{nombre}:ingredientes"

    instrucciones = db.hget(receta_key, "instrucciones")
    if instrucciones:
        ingredientes = db.lrange(ingredientes_key, 0, -1)
        return instrucciones.decode(), [ing.decode() for ing in ingredientes]
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
                print(receta)
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

