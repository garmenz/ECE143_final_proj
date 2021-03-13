import pandas as pd
from plotly.offline import iplot
import plotly.graph_objs as go

df = pd.read_csv('vehicles.csv',
                 usecols=[4,5,6,7,8,9,10,11,12,13,15,16,17,18,22,23,24],
                 encoding='latin')


df.loc[df['year'] >= 2005, 'year_range'] = '2005_and_above'
df.loc[df['year'] < 2005, 'year_range'] = '2000_to_2005'
df.loc[df['year'] < 2000, 'year_range'] = '1990_to_2000'
df.loc[df['year'] < 1990, 'year_range'] = '1970_to_1990'
df.loc[df['year'] < 1970, 'year_range'] = '1950_to_1970'
df.loc[df['year'] <= 1950, 'year_range'] = '1950_and_below'

df.loc[df['odometer'] >= 200000, 'odometer_range'] = '200k_and_above'
df.loc[df['odometer'] < 200000, 'odometer_range'] = '180k_to_200k'
df.loc[df['odometer'] < 180000, 'odometer_range'] = '160k_to_180k'
df.loc[df['odometer'] < 160000, 'odometer_range'] = '140k_to_160k'
df.loc[df['odometer'] < 140000, 'odometer_range'] = '120k_to_140k'
df.loc[df['odometer'] < 120000, 'odometer_range'] = '100k_to_120k'
df.loc[df['odometer'] < 100000, 'odometer_range'] = '80k_to_100k'
df.loc[df['odometer'] < 80000, 'odometer_range'] = '60k_to_80k'
df.loc[df['odometer'] < 60000, 'odometer_range'] = '40k_to_60k'
df.loc[df['odometer'] < 40000, 'odometer_range'] = '20k_to_40k'
df.loc[df['odometer'] <= 20000, 'odometer_range'] = '20k_and_below'



def pie_count(data, field):
    '''
        This function is intend to generate pie charts for specific column from the dataset,
        For any data < 0.5%, it will include as "other".
    '''
    data = data[field].value_counts().to_frame()  # Create a new Dataframe with count of field

    total = data[field].sum()
    data['percentage'] = 100 * data[field] / total  # Create a new column of percentage

    percent_limit = 0.5  # Set Percentage lower limit
    otherdata = data[data['percentage'] < percent_limit]
    maindata = data[data['percentage'] >= percent_limit]
    others = otherdata['percentage'].sum()

    data = maindata
    other_label = "Others(<" + str(percent_limit) + "% each)"  # Create new label
    data.loc[other_label] = pd.Series({field: otherdata[field].sum()})

    labels = data.index.tolist()
    datavals = data[field].tolist()
    title = "{} statistics".format(field)

    trace = go.Pie(labels=labels, values=datavals)

    layout = go.Layout(
        title=title,
        height=500,
    )

    fig = go.Figure(data=[trace], layout=layout)

    iplot(fig)


def pie_count_all(data, field):
    '''
       This function is intend to generate pie charts for specific column from the dataset
    '''
    data = data[field].value_counts().to_frame()  # Create a new Dataframe with count of field
    labels = data.index.tolist()
    datavals = data[field].tolist()
    title = "{} statistics".format(field)

    trace = go.Pie(labels=labels, values=datavals)

    layout = go.Layout(
        title=title,
        height=500,
    )

    fig = go.Figure(data=[trace], layout=layout)

    iplot(fig)






