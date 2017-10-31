from .client import Agent, SSHSALT
from lib.conf.config import settings

def run():
    if settings.MODE == 'AGENT':
        obj = Agent()
    else:
        obj = SSHSALT()
    obj.execute()

