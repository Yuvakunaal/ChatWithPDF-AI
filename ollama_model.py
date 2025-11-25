import ollama
import re

def is_general_greeting(query):
    """Check if the query is a general greeting not related to PDF content"""
    general_phrases = [
        r'hello', r'hi', r'hey', r'greetings',
        r'good morning', r'good afternoon', r'good evening',
        r'how are you', r'what\'s up', r'how do you do',
        r'thank you', r'thanks', r'bye', r'goodbye',
        r'who are you', r'what can you do', r'help'
    ]
    
    query_lower = query.lower().strip()
    
    # Check for exact matches or phrases at the beginning/end of sentences
    for phrase in general_phrases:
        if re.match(rf'^{phrase}[.!?]*$', query_lower) or \
           re.match(rf'^{phrase}\s+', query_lower):
            return True
    
    return False

def ollama_call(pdf_text, user_question):
    # Check if this is a general greeting not related to the PDF
    if is_general_greeting(user_question):
        if user_question.lower().startswith(('hello', 'hi', 'hey', 'greetings', 'yo', 'wassup', 'sup', 'hola', 'namaste', 'heyy', 'hiii', 'hey bro', 'hey man')):
            return "Hello 👋 I'm here to help you with anything in your PDF. Just ask what you want to know!"

        elif user_question.lower().startswith(("how are you", "what's up", "how's everything", "how are things", "doing good", "doing fine", "superb", "fine", "awesome", "great", "fantastic", "amazing", "cool", "perfect", "nice", "mind blowing", "insane")):
            return "I'm doing great and ready to analyze your PDF! Ask me anything from summaries to specific information."

        elif user_question.lower().startswith(('thank', 'appreciate', 'thanks a lot', 'thank you so much', 'tysm', 'thanks buddy', 'thank you bro', 'thanks dear', 'thanks man')):
            return "You're welcome! Always happy to help you understand your PDF better."

        elif user_question.lower().startswith(('bye', 'goodbye', 'ok bye', 'see you', 'catch you later', 'tata', 'cya', 'gtg', 'take care', 'good night', 'goodnight')):
            return "Goodbye! Come back anytime when you want help with another PDF."

        elif user_question.lower().startswith(('who are you', 'what can you do', 'tell about yourself', 'introduce yourself', 'what is your work', 'what is your purpose')):
            return "I'm an AI PDF assistant. I extract the full PDF and answer your questions — summaries, insights, topics, tables, keypoints, anything."

        elif user_question.lower().startswith(('help', 'assist', 'guide me', 'how to use', 'usage', 'what to do', 'confused')):
            return "Upload a PDF and ask anything about it — like 'summarize', 'explain', 'extract dates', 'list tables', 'find topics', etc. I'll read and answer."

        else:
            return "I'm here to help you with your PDF document. What would you like to know about it?"

    prompt = f"""
You are a highly intelligent assistant specialized in extracting, understanding, and reasoning about content from PDF documents. Only use the information provided in the PDF. Do not assume anything that is not explicitly stated.

PDF CONTENT:
{pdf_text}

User Question:
{user_question}

Important Instructions:
1. Always answer using only the PDF content. If the answer is not present, respond exactly: "Not mentioned in the PDF."
2. Keep your answer clear, concise, and relevant to the question.
3. If the question requires a list, table, or bullet points, format it accordingly using plain text.
4. Respect context like sections, headings, tables, and page numbers whenever relevant.
5. Handle dates intelligently if mentioned (e.g., "January 2025" means the whole month; "2024" means the entire year).
6. Avoid adding any external knowledge or assumptions.
7. Summarize lengthy explanations if the user asks for a summary, but provide detailed points if necessary.
8. For multi-part questions, answer each part in order.
9. If the PDF has multiple sections, reference the relevant section if it helps clarify the answer (e.g., "According to Section 2.1…").
10. Always respond in **plain text**, no Markdown or code formatting unless explicitly asked for.
11. If the PDF contains tables, extract relevant rows or columns accurately based on the query.
12. Do not hallucinate numbers, names, or statistics; only report what is present in the PDF.

Answer:
"""

    try:
        response = ollama.chat(model='mistral:instruct', messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])
        
        return response['message']['content']
        
    except Exception as e:
        return "Error: " + str(e)