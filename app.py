import streamlit as st
import cohere

# Set your Cohere API key directly in the code
COHERE_API_KEY = "UvQcnNHSF42oPDGTWv6P9OpGrOCMb9lPgKOjxj3m"  # Replace with your actual Cohere API key

# Initialize the Cohere client
cohere_client = cohere.Client(COHERE_API_KEY)

# Streamlit UI settings
st.set_page_config(page_title="Conversational Q&A Chatbot")
st.header("Hey, Let's Chat")

# Check if session state exists for messages
if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = ["You are a comedian AI assistant."]

# Function to get response from Cohere's API
def get_cohere_response(question):
    # Append user input to the conversation
    st.session_state['flowmessages'].append(f"User: {question}")
    
    # Generate a response using Cohere's model
    prompt = '\n'.join(st.session_state['flowmessages'])  # Convert conversation history into a prompt
    
    # Call Cohere's API to get the response
    response = cohere_client.generate(
        model='xlarge',  # Choose the model (xlarge or another depending on your plan)
        prompt=prompt,
        max_tokens=100,  # Adjust max tokens as needed
        temperature=0.5,  # Temperature for creativity
        stop_sequences=["User:", "AI:"]  # Define stop sequences to structure conversation
    )
    
    # Extract the response text
    ai_response = response.generations[0].text.strip()
    
    # Append the AI's response to the conversation history
    st.session_state['flowmessages'].append(f"AI: {ai_response}")
    
    return ai_response

# UI to input questions
input = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

# If the submit button is clicked, get and display the response
if submit:
    if input:
        response = get_cohere_response(input)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.warning("Please input a question to get a response.")
