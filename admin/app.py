# app.py
from src.web import create_app
from src.core import db
#from flask_migrate import Migrate

app = create_app()  


#migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True)
