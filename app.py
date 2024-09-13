import streamlit as st
import openai
from pinecone import Pinecone
import requests
from streamlit_lottie import st_lottie
from openai import OpenAI

st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto",
)

# Initialize OpenAI API key
openai.api_key = st.secrets["openai_api_key"]
pine_cone_api_key = st.secrets["pinecone_api_key"]
# Initialize Pinecone
pc = Pinecone(api_key=pine_cone_api_key)
index = pc.Index("chatbot")


# Load Lottie animation from URL
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load animations
lottie_question = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_j1adxtyb.json")  # Replace with desired animation
lottie_loading = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_usmfx6bp.json")  # Loading animation

# Custom CSS styling
st.markdown("""
    <style>
    /* Center the main content */
    .main {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }

    /* Style for the title */
    .title {
        font-size: 50px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
    }

    /* Style for the input area */
    textarea {
        font-size: 18px !important;
    }

    /* Style for the answer box */
    .answer {
        background-color: #F0F8FF;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        font-size: 18px;
    }

    /* Style for buttons */
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 10px 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Your functions (unchanged)
def get_openai_embeddings(text):
    response = openai.embeddings.create(input=text, model="text-embedding-ada-002")
    # Access the embedding directly from the 'data' field
    embedding = response.data[0].embedding
    return embedding

def query_pinecone(query_text):
    try:
        # Generate embedding for the query text
        query_embedding = get_openai_embeddings(query_text)

        # Debugging: Check the length of the embedding
        print(f"Query embedding length: {len(query_embedding)}")
        
        # Ensure embedding is the correct length for the Pinecone index
        if len(query_embedding) != 1536:
            raise ValueError(f"Embedding dimension mismatch: Expected 1536, got {len(query_embedding)}")

        # Perform the query in Pinecone using the updated syntax
        query_result = index.query(  # You can set a custom namespace if necessary
            vector=query_embedding,  # Use vector instead of queries
            top_k=5,  # Return top 5 matches
            include_values=False,  # Whether to include the vectors in the result
            include_metadata=True
        )

        # Check if matches are found
        if query_result['matches']:
            # Print the relevant matches with metadata and score
            return query_result
        else:
            print("No matches found.")
            return None

    except Exception as e:
        # Handle any potential errors in querying
        print(f"Error querying Pinecone: {str(e)}")
        return None

def get_answer_from_openai(context, question):
    try:
        # Initialize the OpenAI client
        client = OpenAI(api_key=st.secrets["openai_api_key"])
        
        # Combine context and question into the messages array
        messages = [
            {"role": "system", "content": "You are a sre bot trying to help sre engineers to debug issues"},
            {"role": "user", "content": f"The following is relevant context:\n{context}\n\nQuestion: {question}"}
        ]
        
        # Use the new way to call chat completions
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # Use the appropriate model as per your requirement
            messages=messages,
            max_tokens=150,  # Adjust based on how long you want the answer to be
            temperature=0.2  # Adjust for more or less randomness
        )
        
        # Extract the content of the response
        return completion.choices[0].message.content

    except Exception as e:
        print(f"Error generating answer from OpenAI: {str(e)}")
        return None

# Now combine the two functions (query and answer generation)
def answer_question_using_context(question):
    try:
        # Step 1: Query Pinecone for relevant context
        query_result = query_pinecone(question)

        # Step 2: If context is found, combine it and pass to OpenAI
        if query_result:
            context = ""
            for match in query_result['matches']:
                context += f"ID: {match['id']}, Metadata: {match['metadata']}, Content: {match['metadata'].get('content', '')}\n"
        else:
            context = "No relevant context found in the database."

        # Step 3: Get the answer from OpenAI based on the context
        answer = get_answer_from_openai(context, question)
        intro_message = "Hi, this is the intl-sre bot helping with queries regarding incidents.\n"
        return intro_message + answer

    except Exception as e:
        print(f"Error answering the question: {str(e)}")
        return None

# Streamlit App Layout
def main():
    # Set the page configuration
    # st.set_page_config(page_title="SRE BOT", page_icon="❓", layout="centered")

    # Display the title with custom styling
    st.markdown("<h1 class='title'>AI-Powered Q&A App</h1>", unsafe_allow_html=True)

    # Display the Lottie animation
    st_lottie(lottie_question, height=200)

    # Description
    st.write("Ask any question, and the INTL-SRE bot will provide an answer based on the relevant context from the database.")

    # Input Text Area for the Question
    question = st.text_area("Enter your question below:", height=150)

    # Button to Submit the Question
    if st.button("Get Answer"):
        if question.strip():
            with st.spinner("Analyzing your question and fetching the answer..."):
                # Get the answer
                answer = answer_question_using_context(question)
                if answer:
                    st.markdown("<div class='answer'><b>Answer:</b><br>" + answer + "</div>", unsafe_allow_html=True)
                else:
                    st.error("Could not generate an answer. Please try again.")
        else:
            st.warning("Please enter a question.")

    # Footer
    st.markdown("""
        <hr>
        <div style='text-align: center;'>
            Made by [Pavan (pavanguduru.netlify.app/)
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
