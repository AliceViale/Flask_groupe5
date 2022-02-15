from application import create_app
from flask import render_template

app = create_app()

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('index.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)