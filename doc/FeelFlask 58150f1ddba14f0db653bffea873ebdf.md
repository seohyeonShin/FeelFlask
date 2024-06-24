# FeelFlask

<aside>
<img src="https://www.notion.so/icons/clover-four-leaf_green.svg" alt="https://www.notion.so/icons/clover-four-leaf_green.svg" width="40px" /> Team 7 
Seohyeon Shin 20242013
[Seongyun Woo](https://github.com/Woosyun)
Seung-yu Yang 20244024
Jaebeom Jo 20231172

</aside>

[GitHub - seohyeonShin/FeelFlask](https://github.com/seohyeonShin/FeelFlask)

Streamlit Git Repo

[GitHub - seohyeonShin/FeelFlask_heroku](https://github.com/seohyeonShin/FeelFlask_heroku)

HeroKu Git Repo

[**Our Web Page’s Preview** ](https://feelflask-7gm6rk6tf925umyyt8rkg5.streamlit.app/?embed=true)

**Our Web Page’s Preview** 

<aside>
🍸 [FeelFlask](https://feelflask-7gm6rk6tf925umyyt8rkg5.streamlit.app/)↗️

</aside>

Due to server maintenance costs, the site will be open for one month in `June 2024`. It will be announced after moving to a free server later!

### DemoVideo

[demo_feelFlask.mp4](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/demo_feelFlask.mp4)

# Problem definition

---

The world of cocktails is a creative space with a wide variety of flavor and fragrance combinations, Many people who are not familiar with cocktails often find it challenging to discover the flavors they desire. The vast array of possible ingredient choices can be overwhelming for those who want to make and enjoy cocktails casually. To solve this problem, our app allows users to input their flavor preferences and select the primary ingredients they want to use.

We propose the development of a personalized cocktail recipe recommendation app that addresses the needs of novice cocktail enthusiasts. Our app will collect user input regarding flavor preferences and selected ingredients to generate tailored cocktail recipes. The recommended recipes will provide clear guidance on the ingredients used and their respective quantities, ensuring that users can easily recreate the cocktails at home.
Internally, our proposed system employs embedding techniques to consider the characteristics of each ingredient, such as taste, aroma, and alcohol content. We construct an embedding matrix to generate recipes while considering the similarity between ingredients. Since cocktail recipes can be viewed as sequential combinations, we have selected LSTM (Long Short-Term Memory) as our model architecture, which is trained to predict the next ingredient based on the given list of ingredients. This approach enables the creation of novel combinations while preventing the pairing of incompatible ingredients.
The model's performance is evaluated comprehensively, assessing the quality of the generated recipes from multiple angles. We have incorporated evaluation metrics that directly impact user satisfaction.

# System design

---

![Untitled](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/Untitled.png)

### About OverView

The main system components consist of a post-processing recommendation module composed of `LSTM` and rule-based systems, `FastAPI` for HTTP method calls, `Streamlit` for UI design and implementation, and a user feedback database that collects and stores user input values, output values, and feedback in JSON file format. and also, Fastapi was deployed using `heroku`. 

### Data

We have prepared training cocktail recipe data (train_data.json), preprocessed ingredient characteristics data (flavor.json), and ingredient category data (category.json) as our dataset. Since the ingredients used in cocktails are mostly categorized and rarely change, we did not implement a real-time data pipeline based on our project objectives.

### Machine Learning

The LSTM model and rule-based system serve as the recommendation engine. The LSTM model consists of basic embedding, LSTM, and dense layers. The model is trained to predict the next ingredient based on the input ingredient list. During training, categorical cross-entropy is used as the loss function, and SGD is used as the optimizer. Hyperparameters such as learning rate, optimizer, data augmentation, epochs, and batch size are optimized using `Wandb Sweep`.

The rule-based system adjusts the recommendation results by considering user preferences and ingredient characteristics. For example, it first calls `select_user_seed` to select a seed ingredient based on user preferences, and then calls `adjust_ingredient_quantities` to adjust the ingredient quantities considering the user's preferred ABV and preferences.

The system provides the recommendation module as a service using FastAPI. FastAPI is implemented in fastapi_srv.py and provides user preference configuration and recipe generation functionalities through the `/filter` and `/predict` endpoints.

### UI&UX and Server

`Streamlit` is used to provide the user interface. The main logic of the Streamlit application is implemented in app.py. Users determine their flavor preferences using familiar ingredient images instead of text. They can adjust their desired flavor profile by clicking checkboxes below each ingredient image. This information is stored in the `session_state`. The selected flavor profile is passed to FastAPI through the `/filter` endpoint, and a list of filtered seed ingredient candidates is returned. The returned candidates are presented to the user as tile buttons. When the user selects a seed ingredient, the `/predict` endpoint is used to retrieve the recommended recipe and display it on the screen. To enhance the user experience, random cocktail animations are added to provide a lively and vibrant feel. Additionally, users are asked to provide feedback on the results by inputting a star rating. The collected input, along with the user's preference profile, recommendation results, and star rating (user feedback), are stored in a JSON file.

# Machine learning component

---

<aside>
🍸 Our ML module consist of 2 main components

</aside>

### Cocktail Ingredient Combination Generator

The core of this project is a generator based on the LSTM (Long Short-Term Memory) model that aims to propose creative and plausible cocktail recipes considering user preferences.

we chose LSTM because it is a sequential combination and can be implemented simply.
Above all, the method of predicting the next ingredient based on a given ingredient list is suitable for our recipe generation purpose.This allows us to create new combinations that do not exist before.

We've adopted embedding techniques to effectively communicate each ingredient's characteristics to the model, using scores for `16 flavor attributes` defined in the "flavor.json" file for 302 ingredients. The embedding matrix generated assigns an ID to each ingredient and stores extracted flavor attributes, optimizing it during the model's learning process to understand patterns in ingredient combinations better.
For model training, we preprocessed the cocktail recipe data into ingredient sequences, replacing each ingredient with its corresponding index and applying padding to fix the sequence length. This preprocessed data is transformed into embedding vectors through the embedding layer.
We used the `Teacher Forcing` technique during training, where the model learns to predict the next ingredient based on the input sequence. For instance, predicting "sugar syrup" following "gin" and "lemon juice." Input and target sequences were generated from the recipe sequences for this purpose.

We chose `categorical_crossentropy` as our loss function, suitable for our task that requires considering various ingredients, though it may be less effective for non-primary ingredients. Additionally, user preferences were integrated by utilizing ABV (Alcohol By Volume) and flavor attribute scores, weighting the ingredient probability distribution during prediction to enhance the likelihood of selecting user-preferred ingredients.

### Rule based Quantity Adjuster

The generator provides the combination and order of ingredients but not the exact quantities. To overcome this limitation and offer complete recipes, we developed a rule-based post-processor that adjusts the quantity of each ingredient based on predefined rules.
This adjustment process involves:
1. Initialization: Setting equal amounts for all ingredients.
2. ABV adjustment: Modifying the quantity of high and low alcohol content ingredients based on the difference between the recipe’s total ABV and the user's preferred ABV.
3. Flavor attribute adjustment: Further modifying ingredient quantities considering user-preferred flavor attributes.
4. Iterative optimization: Repeating the above steps to find the optimal ingredient amounts.
This rule-based approach ensures the overall balance of the cocktail recipe while reflecting user preferences, allowing users to receive a recipe adjusted to their taste preferences.

 The combination of the Cocktail Ingredient Combination Generator and the Rule-Based Quantity Adjuster forms the core components of our user-customized cocktail recipe proposal system. The LSTM model and embedding layer-equipped generator create harmonious ingredient combinations, while the rule-based post-processor assigns appropriate quantities reflecting user preferences

# System Evaluation

Our objectives are:

1. Generating recipes that suit user preferences
2. Generating novel and plausible recipes that differ from existing ones

Therefore, evaluating the system using the same methods employed during model training makes it difficult to assess whether we have achieved our task goals. As a result, we train the model using the teaching forcing approach, measuring accuracy, but we define a separate metric called "Performance" to select the final model that satisfies this metric.

The Performance metric consists of "diversity," "ABV_match," and "taste_match," while "similarity" is measured for tracking and observation purposes.

Taste attributes: ['boozy', 'sweet', 'sour', 'bitter', 'umami', 'salty', 'astringent', 'Perceived_temperature', 'spicy', 'herbal', 'floral', 'fruity', 'nutty', 'creamy', 'smoky'].

**"similarity"**

- Measures the degree of similarity between the generated recipe and the existing recipe dataset
- Calculates the cosine similarity between the generated recipe and existing recipe vectors, then outputs the highest similarity score

**"diversity"**

- Measures the diversity among the generated recipes
- Calculates the frequency of ingredients included in the generated recipes and original recipes
- Computes the probability of each ingredient's occurrence and uses the sum of squared probabilities subtracted from 1 as the diversity score

**"ABV_match"**

- Calculates the ABV of the generated recipe and compares it with the preferred ABV, normalizing the difference to output a value between 0 and 1, with 1 indicating a better match
- If the user does not prefer alcohol, a generated recipe with an ABV of 0 is considered a perfect match

**"taste_match"**

- Evaluates whether the taste profile of the generated recipe matches the user's preferences
- Calculates the average of the taste attribute matching scores to produce the final output

![Untitled](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/Untitled%201.png)

![Untitled](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/Untitled%202.png)

![Untitled](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/Untitled%203.png)

![Untitled](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/Untitled%204.png)

![some,, flavor attributes](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/Untitled%205.png)

some,, flavor attributes

# Application Demonstration

![Untitled](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/Untitled%206.png)

Application link : 

<aside>
🍸 [FeelFlask](https://feelflask-7gm6rk6tf925umyyt8rkg5.streamlit.app/)↗️

</aside>

- Clicking the “Restart” button will return you to the first page.

> **How to use**
> 
1. Click “Start Your Journey” button to start the journey for cocktail recommendation.
2. Select drink type you want
    1. Alcoholic: On next page, ABV feature slide that can adjust the value from 0 to 60 is available
    2. Non-Alcoholic: ABV value is set to 0 and no means to modify the value will be provided.

![Start Page of the App](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/Untitled%207.png)

Start Page of the App

![Options for selecting Alcoholic or Non-Alcoholic Drink](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/Untitled%208.png)

Options for selecting Alcoholic or Non-Alcoholic Drink

1. Adjust flavor taste by checking ingredient icon.
    1. you can select several check-boxes below the icon and adjust your flavor profile.
        - after finishing your choice, click “Set My Taste” button on the below to submit your user profile.
    2. values of the profile features for current choice are shown on the plot.

![User Taste adjustment page for alcoholic drink](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/Untitled%209.png)

User Taste adjustment page for alcoholic drink

![User profile plot after checking honey, champagne, lavender](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/Untitled%2010.png)

User profile plot after checking honey, champagne, lavender

1. Select one ingredient out of 9 choices shown on the screen. 
    1. select tile shown on the screen. only one choice is retained.
        - click “Determine” button to submit your decision.
    2. plot of flavor information for selected ingredient is available at the bottom of screen.

![App Design after choosing benedictine for seed ingredient.](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/Untitled%2011.png)

App Design after choosing benedictine for seed ingredient.

![Plot of ingredient flavors after clicking “benedictine”](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/Untitled%2012.png)

Plot of ingredient flavors after clicking “benedictine”

![Loading Animation](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/Untitled%2013.png)

Loading Animation

1. Get recommendation result
    
    
    ![default recommendation result page](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/Untitled%2014.png)
    
    default recommendation result page
    
    ![Recommendation result Case-1](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/Untitled%2015.png)
    
    Recommendation result Case-1
    
    ![Recommendation result Case-2](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/Untitled%2016.png)
    
    Recommendation result Case-2
    
    - Details tab : you can see what ingredients and how much are recommended.
    - Feedback is available. Adjust number of stars for your opinion and click “Submit Feedback” button to submit your ratings.
    - Graphs tab : you can see two graphs showing the usage ratio of each material and recommended cocktail flavor info.
        
        ![Untitled](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/Untitled%2017.png)
        
    - Live Bar tab:  this tab is for demo purposes. you can ignore this tab.
        
        
        ![Untitled](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/Untitled%2018.png)
        
    - Click “Restart” button to return to first-page.
    
    # Reflections
    
    ![Untitled](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/Untitled%206.png)
    
    ## What worked
    
    ---
    
    1. The idea of easy usage worked well, and we can conclude that the balance between usability and accuracy was well achieved. Users of the application didn't have a hard time understanding its purpose or how to use it. The application performed well in terms of understanding user preferences and providing recommendations.
    2. 2024.06.18, Jenny visit the cocktail bar(bebop at 첨단) to test our application. The our app. generate recipe on his signature menu when he puts preference on our app. 🤭 however the unit of garnish isn’t correctly matched(bitter is 40ml 😥😥)
    
    ## Limitations
    
    ![Untitled](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/Untitled%206.png)
    
    1. Because the number of checkbox a user can select is limited, the possible taste combinations are limited. Also, because the adjustment values corresponding to each checkbox are fixed, the possible combinations that can be created are limited.
    2. Since the number of cocktail data was only 500, it can’t be guaranteed that ingredient compositions are well generalized. Due to the small number of data sets, the ingredient quantity prediction pipeline could not be designed with end-to-end deep learning manner. Ingredient quantity prediction could be done with DNN, but we didn’t use it because performance monitored on validation data are not good enough.
    3. The rule-based system used for predicting ingredients and amounts of usage could be more elaborate. As the rule-based recommendation module simply filters ingredients based on the distance between the ingredient’s flavor information and the user’s flavor information, the output ingredient selection tends to be monotonous. The algorithm needs to weight considering the entire combination, rather than simply giving more weight to the ingredient with the shortest distance.
    
    ## Future works in ideal condition
    
    ![Untitled](FeelFlask%2058150f1ddba14f0db653bffea873ebdf/Untitled%206.png)
    
    1. Collect more cocktail dataset.
        
        we will collect more cocktail dataset by crawling on the internet, searching existing cocktail recipe data. Larger datasets will enable end-to-end deep-learning prediction module integration, which leads to more accurate and generalized prediction.
        
    2. Collect user feedback and update cocktail recommendation.
        
        collecting user reactions and reasons for them is very important for a better system. we will modify feedback input system to accept natural language-based user reviews. Then we will deploy our app in the market and collect user’s feedback on the predicted cocktail recipe. As we store feedback information with predicted recipe and seed ingredient and natural-language based user review, we will create user feedback data and use it to update our ML model for better prediction.
        
    3. Update rule-base system or modify prediction pipeline
        
        we can modify rule-base system for more elaborate design. calculating the distance between user flavor and cocktail recipe flavor instead of ingredients can be considered. as more dataset will be used to train lstm, lstm will output more generalized result. just replacing several ingredient on recipe or output several recommendations based on flavor distance between cocktail and user flavor will be enough. also removing rule-based quantity-prediction and using deep-learning based prediction is possible.
        
    
    # Broader Impacts
    
    ---
    
    - Intended usages
        1. This application intended to be used to help home bartender to create cocktails at home, enhancing their bartending skills and allowing them to experiment with new recipes. It could provides a convenient and accessible way for users to enjoy a variety of cocktails without needing to visit a bar.
        2. Also enables users to prepare unique cocktails for parties and gatherings, adding a special touch to events
    - Unintended usages
        1. Underages might use the application to access and create alcoholic beverages and this application can be a tool that promotes illegal underage drinking issues.
        2. Users might overuse the application, leading to excessive consumption of alcohol, resulting in health problems, including alcohol poisoning, addiction, etc.