import pandas as pd
from collections import defaultdict
import chart_studio.plotly as py
import plotly.graph_objects as go
from plotly.offline import iplot
import plotly.express as px


def odometer():
    """
    generate a odometer vs prices plot
    """
    df = pd.read_csv("vehicles.csv",error_bad_lines=False, engine="python")
    rec_dataset = df[['odometer', 'manufacturer', 'price']]
    rec_dataset.dropna(inplace=True)
    rec_dataset = rec_dataset[3000 <= rec_dataset.price ]
    d = dict(tuple(rec_dataset.groupby('manufacturer')))

    for ele in d.copy():
        x = d[ele]['price']
        d[ele]['price'] = x[x.between(x.quantile(.15), x.quantile(.85))] # without outliers
        x = d[ele]['odometer']
        d[ele]['odometer'] = x[x.between(x.quantile(.05), x.quantile(.95))] # without outliers
        if d[ele]['manufacturer'].all() not in ['ford','chevrolet','toyota','honda','nissan']:
            del d[ele]

    price = defaultdict(list)
    myDataFrame = pd.DataFrame()
    for ele in d:
        myDataFrame = myDataFrame.append(pd.DataFrame(d[ele]))
    myDataFrame.dropna(inplace=True)


    #myDataFrame = pd.DataFrame(d['toyota'])
    myDataFrame.dropna(inplace=True)
    myDataFrame.loc[myDataFrame['odometer'] < 200000, 'odometer_range'] = '175-200'
    myDataFrame.loc[myDataFrame['odometer'] < 175000 , 'odometer_range'] = '150-175'
    myDataFrame.loc[myDataFrame['odometer'] < 150000 , 'odometer_range'] = '125-150'
    myDataFrame.loc[myDataFrame['odometer'] < 125000 , 'odometer_range'] = '100-125'
    myDataFrame.loc[myDataFrame['odometer'] < 100000 , 'odometer_range'] = '75-100'
    myDataFrame.loc[myDataFrame['odometer'] < 75000 , 'odometer_range'] = '50-75'
    myDataFrame.loc[myDataFrame['odometer'] < 50000 , 'odometer_range'] = '25-50'
    myDataFrame.loc[myDataFrame['odometer'] <= 25000, 'odometer_range'] = '0-25'

    final = dict(tuple(myDataFrame.groupby('odometer_range')))
    p = pd.DataFrame(columns = ['odometer', 'manufacturer', 'price'],  
                       index = range(20))
    i=0
    for rang  in ['0-25','25-50','50-75','75-100','100-125','125-150','150-175','175-200']:
        for brand in ['ford','chevrolet','toyota','honda','nissan']:
            x = final[rang][final[rang]['manufacturer']==brand]
            price[brand].append(x['price'].mean())
            #print(pd.DataFrame([rang,brand, x['price'].mean()]).T)
            p.loc[i] = [rang,brand.capitalize(), x['price'].mean()] 
            i+=1
            #p.append(pd.DataFrame([rang,brand, x['price'].mean()]).T)

    output = pd.DataFrame.from_dict(price)


    fig = px.line(p, x='odometer', y='price', color='manufacturer', labels=dict(odometer="Odometer (kMiles)", price="Average Price ($)"))
    #fig = px.line(output, x=['50k_and_below','50k_to_100k','100k_to_150k','150k_to_200k'], y=output.toyota)
    #fig = px.scatter(myDataFrame, x="odometer_range", y="price", color='manufacturer')
    fig.show()
