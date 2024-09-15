# AI-Powered Q&A App with Pinecone and OpenAI

An interactive Streamlit application that leverages Pinecone's vector database and OpenAI's language models to provide context-aware answers to user queries.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Introduction

This application is designed to assist SRE (Site Reliability Engineering) engineers by providing answers to questions based on relevant context retrieved from a Pinecone vector database. It uses OpenAI's language models to generate accurate and helpful responses.

## Features

- **Interactive Interface**: Built with Streamlit for a seamless user experience.
- **Contextual Responses**: Retrieves relevant context from Pinecone to enhance answer accuracy.
- **OpenAI Integration**: Utilizes GPT-based models for generating responses.
- **Custom Styling and Animations**: Enhanced UI with custom CSS and Lottie animations.
- **Error Handling**: Robust error handling for API calls and data retrieval.

## Architecture

1. **User Input**: The user enters a question into the Streamlit app.
2. **Embedding Generation**: The app generates an embedding for the question using OpenAI's embedding model (`text-embedding-ada-002`).
3. **Pinecone Query**: The embedding is used to query the Pinecone vector database to retrieve relevant context.
4. **Response Generation**: The retrieved context and the user's question are sent to OpenAI's language model to generate an answer.
5. **Display Output**: The app displays the generated answer to the user.

## Prerequisites

- Python 3.7 or higher
- **API Keys**:
  - OpenAI API Key
  - Pinecone API Key
- Streamlit account (for managing secrets)
- Pinecone index named `chatbot` with the appropriate vector dimension (1536 for `text-embedding-ada-002`)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/ai-powered-qa-app.git
   cd ai-powered-qa-app
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

   **`requirements.txt` should include:**

   ```
   streamlit
   openai
   pinecone-client
   streamlit-lottie
   requests
   ```

4. **Set Up Streamlit Secrets**

   Create a `.streamlit` directory and a `secrets.toml` file:

   ```bash
   mkdir .streamlit
   touch .streamlit/secrets.toml
   ```

   Add your API keys to `secrets.toml`:

   ```toml
   [default]
   openai_api_key = "YOUR_OPENAI_API_KEY"
   pinecone_api_key = "YOUR_PINECONE_API_KEY"
   ```

## Usage

1. **Run the Application**

   ```bash
   streamlit run app.py
   ```

2. **Interact with the App**

   - Open the URL provided by Streamlit in your browser.
   - Enter your question in the text area provided.
   - Click on **"Get Answer"** to receive a response.

## Customization

- **OpenAI Model Selection**

  In the `get_answer_from_openai` function, you can change the model by modifying the `model` parameter:

  ```python
  completion = client.chat.completions.create(
      model="gpt-4",  # Change to your preferred model
      ...
  )
  ```

- **Pinecone Index**

  Ensure the Pinecone index name matches your setup:

  ```python
  index = pc.Index("your_pinecone_index_name")
  ```

- **Styling**

  Modify the CSS in the `st.markdown` section to customize the app's appearance.

- **Animations**

  Replace Lottie animation URLs in the `load_lottieurl` function with your desired animations.

## Troubleshooting

- **Embedding Dimension Mismatch**

  If you encounter an error about embedding dimensions, ensure your Pinecone index is configured with the correct vector dimension (usually 1536 for `text-embedding-ada-002`).

- **API Errors**

  - Make sure your API keys are valid and have the necessary permissions.
  - Check your internet connection.

- **Module Import Errors**

  Ensure all required packages are installed and up to date.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **[OpenAI](https://openai.com/)** for the language models.
- **[Pinecone](https://www.pinecone.io/)** for the vector database services.
- **[Streamlit](https://streamlit.io/)** for the interactive app framework.
- **[LottieFiles](https://lottiefiles.com/)** for the animations.
- Created by [Pavan](https://pavanguduru.netlify.app/)

---

Feel free to customize this README to better suit your project's needs!
