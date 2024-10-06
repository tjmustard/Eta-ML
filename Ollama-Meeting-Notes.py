#import os
#import ollama
from ollama import Client
import json
import webvtt
import argparse

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


def get_contents(transcription, SYSTEM_PROMPTS, host="http://localhost:11434", model_name="llama3.1"):
    #print(host)
    #print(model_name)
    print(SYSTEM_PROMPTS)
    client = Client(host=host)
    response = client.chat(model=model_name, messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPTS
        },
        {
            "role": "user",
            "content": transcription
        }
    ])
    return response["message"]["content"]

def vtt_to_text(vtt_file):
    outlines = []
    # Initialize the parser
    vtt = webvtt.read(vtt_file)
    for caption in vtt:
        ##print(caption.start)
        ##print(caption.end)
        #print(caption.text)
        outlines.append(caption.text)
    return "\n".join(outlines)

def json_to_output(minutes):
    # Initialize an empty list to store the sections and their content
    sections = []

    # Iterate over each section in the minutes data
    for section, content in minutes.items():
        # Convert the content to Markdown text by wrapping it in headings and bold text
        markdown_content = f"**{section}**:\n\n{content}"

        # Add the section and its content to the list of sections
        sections.append(markdown_content)

    # Join all the sections together with a newline character in between
    result = "\n\n".join(sections)

    return result

def meeting_minutes(transcription, host="http://localhost:11434", model_name="llam3.1"):
    LLM = "Model: {}\nServer: {}".format(model_name, host)
    ACTION_ITEMS = get_contents(transcription, SYSTEM_PROMPT_ACTION_ITEMS, host, model_name)
    SUMMARY_NOTES = get_contents(transcription, SYSTEM_PROMPT_SUMMARY_NOTES, host, model_name)
    IDENTITY_PARTICIPANTS = get_contents(transcription, SYSTEM_PROMPT_IDENTITY_PARTICIPANTS, host, model_name)
    DECISIONS = get_contents(transcription, SYSTEM_PROMPT_DECISIONS, host, model_name)

    IMPORTANT_NOTE = get_contents(transcription, SYSTEM_PROMPT_IMPORTANT_NOTE, host, model_name)
    FOLLOW_UPS = get_contents(transcription, SYSTEM_PROMPT_FOLLOW_UPS, host, model_name)
    EXTRACT_QUESTIONS = get_contents(transcription, SYSTEM_PROMPT_EXTRACT_QUESTIONS, host, model_name)

    CAPTURE_AGENDA = get_contents(transcription, SYSTEM_PROMPT_CAPTURE_AGENDA, host, model_name)
    HIGHLIGHT_CONCERNS = get_contents(transcription, SYSTEM_PROMPT_HIGHLIGHT_CONCERNS, host, model_name)
    MEETING_SUMMARY = get_contents(transcription, SYSTEM_PROMPT_MEETING_SUMMARY, host, model_name)
    MOM = get_contents(transcription, SYSTEM_PROMPT_MOM, host, model_name)

    return {
        'LLM Meeting notes' : LLM,
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


def create_parser():
    # Initialize the parser
    parser = argparse.ArgumentParser(description='Convert VTT file to text')

    # Add arguments
    parser.add_argument('--vtt-file', type=str, required=True, help='Path to the input VTT file')
    parser.add_argument('--output-file', type=str, default='output.txt', help='Path to the output text file')
    parser.add_argument('--hostname', type=str, default="http://localhost:11434", help=f'Hostname (default: http://localhost:11434)')
    parser.add_argument('--model-name', type=str, default="llama3.1", help=f'Model name (default: llama3.1)')

    # Parse arguments
    return parser.parse_args()

if __name__ == '__main__':
    # Parse arguments
    args = create_parser()

    # Convert webvtt file to simple text
    transcript = vtt_to_text(args.vtt_file)
    print(f'VTT file converted to text.')

#    client = Client(host=args.hostname)
#    response = client.chat(model=args.model_name, messages=[
#        {
#            "role": "system",
#            "content": "Identify and summarize any action items from the meeting transcription. List the tasks or action items discussed in the meeting. Extract actionable items or to-do tasks from the meeting. "
#        },
#        {
#            "role": "user",
#            "content": "Something about"
#        }
#    ])
#    print(response["message"]["content"])

    minutes = meeting_minutes(transcript, host=args.hostname, model_name=args.model_name)
    print(minutes)
    print(json_to_output(minutes))

#save_as_docx(minutes, f'{base_file_op_path}{file_name}_detailed_meeting_minutes.docx')

#with open(f'{base_file_op_path}{file_name}_minutes.json', 'w') as file:  # Open file in write mode
#    json.dump(minutes, file, indent=4)


