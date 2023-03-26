import streamlit as st
import openai
import tempfile
import numpy as np
from pytube import YouTube
import os

openai.api_key = "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"
st.title("Youtube Video Summarizer App")


def video_to_audio(video_URL):
    # Get the video
    video = YouTube(video_URL)

    # Convert video to Audio
    audio = video.streams.filter(only_audio=True).first()

    temp_dir = tempfile.mkdtemp()
    variable = np.random.randint(1111, 1111111)
    file_name = f'recording{variable}.mp3'
    temp_path = os.path.join(temp_dir, file_name)
    # audio_in = AudioSegment.from_file(uploaded_file.name, format="m4a")
    # with open(temp_path, "wb") as f:
    #     f.write(uploaded_file.getvalue())

    # Save to destination
    output = audio.download(output_path=temp_path)

    audio_file = open(output, "rb")
    with st.spinner("Transcribing Audio..."):
        textt = openai.Audio.translate("whisper-1", audio_file)["text"]

    return textt

    # _, ext = os.path.splitext(output)
    # new_file = final_filename + '.mp3'
    #
    # # Change the name of the file
    # os.rename(output, new_file)


if "audio_button_" not in st.session_state:
    st.session_state.audio_button_state = False


def callback():
    st.session_state.audio_button_state = True


# Video to audio
video_url = st.text_area("Enter youtube video link")
button = st.button("submit", on_click=callback())
text = ""
if button or st.session_state.audio_button_state:
    text = video_to_audio(video_url)
    st.subheader("Transcribed Audio:")
    st.write(text)
    button1 = st.button("Generate Summary")
    button2 = st.button("Generate Insights")

    if button1:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Generate descriptive summary from the below text:\n{text}\n",
            temperature=0.37,
            max_tokens=1005,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        st.success("Successfully Generated Summary")
        st.write(response["choices"][0]["text"])

    if button2:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Generate insights from the below text:\n'{text}\n",
            temperature=0.37,
            max_tokens=1005,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        st.success("Successfully Generated Insights")
        st.write(response["choices"][0]["text"])

# if button1:
#
#     response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=f"Generate descriptive summary from the below text:\n{text}\n",
#         temperature=0.37,
#         max_tokens=1005,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#     )
#
#     st.success("Successfully Generated Summary")
#     st.write(response["choices"][0]["text"])
#
# if button2:
#
#     response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt= f"Generate insights from the below text:\n'{text}\n",
#         temperature=0.37,
#         max_tokens=1005,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#     )
#
#     st.success("Successfully Generated Insights")
#     st.write(response["choices"][0]["text"])
