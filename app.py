from flask import Flask
from flask import render_template,request
from mymodule.backt import backt

import base64
from io import BytesIO
from matplotlib.figure import Figure



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movie')
def movie():
    return render_template(
        'movie.html'
    )

@app.route('/demotrade')
def demotrade():
    x=9
    y=8
    name="sata"

    return render_template(
        'demotrade.html',x=x,y=y,name=name
    )


@app.route('/demotrade/cal',methods=['GET','POST'])
def cal():
    print('POSTデータ受け取ったので処理します')
    data1 = int(request.form['data1'])
    data2 = float(request.form['data2'])
    data3 = int(request.form['data3'])
    data4 = int(request.form['data4'])

    result_list=[]
    Symbol_list=["^N225","DIS","NVDA","RBLX","PLUG","TTD","BABA","ILMN","ORGN","NVEI","C6L.SI"]
    for symbol in Symbol_list:
        result_list.append(backt(data1,data2,symbol,data3,data4))
    
    
    return render_template(
        'cal.html',data1=data1,data2=data2,result_list=result_list,data3=data3,data4=data4
    )
    

@app.route('/community')
def community():
    return render_template(
        'community.html'
    )



@app.route('/hello')
def hello():
    return 'Hello, gorld!'

if __name__ == '__main__':
    app.run(debug=True)