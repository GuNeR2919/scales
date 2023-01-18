from app import create_app, db
from app.models import Weight

app = create_app()

print('scales.py')
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Weight': Weight}
