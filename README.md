A text-based RPG that uses ChatGPT for the game itself and streamlit for the interface.

It has a hard time coming up with an interesting story for the moment, it's hard to escape the corridor...

It runs locally with the following files:
- **text-rpg.py**, contains the code that interfaces with openai and displays the adventure (requires an API key)
- **preprompt.txt**, contains the preprompt given to the ai for each user response
- **history.txt**, contains a summary of the adventure, to limit the size of the the prompt given
- **memory.json**, contains the data we want the ai to remember, about the player and its environment, to avoid hallucination
