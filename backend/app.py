from flask import Flask, send_from_directory
import os
from extensions import db, jwt

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://meal_user:meal_password@localhost:3306/meal_management'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your-secret-key-here'
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'xlsx', 'xls'}
    
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    db.init_app(app)
    jwt.init_app(app)
    
    from extensions import cors
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    
    from routes import api
    app.register_blueprint(api, url_prefix='/api')
    
    @app.route('/')
    def serve_index():
        return send_from_directory('../frontend', 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory('../frontend', path)
    
    return app

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    print("启动Flask应用程序...")
    print("监听地址: 0.0.0.0:5000")
    print("API基础路径: http://localhost:5000/api")
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)