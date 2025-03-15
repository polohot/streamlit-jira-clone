import streamlit as st
from streamlit_quill import st_quill

st.title("Your Reply System")

# Initialize session state for storing replies
if "replies" not in st.session_state:
    st.session_state.replies = []

# Display all replies
st.subheader("Replies List")
if st.session_state.replies:
    for rep in st.session_state.replies:
        st.html(rep)
else:
    st.write("No replies yet.")

# Create a rich text editor
reply = st_quill("", html=True, readonly=False)

# Add button to append reply to the list
if st.button("Add"):
    st.session_state.replies.append(reply)
    st.success("Reply added!")

st.json(st.session_state['replies'])
