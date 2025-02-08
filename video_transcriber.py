import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi

st.title("YouTube Video Transcriber")

video_url = st.text_input("Enter YouTube Video URL:")


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


if video_url:
    video_id = get_video_id(video_url)

    if video_id:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            full_transcript = " ".join(
                [entry["text"] for entry in transcript]
            )  # Combine into one string
            st.write("Transcript:")
            st.write(full_transcript)  # Display the transcript in Streamlit
        except Exception as e:
            st.error(f"An error occurred: {e}")
    elif video_url:
        st.error("Invalid YouTube URL. Please enter a valid URL.")
