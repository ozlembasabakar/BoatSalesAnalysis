# from flask import Flask, render_template, request
# import numpy as np
# import pandas as pd
# from joblib import load
# import statistics
# import matplotlib.pyplot as plt
# import seaborn as sns
# import plotly.graph_objects as go
# import plotly.express as px
# import uuid

# app = Flask(__name__, template_folder="templates")

# @app.route("/")
# def main_page():
#     return render_template('main_page.html')

# @app.route("/median", methods=['GET', 'POST'])
# def medain_graph():
#     request_type_str = request.method
#     if request_type_str == 'GET':
#         random_string = uuid.uuid4().hex
#         path = "static/" + random_string + ".svg"
#         data = pd.read_excel('dataset.xlsx')
#         x = data['price']
#         median_line(x, path)
#         return render_template('median_graph.html', href=path)

#     # else:
#     #     text = request.form['text']
#     #     random_string = uuid.uuid4().hex
#     #     path = "static/" + random_string + ".svg"
#     #     model = load('model_robust.joblib')
#     #     data = pd.read_excel('dataset_price.xlsx')
#     #     median_line_prediction(model, data, text, path)
#     #     return render_template('median_graph.html', href=path)

# def median_line(x, output_file):
   
#     median = statistics.median(x)

#     fig = go.Figure(data=[go.Histogram(x=x, y=list(range(0, 500)))])
#     fig.add_vline(x=median, line_width=3, line_color="red"
#                   , annotation_text='Median: {:.2f}'.format(median)
#                   , annotation_position="bottom right", line_dash="dot"
#                   , annotation_font_size=20
#                   , annotation_font_color="red")
    
#     fig.write_image(output_file, width=800, height=600)
#     fig.show()

# def median_line_prediction(model, x, input_y, output_file):

#     median = statistics.median(x)
        
#     new_pred = float(model.predict([[input_y]]))

#     fig = go.Figure(data=[go.Histogram(x=x, y=list(range(0, 500)))])
#     fig.add_vline(x=new_pred, line_width=3, line_color="black"
#               # , annotation_text='Prediction: {:.2f}'.format(np.array([new_pred]))
#               , annotation_position="top right", line_dash="dot"
#               , annotation_font_size=20
#               , annotation_font_color="black")

#     fig.add_vline(x=median, line_width=3, line_color="red"
#                   # , annotation_text="Median: ${0:.02f}%".format(np.array([median]))
#                   , annotation_position="bottom right", line_dash="dot"
#                   , annotation_font_size=20
#                   , annotation_font_color="red")

#     fig.write_image(output_file, width=800, height=600)
#     fig.show()


# @app.route("/line_chart")
# def line_chart():
#     random_string = uuid.uuid4().hex
#     path = "static/" + random_string + ".svg"
#     dataset = pd.read_excel('dataset.xlsx')
#     data = dataset[['model', 'price']]
#     line_chart_graph_plotly(data, path)
#     return render_template('line_chart.html', href=path)

# def line_chart_graph_plotly(df, output_file):

#     line_chart = df.dropna(how='any',axis=0)
#     srt = line_chart.columns[0]
#     line_chart = line_chart.sort_values(by=str(srt), ascending=True)
    
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(
#         x=line_chart.iloc[:,0],
#         y=line_chart.iloc[:,1]))
    
#     fig.write_image(output_file, width=800, height=600)
#     fig.show()


# @app.route("/heatmap")
# def heatmap_graph():
#     random_string = uuid.uuid4().hex
#     path = "static/" + random_string + ".svg"
#     data = pd.read_excel('dataset3.xlsx')
#     heatmap_graph_plotly(data, path)
#     return render_template('heatmap.html', href=path)

# def heatmap_graph_plotly(df,output_file):
    
#     fig = px.scatter(df, x="yatchAge", y="length", color="price")
    
#     fig.write_image(output_file, width=800, height=600)
#     fig.show()


# @app.route("/graph_3d")
# def graph_3d():
#     random_string = uuid.uuid4().hex
#     path = "static/" + random_string + ".svg"
#     data = pd.read_excel('dataset.xlsx')
#     graph_3d_plotly(data, path)
#     return render_template('3d_graph.html', href=path)

# def graph_3d_plotly(df, file_name):

#     x = df.columns[5]
#     y = df.columns[6]
#     z = df.columns[7] 
    
#     fig = px.scatter_3d(df, x=str(x)
#                         , y=str(y)
#                         , z=str(z)
#                         , color=str(x))
#     fig.show()
#     fig.write_image(file_name, width=800, height=600)

# def line_chart_damage_graph_plotly(df, output_file):

#     fig = go.Figure()
#     fig.add_trace(go.Scatter(
#         x=df.iloc[:,0],
#         y=df.iloc[:,1]))

#     fig.write_image(output_file, width=800, height=600)
#     fig.show()




###############################################################################################################################

from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from joblib import load
import statistics
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import uuid
# from xgboost.xgbregressor import XGBRegressor

app = Flask(__name__, template_folder="templates")

@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/line_charts")
def line_chart():
    random_string = uuid.uuid4().hex
    path = "static/" + random_string + ".svg"
    dataset = pd.read_excel('dataset.xlsx')
    data = dataset[['model', 'price']]
    line_chart_graph_plotly(data, path)
    return render_template('line_chart.html', href=path)

def line_chart_graph_plotly(df, output_file):

    line_chart = df.dropna(how='any',axis=0)
    srt = line_chart.columns[0]
    line_chart = line_chart.sort_values(by=str(srt), ascending=True)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=line_chart.iloc[:,0],
        y=line_chart.iloc[:,1]))
    
    fig.write_image(output_file, width=800, height=600)

    fig.show()
    return fig

@app.route("/graph_3d")
def graph_3d():
    random_string = uuid.uuid4().hex
    path = "static/" + random_string + ".svg"
    data = pd.read_excel('dataset.xlsx')
    graph_3d_plotly(data, path)
    return render_template('3d_graph.html', href=path)

def graph_3d_plotly(df, file_name):

    x = df.columns[5]
    y = df.columns[6]
    z = df.columns[7] 
    
    fig = px.scatter_3d(df, x=str(x)
                        , y=str(y)
                        , z=str(z)
                        , color=str(x))
    fig.write_image(file_name, width=800, height=600)

    fig.show()
    return fig

@app.route("/heatmap")
def heatmap_graph():
    random_string = uuid.uuid4().hex
    path = "static/" + random_string + ".svg"
    data = pd.read_excel('dataset.xlsx')
    heatmap_graph_plotly(data, path)
    return render_template('heatmap.html', href=path)

def heatmap_graph_plotly(df,output_file):
    
    fig = px.scatter(df, x="yatchAge", y="length", color="price")
    
    fig.write_image(output_file, width=800, height=600)
    fig.show()
    return fig



@app.route("/median", methods=['GET', 'POST'])
def medain_graph():
    request_type_str = request.method
    if request_type_str == 'GET':
        random_string = uuid.uuid4().hex
        path = "static/" + random_string + ".svg"
        data = pd.read_excel('dataset.xlsx')
        x = data['price']
        median_line(x, path)
        return render_template('median_graph.html', href=path)

    else:
        text = request.form['text']
        random_string = uuid.uuid4().hex
        path = "static/" + random_string + ".svg"
        model = load('model_rf_rb.joblib')
        dataset = pd.read_excel('dataset.xlsx')
        data = dataset['price']
        median_line_prediction(model, data, text, path)
        return render_template('median_graph.html', href=path)

def median_line(x, output_file):
   
    median = float(pd.DataFrame(x).median())

    fig = go.Figure(data=[go.Histogram(x=x, y=list(range(0, 100)))])
    fig.add_vline(x=median, line_width=3, line_color="black"
                  , annotation_text='Median: {:.2f}'.format(median)
                  , annotation_position="bottom right", line_dash="dot"
                  , annotation_font_size=20
                  , annotation_font_color="dark blue")
    
    fig.write_image(output_file, width=800, height=600)
    return fig

def median_line_prediction(model, x, input_y, output_file):

    median = float(pd.DataFrame(x).median())
    
    new_pred = float(model.predict([[input_y]]))
    fig = go.Figure(data=[go.Histogram(x=x, y=list(range(0, 100)))])
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