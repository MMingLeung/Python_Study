from conf import settings
import json

def load_db():
    '读取数据库'
    with open(settings.db_BASE_DIR, 'r') as file:
        data = json.loads(file.read())
        return data

