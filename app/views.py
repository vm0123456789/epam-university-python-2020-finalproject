from app import app


@app.route('/')
@app.route('/departments')
def departments():
    return 'departments app'

