import os
import ollama
from ollama import Client
#from docx import Document
import json

SYSTEM_PROMPT_ACTION_ITEMS = """
Identify and summarize any action items from the meeting transcription.
List the tasks or action items discussed in the meeting.
Extract actionable items or to-do tasks from the meeting.
"""

SYSTEM_PROMPT_SUMMARY_NOTES ="""
Generate a summary of the key points discussed in the meeting.
Summarize the main topics covered in the meeting transcription.
Provide a brief overview of the meeting based on the transcription.
"""

SYSTEM_PROMPT_IDENTITY_PARTICIPANTS = """
List the participants or speakers in the meeting and their contributions.
Extract information about who spoke during the meeting and what they discussed.
"""

SYSTEM_PROMPT_DECISIONS = """
Identify and summarize any decisions made during the meeting.
Extract details about the decisions taken in the meeting.
Highlight key decision points from the meeting transcription.
"""

SYSTEM_PROMPT_IMPORTANT_NOTE = """
Extract timestamps and associated content from the meeting transcription.
Identify specific timings mentioned during the meeting and their context.
"""

SYSTEM_PROMPT_FOLLOW_UPS = """
List any follow-up tasks or items mentioned at the end of the meeting.
Extract information about follow-up actions discussed in the meeting.
"""

SYSTEM_PROMPT_EXTRACT_QUESTIONS = """
Identify any questions raised during the meeting and provide their context.
List the queries or questions discussed in the meeting transcription.
"""

SYSTEM_PROMPT_CAPTURE_AGENDA = """
Summarize the agenda items covered in the meeting transcription.
Extract information about the topics or agenda items discussed during the meeting.
"""

SYSTEM_PROMPT_HIGHLIGHT_CONCERNS = """
Identify and summarize any concerns or issues raised during the meeting.
Extract details about concerns voiced by participants in the meeting.
"""

SYSTEM_PROMPT_MEETING_SUMMARY = """
Generate a concise summary of the entire meeting based on the transcription.
Summarize the key takeaways and highlights from the meeting.
"""

SYSTEM_PROMPT_MOM = """
Generate detailed minutes of the meeting suitable for sharing with the client. Include key discussion points, decisions made, action items assigned to participants, and any notable follow-up tasks. Provide a comprehensive summary that captures the essence of the meeting and is clear and concise for client communication.
"""

MODEL_NAME = "llama3.1"
HOST = "http://localhost:22434"

client = Client(host=HOST)
response = client.chat(model=MODEL_NAME, messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_contents(transcription, SYSTEM_PROMPTS):
    response = client.chat.completions.create(
        model=model_name,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPTS
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )

    return response.choices[0].message.content


#def save_as_docx(minutes, filename):
#    doc = Document()
#    for key, value in minutes.items():
#        # Replace underscores with spaces and capitalize each word for the heading
#        heading = ' '.join(word.capitalize() for word in key.split('_'))
#        doc.add_heading(heading, level=1)
#        doc.add_paragraph(value)
#        # Add a line break between sections
#        doc.add_paragraph()
#    doc.save(filename)


def meeting_minutes(transcription):
    ACTION_ITEMS = get_contents(transcription, SYSTEM_PROMPT_ACTION_ITEMS)
    SUMMARY_NOTES = get_contents(transcription, SYSTEM_PROMPT_SUMMARY_NOTES)
    IDENTITY_PARTICIPANTS = get_contents(transcription, SYSTEM_PROMPT_IDENTITY_PARTICIPANTS)
    DECISIONS = get_contents(transcription, SYSTEM_PROMPT_DECISIONS)

    IMPORTANT_NOTE = get_contents(transcription, SYSTEM_PROMPT_IMPORTANT_NOTE)
    FOLLOW_UPS = get_contents(transcription, SYSTEM_PROMPT_FOLLOW_UPS)
    EXTRACT_QUESTIONS = get_contents(transcription, SYSTEM_PROMPT_EXTRACT_QUESTIONS)

    CAPTURE_AGENDA = get_contents(transcription, SYSTEM_PROMPT_CAPTURE_AGENDA)
    HIGHLIGHT_CONCERNS = get_contents(transcription, SYSTEM_PROMPT_HIGHLIGHT_CONCERNS)
    MEETING_SUMMARY = get_contents(transcription, SYSTEM_PROMPT_MEETING_SUMMARY)
    MOM = get_contents(transcription, SYSTEM_PROMPT_MOM)

    return {
        'Action Items': ACTION_ITEMS,
        'Summary Notes': SUMMARY_NOTES,
        'Participants': IDENTITY_PARTICIPANTS,
        'Decisions': DECISIONS,

        'Important Note': IMPORTANT_NOTE,
        'Follow Ups': FOLLOW_UPS,
        'Questions': EXTRACT_QUESTIONS,

        'Agenda': CAPTURE_AGENDA,
        'Concerns': HIGHLIGHT_CONCERNS,
        'Meeting Summary': MEETING_SUMMARY,
        'MOM': MOM
    }


file_path = "transcription.txt"
content = read_file(file_path)

file_name = file_path.split("/")[-1].split(".")[0].replace(" ", "")

minutes = meeting_minutes(content)

#save_as_docx(minutes, f'{base_file_op_path}{file_name}_detailed_meeting_minutes.docx')

#with open(f'{base_file_op_path}{file_name}_minutes.json', 'w') as file:  # Open file in write mode
#    json.dump(minutes, file, indent=4)


