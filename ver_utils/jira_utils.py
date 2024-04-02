from atlassian import Jira
import json
from constants import JIRA_URL
from constants import PROJECT_KEY
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_timesheet_jira(data_json):
  """function to validate jira ids."""
  res = {
    "status": "pass",
    "message": {}
  }
  user = data_json["user"]
  key = data_json["token"]
  jira = Jira(url=JIRA_URL,username=user,token=key)

  for epic in data_json["timesheet"]:
    try:
      if jira.get_issue_status(epic) == "Closed":
        res["status"] = "fail"
        res["message"][epic] = "Issue " + epic + " is already Closed. Cannot log time for it."
        logger.info("Issue " + epic + " is already Closed. Cannot log time for it.")
    except Exception as e:
          logger.error(e)
          res["status"] = "fail"
          res["message"][epic] = str(e)
  return res


def create_subtask(data_json):
    """function to create subtasks"""

    res = {"status": 200}

    user = data_json["user"]
    key = data_json["token"]
    if "project_key" in data_json:
      project = data_json["project_key"]
    else:
      project = PROJECT_KEY

    jira = Jira(url=JIRA_URL,username=user,token=key)
    for story in data_json["stories"]:
      try:
        tasks = json.loads(json.dumps(jira.issue_field_value(story, "subtasks")))
        summary_list=[]
        res[story] = {}
        for task in tasks:    
          summary_list.append(task["fields"]["summary"])
        tasks_to_create = data_json["stories"][story]
        for task_to_create in tasks_to_create:
          if task_to_create not in summary_list:
            new_task = jira.issue_create({
                                          "project": {
                                            "key": project
                                          },
                                          "summary": task_to_create,
                                          "description": "Created via python jira utility.",
                                          "issuetype": {
                                            "name": "Small Task Subtask"
                                          },
                                          "parent": {
                                            "key": story
                                          }
                                        })
            logger.info("Task " + new_task["key"] + " added successfully")
            res[story][task_to_create] = "Task " + new_task["key"] + " added successfully"
          else:
            res[story][task_to_create] = "Task already present."
      except Exception as e:
        logger.error(e)
        res[story] = str(e)

    return res

def create_story(data_json):
    """function to create story"""
    user = data_json["user"]
    key = data_json["token"]
    
    jira = Jira(url=JIRA_URL,username=user,token=key)

    res = {
      "message": "",
      "status": 200
    }

    story_data = data_json["story"]
    
    story_json = {
      "issuetype": {
                    "name": "Story"
                  },
      "summary": story_data["summary"],
      "customfield_15301": {
                            "value": story_data["work_type"]
                          },
      "customfield_15300": {
                            "value": story_data["program_category"]
                          }
    }
    story_json["project"] = {}
    if "project_key" in story_data:
      story_json["project"]["key"] = story_data["project_key"]
    else:
      story_json["project"]["key"] = PROJECT_KEY

    if "description" in story_data:
      story_json["description"] = story_data["description"]

    if "assignee" in story_data:
      story_json["assignee"] = {}
      story_json["assignee"]["name"] = story_data["assignee"]

    if "epic" in story_data:
      story_json["customfield_11506"] = story_data["epic"]

    if "labels" in story_data:
      if type(story_data["labels"] == list):
        story_json["labels"] = story_data["labels"]
      else:
        story_json["labels"] = []
        story_json["labels"].append(story_data["labels"])

    logger.info(story_json)
    try:
      new_story = jira.issue_create(story_json)
    except Exception as e:
        logger.error(e)
        res["message"] = str(e)
        res["status"] = 500
        return(res)
    res["message"] = "The story " + new_story["key"] + " was successfully created."
    return(res)

def get_story_details(jira, issue):
    """function to get story details"""

    fields = [ "project:key", "summary", "customfield_15301:value", "customfield_15300:value" ]
    mapping = {
      "project": "project_key",
      "summary": "summary",
      "customfield_15300": "program_category",
      "customfield_15301": "work_type"
    }

    story_json = {
      "description": "This is an auto generated story via utils script.",
      "program_category": "",
      "work_type": "",
      "project_key": "",
      "summary": ""
    }

    for f in fields:
      if (":" in f):
        f_pre = f.split(":")[0]
        f_post = f.split(":")[1]
        details = jira.issue_field_value(issue, f_pre)
        value = details[f_post]
        story_json[mapping[f_pre]] = value
      else:
        value = jira.issue_field_value(issue, f)
        story_json[mapping[f]] = value
    return(story_json)


def clone_story(data_json):
    """function to clone the stories"""

    user = data_json["user"]
    key = data_json["token"]
    story_data = {
      "user": user,
      "token": key
    }

    res = {
      "status": 200
    }
    
    jira = Jira(url=JIRA_URL,username=user,token=key)
    stories = data_json["stories"]
    for story in stories:
      story_details = get_story_details(jira, story)
      story_data["story"] = story_details
      logger.info("Creating story with the following data -->")
      logger.info(story_details)
      resp = create_story(story_data)
      res[story] = resp["message"]

    return(res)


#if __name__ == "__main__":
  