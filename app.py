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
from glob import glob

def read_data(path):

    data = np.load(glob(path+'*_data.npy')[0])

    return data


def read_meta(path,length):
    
    import json
    
    with open(glob(path+'*.json')[0],'r') as j:
        meta_data = json.loads(j.read())
        
    n = int(meta_data["File_Meta"]["sig_len"]/length)

    meta_data["Strips"] = n
    return meta_data




def gm(sec='1'):
    

    se=int(sec)-1
    start=se*10000
    end=(se+1)*10000
    print(start,end)
    
    test = data[start:int(end)]

    ti=np.linspace(0,10000,10000)
    '''
    Visualization
    '''

    fig=go.Figure()
    fig.add_trace(go.Scatter( x=ti, y=test,mode='lines'))


    fig.update_layout(xaxis_range=[ti[0],ti[3000]])
    fig.update_yaxes(fixedrange=True)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


    return graphJSON

    





if __name__ == '__main__':
    
    app = Flask(__name__)
    path = 'C:\\Users\\Lenovo\\new_epk_scratch\\10EDF42\\'

    data = read_data(path)
    meta = read_meta(path,10000)
    @app.route('/callback', methods=['POST', 'GET'])
    def cb():
        return gm(sec=request.args.get('data'))
    
    @app.route('/')
    def index():
        
        return render_template('chartsajax.html',  graphJSON=gm(), meta=meta)

    app.run(debug=True)

