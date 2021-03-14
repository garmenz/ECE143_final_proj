import pandas as pd
from plotly.offline import iplot
import plotly.graph_objs as go


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






