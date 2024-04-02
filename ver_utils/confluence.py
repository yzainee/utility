import json
from atlassian import Confluence
import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_confluence_page(auth_token, parent_page_id, username, jira_id, count):

    confluence = Confluence(
        url='https://confluence.verifone.com',
        username=username,
        token=auth_token,
        cloud=True)

    body = """<html>
    <body> 
    <h1> Dependencies </h1>
    </body></html>"""
    r = confluence.update_or_create(title="Disable terminals in TSS (already deleted in BASE24)", body=body, parent_id=451870322, full_width=False, representation='storage')
    z1 = confluence.attach_file(r"" + jira_id + "-v1.0.sql", name= jira_id + "-Update-SQL.sql", content_type=None, page_id=r['id'], title=None, space=None, comment=None)
    if ("results" in z1):
        link1 = z1['results'][0]['_links']['download']
    else:
        link1 = z1['_links']['download']
    link1 = link1.replace("&", "&amp;")

    z2 = confluence.attach_file(r"" + jira_id + "-COPYTABLE-v1.0.sql", name= jira_id + "-CopyTable-SQL.sql", content_type=None, page_id=r['id'], title=None, space=None, comment=None)
    if ("results" in z2):
        link2 = z2['results'][0]['_links']['download']
    else:
        link2 = z2['_links']['download']
    link2 = link2.replace("&", "&amp;")

    z3 = confluence.attach_file(r"" + jira_id + "-BACKOUT-v1.0.sql", name= jira_id + "-Rollback-SQL.sql", content_type=None, page_id=r['id'], title=None, space=None, comment=None)
    if ("results" in z3):
        link3 = z3['results'][0]['_links']['download']
    else:
        link3 = z3['_links']['download']
    link3 = link3.replace("&", "&amp;")

    body = """<html>
    <body>

    <h1> Dependencies </h1> 
    <p> This implementation does not require any outage to services. This is RTDB(1/2) Postgres change only and will not require any restarts of TSS or TSS-SE. 
    <br/>The JIRA for this script is <span class='jira-issue' data-jira-key='$JIRA_ID'><a href='https://jira.verifone.com/browse/$JIRA_ID' class="jira-issue-key">PAG-25381</a></span>
    </p>
    <br/>
    <h1>1. Prerequisites</h1>
    <p>Download the following scripts</p>
    <br/><strong><a href='$LINK1'>Update-SQL</a>
    <br/><a href='$LINK2'>CopyTable-SQL</a>
    <br/><a href='$LINK3'>Rollback-SQL</a>
    </strong>
    <br/>
    <h1>2. Install Instructions (Applicable on RTDB1 and RTDB2)</h1>
    <h3>2.1 Log on to the rtdb(n), switch to user postgres and load the TSS database</h3>
    <div style="background-color:black;color:white;">
        <p>
            sudo su - postgres
            <br/>/usr/pgsql-9.4/bin/psql tss
        </p>
    </div>

    <h3>2.2. Count number of records in the terminalinformation table. Please note the count for future use. (PRE-COUNT)</h3>
    <div style="background-color:black;color:white;">
        <p>
            select currentsettlementdate,count(*) from terminalinformation where currentsettlementdate='2099-01-01' group by currentsettlementdate order by currentsettlementdate;
        </p>
    </div>

    <h3>2.3. Copy the terminalinformation table contents to a new table. This table will provide a record of the affected terminals in case a rollback is required</h3>
    <div>
        <ul>
            <li>Run CopyTable-SQL</li>
            <li>Verify: Table terminalinformation_$JIRA_ID should exist in the TSS database with $COUNT records</li>
        </ul>
    </div>

    <h3>2.4. Update the terminal information table</h3>
    <div>
        <ul>
            <li>Run Update-SQL</li>
        </ul>
    </div>

    <h3>2.5. Count number of records in the terminalinformation table. Please note the count for future use. (POST-COUNT)</h3>
    <div style="background-color:black;color:white;">
        <p>
            select currentsettlementdate,count(*) from terminalinformation where currentsettlementdate='2099-01-01' group by currentsettlementdate order by currentsettlementdate;
        </p>
    </div>

    <h1>3. PIV (Verify the row counts)</h1>
    <p>
        Verify POST_COUNT is less than or equal to (PRE-COUNT + $COUNT) i.e 
        <br/>PRE-COUNT &lt;= POST-COUNT &lt;= (PRE-COUNT + $COUNT)
        <br/>Note: We don't check the exact count as while the file is being generated by WBC and today some terminals might have already been updated or modified, resulting in a slight mismatch.
    </p>

    <h1>4. Rollback Steps (POST-COUNT)</h1>
    <div>
        <ul>
            <li>Run Rollback-SQL</li>
        </ul>
        <ul>
            <li>Run the below query to verify the count is equal to the PRE-COUNT</li>
            <div style="background-color:black;color:white;">
                <p>
                    select currentsettlementdate,count(*) from terminalinformation where currentsettlementdate='2099-01-01' group by currentsettlementdate order by currentsettlementdate;
                </p>
            </div>
        </ul>
    </div>

    </body> 
    </html>"""
    body = body.replace("$JIRA_ID", jira_id).replace("$COUNT", str(count)).replace("$LINK1", link1).replace("$LINK2", link2).replace("$LINK3", link3)
    r = confluence.update_or_create(title="Disable terminals in TSS (already deleted in BASE24)", body=body, parent_id=451870322, full_width=False, representation='storage')
    return ("https://confluence.verifone.com/pages/viewpage.action?pageId=" + r['id'])

def generate_sql_files(file_loc, jira_id, usecols):
    data = pd.read_excel(file_loc, na_values=['NA'], usecols=usecols)
    columns_len = len(data.columns)
    all_ids = []
    for i in range(0,columns_len):
        data[data.columns[i]].fillna("NA", inplace=True)
        for d in data[data.columns[i]]:
            if d != "NA":
                all_ids.append(int(d))
    count = len(all_ids)

    comment1 = "-- " + jira_id + " - test\n"
    comment2 = "-- Number of TIDs: " + str(count) + "\n"

    rollback_query = """update terminalinformation \nset acquirer = terminalinformation_$JIRA_ID.acquirer, currentsettlementdate = terminalinformation_$JIRA_ID.currentsettlementdate, nextscheduledcutoverdatetime = terminalinformation_$JIRA_ID.nextscheduledcutoverdatetime \nfrom terminalinformation_$JIRA_ID \nwhere terminalinformation.infoid = terminalinformation_$JIRA_ID.infoid;"""
    rollback_query = rollback_query.replace("$JIRA_ID", jira_id)

    copytable_query = """CREATE TABLE terminalinformation_$JIRA_ID AS SELECT * FROM terminalinformation where acquirer = 'Westpac' and terminalid in ($IDS)"""
    copytable_query = copytable_query.replace("$JIRA_ID", jira_id)
    id_str = ",\n".join([str(item) for item in all_ids])
    copytable_query = copytable_query.replace("$IDS", id_str)

    update_query = """update terminalinformation set acquirer = 'Westpac_error', currentsettlementdate = '2099-01-01', nextscheduledcutoverdatetime = '2099-01-01 10:30:00+00' where acquirer = 'Westpac' and terminalid = '$ID';\n"""


    with open(r"" + jira_id + "-BACKOUT-v1.0.sql", 'w') as filehandle:
        filehandle.write(comment1)
        filehandle.write(comment2)
        filehandle.write(rollback_query)

    with open(r"" + jira_id + "-COPYTABLE-v1.0.sql", 'w') as filehandle:
        filehandle.write(comment1)
        filehandle.write(comment2)
        filehandle.write(copytable_query)

    with open(r"" + jira_id + "-v1.0.sql", 'w') as filehandle:
        filehandle.write(comment1)
        filehandle.write(comment2)
        filehandle.write("BEGIN;\n")
        for id in all_ids:
            filehandle.write(update_query.replace("$ID", str(id)))
        filehandle.write("COMMIT;")
    return count


def perform_suspension(auth_token, parent_page_id, username, jira_id, usecols):
    logger.info("Process to generate sql files started.")
    count = generate_sql_files("suspension_list.xlsx", jira_id, usecols)
    logger.info("Total number of TIDs affected: " + str(count))
    logger.info("Generating confluence page link.")
    page_link = generate_confluence_page(auth_token, parent_page_id, username, jira_id, count)
    return page_link

def delete_local_files(jira_id):
    logger.info("Processing done. Deleting all local files.")
    os.remove("suspension_list.xlsx")
    os.remove(r"" + jira_id + "-BACKOUT-v1.0.sql")
    os.remove(r"" + jira_id + "-COPYTABLE-v1.0.sql")
    os.remove(r"" + jira_id + "-v1.0.sql")
