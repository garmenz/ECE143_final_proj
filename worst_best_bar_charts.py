

import pandas as pd 
from matplotlib import pyplot as plt 

from openpyxl import Workbook
from openpyxl.chart import (
    Reference,
    Series,
    BarChart3D,
)


df = pd.read_csv('vehicles.csv')
rec_dataset = df[['condition', 'odometer', 'title_status', 'manufacturer', 'model', 'price', 'year', 'image_url']]
# drop empty entry
rec_dataset.dropna(inplace=True)


def decide_value_of_cars(carInfo, importance):
    '''
    given a car info, return the importance score
    param:
    @ carInfo: all the information of the cars including condition, odometer, title_status, manufacture and model
    @ score: the score by weighting different factors
    
    :type carInfo: car object 
    :type importance: float percentage, score based from 0-100 
    '''
    
    assert isinstance(carInfo, pd.Series)
    
    condition = carInfo.condition # (new, excellent, like new, good, fair, salvage) :type: string
    if condition is None:
        condition = 'unspecified'
    else:
        condition = condition.strip()
        
    mileage = carInfo.odometer # :type: float
    if mileage is None:
        mileage = 'unspecified'
        
    title_status = carInfo.title_status # (clean, rebuilt, salvage, lien, parts only, missing) :typt: string
    if title_status is None:
        title_status = 'unspecified'
    else:
        title_status = title_status.strip()
        
    year = carInfo.year # :type: float 
    if year is None:
        year = 'unspecified'
    
    # lets weigh these values 
    if (importance == 'condition'):
        weights_dict = {
        'condition':0.5,
        'odometer':0.16666667,
        'title_status':0.16666667,
        'year':0.16666667 
    }
        
    elif (importance == 'odometer'):
        weights_dict = {
        'condition':0.16666667,
        'odometer':0.5,
        'title_status':0.16666667,
        'year':0.16666667 
    }
        
    elif (importance == 'title_status'):
        weights_dict = {
        'condition':0.16666667,
        'odometer':0.16666667,
        'title_status':0.5,
        'year':0.16666667 
    }
        
    elif (importance == 'year'):
        weights_dict = {
        'condition':0.16666667,
        'odometer':0.16666667,
        'title_status':0.16666667,
        'year':0.5 
    }
        
    else: # if user doesn't specify an importance factor, lets weigh everything the same
         weights_dict = {
        'condition':0.057,
        'odometer':0.42,
        'title_status':0.006,
        'year':0.517 
    }
    
    condition_dict = {
        'new': 100,
        'excellent': 95,
        'like new': 90,
        'good': 85,
        'fair': 60, 
        'salvage': 5,
        'unspecified' : 0
        
    }
    
    title_status_dict = {
        'clean': 100,
        'lien': 90, 
        'rebuilt': 40, 
        'missing': 20, 
        'parts_only': 10,
        'salvage': 5,
        'unspecified' : 0
    }
    
    odometer_dict = {
        '100k_and_below': 100,
        '100k_to_120k': 90, 
        '120k_to_150k': 80, 
        '150k_to_180k': 50,
        '180k_to_200k': 30,
        '200k_to_300k': 15,
        '300k_and_above': 5,
        'unspecified' : 0
    }
    
    year_dict = {
        '2005_and_above': 100,
        '2000_to_2005': 90,
        '1990_to_2000': 60, 
        '1970_to_1990': 40, 
        '1950_to_1970': 20,
        '1950_and_below': 10,
        'unspecified' : 0
    }
    
    # lets find the ranges for the mileage 
    if(mileage <= 100000):
        mileage_score = '100k_and_below'
    elif(100000 < mileage <= 120000):
        mileage_score = '100k_to_120k'
    elif(120000 < mileage <= 150000):
        mileage_score = '120k_to_150k'
    elif(150000 < mileage <= 180000):
        mileage_score = '150k_to_180k'
    elif(180000 < mileage <= 200000): 
        mileage_score = '180k_to_200k'
    elif(200000 < mileage <= 300000): 
        mileage_score = '200k_to_300k'
    elif(mileage > 300000):
        mileage_score = '300k_and_above'
    else:
        mileage_score = 'unspecified'
    
    # now lets find the ranges for the years 
    if(year >= 2005): 
        year_score = '2005_and_above'
    elif(2000 <= year < 2005): 
        year_score = '2000_to_2005'
    elif(1990 <= year < 2000):
        year_score = '1990_to_2000'
    elif(1970 <= year < 1990): 
        year_score = '1970_to_1990'
    elif(1950 <= year < 1970): 
        year_score = '1950_to_1970' 
    elif(year < 1950): 
        year_score = '1950_and_below'
    else:
        year_score = 'unspecified'
        
    # now lets calculate the score 
    try:
        score = condition_dict[condition]*weights_dict['condition'] + title_status_dict[title_status]*weights_dict['title_status'] + odometer_dict[mileage_score]*weights_dict['odometer'] + year_dict[year_score]*weights_dict['year']
    except Exception as e:
        print(e)
        score = 0
    
    return score





def cars_in_price_range(cars_dt, lower_bound, upper_bound,  num_of_sel=5, importance=None, order=True):
    '''
    given an input price range, return the list of cars with info of condition, odometer, title_status, manufacture and model, [optional] image_url, description
    param:
    @ lower_bound: lower bound of the price
    @ upper_bound: upper bound of the price
    @ num_of_sel: how many number of cars to display at the end (default=5)
    @ cars_dt: full car dataset
    @ importance: the importance score for quantifiable factors (in a dictionary) [sum is 1]
    return:
    @ list of cars in pandas dataframe with information of the cars
    '''
    scores = list()
    sub_set = cars_dt.query('@lower_bound <= price <= @upper_bound') # get all the cars within the proice range
    for index, row in sub_set.iterrows():
        scores.append( decide_value_of_cars(row,importance) )
    sub_set['score'] = scores # add the scores to the dataframe under 'score' column
    sub_set.sort_values(by='score',ascending = order, inplace=True) # Sort by scores, tops scores at the beggining
    sub_set = sub_set.head(num_of_sel) # get the first num_of_sel rows
    print(sub_set)
    return sub_set



def most_freq_manufacturer(x): 
    '''
    This functions takes in a pd.DataFrame object. It will return a list of cars of the 5 most frequent manufacturers.
    
    :param x: input DataFrame object 
    '''
    assert isinstance(x,pd.DataFrame)
    
    col_manufacturer = x['manufacturer']
    most_frequent = {}
    
    for index, value in col_manufacturer.items(): 
        if value in most_frequent.keys(): 
            count = most_frequent[value]
            most_frequent[value] = count + 1
        else: # this means key does not exist 
            most_frequent[value] = 1
            
    most_frequent = dict(sorted(most_frequent.items(), key=lambda item: item[1])) # lets order our dictionary by its values 
    
    keys = list(most_frequent.keys())
    keys_list = keys[-5:]
    keys_list.reverse() # first item in list is most popular
    return keys_list

def how_many_are(x,manu_list):
    '''
    This function takes in a pd.DataFrame and a list of car manufacture. It checks how many cars in the input data frame
    are from each of the car manufacturers in the input list. Returns a list of the count
    
    :param x: input pd.DataFrame 
    :param manu_list: input car manufacturer list 
    '''
    assert isinstance(x,pd.DataFrame)
    assert isinstance(manu_list, list)
    assert all(isinstance(manu, str) for manu in manu_list)
    
    col_manufacturer = x['manufacturer']
    most_frequent = {}
    
    for index, value in col_manufacturer.items(): 
        if value in most_frequent.keys(): 
            count = most_frequent[value]
            most_frequent[value] = count + 1
        else: # this means key does not exist 
            most_frequent[value] = 1
            
    data_values = [] # we are starting in decending order ford down to nissan 
    
    for manufacturer in manu_list: 
        number = most_frequent[manufacturer]
        data_values.append(number)
        
    return data_values

def specific_manufacturer(x,manu_list):
    '''
    This function takes in a pd.DataFrame and a list of car manufacture. It returns a df with just those
    given manufacturers 
    
    :param x: input pd.DataFrame 
    :param manu_list: input car manufacturer list 
    '''
    
    assert isinstance(x, pd.DataFrame)
    assert isinstance(manu_list, list)
    assert all(isinstance(manu, str) for manu in manu_list)
    
    
    frequent_manu = x.loc[x['manufacturer'].isin(manu_list)].groupby('manufacturer').head(5000) # should be a dataframe only with data of the most frequent manufacturers. same size for each 
    
    return frequent_manu


def generate_bar_charts():
    '''
    This function is used to generate bar charts for the 5000 worst cars and the 5000 best cars.
    '''

    # The following is for the bar chart for worst cars df 
    
    # Note: in order to generate worst_cars_df we must change the ascending order of cars_in_price_range to True
    
    most_popular_cars = most_freq_manufacturer(rec_dataset) # lowest number is 12677 which is for Nissan. Ford is highest with 38526

    fixed_data = specific_manufacturer(rec_dataset, most_popular_cars) # lets grab some data just of the specific manufacturers, 5000 of for each 

    
    worst_cars_df = cars_in_price_range(fixed_data, 5000, 30000, num_of_sel=5000, order=True) # grabbing the worst cars 
    data_for_mpc = how_many_are(worst_cars_df, most_popular_cars) # grabbing the counts for car manufacturer
    
    
    # lets create our bar charts 
    
    wb = Workbook()
    ws = wb.active
    
    rows = [
        (None,"Total for each manufacturer"),
        ("Ford", data_for_mpc[0]),
        ("Chevrolet", data_for_mpc[1]),
        ("Toyota", data_for_mpc[2]),
        ("Honda", data_for_mpc[3]),
        ("Nissan", data_for_mpc[4])
    ]
    
    for row in rows:
        ws.append(row)
    
    data = Reference(ws, min_col=2, min_row=1, max_col=2, max_row=6)
    titles = Reference(ws, min_col=1, min_row=2, max_row=6)
    chart = BarChart3D()
    chart.title = "The 5,000 Worst Cars based on Manufacturer"
    chart.y_axis.title = 'Total'
    chart.add_data(data=data, titles_from_data=True)
    chart.set_categories(titles)
    
    ws.add_chart(chart, "E5")
    wb.save("bar3d.xlsx")
    
    
    # The following is for the bar chart (the best cars)
    
    # Note: To generate the best_car_ df, we must change the ascending order of cars_in_price_range to False
    
    
    most_popular_cars = most_freq_manufacturer(rec_dataset) 
    fixed_data = specific_manufacturer(rec_dataset, most_popular_cars) 
    
    best_cars_df = cars_in_price_range(fixed_data, 5000, 20000, num_of_sel=5000, order=False)
    data_for_mpc = how_many_are(best_cars_df, most_popular_cars)
    
    wb = Workbook()
    ws = wb.active
     
    rows = [
        (None,"Total for each manufacturer"),
        ("Ford", data_for_mpc[0]),
        ("Chevrolet", data_for_mpc[1]),
        ("Toyota", data_for_mpc[2]),
        ("Honda", data_for_mpc[3]),
        ("Nissan", data_for_mpc[4])
    ]
    for row in rows:
        ws.append(row)
    data = Reference(ws, min_col=2, min_row=1, max_col=2, max_row=6)
    titles = Reference(ws, min_col=1, min_row=2, max_row=6)
    chart = BarChart3D()
    chart.title = "The 5,000 Best Cars based on Manufacturer"
    chart.y_axis.title = 'Total'
    chart.add_data(data=data, titles_from_data=True)
    chart.set_categories(titles)
    ws.add_chart(chart, "E5")
    wb.save("bar2_3d.xlsx")
    
  
    
