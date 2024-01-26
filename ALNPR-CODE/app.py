from flask import Flask, render_template, request
import os
from deeplearning import OCR
import pandas as pd

#webserver gateway interface
app = Flask(__name__)

BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH,'static/upload/')
predd=0

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        upload_file = request.files['image_name']
        filename = upload_file.filename
        path_save = os.path.join(UPLOAD_PATH,filename)
        upload_file.save(path_save)
        text = OCR(path_save,filename)
        global predd
        predd=text
        print("The predd value is",predd)
        return render_template('index.html',upload=True, upload_image=filename, text=predd)
    return render_template('index.html',upload=False)

print("The predd value is",predd)

def read_data():
    return pd.read_excel('database.xlsx')

@app.route('/num_p')
def num_p():
    global predd
    data_0 = read_data()
    data = pd.DataFrame(data_0)

    # plate_to_search = 'MH20CS1941'  # Make sure to enclose the value in quotes


    df = data[data['number_plate'] == predd]
    # print(df)
    print(predd)

    post = df.to_dict('records')

    print(post)

    for record in post:
        print(record['reg_name'])
    return render_template('num_p.html',post=post)


if __name__=="__main__":
    app.run(debug=True)
