from lxml import objectify
import zipfile

import pandas as pd

def extract(collection, fields):
    return pd.DataFrame([dict(x.attrib) for x in collection],
                        columns=fields)

path = 'JIRA-backup.zip'
zf = zipfile.ZipFile(path, 'r')

entities = zf.open('entities.xml')

parsed = objectify.parse(entities)

# IssueTypes
issue_types = extract(parsed.findall('IssueType'), ['id', 'name'])

# Issues
fields = ['number', 'key', 'reporter', 'assignee', 'status', 'created',
          'type']
issues = extract(parsed.findall('Issue'), fields)

# Replace issue id with issue name
id_to_name = issue_types.set_index('id')['name']
issues['type'] = issues.type.map(id_to_name)
