# Dicoding Rock Paper Scissor Classifier

This project was created to qualify as a graduate of Indosat-Dicoding Scholarship in Machine Learning Skill Track, specifically Machine Learning for Beginner Class.

## Project Background

To build the model, I was provided with 2188 different images of a person's hand making a symbol of either rock, paper, or scissor. The number of images was almost equally distributed between all categories, 712 for paper, 726 for rock, and 750 for scissor. I must create a model with a minimum 80% accuracy, without using any additional external data supply, and I was not allowed to use trained mature models such as ResNet or XCeption.

## Project Overview

To build the model, I have done the following:
1. Check the image to ensure the image are classified correctly by the Dicoding team
2. Use Tensorflow ImageDataGenerator to generate augmented image
3. Build a Convolutional Neural Network, with 3 Convolutional layers, 3 MaxPool layers, and 2 Dense layers (1 of them is the output layer)
4. Visualize the accuracy graph and the test result
5. Implement a code to allow the user to upload their image and test the model

## Project Result

The model got 97,14% validation accuracy at the end of the training phase, and I got a 5-star score from the Dicoding team. You can look for my [LinkedIn profile](https://www.linkedin.com/in/william-mulyawan/) to see the certificate.
