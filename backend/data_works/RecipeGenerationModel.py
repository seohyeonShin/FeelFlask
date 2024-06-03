
import numpy as np
import tensorflow as tf
import json
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from CocktailEmbeddingMaker import CocktailEmbeddingMaker
from CocktailEmbeddingMaker import Eval
import wandb
class RecipeGenerationModel:
    #RecipeGenerationModel(cocktail_embedding_maker, wandb_flag=True, max_recipe_length=10)
    def __init__(self, cocktail_embedding_maker,eval_obj,json_data,flavor_data,category_data,wandb_Flag=False, max_recipe_length=10):
        self.cocktail_embedding_maker = cocktail_embedding_maker
        self.ingredient_ids = cocktail_embedding_maker.ingredient_ids
        self.num_ingredients = cocktail_embedding_maker.num_ingredients
        self.max_recipe_length = max_recipe_length
        self.ingredient_embedding_matrix = cocktail_embedding_maker.create_ingredient_embedding_matrix()
        self.sweep_config = None
        self.evaluation_metrics=None
        self.sweep_id = None
        self.wandb = wandb_Flag
        
        self.total_amount = 200
        self.Eval = eval_obj
        self.attributes = ['ABV', 'boozy', 'sweet', 'sour', 'bitter', 'umami', 'salty', 'astringent', 'Perceived_temperature', 'spicy', 'herbal', 'floral', 'fruity', 'nutty', 'creamy', 'smoky']
        self.evaluation_metrics = ['diversity', 'abv_match', 'taste_match']
        # Best 모델 판정 및 저장
    def save_best_model(self, performance, abv_match, taste_match, threshold_performance, threshold_abv_match, threshold_taste_match,run_id):

        if performance >= threshold_performance and abv_match >= threshold_abv_match and taste_match >= threshold_taste_match:
            self.model.model.save(f'best_model_{run_id}.h5')
            print("Best model saved.")
        else:
            print("Model does not meet the threshold criteria.")

    def build_model(self):
        hidden_units = 128
        optimizer = 'adam'
        if self.wandb:
            hidden_units = wandb.config.get('hidden_units', 128)
            optimizer =  wandb.config.get('optimizer', 'adam')
        
        model = Sequential([
            Embedding(self.num_ingredients, self.ingredient_embedding_matrix.shape[1],
                      weights=[self.ingredient_embedding_matrix], input_length=self.max_recipe_length, trainable=False),
            LSTM(hidden_units, return_sequences=True),
            LSTM(hidden_units),
            Dense(64, activation='gelu'),
            Dense(self.num_ingredients, activation='softmax')
        ])
        
        model.compile(loss='categorical_crossentropy', optimizer=optimizer,metrics=['accuracy'])
        return model

    def train(self, recipes,test_user_list, epochs=50, batch_size=32,learning_rate=0.001):
        ingredient_sequences = []
        next_ingredients = []

        for recipe in recipes:
            sequence = [self.ingredient_ids[self.cocktail_embedding_maker.normalize_string(ingredient)] for ingredient in recipe]
            for i in range(1, len(sequence)):
                ingredient_sequences.append(sequence[:i])
                next_ingredients.append(sequence[i])

        ingredient_sequences = tf.keras.preprocessing.sequence.pad_sequences(ingredient_sequences, maxlen=self.max_recipe_length)
        next_ingredients = tf.keras.utils.to_categorical(next_ingredients, num_classes=self.num_ingredients)
        evaluation_interval = 5
        if self.wandb:
            # wandb 초기화
            wandb.init(project='cocktail_recipe_generation_v2')
            epochs = wandb.config.get('epochs', 50)
            batch_size = wandb.config.get('batch_size', 32)
            learning_rate = wandb.config.get('lr', 0.001)
            optimizer = wandb.config.get('optimizer', 'adam')
            
        self.model = self.build_model()
        for epoch in range(epochs):
            history = self.model.fit(ingredient_sequences, next_ingredients, epochs=1, batch_size=batch_size, verbose=0)
            loss = history.history['loss'][0]
            accuracy = history.history['accuracy'][0]
            if self.wandb:
                # wandb 로깅
                wandb.log({
                    'epoch': epochs,
                    'loss': loss,
                    'accuracy': accuracy,
                })
        # eval을 호출 해서 평가를 수행하고 결과를 evaluation_result에 저장한다. 
        # 저장후 evaluation_metrics에 지정된 평가 지표 합을 계산해서 performance변수에 저장한다. 
        #wandb에 performance와 개별 평가 지표결과를 로깅한다. 
            # 모델 평가
        # print("evaluating model")

        evaluation_results,recipe_profile_list = self.Eval.evaluate_model(self.model, test_user_list)
        if self.wandb:
            for recipe_profile in recipe_profile_list:
                for key in self.attributes:
                    wandb.log({key: recipe_profile[key]})
            
       
        # 평가 지표 계산
        performance = sum(evaluation_results[metric] for metric in self.evaluation_metrics)
                # Best 모델 판정 및 저장
        threshold_performance = 2.07
        threshold_abv_match = 0.656
        threshold_taste_match = 0.616
        # save_best_model(self, performance, abv_match, taste_match, threshold_performance, threshold_abv_match, threshold_taste_match,run_id):
        if self.wandb:
            save_id = wandb.run.id
        else:
            save_id = 'test'
        self.save_best_model(
                            performance, 
                            evaluation_results['abv_match'], 
                            evaluation_results['taste_match'], 
                            threshold_performance, 
                            threshold_abv_match, 
                            threshold_taste_match,save_id) 

        if self.wandb:
            # 평가 지표 로깅
            wandb.log({
                'performance': performance, **evaluation_results})
            wandb.finish()
        return loss, accuracy, performance


if __name__ == '__main__':
    import sys 
    import os 
    # os.chdir('G:\내 드라이브\DOC\Lecture\DataEng\FeelFlask\backend\data_works')
    # sys.path.append('G:\내 드라이브\DOC\Lecture\DataEng\FeelFlask\backend\data_works')
    # sys.path.append('G:\내 드라이브\DOC\Lecture\DataEng\FeelFlask\backend')
    with open('./train_data.json', 'r') as f:
        json_data = json.load(f)
    with open('../flavor.json', 'r') as f:
        flavor_data = json.load(f)
    with open('../category.json', 'r', encoding='utf-8') as f:
        category_data = json.load(f)
    cocktail_embedding_maker = CocktailEmbeddingMaker(json_data, flavor_data,category_data)
    eval_obj = Eval(json_data,flavor_data,category_data)
    # RecipeGenerationModel 인스턴스 생성
    recipe_generation_model = RecipeGenerationModel(cocktail_embedding_maker,eval_obj,json_data,flavor_data,category_data
                                                    , False, max_recipe_length=10)
    test_user_list = eval_obj.generate_random_user_list(5)
    # 학습 데이터 준비
    train_recipes = [recipe['recipe'].keys() for recipe in json_data['cocktail_info']]

    # 모델 학습
    loss, accuracy, performance = recipe_generation_model.train(train_recipes,test_user_list)
    recipe_generation_model.model.save(f'testmodel_2024_0603.h5')