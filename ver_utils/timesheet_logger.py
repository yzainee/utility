from atlassian import Jira
from pathlib import Path
import json
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta, MO, FR
from constants import JIRA_URL
from jira_utils import validate_timesheet_jira
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_time(data_json):
    """function to log the time"""
    
    todayDate = date.today()
    res = {}
    week_log = {}

    date_time = "dateT00:00:00.000+0000"
    if "user" in data_json and "token" in data_json:
        user = data_json["user"]
        key = data_json["token"]
        data_json["issues"] = []

        val_results = validate_timesheet_jira(data_json)
        if val_results["status"] == "fail":
            res["status"] = 400
            res["message"] = val_results["message"]
            return res
        else:
            logger.info("All jira issues validated. Logging to begin.")

        jira = Jira(url=JIRA_URL,username=user,token=key)
        timesheet_json = data_json["timesheet"]
        for data in timesheet_json:
            ticket=data
            time_data = timesheet_json[data]
            for log_date in time_data:
                hrs = time_data[log_date]
                if hrs == 0:
                    continue
                if isinstance(hrs, str):
                    hrs = float(hrs)
                date_val = datetime.strptime(log_date, "%Y-%m-%d")
                try:
                    if log_date in week_log:
                        week_log[log_date] = week_log[log_date] + hrs
                    else:
                        week_log[log_date] = hrs
                    logger.info(ticket + "->" + date_time.replace("date", log_date) + " :: " + str(hrs))
                    issue = jira.issue_worklog(ticket, date_time.replace("date", log_date), hrs*60*60 )
                except Exception as e:
                    logger.error(e)
                    res["message"] = str(e)
                    res["status"] = 500
                    return res
        res["message"] = "Your timesheet was logged successfully."
        res["logged_data"] = week_log
        res["status"] = 200
        return res
    else:
        logger.error("Username or Jira token missing.")
        res["message"] = "Username or Jira token missing."
        res["status"] = 400
        return res

def generate_timesheet(data_json):
    """function to generate the timesheet data for the week."""
    res = {
        "data" : {},
        "status": 200

    }
    todayDate = date.today()
    monday_date = todayDate + relativedelta(weekday=MO(-1))
    print(monday_date)
    issues = data_json["issues"]
    for issue in issues:
        res["data"][issue] = {}
        date_val = monday_date
        for counter in range(1,6):
            res["data"][issue][str(date_val)] = 0
            date_val = date_val + timedelta(days=1)
    return res
"""
if __name__ == "__main__":
    print("start")

    print("end")"""
