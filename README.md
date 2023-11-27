# JIRA Task Subscriber

This Python script is designed to monitor multiple JIRA instances for new tasks based on provided JQL queries. When a
new task is identified, the script opens the task in a web browser and sends a desktop notification with the task's
link.

## Configuration

The script requires a JSON configuration file located at `~/.jira-task-subscriber/config.json`.

### Configuration File Format

The configuration file should contain the following details for each JIRA instance:

- `server`: The URL of the JIRA server.
- `user`: Username for JIRA login.
- `token`: API token for JIRA authentication.
- `jqlQuery`: JQL query to identify new tasks.

Example:

```json
{
  "instances": [
    {
      "server": "https://your-jira-instance.atlassian.net",
      "user": "your-email@example.com",
      "token": "your-api-token",
      "jqlQuery": "project = YOURPROJECT AND status = 'To Do'"
    }
    // Additional instances as needed
  ]
}
```

## Requirements

    Python 3.x
    Python libraries: webbrowser, os, json, jira, time, datetime, plyer, pygame.

## Installation

    Ensure Python 3.x is installed on your system.
    Install required Python libraries: pip install jira plyer.

## Configuring JIRA Task Subscriber as a User-Level Service

This guide provides step-by-step instructions on setting up the `jira_task_subscriber.service` to run as a user-level
systemd service. Running it as a user-level service is particularly useful for scripts that require user environment
interaction or do not need elevated system privileges.

### Service Definition File

First, here is the service definition for `jira_task_subscriber.service`:

```ini
[Unit]
Description = JIRA Task Subscriber Service
After = network.target

[Service]
Type = simple
ExecStart = /home/czubillaga/neo9/devops/tools/jira-task-subsriber/main.py
Restart = on-failure

[Install]
WantedBy = default.target

```

### Steps to Configure the Service

1. Create the User Service Directory

If it doesn't already exist, create the systemd user service directory:

```bash
mkdir -p ~/.config/systemd/user/
```

2. Place the Service File

Move or copy your service file into this directory:

```bash
cp /path/to/jira_task_subscriber.service ~/.config/systemd/user/
```

Replace /path/to/jira_task_subscriber.service with the actual path to your service file.

3. Reload Systemd Daemons

Once the service file is in place, reload the systemd daemons to recognize your new service:

```bash
systemctl --user daemon-reload
```

4. Enable the Service

Enable the service to start automatically upon login:

```bash
systemctl --user enable jira_task_subscriber.service
```

5. Start the Service

Start the service immediately without needing to log out and back in:

```bash
systemctl --user start jira_task_subscriber.service
```

6. Check the Service Status

To ensure the service is running properly, check its status:

```bash
systemctl --user status jira_task_subscriber.service
```

Logs Monitoring

To view the logs generated by the service, use the following command:

```bash
journalctl --user -u jira_task_subscriber.service
```

## Features

    Multiple JIRA Instances: Supports monitoring multiple JIRA instances simultaneously.
    Desktop Notifications: Sends notifications with task details directly to your desktop.
    Automatic Task Opening: Opens new tasks in the default web browser for quick access.

## Troubleshooting

    Ensure all the required libraries are installed.
    Verify that the JIRA API token is valid and has the necessary permissions.
    Check the format of the configuration file and ensure it matches the expected schema.
