import streamlit as st
import random
from main import medicine_details,medication_optimization

st.title("DrugAI")
st.markdown(f"""<p style="font-size:1.5rem;">Type your medication in the text box bellow and get to know more about your medication.</p>""",unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Enter your Medication (comma seperated)"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    all_meds = [pro.strip() for pro in prompt.split(",")]

    total_meds = len(all_meds)
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = f"Collecting information for {prompt.title()} ....."
    # st.chat_message("assistant").write(response)
    # medicine,salts,full_match,other_matches = medicine_details(prompt.lower())
    # final_med,total_salts,salts,medicines = medication_optimization(all_meds)
    enter = "\n\n"
    with st.spinner("Collecting Information for your medication..."):
        (
            final_med,
            total_salts,
            salts,
            medicines,
        ) = medication_optimization(all_meds)
    print("Total salts",total_salts)
    print("Salts",salts)
    response = f"**For the following medicines:**  {', '.join([s.title() for s in medicines])}.\n\n :red[**You are consuming:**] {', '.join([s.title() for s in salts])}"
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    print(final_med)
    if len(final_med.keys()) == 0:
        response = "No Alternatives are there"
    else:
        alt = final_med.keys()
        response = f':green[**You can reduce your medicines to {len(alt)} from {total_meds}.**]'
        for k in final_med:
            num_alters = len(final_med[k])
            display = num_alters if num_alters < 5 else 5
            response += f"\t\n\n**For salt combination** [{', '.join([s.title() for s in k])}] There are **{num_alters}** alternatives.\t\n\n**Some of alternatives are:**\n\n{f'{enter}'.join([s.title() for s in random.choices(final_med[k],k=display)])}"

    # response = f"Medicine Name: {medicine.title()} \n\nSalt Composition: {', '.join([s.title() for s in salts])}\n\nAlternatives: {', '.join([m.title() for m in full_match])}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

