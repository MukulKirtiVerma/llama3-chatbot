# import streamlit as st
# from transformers import AutoTokenizer, AutoModelForCausalLM
# import torch
# from dotenv import load_dotenv
# import os
# from huggingface_hub import login


# load_dotenv()

# huggingface_token = os.getenv("HUGGINGFACE_TOKEN")

# if huggingface_token is None:
#     raise ValueError("Please set the HUGGINGFACE_TOKEN environment variable.")

# login(token=huggingface_token)


# @st.cache_resource
# def load_model():
#     model_name = "meta-llama/Llama-2-7b-chat-hf"
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     model = AutoModelForCausalLM.from_pretrained(
#         model_name,
#         device_map="auto",
#         torch_dtype=torch.float16,
#     )
#     return tokenizer, model

# def generate_response(tokenizer, model, prompt):
#     inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
#     outputs = model.generate(
#         **inputs,
#         max_new_tokens=150,
#         do_sample=True,
#         temperature=0.7,
#         top_p=0.9,
#     )
#     response = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return response[len(prompt):].strip()

# def main():
#     st.title("Llama 3 Chatbot")
#     st.write("Ask me anything!")

#     if "history" not in st.session_state:
#         st.session_state.history = []

#     user_input = st.text_input("You:", key="input")

#     if st.button("Send") or user_input:
#         with st.spinner("Thinking..."):
#             tokenizer, model = load_model()
#             conversation = "\n".join(
#                 [f"User: {item['user']}\nBot: {item['bot']}" for item in st.session_state.history]
#             )
#             prompt = conversation + f"\nUser: {user_input}\nBot:"
#             response = generate_response(tokenizer, model, prompt)
#             st.session_state.history.append({"user": user_input, "bot": response})

#     for chat in st.session_state.history:
#         st.markdown(f"**You:** {chat['user']}")
#         st.markdown(f"**Bot:** {chat['bot']}")

# if __name__ == "__main__":
#     main()

import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


@st.cache_resource
def load_model():
    model_path = "/model"  # Path to your local model directory
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    # Set the pad_token to eos_token if pad_token is not available
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
        device_map="auto",
    )

    # Update the model's pad_token_id
    model.config.pad_token_id = tokenizer.pad_token_id

    return tokenizer, model

def generate_response(tokenizer, model, prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=tokenizer.pad_token_id,  # Explicitly set pad_token_id
    )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Remove the prompt from the response
    return response[len(prompt):].strip()

def main():
    st.title("GPT-Neo Chatbot")
    st.write("Ask me anything!")

    if "history" not in st.session_state:
        st.session_state.history = []

    user_input = st.text_input("You:", key="input")

    if st.button("Send") or user_input:
        with st.spinner("Thinking..."):
            tokenizer, model = load_model()
            # Concatenate conversation history
            conversation = "\n".join(
                [f"User: {item['user']}\nBot: {item['bot']}" for item in st.session_state.history]
            )
            prompt = conversation + f"\nUser: {user_input}\nBot:"
            response = generate_response(tokenizer, model, prompt)
            st.session_state.history.append({"user": user_input, "bot": response})

    # Display conversation
    for chat in st.session_state.history:
        st.markdown(f"**You:** {chat['user']}")
        st.markdown(f"**Bot:** {chat['bot']}")

if __name__ == "__main__":
    main()
