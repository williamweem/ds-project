# Offline Store Recommender System

This project was created for an offline retail company to help them boost their sales. Our idea was to use a recommender system to help the store manager choose which product to include in their promotion strategy, which hopefully would seem interesting to their customer. To help with the project, we used a paper called "A Case Study in a Recommender System Based on Purchase Data" (Pradel et al, 2011) as references.

## Project Background

To build the model, we were provided with 463505 rows of data, in which each row represents a product in a transaction. The columns provided are the price, product name, product category, transaction id, customer id, and the transaction date. The data were collected in 13 months range, and the distribution of data among the dates is quite balanced. There is more than 100 product category in the dataset. The goal is to provide a recommendation for each user in product category level.

## Project Overview

To build the model, I have done the following:
1. Preprocess the data
2. Separate the data according to their date range, and then perform nested time-series cross-validation

    ![Nested Time Series Cross Validation](https://i.stack.imgur.com/fXZ6k.png)

3. Engineer a function to recommend for each user using 2 kinds of model: Funk's SVD and Non-Negative Matrix Factorization
4. Validate the recommendation using 3 metrics: precision, recall, f1-score
5. Tune the hyperparameter of the model
5. Validate the final result, and give the recommendations for each user

## Project Result

The model got 22.8% precision value, 18.7% recall value, and 17.1% f1-score value. While the numbers seem to be low at first sight, it turns out these numbers are significantly higher than the result of the paper that we referencing to (14.54% precision value, 13.47% recall value, 11.98% f1-score value).
