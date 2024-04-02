RESP_V1 = {
    "instructions": "Make a GET API call for the sample payload. Make a POST call with the correct payload for action.",
    "/api/v1/generate_timesheet": "API to generate timesheets data for the week.",
    "/api/v1/log_timesheet": "API to log weekly timesheets.",
    "/api/v1/create_subtasks": "API to create Jira subtasks.",
    "/api/v1/create_story": "API to create Jira story.",
    "/api/v1/clone_story": "API to clone Jira stories."
}

RESP_V2 = {
    "instructions": "Make a GET API call for a specific operation to get more details about the same.",
    "/api/v2/project_details": "API to add project details for a team member.",
    "/api/v1/member_details": "API to get the project details for a team member.",
    "/api/v1/import_to_xl": "API to create xl sheet with the project details."
}

TIMESHEET_GEN = {
    "issues": ["<Epic#1>", "GBLTSSA-325", "GBLTSSA-327"]
}

TIMESHEET = {
            "user": "your_jira_name@verifone.com",
            "token": "your_jira_token",
            "timesheet":
            {
                "<Epic#1>": {"yyyy-mm-dd":"hours", "yyyy-mm-dd":"hours"},
                "<Epic#2>": {"yyyy-mm-dd":"hours"},
                "GBLTSSA-325" : {"2023-03-10":1.5, "2023-03-11":2}
            }
        }

SUBTASK = {
            "user": "your_jira_name@verifone.com",
            "token": "your_jira_token",
            "project_key": "project key. Default is PAG",
            "stories": {
                "<Story#1>": ["subtask#1", "subtask#2", "subtask#3"],
                "<Story#2>": ["subtask#1", "subtask#2"],
                "PAG-2222" : ["Development", "Code Review", "Manual Test", "Confluence Update"]
            }
        }

STORY = {
            "user": "your_jira_name@verifone.com",
            "token": "your_jira_token",
            "story": {
                "project_key": "project key. Default is PAG",
                "work_type": "(Mandatory) Ex- NPI - CAPEX",
                "program_category": "(Mandatory) Ex- Greenbox Integration",
                "summary": "(Mandatory) Story summary",
                "assignee": "Jira id for the assignee Ex - abcdp1",
                "epic": "epic number Ex - SGC-212121",
                "description": "Short description of the story. Details can be added later",
                "labels": ["label1", "label2"]
            }
}

CLONE = {
            "user": "your_jira_name@verifone.com",
            "token": "your_jira_token",
            "stories": ["PAG-22312", "<story to be cloned>"]
}