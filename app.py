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

# Function to generate speech and return the HTML autoplay audio tag
def text_to_speech(text):
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    filename = temp_file.name
    temp_file.close()  # Close the file to allow other processes to use it

    # Generate speech
    tts = gTTS(text=text, lang="en")
    tts.save(filename)

    # Convert audio file to base64
    with open(filename, "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode()

    # Return autoplay HTML audio tag
    audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
    """

    # Allow the file to finish playing before removing it
    time.sleep(1)
    
    try:
        os.remove(filename)  # Safely remove the file
    except PermissionError:
        pass  # Ignore file permission error if it's still in use

    return audio_html

# Initialize session state
if "current_step" not in st.session_state:
    st.session_state.current_step = 0

# Streamlit UI
st.title("🧠 Patient-Carer Communication (Daily Scenario)")
st.write("_Carer is interacting with the patient using BCI technology._")

# Custom CSS for chat layout
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
        color: white;  /* White text */
        background: none; /* No background */
    }
    .processing {
        align-self: center;
        font-style: italic;
        color: gray;
        background: none; /* No background */
    }
    </style>
""", unsafe_allow_html=True)

# Create a div container for the chat
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display all previous Q&A pairs with correct audio flow
for i in range(st.session_state.current_step):
    st.markdown(f'<div class="chat-message"><strong>Carer:</strong> {conversation[i]}</div>', unsafe_allow_html=True)
    st.markdown(text_to_speech(conversation[i]), unsafe_allow_html=True)  # Play Carer's question
    time.sleep(3)  # Ensure no overlap
    st.markdown(f'<div class="chat-message"><strong>Patient:</strong> {patient_responses[i]}</div>', unsafe_allow_html=True)
    st.markdown(text_to_speech(patient_responses[i]), unsafe_allow_html=True)  # Play Patient's response
    time.sleep(3)  # Pause to let response finish before next question

# Show the current question from the Carer
if st.session_state.current_step < len(conversation):
    current_question = conversation[st.session_state.current_step]

    # Show the Carer's question (White text, No background)
    st.markdown(f'<div class="chat-message"><strong>Carer:</strong> {current_question}</div>', unsafe_allow_html=True)
    st.markdown(text_to_speech(current_question), unsafe_allow_html=True)  # Auto-play Carer's question
    time.sleep(3)  # Pause to let Carer's voice finish

    # Show "Processing brain signals..." (Gray italic text, No background, No voice-over)
    st.markdown('<div class="processing">🧠 Processing brain signals...</div>', unsafe_allow_html=True)
    time.sleep(5)  # Simulating signal processing delay

    # Generate and display Patient's response (White text, No background)
    response = patient_responses[st.session_state.current_step]
    st.markdown(f'<div class="chat-message"><strong>Patient:</strong> {response}</div>', unsafe_allow_html=True)

    # Play only the Patient's response after processing delay (No overlap)
    st.markdown(text_to_speech(response), unsafe_allow_html=True) 
    time.sleep(3)  # Ensure no overlap before next question

    # Wait another 5 seconds before moving to the next question
    time.sleep(5)

    # Move to the next question and rerun
    st.session_state.current_step += 1
    st.rerun()

# Close the chat container div
st.markdown('</div>', unsafe_allow_html=True)

# Final completion message when all questions are answered
if st.session_state.current_step == len(conversation):
    st.balloons()
    st.write("🎉 Conversation complete! The carer has received the patient's responses.")
