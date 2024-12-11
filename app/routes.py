from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Recipe, Category


@app.route("/")
def index():
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    categories = Category.query.all()
    return render_template("index.html", recipes=recipes, categories=categories)


@app.route("/category/<int:category_id>")
def category(category_id):
    category = Category.query.get_or_404(category_id)
    recipes = category.recipes
    categories = Category.query.all()
    return render_template(
        "index.html", recipes=recipes, categories=categories, current_category=category
    )


@app.route("/recipe/new", methods=["GET", "POST"])
def new_recipe():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        prep_time = request.form["prep_time"]
        ingredients = request.form["ingredients"]
        instructions = request.form["instructions"]
        category_id = request.form["category_id"]

        recipe = Recipe(
            title=title,
            description=description,
            prep_time=prep_time,
            ingredients=ingredients,
            instructions=instructions,
            category_id=int(category_id),
        )

        try:
            db.session.add(recipe)
            db.session.commit()
            flash("Recette ajoutée avec succès!", "success")
            return redirect(url_for("index"))
        except:
            db.session.rollback()
            flash("Erreur lors de l'ajout de la recette", "error")

    categories = Category.query.all()
    return render_template("new_recipe.html", categories=categories)


@app.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template("recipe_detail.html", recipe=recipe)


@app.route("/recipe/<int:recipe_id>/edit", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    categories = Category.query.all()
    if request.method == "POST":
        recipe.title = request.form["title"]
        recipe.description = request.form["description"]
        recipe.prep_time = request.form["prep_time"]
        recipe.ingredients = request.form["ingredients"]
        recipe.instructions = request.form["instructions"]
        recipe.category_id = request.form["category_id"]

        try:
            db.session.commit()
            flash("Recette modifiée avec succès!", "success")
            return redirect(url_for("recipe_detail", recipe_id=recipe.id))
        except:
            db.session.rollback()
            flash("Erreur lors de la modification de la recette", "error")
    return render_template("edit_recipe.html", recipe=recipe, categories=categories)


@app.route("/recipe/<int:recipe_id>/delete", methods=["POST"])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    try:
        db.session.delete(recipe)
        db.session.commit()
        flash("Recette supprimée avec succès!", "success")
        return redirect(url_for("index"))
    except:
        db.session.rollback()
        flash("Erreur lors de la suppression de la recette", "error")
        return redirect(url_for("recipe_detail", recipe_id=recipe.id))
