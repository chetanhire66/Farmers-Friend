import google.generativeai as genai

API_KEY = "AIzaSyDX7joqUHHK7gqvvuWE3evfUIiCxYg-3ko"
genai.configure(api_key=API_KEY)

gemini_model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction="""
    You are Smart Crop Advisor.
    Give advice on crop recommendations, pest control, and fertilizers.
    Always respond politely and concisely.
    """
)

gemini_chat = gemini_model.start_chat(history=[])

def gimini(text_input, language="en"):
    """
    text_input: farmer's question
    language: 'en' (English), 'hi' (Hindi), 'mr' (Marathi)
    """

    try:
        # Modify input based on language
        if language == "hi":
            text_input = f"कृपया हिंदी में उत्तर दें: {text_input}"
        elif language == "mr":
            text_input = f"कृपया मराठीत उत्तर द्या: {text_input}"

        response = gemini_chat.send_message(text_input)
        response_text = response.text.strip()
        print(f"Gemini ({language}):", response_text)
        return response_text  

    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            response_text = "⚠️ Daily limit reached. Try tomorrow or upgrade plan."
        else:
            response_text = "❌ Sorry, something went wrong with Gemini."
        
        print("Gemini Error:", error_msg)
        return response_text  
