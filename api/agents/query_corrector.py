import anthropic
import os
import json
from dotenv import load_dotenv

load_dotenv()
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
CLAUDE_HAIKU="claude-3-haiku-20240307"

def query_corrector_agent(uuid, query, app_list, os):
    """
    Correct the query using the Anthropics API.
    """
    system_prompt = f"""
You are a \"{os} Automation Query: App inclusion and correction bot\".
Given a user query you have to modify it to include the type of App needed for the task and correct any other formation problems with it.

Please follow these instructions:
- You will be provided a query to process.
- You will be also provided a dict that is a list of applications on the user system.
- You to modify the query to include the most appropriate application for the task.
- IF the app list doesn't contain a compatible app, you have to modify the query to use a web app like ones provided by Google, Microsoft, etc.
- The query should be self sustainable and should not require any additional information from the user. If the query doesn't have enough information, make that infromation or modify it in such a way that it uses some browser to get the information.
- You also have to return an app list in the same response.
- Strictly use JSON format as output.

Sample response
{{\"corrected_query\": \"Use Microsoft Excel to create some dummy student data like (name, grade, subject, score), create a new sheet that calculates the average score for each student across all subjects. Create a pivot table showing the average score by grade and subject.\", \"selected_app_list\": [\"Excel.lnk\"]}}
"""
    message_array = [
        {
        "role": "user",
        "content": """
User query:
<query>
Create a presentation about the benefits of renewable energy. Include a pie chart showing the global energy mix and a bar plot comparing the costs of different energy sources. Use a green technology theme and make it look professional.
</query>

App list:
<app_list>
{
    "AllUsersPrograms": {
      "Access.lnk": null,
      "Brave.lnk": null,
      "Epic Games Launcher.lnk": null,
      "Excel.lnk": null,
      "Microsoft Edge.lnk": null,
      "OneDrive.lnk": null,
      "OneNote.lnk": null,
      "Outlook.lnk": null,
      "PowerPoint.lnk": null,
      "Publisher.lnk": null,
      "Word.lnk": null
    },
    "StartMenu": {
      "Programs": {
        "Administrative Tools.lnk": null,
        "F1_23.lnk": null,
        "File Explorer.lnk": null
      }
    },
    "AllUsersDesktop": {
      "Brave.lnk": null,
      "VLC media player.lnk": null
    }
  }
</app_list>
"""
        },
        {
        "role": "assistant",
        "content": "{\"corrected_query\": \"Create a presentation using PowerPoint about the benefits of renewable energy. Include a pie chart showing the global energy mix and a bar plot comparing the costs of different energy sources. Use a green technology theme and make it look professional. Use Microsoft Edge to search about benefits of renewable energy and costs of different energy sources.\", \"selected_app_list\": [\"PowerPoint.lnk\",\"Microsoft Edge.lnk\"]}"
        },
        {
        "role": "user",
        "content": """
Perfect job, well done.

Now similarly correct the following query using the app list provided:
<query>
Write a press release announcing the launch of a new sustainable fashion line. Include quotes from the designer and information about the eco-friendly materials used. Format the document with a header, subheadings, and a footer with contact information.
</query>

New App list:
<app_list>
{
    "AllUsersPrograms": {
      "Access.lnk": null,
      "Brave.lnk": null,
    },
    "StartMenu": {
      "Programs": {
        "Administrative Tools.lnk": null,
        "F1_23.lnk": null,
        "File Explorer.lnk": null
      }
    },
    "AllUsersDesktop": {
      "Brave.lnk": null,
      "VLC media player.lnk": null
    }
  }
</app_list>
"""
        },
        {
        "role": "assistant",
        "content": "{\"corrected_query\": \"Write a press release using Google Docs announcing the launch of a new sustainable fashion line. Use Brave to google information about a new sustainable fashion line and include quotes from the designer and information about any eco-friendly materials used. Format the document with a header, subheadings, and a footer with contact information.\", \"selected_app_list\": [\"Brave.lnk\"]}"
        },
        {
        "role": "user",
        "content": f"""
You perfectly handeled a sitution where the app was not available in the app list. Well done.

Now correct the following query using the app list provided:
<query>
{query}
</query>

New App list:
<app_list>
{app_list}
</app_list>
"""
        }
    ]
    response_message = anthropic_client.messages.create(
        model=CLAUDE_HAIKU,
        system=system_prompt,
        messages=message_array,
        max_tokens=4096,
        metadata={"user_id": uuid},
        temperature=1.0
    )
    response_dict = json.loads(response_message.content[0].text)
    return response_dict
