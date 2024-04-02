import flask
from flask import Flask, request, send_file
from flask.json import jsonify
import logging
from timesheet_logger import log_time, generate_timesheet
from jira_utils import create_subtask, create_story, clone_story
from responses import RESP_V1, RESP_V2, TIMESHEET, SUBTASK, STORY, CLONE, TIMESHEET_GEN
from confluence import perform_suspension, delete_local_files

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("""
    ********************************************
    **            Verifone Uility             **
    **                 0.1.0                  **
    ********************************************
    """)

@app.route('/')
def heartbeat():
    """Handle the REST API endpoint /."""
    return flask.jsonify({"message": "Service up and running. Use the GET api call /api/v1/info for more information."})

@app.route('/api/v1/info')
def info():
    """Handle the REST API endpoint /api/v1/info."""
    return flask.jsonify(RESP_V1)

@app.route('/api/v1/log_timesheet', methods=['GET'])
def log_timesheet_get():
    """Handle the GET REST API endpoint /api/v1/log_timesheet."""
    input_json = {"issues": ["<Epic#1>"]}
    res = generate_timesheet(input_json)
    logger.info(res["data"])
    TIMESHEET["timesheet"] = (res["data"])
    return flask.jsonify(TIMESHEET)

@app.route('/api/v1/log_timesheet', methods=['POST'])
def log_timesheet_post():
    """Handle the POST REST API endpoint /api/v1/log_timesheet."""
    input_json = request.get_json(force=True)
    #logger.info(input_json)
    res = {
        "instructions": "Use the GET api call /api/v1/log_timesheet for more information."
    }
    if "user" not in input_json:
        res["message"] = "ERROR.. The field user is mandatory."
        return res, 400
    if "token" not in input_json:
        res["message"] = "ERROR.. The field token is mandatory."
        return res, 400
    if "timesheet" not in input_json:
        res["message"] = "ERROR.. The field timesheet not found. No action taken."
        return res, 400

    logger.info(input_json["user"])
    logger.info(input_json["timesheet"])
    res = log_time(input_json)
    status = res["status"]
    del res["status"]
    return res, status

@app.route('/api/v1/generate_timesheet', methods=['GET'])
def generate_timesheet_get():
    """Handle the GET REST API endpoint /api/v1/generate_timesheet."""
    return flask.jsonify(TIMESHEET_GEN)

@app.route('/api/v1/generate_timesheet', methods=['POST'])
def generate_timesheet_post():
    """Handle the POST REST API endpoint /api/v1/generate_timesheet."""
    input_json = request.get_json(force=True)
    res = generate_timesheet(input_json)
    logger.info(res["data"])
    status = res["status"]
    del res["status"]
    return res, status

@app.route('/api/v1/create_subtasks', methods=['GET'])
def create_subtask_get():
    """Handle the GET REST API endpoint /api/v1/create_subtasks."""
    return flask.jsonify(SUBTASK)

@app.route('/api/v1/create_subtasks', methods=['POST'])
def create_subtask_post():
    """Handle the POST REST API endpoint /api/v1/create_subtasks."""
    input_json = request.get_json(force=True)
    #logger.info(input_json)
    res = {
        "instructions": "Use the GET api call /api/v1/create_subtasks for more information."
    }
    if "user" not in input_json:
        res["message"] = "ERROR.. The field user is mandatory."
        return res, 400
    if "token" not in input_json:
        res["message"] = "ERROR.. The field token is mandatory."
        return res, 400
    if "stories" not in input_json:
        res["message"] = "ERROR.. The field stories not found. No action taken."
        return res, 400

    logger.info(input_json["user"])
    logger.info(input_json["stories"])
    res = create_subtask(input_json)
    status = res["status"]
    del res["status"]
    return res, status

@app.route('/api/v1/create_story', methods=['GET'])
def create_story_get():
    """Handle the GET REST API endpoint /api/v1/create_story."""
    return flask.jsonify(STORY)

@app.route('/api/v1/create_story', methods=['POST'])
def create_story_post():
    """Handle the POST REST API endpoint /api/v1/create_story."""
    input_json = request.get_json(force=True)
    #logger.info(input_json)
    res = {
        "instructions": "Use the GET api call /api/v1/create_story for more information."
    }
    if "user" not in input_json:
        res["message"] = "ERROR.. The field user is mandatory."
        return res, 400
    if "token" not in input_json:
        res["message"] = "ERROR.. The field token is mandatory."
        return res, 400
    if "story" not in input_json:
        res["message"] = "ERROR.. The field story not found. No action taken."
        return res, 400
    story_json = input_json["story"]
    if "work_type" not in story_json:
        res["message"] = "ERROR.. The field work_type is mandatory."
        return res, 400
    if "program_category" not in story_json:
        res["message"] = "ERROR.. The field program_category is mandatory."
        return res, 400
    if "summary" not in story_json:
        res["message"] = "ERROR.. The field summary is mandatory."
        return res, 400

    logger.info(input_json["user"])
    logger.info(input_json["story"])
    res = create_story(input_json)
    status = res["status"]
    del res["status"]
    return res, status

@app.route('/api/v1/clone_story', methods=['GET'])
def clone_story_get():
    """Handle the GET REST API endpoint /api/v1/clone_story."""
    return flask.jsonify(CLONE)

@app.route('/api/v1/clone_story', methods=['POST'])
def clone_story_post():
    """Handle the POST REST API endpoint /api/v1/clone_story."""
    input_json = request.get_json(force=True)
    #logger.info(input_json)
    res = {
        "instructions": "Use the GET api call /api/v1/clone_story for more information."
    }
    if "user" not in input_json:
        res["message"] = "ERROR.. The field user is mandatory."
        return res, 400
    if "token" not in input_json:
        res["message"] = "ERROR.. The field token is mandatory."
        return res, 400
    if "stories" not in input_json:
        res["message"] = "ERROR.. The field stories not found. No action taken."
        return res, 400

    logger.info(input_json["user"])
    res = clone_story(input_json)
    status = res["status"]
    del res["status"]
    return res, status

@app.route('/api/v2/generate_suspension', methods=['POST'])
def generate_suspension_post():
    """Handle the POST REST API endpoint /api/v2/generate_suspension."""
    res = {}
    input_json = request.form
    logger.info(input_json)

    if "auth_token" not in input_json:
        res["message"] = "ERROR.. The field auth_token is mandatory."
        return res, 400
    else:
        auth_token = input_json["auth_token"]

    if "parent_page_id" not in input_json:
        res["message"] = "ERROR.. The field parent_page_id is mandatory."
        return res, 400
    else:
        parent_page_id = input_json["parent_page_id"]

    if "username" not in input_json:
        res["message"] = "ERROR.. The field username is mandatory."
        return res, 400
    else:
        username = input_json["username"]

    if "jira_id" not in input_json:
        res["message"] = "ERROR.. The field jira_id is mandatory. Its the ticket number raised to perform these changes."
        return res, 400
    else:
        jira_id = input_json["jira_id"]

    if "use_cols" not in input_json:
        res["message"] = "ERROR.. The field use_cols is mandatory. Comma separated values which tells which columns to read from the xl. ex- 'CV,CW'"
        return res, 400
    else:
        use_cols = input_json["use_cols"]

    if 'suspension_list' in request.files:
        file = request.files['suspension_list']
        if file.filename != "":
            file.save("suspension_list.xlsx")
            file_link = perform_suspension(auth_token, parent_page_id, username, jira_id, use_cols)
            delete_local_files(jira_id)
            res["Confluence_page_link"] = file_link
            return res, 200 
        else:
            res["message"] = "ERROR.. File not found. Please attach the xl file under the name 'suspension_list'."
            return res, 400
    else:
        logger.info(request.files)
        res["message"] = "ERROR.. No input file found. Please attach the xl file under the name 'suspension_list'."
        return res, 400
    return {}


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)
    #app.run()