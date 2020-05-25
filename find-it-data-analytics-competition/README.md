# Hotel Booking Cancellation Prediction

This project was created to compete in Find IT Data Analytics Competition that was hosted by Universitas Gadjah Mada in the city of Jogjakarta, Indonesia. The team consists of 3 persons, including me.

## Project Background

To build the model, we were provided with 119390 rows of data with 32 different variables, one of them being the cancellation status of this particular transaction. To win the competition, we were expected to not only build a high-accuracy model but also provide insight for the hotel manager.

## Project Overview

To build the model, we have done the following:
1. Preprocess the data and engineer new features
2. Try different models, such as XGBoost, Catboost, Random Forest, Logistic Regression, and K-Nearest Neighbour
    - After trying different combination, we choose Catboost and Random Forest as our best models
3. Select the features we want to include using feature importance and SHAP value
4. Build a stacked model to combine our Catboost and Random Forest model. The next layer of the stacked model is a simple logistic regression
5. Validate the model

## Project Result

The model got 98,19% validation accuracy at the end of the training phase, and unfortunately the competition has been postponed due to the Coronavirus pandemic. I will update this repo if there are any changes in the final stage later.
