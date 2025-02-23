import chat
import streamlit as st
from streamlit_chat import message

import csv
from datetime import datetime
import time

#Creating the chatbot interface
st.title("LLM-Powered Agreed Earth Chatbot")
#st.subheader("AVA-Abonia Virtual Assistant")

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

# Define a function to clear the input text
def clear_input_text():
    global input_text
    input_text = ""

# We will get the user's input by calling the get_text function
def get_text():
    global input_text
    input_text = st.text_input("Ask your Question", key="input", on_change=clear_input_text)
    return input_text

def main():
    user_input = get_text()

    if user_input:
        output = chat.answer(user_input)
        
        # store the output 
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

    if st.session_state['generated']:
        now = str(datetime.now().date())+'.csv'

        # assign header columns
        headerList = ['Time Stamp', 'Question', 'Answer']

        # open CSV file and assign header
        with open(now, 'w') as file:
            dw = csv.DictWriter(file, delimiter=',',fieldnames=headerList)
            dw.writeheader()

        for i in range(len(st.session_state['generated'])-1, -1, -1):          
       
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')            
            message(st.session_state["generated"][i], key=str(i))
            #timestamp = time.strftime('%d-%m-%Y %H:%M:%S')
            timestamp = datetime.now()


            with open(now,"a") as fp:
                wr = csv.writer(fp, dialect='excel')
                wr.writerow([timestamp,st.session_state['past'][i],st.session_state["generated"][i]])

# Run the app
if __name__ == "__main__":
    main()

