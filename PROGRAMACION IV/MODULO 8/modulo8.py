from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from celery import Celery

app = Flask(__name__)

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.your-email-provider.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@example.com'

mail = Mail(app)

# Configuración de Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Simulación de la base de datos en memoria
recipes = {}

@app.route('/')
def index():
    return render_template('index.html', recipes=recipes)

@app.route('/recipe/<int:id>')
def view_recipe(id):
    recipe = recipes.get(id)
    if not recipe:
        return "Recipe not found!", 404
    return render_template('recipe.html', recipe=recipe)

@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        id = len(recipes) + 1
        name = request.form['name']
        ingredients = request.form['ingredients'].split(',')
        instructions = request.form['instructions']
        recipes[id] = {'name': name, 'ingredients': ingredients, 'instructions': instructions}

        # Enviar correo electrónico de confirmación de manera asíncrona
        send_email_task.delay(name, request.form['email'])
        
        return redirect(url_for('index'))
    return render_template('add_recipe.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_recipe(id):
    recipe = recipes.get(id)
    if not recipe:
        return "Recipe not found!", 404

    if request.method == 'POST':
        recipe['name'] = request.form['name']
        recipe['ingredients'] = request.form['ingredients'].split(',')
        recipe['instructions'] = request.form['instructions']
        return redirect(url_for('view_recipe', id=id))
    
    return render_template('update_recipe.html', recipe=recipe)

@app.route('/delete/<int:id>')
def delete_recipe(id):
    if id in recipes:
        del recipes[id]
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query'].lower()
        results = {id: r for id, r in recipes.items() if query in ','.join(r['ingredients']).lower()}
        return render_template('search.html', results=results, query=query)
    return render_template('search.html')

@celery.task
def send_email_task(recipe_name, recipient_email):
    msg = Message(f"Recipe {recipe_name} Added", recipients=[recipient_email])
    msg.body = f"The recipe '{recipe_name}' has been successfully added to your recipe book."
    mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)





