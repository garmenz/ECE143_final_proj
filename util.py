import numpy as np
import pandas as pd

def cars_in_price_range(cars_dt, lower_bound, upper_bound,  num_of_sel=5, importance=None):
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
    sub_set = cars_dt.copy()
    sub_set = sub_set.query('@lower_bound <= price <= @upper_bound') # get all the cars within the proice range
    for index, row in sub_set.iterrows():
        scores.append( decide_value_of_cars(row,importance) )
    sub_set['score'] = scores # add the scores to the dataframe under 'score' column
    sub_set.sort_values(by='score',ascending = False, inplace=True) # Sort by scores, tops scores at the beggining
    sub_set = sub_set.head(num_of_sel) # get the first num_of_sel rows
    return sub_set


def decide_value_of_cars(carInfo, importance):
    '''
    given a car info, return the importance score
    param:
    @ carInfo: all the information of the cars including condition, odometer, title_status, manufacture and model
    @ score: the score by weighting different factors

    :type carInfo: car object
    :type importance: float percentage, score based from 0-100
    '''
    # so to calculate the importance score, I want to measure that off of 'condition' 'odometer' and 'title_status'
    # 'manufacturer', 'model', and 'year' are just details of the car

    assert isinstance(carInfo, pd.Series)

    condition = carInfo.condition  # (new, excellent, like new, good, fair, salvage) :type: string
    if condition is None:
        condition = 'unspecified'
    else:
        condition = condition.strip()

    mileage = carInfo.odometer  # :type: float
    if mileage is None:
        mileage = 'unspecified'

    title_status = carInfo.title_status  # (clean, rebuilt, salvage, lien, parts only, missing) :typt: string
    if title_status is None:
        title_status = 'unspecified'
    else:
        title_status = title_status.strip()

    year = carInfo.year  # :type: float
    if year is None:
        year = 'unspecified'

    # lets weigh these values
    if (importance == 'condition'):
        weights_dict = {
            'condition': 0.5,
            'odometer': 0.16666667,
            'title_status': 0.16666667,
            'year': 0.16666667
        }

    elif (importance == 'odometer'):
        weights_dict = {
            'condition': 0.16666667,
            'odometer': 0.5,
            'title_status': 0.16666667,
            'year': 0.16666667
        }

    elif (importance == 'title_status'):
        weights_dict = {
            'condition': 0.16666667,
            'odometer': 0.16666667,
            'title_status': 0.5,
            'year': 0.16666667
        }

    elif (importance == 'year'):
        weights_dict = {
            'condition': 0.16666667,
            'odometer': 0.16666667,
            'title_status': 0.16666667,
            'year': 0.5
        }

    else:  # if user doesn't specify an importance factor, lets weigh everything the same
        weights_dict = {
            'condition': 0.057,
            'odometer': 0.42,
            'title_status': 0.006,
            'year': 0.517
        }

    condition_dict = {
        'new': 100,
        'excellent': 95,
        'like new': 90,
        'good': 85,
        'fair': 60,
        'salvage': 5,
        'unspecified': 0

    }

    title_status_dict = {
        'clean': 100,
        'lien': 90,
        'rebuilt': 40,
        'missing': 20,
        'parts_only': 10,
        'salvage': 5,
        'unspecified': 0
    }

    odometer_dict = {
        '100k_and_below': 100,
        '100k_to_120k': 90,
        '120k_to_150k': 80,
        '150k_to_180k': 50,
        '180k_to_200k': 30,
        '200k_to_300k': 15,
        '300k_and_above': 5,
        'unspecified': 0
    }

    year_dict = {
        '2005_and_above': 100,
        '2000_to_2005': 90,
        '1990_to_2000': 60,
        '1970_to_1990': 40,
        '1950_to_1970': 20,
        '1950_and_below': 10,
        'unspecified': 0
    }

    # lets find the ranges for the mileage
    mileage_score = max((1 - mileage / 200000) * 100, 0)

    # now lets find the ranges for the years
    year_score = max((1 - (2021 - year) / (2021 - 1950)) * 100, 0)

    # now lets calculate the score
    try:
        score = condition_dict[condition] * weights_dict['condition'] + title_status_dict[title_status] * weights_dict[
            'title_status'] + mileage_score * weights_dict['odometer'] + year_score * weights_dict['year']
    except Exception as e:
        # print(f"ERROR: {e}")
        score = 0

    return score

def path_to_image_html(path):
    return '<img src="'+ path + '" width="100" >'

def preference_selection(cars_dt, State=None, Fuel=None, Type=None, color=None, Cylinder=None, Transmission=None, year_min=None, year_max=None, importance=None, num_of_sel=15):
    '''
    given user's preference in fuel, type, color, cylinders, transmission, year, state, return manufacture, model and price
    param:
    @ state, fuel, type, cylinder, transmission, year: user preference choice
    return:
    @ list of cars in pandas dataframe with manufacture, model and price
    '''
    scores = list()
    new_dt = cars_dt
    if State is not 'None':
        new_dt = new_dt[new_dt['state']==State.lower()]
    if Fuel is not 'None':
        new_dt = new_dt[new_dt['fuel']==Fuel.lower()]
    if Type is not 'None':
        new_dt = new_dt[new_dt['type']==Type.lower()]
    if Cylinder is not 'None':
        cyl_str = f'{Cylinder} cylinders'
        new_dt = new_dt[new_dt['cylinders']==cyl_str]
    if color is not 'None':
        new_dt = new_dt[new_dt['paint_color']==color.lower()]
    if Transmission is not 'None':
        new_dt = new_dt[new_dt['transmission']==Transmission.lower()]
    if year_min is not None:
        new_dt = new_dt[new_dt['year']>=year_min]
    if year_max is not None:
        new_dt = new_dt[new_dt['year']<=year_max]

    print(f'Thank you for your input. Your selection is: \nstate: {State}, \nFuel: {Fuel}, \nType: {Type}, \nColor: {color}, \nCylinder: {Cylinder}, \nTransmission: {Transmission}, \nYear range: {year_min}-{year_max}')
    for index, row in new_dt.iterrows():
        scores.append( decide_value_of_cars(row,importance) )
    new_dt['score'] = scores # add the scores to the dataframe under 'score' column
    new_dt.sort_values(by='score',ascending = False, inplace=True) # Sort by scores, tops scores at the beggining
    new_dt = new_dt.head(num_of_sel) # get the first num_of_sel rows

    return new_dt[['condition', 'odometer', 'title_status', 'manufacturer', 'model', 'price', 'year', 'image_url', 'score']]
