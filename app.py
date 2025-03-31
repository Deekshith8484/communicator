import streamlit as st
import time
import random
import base64
import os
import tempfile
from gtts import gTTS

# Define the caregiving scenario
conversation = [
    "Good morning! How are you feeling today?",
    "Would you like to rest a little longer or have some breakfast?",
    "What would you like for breakfast? Toast and eggs, or maybe some cereal?",
    "Would you like your eggs scrambled or fried?",
    "Would you like butter or jam on your toast?",
    "What flavor of jam—strawberry or grape?",
    "Are you sitting comfortably?",
    "Would you like a pillow for support or to switch to a different chair?",
    "Would you like a soft pillow for your back or a cushion for your seat?",
    "Would you like something to drink? Maybe coffee, tea, or juice?",
    "Would you like it with honey or sugar?",
    "Would you like to change into something more comfortable?",
    "Would you prefer your blue sweater or the soft cardigan?",
    "Would you like to go for a short walk or stay inside and read?",
    "Would you like to go to the garden or just around the house?",
    "Would you like to rest for a bit?",
    "Would you like a blanket to keep warm?",
    "Would you like to listen to some music or watch TV?",
    "Soft instrumental or something more upbeat?",
]

# Corresponding patient responses
patient_responses = [
    "Good morning! A little tired.", "Breakfast.", "Toast and eggs.", "Scrambled.",
    "Jam.", "Strawberry.", "No.", "Pillow.", "For my back.", "Tea.", "Honey.",
    "Yes.", "Cardigan.", "Walk.", "Garden.", "Yes.", "Yes, please.",
    "Music.", "Soft instrumental."
]

# Generate speech and return autoplay HTML tag
@st.cache_data(show_spinner=False)
def text_to_speech(text):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    filename = temp_file.name
    temp_file.close()

    tts = gTTS(text=text, lang="en")
    tts.save(filename)

    with open(filename, "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode()

    try:
        os.remove(filename)
    except PermissionError:
        pass

    audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
    """
    return audio_html

# Initialize session state
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "audio_html" not in st.session_state:
    st.session_state.audio_html = []

# Title
st.title("🧠 Mindstorms Communicator")
st.write("_Carer is interacting with the patient using BCI technology._")

# Custom styling
st.markdown("""
    <style>
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .chat-message {
        display: flex;
        align-items: center;
        max-width: 80%;
        padding: 10px;
        border-radius: 10px;
        font-size: 18px;
        color: white;
        background: none;
    }
    .processing {
        align-self: center;
        font-style: italic;
        color: gray;
        background: none;
    }
    </style>
""", unsafe_allow_html=True)

# Restart button
if st.button("🔁 Restart Conversation"):
    st.session_state.current_step = 0
    st.session_state.audio_html = []
    st.experimental_rerun()

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display all previous Q&A and audio
for i in range(st.session_state.current_step):
    st.markdown(f'<div class="chat-message"><strong>Carer:</strong> {conversation[i]}</div>', unsafe_allow_html=True)
    st.markdown(st.session_state.audio_html[i][0], unsafe_allow_html=True)
    time.sleep(3)

    st.markdown(f'<div class="chat-message"><strong>Patient:</strong> {patient_responses[i]}</div>', unsafe_allow_html=True)
    st.markdown(st.session_state.audio_html[i][1], unsafe_allow_html=True)
    time.sleep(3)

# Handle current step
if st.session_state.current_step < len(conversation):
    index = st.session_state.current_step
    question = conversation[index]
    response = patient_responses[index]

    # Show question
    st.markdown(f'<div class="chat-message"><strong>Carer:</strong> {question}</div>', unsafe_allow_html=True)
    q_audio = text_to_speech(question)
    st.markdown(q_audio, unsafe_allow_html=True)
    time.sleep(3)

    # Show processing
    st.markdown('<div class="processing">🧠 Processing brain signals...</div>', unsafe_allow_html=True)
    time.sleep(5)

    # Show response
    st.markdown(f'<div class="chat-message"><strong>Patient:</strong> {response}</div>', unsafe_allow_html=True)
    r_audio = text_to_speech(response)
    st.markdown(r_audio, unsafe_allow_html=True)
    time.sleep(3)

    # Save audio to session state
    st.session_state.audio_html.append((q_audio, r_audio))
    
    # Wait before next step
    time.sleep(5)
    st.session_state.current_step += 1
    st.rerun()

# End of conversation
else:
    st.markdown('</div>', unsafe_allow_html=True)
    st.balloons()
    st.write("🎉 Conversation complete! The carer has received the patient's responses.")
