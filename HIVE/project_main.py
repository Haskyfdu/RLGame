
from flask import Flask
from HIVE.project_config import ProjectConfig
from HIVE.algorithms.main import blueprint_main


app = Flask(__name__, static_folder=ProjectConfig.Path['Static_Path'],
            template_folder=ProjectConfig.Path['Templates_Path'])
app.register_blueprint(blueprint_main)


if __name__ == '__main__':

    app.run(host='127.0.0.1', port=9001, debug=False)
