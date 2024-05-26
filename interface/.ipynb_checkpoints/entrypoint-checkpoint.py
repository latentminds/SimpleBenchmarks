import streamlit as st
from streamlit_javascript import st_javascript

url = st_javascript("await fetch('').then(r => window.parent.location.href)")

st.write("# Simple benchmarking 🎯")

st.page_link(page=url+'/vizu?model=Mistral-7B-v0.1', label = "Mistral-7B-v0.1")
st.page_link(page=url+'/vizu?model=Meta-Llama-3-8B', label = "Meta-Llama-3-8B")
st.page_link(page=url+'/vizu?model=gemma-7b', label = "gemma 7B")
st.page_link(page=url+'/vizu?model=Mistral-7B-v0.3', label = "Mistral-7B-v0.3")