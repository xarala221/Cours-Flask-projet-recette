from app import app, db
from app.models import Category, Recipe


def init_db():
    with app.app_context():
        # Création des tables
        db.create_all()

        # Vérification si les catégories existent déjà
        if Category.query.count() == 0:
            # Création des catégories de base
            categories = ["Entrées", "Plats principaux", "Desserts", "Boissons"]

            for cat_name in categories:
                cat = Category(name=cat_name)
                db.session.add(cat)

            # Ajout d'une recette de test
            # dessert_cat = Category(name="Desserts")
            # db.session.add(dessert_cat)
            # db.session.commit()

            test_recipe = Recipe(
                title="Gâteau au chocolat",
                description="Un délicieux gâteau au chocolat facile à faire",
                prep_time=45,
                ingredients="""200g de chocolat noir
200g de beurre
200g de sucre
4 œufs
100g de farine""",
                instructions="""1. Préchauffer le four à 180°C
2. Faire fondre le chocolat et le beurre
3. Mélanger les autres ingrédients
4. Cuire 25 minutes""",
                category=dessert_cat,
            )
            db.session.add(test_recipe)
            db.session.commit()

            print("Base de données initialisée avec succès!")
        else:
            print("Les catégories existent déjà!")


if __name__ == "__main__":
    init_db()
