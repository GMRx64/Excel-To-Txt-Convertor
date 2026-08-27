from flask import Flask ,render_template,url_for,request,Response,redirect,send_file,flash
from flask_sqlalchemy import SQLAlchemy

import pandas as pd

app = Flask(__name__ ,template_folder='templates')
app.secret_key = 'gmrx64'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

#create a db table / model for database

class UserLogin(db.Model):
    _id = db.Column('id',db.Integer,primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(50))
    cnfrm_pass = db.Column(db.String(50))

    def __repr__(self):
        return f'{self.email} : {self.password}'

#routes

@app.route('/',methods = ['GET','POST'])
def authentication():
    if request.method == 'GET':
        return render_template('auth.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user_detail = db.session.query(UserLogin.email, UserLogin.password).all()
        print(user_detail)
    for i in range(len(user_detail)):
        user_email = user_detail[i][0]
        user_pass  = user_detail[i][1]
        if(user_email == email and user_pass == password):
            return redirect(url_for('main'))
        elif(user_email != email and user_pass == password):    
            flash('Invalid username !','email_err') 
            return redirect(url_for('authentication'))
        elif(user_email == email and user_pass != password):    
            flash('Invalid Password !','pass_err') 
            return redirect(url_for('authentication'))
    flash('Signup to continue!!!' , 'signup_err')    
    return redirect(url_for('authentication'))
                            
        
@app.route('/signup',methods = ['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cnfrm_password = request.form['cnfrm_password']

        #Check for existing username in the database and validate
        
        user_detail = db.session.query(UserLogin.username, UserLogin.email ,UserLogin.password).all()
        for i in range(len(user_detail)):
            user_userName = user_detail[i][0]
            user_email  = user_detail[i][1]
            if(user_userName == username or user_email == email):
                if(password!= cnfrm_password):
                    flash('Pasword do not match with confirm password!!','pass_error')
                    flash('User already Exist!!','user_email_error')
                    return redirect(url_for('signup'))
                flash('User already Exist!!','user_email_error')
                return redirect(url_for('signup'))
            elif(user_userName != username and user_email != email ):
                if(password == cnfrm_password):
                    user = UserLogin(username = username,email = email, password = password , cnfrm_pass = cnfrm_password)
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for('authentication'))
                elif(password!= cnfrm_password):
                    flash('Pasword do not match with confirm password!!','error')
                    return redirect(url_for('signup'))
        if( UserLogin.query.first() is None):
            if(password == cnfrm_password):
                user = UserLogin(username = username,email = email, password = password , cnfrm_pass = cnfrm_password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('authentication'))
            elif(password!= cnfrm_password):
                flash('Pasword do not match with confirm password!!','error')
                return redirect(url_for('signup'))        
        return redirect(url_for('signup'))                    




@app.route('/Excel_to_csv',methods =['GET','POST'])
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

        # download file into the system
        send_file_query = send_file(f"./text_files/{fileName}.txt", as_attachment=True,download_name=f"{fileName}.txt")
        send_file_res = send_file_query.status_code
        if send_file_res == 200 :
            return send_file_query
        else:
            raise FileExistsError('File Not Found') 

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0' , debug=True)