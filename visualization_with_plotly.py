import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
import plotly.express as px
import plotly.graph_objects as go
from joblib import dump, load
from joblib import load


model = load('model.joblib')
dataset = pd.read_excel('dataset.xlsx')

def line_chart_graph(df):

    line_chart = df.dropna(how='any',axis=0)
    srt = line_chart.columns[0]
    line_chart = line_chart.sort_values(by=str(srt), ascending=True)
    
    plt.plot(line_chart.iloc[:,0], line_chart.iloc[:,1], linewidth=0.7)
    plt.xlabel(str(line_chart.columns[0]))
    plt.ylabel(str(line_chart.columns[1]))
    plt.grid(True)
    plt.show()

def heatmap_graph(df):
    
    df = df.dropna(how='any',axis=0)

    new_df = pd.pivot_table(df,index=[str(df.columns[1])], columns = str(df.columns[2]), values = str(df.columns[0]))
    
    ax = sns.heatmap(new_df)

price = []
length = []
yatchage = []
for m in range(len(dataset['price'])):
    if 'nan' in str(dataset['price'][m]):
        price.append(0)
        length.append(dataset['length'][m])
        yatchage.append(dataset['yatchAge'][m])
        
    if float(dataset['price'][m]) < 600000:
        price.append(dataset['price'][m])
        length.append(dataset['length'][m])
        yatchage.append(dataset['yatchAge'][m])

dataset_2 = pd.DataFrame(list(zip(price, length, yatchage)),
               columns =['price', 'length', 'yatchAge'])

def median_graph(model, df, input_y, fig_name):

    median = statistics.median(df)
    
    sns.distplot(df, hist=True, kde=False, rug=False )
    min_ylim, max_ylim = plt.ylim()
    plt.text(median*1.1, max_ylim*0.9, 'Median: {:.2f}'.format(median))
    plt.axvline(x=median, 
                color='red')
    
    # input_price = np.array(input_price).reshape(1, -1) 
    new_pred = model.predict([[input_y]])
    plt.text(new_pred*1.1, max_ylim*0.5, 'Boat Price: {:.2f}'.format(int(new_pred)))
    plt.axvline(x=int(new_pred),
                color='black')
    plt.savefig(str(fig_name) + '.svg')

def float_num(floats_str):
  floats = float(floats_str)
  as_np_arr = np.array(floats)
  return as_np_arr

def median_line(model, df, x, y, input_y, output_file):
    
    median = float(pd.DataFrame(x).median())
    
    new_pred = float(model.predict([[input_y]]))
    fig = go.Figure(data=[go.Histogram(x=x, y=y)])
    fig.add_vline(x=new_pred, line_width=3, line_color="black"
              , annotation_text='Prediction: {:.2f}'.format(new_pred)
              , annotation_position="top right", line_dash="dot"
              , annotation_font_size=20
              , annotation_font_color="black")
    
    fig.add_vline(x=median, line_width=3, line_color="red"
                  , annotation_text='Median: {:.2f}'.format(median)
                  , annotation_position="bottom right", line_dash="dot"
                  , annotation_font_size=20
                  , annotation_font_color="red")
                  
    
    fig.write_image(output_file, width=800, height=600)
    return fig

def line_chart_graph_plotly(df, output_file):

    line_chart = df.dropna(how='any',axis=0)
    srt = line_chart.columns[0]
    line_chart = line_chart.sort_values(by=str(srt), ascending=True)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=line_chart.iloc[:,0],
        y=line_chart.iloc[:,1],
        name='Gaps',))
    
    fig.write_image(output_file, width=800, height=600)
    fig.show()

def heatmap_graph_plotly(df,output_file):
    
    fig = px.scatter(df, x="yatchAge", y="length", color="price")
    # fig.update_xaxes(side="top")
    
    fig.write_image(output_file, width=800, height=600)
    fig.show()

def scatter_3d(df, file_name):
    x = df.columns[-3]
    y = df.columns[-1]
    z = df.columns[-5] 
    
    fig = px.scatter_3d(df, x=str(x)
                        , y=str(y)
                        , z=str(z),)
    
    fig.write_image(file_name, width=800, height=600)
    fig.show()


dataset_2.to_excel('dataset2.xlsx', index = False)
dataset['price'].to_excel('dataset_price.xlsx', index = False)
  
