from pymongo import MongoClient
from bson.objectid import ObjectId

# para configurar y establecer conexion 
DB_HOST = 'your_host'  # e.g., 'localhost'
DB_PORT = 27017  # Default MongoDB port
DB_NAME = 'recipes_db'


def connect_to_db():
    try:
        client = MongoClient(DB_HOST, DB_PORT)
        db = client[DB_NAME]
        return db
    except Exception as e:
        print(f"Error: {e}")
        return None


def crear_tabla():
    db = connect_to_db()
    if db is None:
        return
   
    db.recetas.create_index("nombre", unique=True)
    db.ingredientes.create_index("receta_id")


def agregar_receta(nombre, instrucciones, ingredientes):
    db = connect_to_db()
    if db is None:
        return
    recetas_collection = db.recetas
    ingredientes_collection = db.ingredientes

    receta_id = recetas_collection.insert_one({
        "nombre": nombre,
        "instrucciones": instrucciones
    }).inserted_id

    for ingrediente in ingredientes:
        ingredientes_collection.insert_one({
            "receta_id": receta_id,
            "ingrediente": ingrediente
        })


def editar_receta(nombre, nuevas_instrucciones, nuevos_ingredientes):
    db = connect_to_db()
    if db is None:
        return
    recetas_collection = db.recetas
    ingredientes_collection = db.ingredientes

    receta = recetas_collection.find_one_and_update(
        {"nombre": nombre},
        {"$set": {"instrucciones": nuevas_instrucciones}},
        return_document=True
    )
    if receta:
        receta_id = receta["_id"]
        ingredientes_collection.delete_many({"receta_id": receta_id})
        for ingrediente in nuevos_ingredientes:
            ingredientes_collection.insert_one({
                "receta_id": receta_id,
                "ingrediente": ingrediente
            })


def eliminar_receta(nombre):
    db = connect_to_db()
    if db is None:
        return
    recetas_collection = db.recetas
    ingredientes_collection = db.ingredientes

    receta = recetas_collection.find_one_and_delete({"nombre": nombre})
    if receta:
        receta_id = receta["_id"]
        ingredientes_collection.delete_many({"receta_id": receta_id})


def obtener_recetas():
    db = connect_to_db()
    if db is None:
        return []
    recetas_collection = db.recetas
    return list(recetas_collection.find({}, {"nombre": 1, "_id": 0}))


def buscar_receta(nombre):
    db = connect_to_db()
    if db is None:
        return None
    recetas_collection = db.recetas
    ingredientes_collection = db.ingredientes

    receta = recetas_collection.find_one({"nombre": nombre}, {"instrucciones": 1, "_id": 1})
    if receta:
        receta_id = receta["_id"]
        ingredientes = list(ingredientes_collection.find({"receta_id": receta_id}, {"ingrediente": 1, "_id": 0}))
        return receta["instrucciones"], [ing["ingrediente"] for ing in ingredientes]
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
                print(receta["nombre"])
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
