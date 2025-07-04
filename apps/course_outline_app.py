
import streamlit as st
import pathlib
from PIL import Image
LOGO_PATH = pathlib.Path(__file__).resolve().parents[1] / 'shared' / 'logo.png'
if LOGO_PATH.exists():
    image = Image.open(LOGO_PATH)
    st.image(image, width=120)
else:
    st.error('❌ logo.png not found')
import pathlib
from PIL import Image

LOGO_PATH = pathlib.Path(__file__).resolve().parents[1] / 'shared' / 'logo.png'
st.write(f"Logo Path: {LOGO_PATH}")
st.write(f"Logo Exists: {LOGO_PATH.exists()}")

if LOGO_PATH.exists():
    image = Image.open(LOGO_PATH)
    st.image(image, width=120)
else:
    st.error("❌ logo.png not found at runtime")



import streamlit as st
import pathlib
from PIL import Image

LOGO_PATH = pathlib.Path(__file__).resolve().parents[1] / 'shared' / 'logo.png'
st.write(f"Logo Path: {LOGO_PATH}")
st.write(f"Logo Exists: {LOGO_PATH.exists()}")

if LOGO_PATH.exists():
        image = Image.open(image_file)
        st.image(image, width=120)
else:
    st.error("❌ logo.png not found at runtime")



import streamlit as st
import pathlib

LOGO_PATH = pathlib.Path(__file__).resolve().parents[1] / 'shared' / 'logo.png'
st.write(f"Logo Path: {LOGO_PATH}")
st.write(f"Logo Exists: {LOGO_PATH.exists()}")

if LOGO_PATH.exists():
else:
    st.error("❌ logo.png not found at runtime")



import streamlit as st
import pathlib

LOGO_PATH = pathlib.Path(__file__).resolve().parents[1] / 'shared' / 'logo.png'
st.write(f"Logo Path: {LOGO_PATH}")
st.write(f"Logo Exists: {LOGO_PATH.exists()}")

if LOGO_PATH.exists():
else:
    st.error("❌ logo.png not found at runtime")



import streamlit as st
import os
from openai import OpenAI
from weasyprint import HTML
from jinja2 import Template
import uuid

LOGO_PATH = "logo.png"
TEMPLATE_PATH = "course_outline_template.html"

def generate_outline(api_key, course_description):
    client = OpenAI(api_key=api_key)
    prompt = f"""You are an expert instructional designer.

Given the following user input, interpret the course name, level (Basic/Intermediate/Advanced), and duration (e.g. 2 days = 16 hours). Based on that, generate a detailed training outline.

User Input:
{course_description}

Instructions:
1. Extract course title, level, and total duration.
2. Break the duration into Modules (3–5), each with Topics (2–3).
3. For each Topic:
   - Title
   - Duration in hours
   - 3–5 Learning Objectives
   - 5–8 Content Points
   - 1 Hands-on Lab/Activity (with time allocation)
   - 3–5 Q&A items
4. Ensure total topic + lab durations match the overall time.
5. Output clearly in this structure:

Course Title: ...
Level: ...
Total Duration: ... hours
Summary: ...

Module 1: ...
  - Topic 1: ...
    Duration: ... hours
    Objectives: ...
    Content Points: ...
    Lab: ...
    Q&A: ...
  - Topic 2: ...
    ...
Module 2: ...
...

"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=3000
    )
    return response.choices[0].message.content

def parse_outline(md):
    lines = md.splitlines()
    course = {"title": "", "level": "", "duration": "", "summary": "", "modules": []}
    module = None
    topic = None
    stage = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.lower().startswith("course title:"):
            course["title"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("level:"):
            course["level"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("total duration:"):
            course["duration"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("summary:"):
            course["summary"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("module"):
            if module:
                if topic:
                    module["topics"].append(topic)
                    topic = None
                course["modules"].append(module)
            module = {"title": line, "topics": []}
        elif line.lower().startswith("- topic"):
            if topic:
                module["topics"].append(topic)
            topic = {"title": line.split(":", 1)[1].strip(), "duration": "", "objectives": [], "content": [], "lab": "", "qa": []}
        elif line.lower().startswith("duration:") and topic:
            topic["duration"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("objectives:"):
            stage = "objectives"
        elif line.lower().startswith("content"):
            stage = "content"
        elif line.lower().startswith("lab:"):
            topic["lab"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("q&a"):
            stage = "qa"
        elif line.startswith("-") and topic:
            item = line[1:].strip()
            if stage == "objectives":
                topic["objectives"].append(item)
            elif stage == "content":
                topic["content"].append(item)
            elif stage == "qa":
                topic["qa"].append(item)

    if topic and module:
        module["topics"].append(topic)
    if module:
        course["modules"].append(module)
    return course

def render_pdf(course):
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = Template(f.read())

    html = template.render(
        course_name=course["title"],
        summary=course["summary"],
        duration=course["duration"],
        level=course["level"],
        Modules=course["modules"]
    )
    filename = f"{course['title'].replace(' ', '_')}_{uuid.uuid4().hex[:8]}.pdf"
    HTML(string=html, base_url=".").write_pdf(filename)
    return filename

# Streamlit UI
st.set_page_config(page_title="3EK Smart Course Planner", layout="centered")
st.image(LOGO_PATH, width=120)
st.title("🧠 3EK AI-Powered Course Planner")

api_key = st.text_input("🔐 Enter your OpenAI API Key", type="password")
description = st.text_area("✍️ Enter course name, level and duration (e.g. 'Basics of AWS and Azure, Intermediate, 2 Days')")

if st.button("🚀 Generate Plan"):
    if not api_key or not description:
        st.error("API key and course description are required.")
    else:
        with st.spinner("Generating detailed plan..."):
            outline = generate_outline(api_key, description)
            course = parse_outline(outline)
            pdf_path = render_pdf(course)
        st.success("✅ Detailed Training Plan Ready!")
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Download PDF", f, file_name=pdf_path)
