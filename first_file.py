from flask import Flask ,render_template,url_for

app = Flask(__name__ ,template_folder='templates')

#routes

@app.route('/')
def main():
    return render_template('index.html' , webName = "Excel to text generator")


if __name__ == "__main__":
    app.run(host='0.0.0.0' , debug=True)