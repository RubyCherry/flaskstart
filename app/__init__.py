from flask import Flask
import os
from flask_debugtoolbar import DebugToolbarExtension
from flask import  session, request


# app = Flask(__name__, template_folder='bulma')
# app.debug=True

# app.config['SECRET_KEY'] = '123456789'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
# app.config['CORS_HEADERS'] = 'Content-Type'

# toolbar = DebugToolbarExtension(app)


# from . import db
# from app import routes
# from app import special
def create_app(test_config=None):
    print('create_APP')
    app = Flask(__name__, 
                instance_relative_config=True, 
                template_folder='bulma')
    
    app.config.from_mapping(
        SECRET_KEY='123456789',
        DATABASE=os.path.join(app.instance_path, 'database')
    )
    
    
    print("DB? ",os.path.join(app.instance_path, 'database'))
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    toolbar = DebugToolbarExtension(app)
    
    from app import db
    # db.init_db(app)
    
    
    from . import routes,links
    from app.rts  import lnk
    from app.general import gen_routes
    
    from app.icons import icons
        
    app.register_blueprint(gen_routes.bp)
    app.register_blueprint(routes.bp)
    app.register_blueprint(links.bp)
    
    app.register_blueprint(lnk.bp)
    
    app.register_blueprint(icons.icons_bp)
    
    # print(app.iter_blueprints)
    # b= app.iter_blueprints()
    # for x in b:
    #     print(x,x.template_folder)
    #     print(x.static_folder)
    
    db.init_db(app)
    
    
    @app.route('/hello')
    def hello():
        return '<body>Hello, World!</body>'
    
    
    return app