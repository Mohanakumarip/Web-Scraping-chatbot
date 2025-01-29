import requests
from bs4 import BeautifulSoup
from transformers import pipeline

# Step 1: Extract content from the website
def extract_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract only text content (e.g., from <p> tags)
        paragraphs = soup.find_all('p')
        content = "\n".join([p.get_text() for p in paragraphs if p.get_text()])
        
        return content
    except requests.exceptions.RequestException as e:
        return f"Error fetching content: {e}"

# Step 2: Preprocess the content (can add more processing if needed)
def preprocess_content(content):
    return content.strip()  # Remove leading/trailing whitespace

# Step 3: Build a chatbot using a Question-Answering model
def build_chatbot(content):
    # Initialize a pre-trained question-answering pipeline
    qa_pipeline = pipeline("question-answering")
    
    def chatbot(question):
        result = qa_pipeline({
            "context": content,
            "question": question
        })
        return result['answer']
    
    return chatbot

# Example Usage
if __name__ == "__main__":
    url = input("Enter the website URL: ")
    print("Extracting content...")
    raw_content = extract_content(url)
    
    if "Error fetching content" in raw_content:
        print(raw_content)
    else:
        content = preprocess_content(raw_content)
        print("Content extracted successfully!")
        
        chatbot = build_chatbot(content)
        
        print("\nChatbot is ready! Ask your questions (type 'exit' to quit):")
        while True:
            user_question = input("You: ")
            if user_question.lower() == 'exit':
                print("Goodbye!")
                break
            answer = chatbot(user_question)
            print(f"Chatbot: {answer}")
