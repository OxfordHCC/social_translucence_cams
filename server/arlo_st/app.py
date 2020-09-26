from functools import wraps
from flask import (
    Flask,
    request,
    jsonify,
    Response
)
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity
)
from flask_cors import CORS
from jsonschema import validate, ValidationError
from arlo_st import (
    adapters,
    controller,
    library,
    issues,
    translogs,
    users
)
from arlo_st.env import JWT_SECRET_KEY


# TODO: log actions: view, delete
# TODO: normalize flask responses to { err, data } json objects
# TODO: break-up zoneminder classes into separate modules

def validate_body(schema=None):
    def decorator(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            try:
                print(request.get_json())
                validate(instance=request.get_json(), schema=schema)
                return func(*args, **kwargs)
            except ValidationError as e:
                return {"error": e.message}, 400
        return decorated
    return decorator

def no_res_no_error():
    return { "error": None }, 200

def translog(event_type=None):
    def decorator(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            user = get_jwt_identity()
            translogs.create(user, event_type)
            return func(*args, **kwargs)
        return decorated
    return decorator

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    jwt = JWTManager(app)

    @app.errorhandler(library.RecordingNotFound)
    def handle_recordingNotFound(e):
        return {"error": str(e)}, 404

    @app.route('/login', methods=['POST'])
    def login():
        if not request.is_json:
            return jsonify({"err": "Missing JSON in request"}), 400

        username = request.json.get('username', None)
        if not username:
            return jsonify({"err": "Missing username parameter"}), 400

        password = request.json.get('password', None)
        if not password:
            return jsonify({"err": "Missing password parameter"}), 400

        try:
            user = users.get(username)
            users.raise_authenticate(user, password)
        except(users.IncorrectPassword, users.UserNotFound):
            return jsonify({"err": "Invalid credentials"}), 401
        
        # Identity can be any data that is json serializable
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    @app.route('/register', methods=['POST'])
    def register_user():
        if not request.is_json:
            return jsonify({"err": "Missing JSON in request"}), 400

        username = request.json.get('username', None)
        if not username:
            return jsonify({"err": "Missing username parameter"}), 400

        password = request.json.get('password', None)
        if not password:
            return jsonify({"err": "Missing password parameter"}), 400

        try:
            new_user = users.register(username, password)
        except users.UserEExist:
            return jsonify({"err": "User already exists"})
            
        access_token = create_access_token(identity=new_user.id)
        return jsonify(access_token=access_token), 200

    @app.route('/library', strict_slashes=False)
    @jwt_required
    @translog("test")    
    def get_library():
        library_res = library.get_all()
        return jsonify(data=library_res)

    #stream video from local library
    @app.route('/library/<video_id>')
    @jwt_required
    def get_library_video(video_id):
        file_generator = library.read_recording(video_id)
        return Response(file_generator, mimetype="video/mp4")

    #start video sync
    @app.route('/library/<video_id>/sync', methods=['POST'])
    @jwt_required
    def sync_library_video(video_id):
        library.sync_recording(video_id)
        return no_res_no_error()
        
    @app.route('/camera/')
    @app.route('/camera')
    @jwt_required
    def get_cameras():
        return jsonify(data=controller.getCameras())

    @app.route('/camera/<camera_id>/stream_url')
    @jwt_required
    def get_camera_stream_url(camera_id):
        return controller.get_camera_stream(camera_id)

    @app.route('/translog')
    @jwt_required
    def get_translogs():
        return jsonify(data=translogs.get())

    @app.route('/issue')
    @app.route('/issue/')
    @jwt_required
    def get_issue():
        return jsonify(data=issues.get())

    @app.route('/adapter/')
    @app.route('/adapter')
    @jwt_required
    def get_adapter():
        return jsonify(data=adapters.get_registered())

    @app.route('/adapter-types/')
    @app.route('/adapter-types')
    @jwt_required
    def get_adapter_types():
        return jsonify(data=adapters.get_types())

    #@validate_body(schema={
    #     "type": "object",
    #     "properties":{
    #         "type":{
    #             "type":"string"
    #             },
    #         "name":{
    #             "type": "string"
    #             },
    #         "options":{
    #             "type": "object"
    #             }
    #         }
    #})
    @app.route('/adapter', methods=['POST'])
    @jwt_required
    def post_adapter():
        try:
            json_body = request.get_json()
            print('body is ')
            print(json_body)
            validate(instance=json_body, schema={
                "type": "object",
                "properties":{
                    "adapter_type":{
                        "type": "string"
                    },
                    "name":{
                        "type": "string"
                    },
                    "options":{
                        "type": "object"
                    }
                },
                "required":["name", "adapter_type"]
            })
            adapter_type = json_body['adapter_type']
            adapter_name = json_body['name']
            adapter_options = json_body['options']

            adapters.register(adapter_type, adapter_name, adapter_options)
            return no_res_no_error()
        except ValidationError as e:
            app.logger.exception(e)
            return {"error": str(e)}, 400
        except adapters.UnknownAdapterTypeError as e:
            app.logger.exception(e)
            return {"error": str(e)}, 400
        except adapters.MalformedAdapterOptions as e:
            app.logger.exception(e)
            return {"error": str(e)}, 400
        except Exception as e:
            app.logger.exception(e)
            return {"error": str(e)}, 500

    #libraryFs.integrityCheck() #check fs integrity
    adapters.init_adapters()
    adapters.sync()

    return app

