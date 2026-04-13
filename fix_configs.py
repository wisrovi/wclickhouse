import os
import re

db_config_pattern = re.compile(r'db_config = \{.*?\}', re.DOTALL)
new_db_config = '''db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }'''

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()
    
    new_content = db_config_pattern.sub(new_db_config, content)
    
    with open(path, 'w') as f:
        f.write(new_content)

for root, dirs, files in os.walk('wclickhouse/examples'):
    for file in files:
        if file.endswith('.py'):
            fix_file(os.path.join(root, file))
