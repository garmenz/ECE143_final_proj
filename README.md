# ECE143 Final Project Team 10


## Problem: 
Build a system that provides some guidelines for people who want to buy a used car; given a specific budget, the system determines the cars that are in the best condition for that price and also determines how fast these cars devalue against different models.
## Dataset: 
[Used Car dataset](https://www.kaggle.com/austinreese/craigslist-carstrucks-data) from Kaggle

The dataset contains twenty-six columns, which cover states of the vehicle like image, size, entry price, years and manufacturer that we can use to analyze.
## Proposed Solution and Real World Application:
- Proposed Solution: With the dataset we have, we would first preprocess the data to gather the quantities of our interest and perform some visualization of the dataset. Then in order to build our recommendation system for the customer, we would perform some different selection cut depending on the budget given by the customer. The selection would return a list of cars that we recommended based on our consideration over the condition, the mileage, the year-made and etc.. With the list of cars in the recommendation list, we would also evaluate the depreciation of a certain manufacture/model over a certain period of time and determine which manufacture/model can best preserve its value.
- Real World Application: The solution of this project can help users gather a list of the most valuable cars they could get within their budget. In addition, the users can know how fast the car devalues over time before their purchase. Our evaluation metrics including MSRP for the model, year, mileage, condition… 

## Timeline:
|  Step                        | Estimated Completion Time | Person(s) in charge      |
|------------------------------|---------------------------|--------------------------|
| Data Preprocessing           | Jan 31st                  | Everybody                |
| Rating System (backend)      | Feb 14th                  | Team(Cid,Manuel, Jiawen) |
| Rating System (frontend)     | Feb 7th                   | Team(Minting, Sunny)     |
| Depreciation Evaluation      | Feb 21st                  | Team(Cid,Manuel, Jiawen) |
| Data Visualization           | Feb 21st                  | Team(Minting, Sunny)     |
| Presentation + Documentation | Feb 28th                  | Everybody                |


## How To Run Code:
In order to run this project successfully please follow the steps below.
1. Click [Here](https://www.kaggle.com/austinreese/craigslist-carstrucks-data) in order to download the dataset from Kaggle
2. Make sure to unzip the dataset once it has finished downloading
3. Copy the vehicles.csv file inside the code repository folder
4. Make sure there is a vehicles.csv in your local directory
5. As long as you are running the python or juypter file inside of the local respository, there should be no problems and running each file normally.
        
## Link to Presentation
[Click Here for Google Slides Presentation](https://docs.google.com/presentation/d/1JSlg4pieSZyxN_lUIDyFe51r9pSUTss_vcwsqD657C8/edit?usp=sharing)
## File Structure:
    Group10_Assignment3.ipynb
        + Test Cases for Assignment 3
    Used_car_recommended_system.ipynb
        + Runs the backend of the recommendation system and contains all the plots
    plot.py
        + Plots a odometer vs price graph
    util.py
        + Contains helper functions to run the backend
    Front_End.ipynb
        + Contains the dashboard for the recommendation system
    Distributions.py
        + Contains the plots for popularity charts
## Modules
    ipywidgets
    IPython.display
    ipywidgets
    ipywidgets
    matplotlib.pyplot
    IPython.core.display
    scipy.stats
    matplotlib 
    util
    numpy
    pandas
    IPython.core.display
    collections
    chart_studio.plotly
    plotly.graph_objects
    plotly.offline
    plotly.express