from app import app, db
from app.models import Employee, Department


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Employee': Employee, 'Department': Department}