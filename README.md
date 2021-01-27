# ECE143_final_proj

Proposal 10: Used Car Recommender System

Problem: 
Build a system that provides some guidelines for people who want to buy a used car; given a specific budget, the system determines the cars that are in the best condition for that price and also determines how fast these cars devalue against different models.
Dataset: 
Kaggle dataset (https://www.kaggle.com/austinreese/craigslist-carstrucks-data)
The dataset contains twenty-six columns, which cover states of the vehicle like image, size, entry price, years and manufacturer that we can use to analyze.
Proposed Solution and Real World Application:
Proposed Solution: With the dataset we have, we would first preprocess the data to gather the quantities of our interest and perform some visualization of the dataset. Then in order to build our recommendation system for the customer, we would perform some different selection cut depending on the budget given by the customer. The selection would return a list of cars that we recommended based on our consideration over the condition, the mileage, the year-made and etc.. With the list of cars in the recommendation list, we would also evaluate the depreciation of a certain manufacture/model over a certain period of time and determine which manufacture/model can best preserve its value.
Real World Application: The solution of this project can help users gather a list of the most valuable cars they could get within their budget. In addition, the users can know how fast the car devalues over time before their purchase. Our evaluation metrics including MSRP for the model, year, mileage, condition… 
Timeline:
Step
Estimated Completion Time
Person(s) in charge
Data Preprocessing
Extract
Clean Up

Jan 31st 
All of us
Rating System (backend)
Depending on a user’s preference(make,year,model), return the best value car

Feb 14th
Team(Cid,Manuel, Jiawen)
Rating System (frontend)
Interaction with users

Feb 7th
Team(Minting, Sunny)
Depreciation Evaluation
Feb 21st
Team(Cid,Manuel, Jiawen)
Data Visualization
Feb 21st
Team(Minting, Sunny)
Presentation + Documentation
Feb 28th
Everybody

