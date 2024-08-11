from flask import Flask, render_template, request, redirect, url_for
import redis

app = Flask(__name__)

# Configuración de Redis
REDIS_HOST = 'your_host'
REDIS_PORT = 6379
REDIS_DB = 0

def connect_to_db():
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        return r
    except Exception as e:
        print(f"Error: {e}")
        return None

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

@app.route('/')
def index():
    recetas = obtener_recetas()
    return render_template('index.html', recetas=recetas)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        instrucciones = request.form['instrucciones']
        ingredientes = request.form['ingredientes'].split(',')
        agregar_receta(nombre, instrucciones, [ing.strip() for ing in ingredientes])
        return redirect(url_for('index'))
    return render_template('add_recipe.html')

@app.route('/editar/<nombre>', methods=['GET', 'POST'])
def editar(nombre):
    receta = buscar_receta(nombre)
    if not receta:
        return redirect(url_for('index'))
    if request.method == 'POST':
        nuevas_instrucciones = request.form['instrucciones']
        nuevos_ingredientes = request.form['ingredientes'].split(',')
        editar_receta(nombre, nuevas_instrucciones, [ing.strip() for ing in nuevos_ingredientes])
        return redirect(url_for('index'))
    instrucciones, ingredientes = receta
    return render_template('edit_recipe.html', nombre=nombre, instrucciones=instrucciones, ingredientes=', '.join(ingredientes))

@app.route('/eliminar/<nombre>', methods=['POST'])
def eliminar(nombre):
    eliminar_receta(nombre)
    return redirect(url_for('index'))

@app.route('/ver/<nombre>')
def ver(nombre):
    receta = buscar_receta(nombre)
    if not receta:
        return redirect(url_for('index'))
    instrucciones, ingredientes = receta
    return render_template('view_recipe.html', nombre=nombre, instrucciones=instrucciones, ingredientes=ingredientes)

if __name__ == "__main__":
    app.run(debug=True)


