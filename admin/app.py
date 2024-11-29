from src.web import create_app
from src.core.database import db

app = create_app()  

if __name__ == "__main__":
    app.run(debug=True)
