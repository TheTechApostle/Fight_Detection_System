import streamlit as st

# Title
st.title("👋 Welcome to My Question App")

# Subtitle
st.subheader("A simple app that greets you")

# User input
name = st.text_input("Enter your name")

# Button
if st.button("Greet Me"):
    if name:
        st.success(f"Hello, {name}! 👋")
    else:
        st.warning("Please enter your name first.")
