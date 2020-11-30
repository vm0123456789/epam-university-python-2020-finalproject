from app import app

# ========= SUPPLEMENTARY =========

@app.context_processor
def global_variables():
    return dict(COMPANY_NAME="Dunder Mifflin Paper Company Inc. Scranton Branch departments")





# ========= VIEWS ==============

@app.route('/')
@app.route('/departments')
def departments():
    return

