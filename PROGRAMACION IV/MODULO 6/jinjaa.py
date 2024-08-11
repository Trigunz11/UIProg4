from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)




