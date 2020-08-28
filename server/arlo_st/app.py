from functools import wraps
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from jsonschema import validate, ValidationError
from arlo_st import adapters, controller, library

# TODO: log actions: view, delete

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

def create_app():
    app = Flask(__name__)
    CORS(app)
    adapters.set_logger(app.logger)

    @app.errorhandler(library.RecordingNotFound)
    def handle_recordingNotFound(e):
        return {"error": str(e)}, 404

    @app.route('/library/')
    @app.route('/library')
    def get_library():
        library_res = controller.getLibrary()
        return jsonify(library_res)

    #get video from local library
    @app.route('/library/<video_id>')
    def get_library_video(video_id):
        file_generator = library.get_recording(video_id)
        return Response(file_generator, mimetype="video/mp4")

    #start video sync
    @app.route('/library/<video_id>/sync', methods=['POST'])
    def sync_library_video(video_id):
        res = library.sync_library(video_id)
        return jsonify(res)
        
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
        return jsonify(adapters.get_types())

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
            return {"error": None}, 200
        except ValidationError as e:
            app.logger.exception(e)
            return {"error": str(e)}, 400
        except adapters.UnknownAdapterTypeError as e:
            app.logger.exception(e)
            return {"error": str(e)}, 400
        except Exception as e:
            app.logger.exception(e)
            return {"error": str(e)}, 500


    #libraryFs.integrityCheck() #check fs integrity
    adapters.init_adapters()

    return app

