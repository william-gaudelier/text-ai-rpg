from openai import OpenAI
import streamlit as st
import re

st.title("Text-AI RPG")


# Loading preprompts
if "preprompt" not in st.session_state:
    with open('preprompt.txt', 'r') as file:
        st.session_state.preprompt = file.read()

with open('memory.json', 'r') as file:
    st.session_state.memory = file.read()
    
with open('history.txt', 'r') as file:
    st.session_state.history = file.read()
    
if "character_created" not in st.session_state:
    st.session_state.character_created = False
    

# Initializing OpenAI API client
if "client" not in st.session_state:
    st.session_state.client = OpenAI(
        api_key = "YOUR_API_KEY_HERE"
    )


# Initializing the messages
if "messages" not in st.session_state:
    msg = """Please provide the following information regarding your character.
    They are all optional, and you can ask to generate random ones.<br>
        <ul>
            <li>Name</li>
            <li>Age</li>
            <li>Gender</li>
            <li>Species</li>
            <li>Height</li>
            <li>Weight</li>
            <li>Body characteristics</li>
            <li>Background information</li>
            <li>Extra facts</li>
            <li>Current abilities</li>
            <li>Current inventory</li>
        </ul>
        """
    st.session_state.messages = [msg]


# Printing the previous messages
for n, msg in enumerate(st.session_state.messages):
    if n % 2 == 0:
        st.markdown(
            f"<div style='padding: 8px; margin: 4px auto'>{msg}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div style='background-color: #2e2e2e; padding: 8px; margin: 4px auto; border-radius: 10px;'>{msg}</div>",
            unsafe_allow_html=True,
        )


# Handling user input
def submit_message():
    message = st.session_state.user_input.strip()
    st.session_state.user_input = ""
            
    if message:
        st.session_state.messages.append(message)

        client = st.session_state.client
        
        # Making the prompt
        prompt = st.session_state.preprompt
        memory = st.session_state.memory
        history = st.session_state.history
        prompt = prompt.replace("<game state>", memory)
        prompt = prompt.replace("<history>", history)
        prompt = prompt.replace("<last context>", st.session_state.messages[-2])
        prompt = prompt.replace("<player's actions>", message)
        
        # Getting the GM response
        response = client.chat.completions.create(
            model = "o1-mini",
            store = True,
            messages = [
                {"role": "user", "content": prompt}
            ]
        ).choices[0].message.content
        st.session_state.debug = response
        
        # If charater not yet created
        if not st.session_state.character_created:
            # Only updating memory
            pattern = r"```json(.*)```"
            match = re.search(pattern, response, re.DOTALL).group(1).strip()
            with open('memory.json', 'w') as file:
                file.write(match)
            st.session_state.character_created = True
            
            first_text = """You sit in the cold, damp cell of the asylum, the weight of your fate pressing heavy on your shoulders. Chains rattle in the distance, the air thick with the scent of decay. Then—a clatter above. A figure peers down, armor glinting in the dim torchlight. Without a word, they drop something: a rusted key, landing near your feet. A silent offering. The choice is yours. Stay in this forgotten prison, or rise, unchain yourself, and step into the unknown where only death—or something worse—awaits."""
            st.session_state.messages.append(first_text)
            
        # Character is already created
        else:
            # Printing response
            pattern = r"Task 2:(.*)Task 3:"
            match = re.search(pattern, response, re.DOTALL).group(1).strip()
            st.session_state.messages.append(match)
            
            # Updating history
            pattern = r"Task 1:(.*)Task 2:"
            match = re.search(pattern, response, re.DOTALL).group(1).strip()
            with open('history.txt', 'a') as file:
                file.write(match+'\n')
            
            # Updating memory
            pattern = r"```json(.*)```"
            match = re.search(pattern, response, re.DOTALL).group(1).strip()
            with open('memory.json', 'w') as file:
                file.write(match)    


# Getting the user input
user_input = st.text_input(
    "What do you do?",
    key = "user_input",
    on_change = submit_message
)


# Sidebar for debug
with st.sidebar:
    if "debug" in st.session_state:
        st.markdown("## Debug\n"+st.session_state.debug, unsafe_allow_html=True)