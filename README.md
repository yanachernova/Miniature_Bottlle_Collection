# Miniature_Bottlle_Collection
Project for share and exchange a Miniature bottles around the world

Installation:
git clone https://github.com/yanachernova/Miniature_Bottlle_Collection.git
pip install pipenv
pipenv shell

Flask Configuration:
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JWT_SECRET_KEY'] = 'super-secrets'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''

Configuring From Files
Example Usage
app = Flask(__name__)
app.url_map.strict_slashes = False

Run Flask
python app.py runserver

Reference
Flask
Flask Extension
Flask-SQLalchemy
