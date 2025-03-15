import streamlit as st
import io
import base64

# Initialize session state for log storage
if 'lsLog' not in st.session_state:
    st.session_state.lsLog = [{"topic": "TopicName", "owner": "OwnerName"}]

# Function to update display
def add_log(input_text, input_image):
    if input_text or input_image:
        new_entry = {}
        if input_text:
            new_entry["Text"] = input_text
        
        if input_image:
            # Convert the file to a base64 string for display
            file_bytes = input_image.read()
            encoded_image = base64.b64encode(file_bytes).decode()
            new_entry["image"] = f"data:image/jpeg;base64,{encoded_image}"
        
        st.session_state.lsLog.append(new_entry)
        st.rerun()

# Display the first element and the latest entry
st.subheader("Latest Log Entry")
if len(st.session_state.lsLog) > 1:
    st.write(st.session_state.lsLog[0])
    st.write(st.session_state.lsLog[-1])
else:
    st.write(st.session_state.lsLog[0])

# Forum-style input form
st.subheader("Add a Log Entry")
input_text = st.text_area("Enter text:")
input_image = st.file_uploader("Upload an image:", type=["png", "jpg", "jpeg"])

if st.button("Add Log"):
    add_log(input_text, input_image)
