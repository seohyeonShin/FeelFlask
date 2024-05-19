import numpy as np

class CocktailEmbeddingMaker:
    def __init__(self, json_data, flavor_data):
        self.cocktail_info = json_data['cocktail_info']
        self.flavor_data = flavor_data
        self.init()

    def normalize_string(self, name):
        return name.replace('\\"', '"').replace("\\'", "'")

    def init(self):
        ingredient_ids = {}
        for idx, item in enumerate(self.flavor_data):
            item['ID'] = idx
            normalized_name = self.normalize_string(item['name'])
            ingredient_ids[normalized_name] = idx

        self.ingredient_ids = ingredient_ids
        self.num_ingredients = len(self.flavor_data)
        self.embedding_dim = 64
    def create_ingredient_embedding_matrix(self):
        ingredient_embedding_matrix = np.zeros((self.num_ingredients, len(self.flavor_data[0]) - 1))
        
        for ingredient_dict in self.flavor_data:
            ingredient_name = ingredient_dict['name']
            if ingredient_name in self.ingredient_ids:
                ingredient_id = self.ingredient_ids[ingredient_name]
                ingredient_embedding = [ingredient_dict[flavor] for flavor in ingredient_dict if flavor != 'name']
                ingredient_embedding_matrix[ingredient_id] = ingredient_embedding
        
        return ingredient_embedding_matrix

    def create_recipe_embedding_2(self, recipe):
        ingredient_embedding_matrix = self.create_ingredient_embedding_matrix()
        
        total_amount = sum(recipe.values())
        normalized_amount = {ingredient: amount / total_amount for ingredient, amount in recipe.items()}
        
        weighted_embeddings = []
        for ingredient, amount in normalized_amount.items():
            normalized_ingredient = self.normalize_string(ingredient)
            if normalized_ingredient not in self.ingredient_ids:
                raise KeyError(f"Ingredient '{normalized_ingredient}' not found in ingredient_ids")
            ingredient_id = self.ingredient_ids[normalized_ingredient]
            ingredient_embedding = ingredient_embedding_matrix[ingredient_id]
            weighted_embedding = ingredient_embedding * amount
            weighted_embeddings.append(weighted_embedding)
        
        recipe_embedding = np.sum(weighted_embeddings, axis=0)
        return recipe_embedding
    
    def create_recipe_embedding_1(self, recipe):
        embedding_matrix = np.random.rand(self.num_ingredients, self.embedding_dim)
        total_amount = sum(recipe.values())
        normalized_amount = {ingredient: amount / total_amount for ingredient, amount in recipe.items()}
        weighted_embeddings = []
        for ingredient, amount in normalized_amount.items():
            normalized_ingredient = self.normalize_string(ingredient)
            if normalized_ingredient not in self.ingredient_ids:
                raise KeyError(f"Ingredient '{normalized_ingredient}' not found in ingredient_ids")
            ingredient_id = self.ingredient_ids[normalized_ingredient]
            ingredient_embedding = embedding_matrix[ingredient_id]
            weighted_embedding = ingredient_embedding * amount
            weighted_embeddings.append(weighted_embedding)
        recipe_embedding = np.sum(weighted_embeddings, axis=0)
        return recipe_embedding

    def create_recipe_embedding_list(self):
        recipe_embeddings = dict()
        for cocktail in self.cocktail_info:
            name = cocktail['cocktail_name']
            recipe = cocktail['recipe']
            recipe_embedding = self.create_recipe_embedding_2(recipe)
            recipe_embeddings[name] = {'recipe_embedding': recipe_embedding}
        return recipe_embeddings
    
    def calculate_recipe_taste_weights(self, recipe):
        recipe_ingredients = [d for d in self.flavor_data if d['name'] in list(recipe.keys())]
        total_amount = sum(recipe.values())
        ingredient_ratios = {ingredient: amount / total_amount for ingredient, amount in recipe.items()}
        recipe_taste_weights = {}
        for ingredient, ratio in ingredient_ratios.items():
            ingredient_dict = next((d for d in recipe_ingredients if d['name'] == ingredient), None)
            if ingredient_dict:
                for taste, weight in ingredient_dict.items():
                    if taste != 'name':
                        recipe_taste_weights[taste] = recipe_taste_weights.get(taste, 0) + weight * ratio
        return recipe_taste_weights

    def create_taste_embedding_list(self):
        taste_embeddings = dict()
        for cocktail in self.cocktail_info:
            name = cocktail['cocktail_name']
            recipe = cocktail['recipe']
            recipe_taste_weights = self.calculate_recipe_taste_weights(recipe)
            taste_embeddings[name] = {'taste_embedding': np.array(list(recipe_taste_weights.values()))}
        return taste_embeddings

    def create_combined_embedding_list(self):
        recipe_embeddings = self.create_recipe_embedding_list()
        taste_embeddings = self.create_taste_embedding_list()

        combined_embeddings = {}
        for name in recipe_embeddings.keys():
            combined_embeddings[name] = {
                'recipe_embedding': recipe_embeddings[name]['recipe_embedding'],
                'taste_embedding': taste_embeddings[name]['taste_embedding']
            }

        return combined_embeddings