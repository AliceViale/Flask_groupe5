from application import create_app
from flask import render_template

app = create_app()

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

# et on lance l'appli !
if __name__ == '__main__':
    app.run(debug=True)