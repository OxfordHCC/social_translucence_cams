from subprocess import call
from flask import Flask, request, jsonify
from arlo_st import adapters
from arlo_st import controller
from arlo_st import libraryFs
from jsonschema import validate, ValidationError
from functools import wraps
import json

# TODO: log actions: view, delete

def validate_body(schema = None):
    def decorator(func):
        print('b')
        @wraps(func)
        def decorated(*args, **kwargs):
            print('c')
            try:
                print(request.get_json())
                validate(instance=request.get_json(), schema=schema)
                return func(*args, **kwargs)
            except ValidationError as e:
                return { "error": e.message }, 400
        return decorated
    return decorator

def create_app():
    app = Flask(__name__)

    adapters.setLogger(app.logger)
    #test route
    @app.route('/')
    def hello_world():
        return 'Hello, World!'
    
    @app.route('/library/')
    @app.route('/library')
    def get_library():
        library = controller.getLibrary()
        return jsonify(library)

    @app.route('/camera/')
    @app.route('/camera')
    def get_cameras():
        return jsonify(controller.getCameras())

    @app.route('/adapter/')
    @app.route('/adapter')
    def get_adapter():
        return jsonify(adapters.get())

    @app.route('/adapter-types/')
    @app.route('/adapter-types')
    def get_adapter_types():
        return jsonify(adapters.getTypes())
    

    # @validate_body(schema={
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
    def post_adapter():
        app.logger.debug("wtf")
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
            
            adapters.add(adapter_type, adapter_name, adapter_options)
            return { "error": None }, 200
        except ValidationError as e:
            app.logger.exception(e)
            return { "error": str(e)}, 400
        except adapters.UnknownAdapterTypeError as e:
            app.logger.exception(e)
            return { "error": str(e)}, 400
        except Exception as e:
            app.logger.exception(e)
            return { "error": str(e)}, 500


    #libraryFs.integrityCheck() #check fs integrity
    adapters.initAdapters()


    return app
    

