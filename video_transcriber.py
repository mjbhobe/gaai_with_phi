import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_video_id(url):
    """Extracts the video ID from a YouTube URL."""
    from urllib.parse import urlparse, parse_qs

    parsed_url = urlparse(url)
    if "youtu.be" in parsed_url.netloc:
        video_id = parsed_url.path[1:]  # Extract from short URLs
    elif "youtube.com" in parsed_url.netloc or "www.youtube.com" in parsed_url.netloc:
        try:
            query_params = parse_qs(parsed_url.query)
            video_id = query_params["v"][0]
        except KeyError:
            video_id = None
    else:
        video_id = None
    return video_id


def get_model_response(prompt: str) -> str:
    """pass in any prompt to model & get response"""
    model = genai.GenerativeModel("gemini-2.0-flash")
    gen_config = genai.GenerationConfig(temperature=0.0, max_output_tokens=1024 * 5)
    response = model.generate_content(prompt, generation_config=gen_config)

    return response.text


def get_punctuated_transcript(video_transcript: str) -> str:
    """calls and LLM that punctuates raw text"""

    prompt = f"""
    You are an expert transcriber, who can format raw text using the correct punctuations & formatting (such as inserting logical paragraphs, bullets or numbered lists where applicable) to create a professional looking text. 

    ## Instructions ----
    Don't generate any spurious text such as "Ok, here is....". 
    Do generate a title/header for the script with proper markdpwn followed by the script 
    using professional formatting as described above.

    Please transcribe the following raw script:

    {video_transcript}
    """
    # model = genai.GenerativeModel("gemini-1.5-flash")
    # response = model.generate_content(prompt)

    return get_model_response(prompt)


def get_summary(text: str) -> str:
    """summarize long text"""
    prompt = f"""
    Please summarize the following text. Do not miss out any key points & messages
    from the text provided. Use good formatting in your response, such as paragraphs,
    bullets, numbered lists etc., as appropriate. Don't generate any spurious text such as 
    "Ok here is a summary..."

    Text to summarize:

    {text}
    """
    # model = genai.GenerativeModel("gemini-1.5-flash")
    # gen_config = genai.GenerationConfig(temperature=0.0, max_output_tokens=1024 * 5)
    # response = model.generate_content(prompt, generation_config=gen_config)

    return get_model_response(prompt)


def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    full_transcript = " ".join(
        [entry["text"] for entry in transcript]
    )  # Combine into one string
    # now ask our LLM to punctuate it
    return get_punctuated_transcript(full_transcript)


# -------------------------------------------------------------------

st.set_page_config(
    page_title="Generative AI Video Transcriber",
    page_icon="✨",
)

st.title("YouTube Video Transcriber 📽️💬")

video_url = st.text_input(
    "Enter (or paste) YouTube Video URL into text box below and press Enter to transcribe & summarize it:"
)


if video_url:
    video_id = get_video_id(video_url)

    if video_id:
        try:
            st.video(video_url)
            with st.spinner("Generating transcript & summary..."):
                transcript = get_transcript(video_id)
                summary = get_summary(transcript)
            st.write(transcript)
            # transcript = YouTubeTranscriptApi.get_transcript(video_id)
            # full_transcript = " ".join(
            #     [entry["text"] for entry in transcript]
            # )  # Combine into one string
            # st.write("Transcript:")
            # st.write(full_transcript)  # Display the transcript in Streamlit

            st.markdown("---")
            st.markdown(
                f"<h2 style='color=skyblue;'>Summary</h2>",
                unsafe_allow_html=True,
            )
            st.write(summary)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    elif video_url:
        st.error("Invalid YouTube URL. Please enter a valid URL.")
