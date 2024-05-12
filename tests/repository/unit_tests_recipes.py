from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

import src.repository.recipes as recipe_repository
from src.database.models import Recipe

class RecipesUnitTest(IsolatedAsyncioTestCase):

    def setUp(self):
        self.db = MagicMock(spec=Session)
        # self.user = User(id=1, name)
        #self.user = Magic(spec=User)

    async def test_get_recipes(self):
        # when
        recipes = [Recipe(), Recipe(), Recipe()]
        self.db.query().filter().offset().limit().all.return_value = recipes

        # call
        result = await recipe_repository.get_recipes(0, 10, 1, self.db)

        # assert
        self.assertEqual(3, len(result))
        self.assertEqual(recipes, result)

    async def test_create_recipes(self):
        # when
        body = Recipe(id=1, title='Test recipe')

        # call
        result = await recipe_repository.create_recipe(body, self.db)

        # assert
        self.assertEqual(body, result)

    async def test_remove_recipes(self):
        # when
        recipe = Recipe(id=1, title='Test recipe')
        self.db.query().filter().first.return_value = recipe

        # call
        result = await recipe_repository.remove_recipe(2, self.db)

        # assert
        self.assertEqual(recipe, result)
        self.assertEqual(1, result.id)
    
if __name__ == '__main__':
    main()
