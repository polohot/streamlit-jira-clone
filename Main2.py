import streamlit as st
import pandas as pd

# Sample Data
data = pd.DataFrame({
    "A": ["Apple", "Banana", "Cherry", "Date", "Elderberry"],
    "B": ["ClickA", "ClickB", "ClickC", "ClickD", "ClickE"]
})

# Initialize session state for storing selected items
if "selected_items" not in st.session_state:
    st.session_state.selected_items = []

def add_to_session_state(fruit):
    st.session_state.selected_items.append(fruit)
    st.rerun()

st.write("### Click a button to add the corresponding fruit to the session state:")

def render_table():
    table_data = []
    for index, row in data.iterrows():
        table_data.append([row["A"], st.button(row["B"], key=index, on_click=add_to_session_state, args=(row["A"],))])
    return table_data

# Show DataFrame with buttons in the second column
st.write("### Data Table")
st.dataframe(data, hide_index=True)

# Display selected items
st.write("### Selected Items:")
st.write(st.session_state.selected_items)