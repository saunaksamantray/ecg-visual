from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
import numpy as np
import mne
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import datetime

def read_edf(path=None,no_samples=100000):
    try:
        if path != None :
            edf = mne.io.read_raw_edf(path)
            data=edf.get_data().T
            data=data[:,0]
            data=data[0:int(no_samples)]
            print(len(data))
            frequency=edf.info['sfreq']
            time = edf.times
            ntime = edf.n_times
            ch_names = edf.ch_names
            df = edf.to_data_frame(picks=ch_names[0])
    except Exception as e:
        print('Error: ',e)
        return False
    return np.array(data),frequency, edf.info, time, ntime,ch_names, df


    '''
    example
    data,f=read_edf('D:/SELECTED_RECORDS/11-38-14/11-38-14.edf')
    '''
    print("Example : D:/SELECTED_RECORDS/11-38-14/11-38-14.edf ")

    #path1=input("Path to edf file " )


    
path1="D:/SELECTED_RECORDS/11-38-14/11-38-14.edf"
data,f,info,time, ntime,ch_names, frame=read_edf(path1)

app = Flask(__name__)

@app.route('/callback', methods=['POST', 'GET'])
def cb():
    return gm(request.args.get('data'))
   
@app.route('/')
def index():
    return render_template('chartsajax.html',  graphJSON=gm())

def gm(sec='1'):
    
    
    #length=input("Enter no. of samples  to visualize (max 100000 samples) :  ")
    length=10000
    
    se=int(sec)-1
    start=se*10000
    end=(se+1)*10000
    print(start,end)
    
    test = data[start:int(end)]

    '''
    example 
    df1 = pd.read_csv('D:/SELECTED_RECORDS/11-38-14/generic_extended_ann.csv') 

    '''
    #print("Example : D:/SELECTED_RECORDS/11-38-14/generic_extended_ann.csv")
    #path2=input("Path to edf file annotation : " )


    
    path2="D:/SELECTED_RECORDS/11-38-14/generic_extended_ann.csv"
    df1 = pd.read_csv(path2) 
    rpeaks=df1['Msec']
    ann=df1['Type']

    ti=np.linspace(0,10000,10000)
    '''
    Visualization
    '''

    #set number of rpeaks
    s=500
    fig=go.Figure()
    fig.add_trace(go.Scatter( x=ti, y=test,mode='lines'))

#
#    #Position for annotatiom 
#   y1=[1*0.003]*500
#    fig.add_trace(go.Scatter(x=tir[0:s],y=y1,text=ann[0:s],mode='lines+markers+text',textposition="top center",line=dict(color='firebrick',width=2,dash='dashdot')))



    fig.update_layout(xaxis_range=[ti[0],ti[3000]])
    fig.update_yaxes(fixedrange=True)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

if __name__ == "__main__":
    app.run()





