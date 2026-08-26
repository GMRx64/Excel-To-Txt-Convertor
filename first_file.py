from flask import Flask ,render_template,url_for,request,Response,redirect,send_file
import pandas as pd
import subprocess as sbp

app = Flask(__name__ ,template_folder='templates')

#routes

@app.route('/',methods =['GET','POST'])
def main():
    if request.method == 'GET':
        return render_template('Exc-Txt.html')

    elif request.method == 'POST':
        file = request.files['file'] 
        fileName = file.filename[:file.filename.find('.')]

        #Read dataframe and convert xlsx into string format
        df = pd.read_excel(file)
        df = df.drop(columns=[col for col in df.columns if 'Unnamed' in col])
        df = df.to_string(index=False,col_space=15)

        "Creates a text file and write the data into it"

        f = open(f'./text_files/{fileName}.txt','w')
        f.write(df)
        f.close()
        # download
        send_file_query = send_file(f"./text_files/{fileName}.txt", as_attachment=True,download_name=f"{fileName}.txt")
        send_file_res = send_file_query.status_code
        if send_file_res == 200 :
            return send_file_query
        else:
            raise FileExistsError('File Not Found') 

if __name__ == "__main__":
    app.run(host='0.0.0.0' , debug=True)