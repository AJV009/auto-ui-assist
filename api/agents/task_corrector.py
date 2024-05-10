import anthropic
import os
import json
from dotenv import load_dotenv
from utils.trace import store_agent_conversation_array, fetch_agent_conversation_array

load_dotenv()
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
CLAUDE_HAIKU=os.getenv("ANTHROPIC_CLAUDE_HAIKU")
CLAUDE_SONNET=os.getenv("ANTHROPIC_CLAUDE_SONNET")
CLAUDE_OPUS=os.getenv("ANTHROPIC_CLAUDE_OPUS")

def task_corrector_agent(userid, sessionid, task, app_list, os, refinement=None):
    """
    Correct the task using the Anthropics API.
    """

    system_prompt = f"""
You are a \"{os} Task Automation Helper: Task correction & info extraction\".
Given a user task you have to modify it to include the following information:
- Apps needed for the task, as 'launch_app_list' in the response
- Correct any other grammer or task formation problems with it. Finally rewrite the task with more clarity and precision for the planning stage bot. Add this task as 'corrected_task'
- You can include a list of clarification questions to be asked to the user in 'refinement_questions'

Please follow these instructions:
- You will be provided a task to process.
- You will be also provided a dict that is a list of applications on the user system.
- You have to modify the task to include the most appropriate application for the task.
- IF the app list doesn't contain a compatible app, you have to modify the task to use a web app like ones provided by Google, Microsoft, etc. (Google Sheets instead of Excel, Google Docs instead of Word, etc.)
- If the task needs more clarification, add percise set of questions in 'refinement_questions' to ask the user. Do not ask when not needed. THe processing of task will only continue after the task is clear from any questions or doubts from your end.
- You also have to return an app list in the same response.
- Strictly use JSON format as output.

Sample response
{{\"corrected_task\": \"Use Microsoft Excel to create some student data like (name, grade, subject, score), create a new sheet that calculates the average score for each student across all subjects. Create a pivot table showing the average score by grade and subject.\", \"launch_app_list\": [\"Excel.lnk\"], \"refinement_questions\": [\"Can you provide some of this mentioned student data?\"]}}
"""

    fewshot_message_array = [
        {
        "role": "user",
        "content": """
Correct the following task
<task>
Write a press release announcing the launch of a new sustainable fashion line. Include quotes from the designer and information about the eco-friendly materials used. Format the document with a header, subheadings, and a footer with contact information.
</task>

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
        "content": "{\"corrected_task\": \"Write a press release using Google Docs announcing the launch of a new sustainable fashion line. Use Brave to google information about a new sustainable fashion line and include quotes from the designer and information about any eco-friendly materials used. Format the document with a header, subheadings, and a footer with contact information.\", \"launch_app_list\": [\"Brave.lnk\"]}"
        },
        {
        "role": "user",
        "content": """
User task:
<task>
Open the renewable eneergy presentation. And add a pie chart showing the global energy mix and a bar plot comparing the costs of different energy sources. Use a green technology theme and make it look professional.
</task>

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
        "content": "{\"corrected_task\": \"Open the renewable energy presentationin PowerPoint. And add a pie chart showing the global energy mix and a bar plot comparing the costs of different energy sources. Use a green technology theme and make it look professional. Use Microsoft Edge if required to search about benefits of renewable energy and costs of different energy sources.\", \"launch_app_list\": [\"PowerPoint.lnk\",\"Microsoft Edge.lnk\"], \"refinement_questions\": [\"Can you please tell me where this exact presentation file is and whats its exact name? Or shall I open the PowerPoint recents and pick the the most relevant?\"]}"
        },
        {
        "role": "user",
        "content": """
User task:
<task>
Open the renewable energy presentationin PowerPoint. And add a pie chart showing the global energy mix and a bar plot comparing the costs of different energy sources. Use a green technology theme and make it look professional. Use Microsoft Edge if required to search about benefits of renewable energy and costs of different energy sources.
</task>

Refinement details:
<refinement>
Can you please tell me where this exact presentation file is and whats its exact name? Or shall I open the PowerPoint recents and pick the the most relevant?
Yes its in my desktop. The file name is "Renewable Energy Presentation.pptx"
</refinement>

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
        "content": "{\"corrected_task\": \"Open the \"Renewable Energy Presentation.pptx\" found in the desktop. And add a pie chart showing the global energy mix and a bar plot comparing the costs of different energy sources. Use a green technology theme and make it look professional. Use Microsoft Edge if required to search about benefits of renewable energy and costs of different energy sources.\", \"launch_app_list\": [\"Microsoft Edge.lnk\"]}"
        }
    ]
    
    init_task_frame = {
      "role": "user",
      "content": f"""
You perfectly handeled a sitution where the app was not available in the app list. Well done.

Now correct the following task using the app list provided:
<task>
{task}
</task>

New App list:
<app_list>
{app_list}
</app_list>
"""
      }
  
    # prepare the message array
    message_array = fewshot_message_array

    if refinement:
      message_array = fetch_agent_conversation_array(
        userid=userid,
        sessionid=sessionid,
        agent_name="task_corrector_agent"
      )
      refinement_frame = {
        "role": "user",
        "content": f"""
The updated task:
<task>
{task}
</task>

Refinement details:
<refinement>
{refinement}
</refinement>

New App list:
<app_list>
{app_list}
</app_list>
"""
      }
      message_array.append(refinement_frame)
    else:
      message_array.append(init_task_frame)
      
    # dump to a json file for debugging
    with open("task_corrector_agent.json", "w") as f:
      json.dump(message_array, f, indent=2)

    response_message = anthropic_client.messages.create(
        model=CLAUDE_SONNET,
        system=system_prompt,
        messages=message_array,
        max_tokens=4096,
        metadata={"user_id": userid+"-"+sessionid},
        temperature=1.0
    )

    message_array.append(
        {
            "role": "assistant",
            "content": response_message.content[0].text
        }
    )
    store_agent_conversation_array(
      userid=userid,
      sessionid=sessionid,
      agent_name="task_corrector_agent",
      conversation_array=message_array
    )

    response_dict = json.loads(response_message.content[0].text)
    return response_dict
