#!/usr/bin/env python
import webbrowser
import os
import json
import pygame
from jira import JIRA
from jira.resources import Issue
import time
from datetime import datetime, timedelta
from plyer import notification

# Load the JSON configuration file
config_path = os.path.expanduser('~/.jira-task-subscriber/config.json')
with open(config_path, 'r') as file:
    config = json.load(file)

# Interval for checking new tasks
interval = 60
# Dictionary to store the last checked time for each instance
last_checked_per_instance = {}

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
app_icon = script_dir + '/danger.png'

# Initialize last_checked time for each JIRA instance
for instance in config["instances"]:
    server = instance["server"]
    last_checked_per_instance[server] = None


def notify(title: str, message: str):
    """Show a desktop notification."""
    notification.notify(
        title=title,
        message=message,
        app_name="JIRA Notifier",
        timeout=0,
        hints={'sound': 'message-new-instant'}
    )


def trigger_actions(server: str, task: Issue):
    """Open the task in a web browser and show a notification with the task link."""
    url = "{}/browse/{}".format(server, task)
    webbrowser.open(url=url, new=1)
    notification.notify(
        title=task.key,
        message=url,
        app_name="JIRA Notifier",
        app_icon=app_icon,
        timeout=0,
    )
    pygame.init()
    sound = f'{script_dir}/pipe.wav'
    sonido_alerta = pygame.mixer.Sound(sound)
    sonido_alerta.play()
    while pygame.mixer.get_busy():
        pass
    pygame.quit()


# Main loop to check for new JIRA tasks
while True:
    for instance in config["instances"]:
        server = instance["server"]
        jira_options = {'server': server}
        jira_user = instance["user"]
        jira_token = instance["token"]
        jql_query = instance["jqlQuery"]
        last_checked = last_checked_per_instance[server]

        # Authenticate with JIRA
        try:
            jira = JIRA(options=jira_options, basic_auth=(jira_user, jira_token))
            user = jira.current_user()
        except Exception as e:
            print(f"Authentication error: {e}")

        # If no tasks checked before, get the most recent one
        if last_checked is None:
            task = jira.search_issues(jql_query, maxResults=1)[0]
            last_checked_per_instance[server] = task.fields.created
            trigger_actions(server=server, task=task)
            continue

        # Prepare to check for tasks created after the last checked time
        date_format = "%Y-%m-%dT%H:%M:%S"
        last_checked = datetime.strptime(last_checked[:-9], date_format)  # Ignoring timezone
        last_checked = last_checked + timedelta(minutes=1)

        # Search for new tasks
        tasks = jira.search_issues(f"created > '{last_checked.strftime('%Y/%m/%d %H:%M')}' AND " + jql_query)

        # Process new tasks
        while len(tasks) > 0:
            task = tasks.pop()
            trigger_actions(server=server, task=task)
            last_checked_per_instance[server] = task.fields.created

    # Wait for the next interval
    time.sleep(interval)
