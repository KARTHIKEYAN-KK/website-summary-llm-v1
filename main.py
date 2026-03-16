import os
from dotenv import load_dotenv
from openai import OpenAI
from scraper import fetch_website_contents
from IPython.display import Markdown, display

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.rule import Rule
from rich import box

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# openai = OpenAI()
openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')

# print(fetch_website_contents('https://akni.in/')['content'])

system_prompt = """
You are a helpful assistant that analyzes the contents of a website,
and provides a summary, ignoring text that might be navigation related.
Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown.
"""

user_prompt_prefix = """
Here are the contents of a website.
Provide a short summary of this website.
If it includes news or announcements, then summarize these too.
"""


def message_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + website}
    ]


def summarize(url):
    website = fetch_website_contents(url)
    response = openai.chat.completions.create(
        model='gpt-oss:20b',
        # model='gpt-4.1-nano',
        messages=message_for(website)
    )
    return response.choices[0].message.content

console = Console()

def display_summary(url):
    summary = summarize(url)

    console.print(Rule("[bold cyan]AI Website Summarizer"))

    console.print(
        Panel(
            url,
            title="Analyzing Website",
            border_style="yellow",
            box=box.ROUNDED
        )
    )

    console.print(Rule("[bold green]Summary"))
    console.print(Markdown(summary))

display_summary("https://akni.in/")
