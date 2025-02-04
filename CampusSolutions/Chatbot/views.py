# implemneting the chatbot logic
from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Initialize Gemini API
genai.configure(api_key=API_KEY)


@csrf_exempt
@login_required(login_url="/")
def chatbot(request):
    if request.method == "POST":
        try:
            # Get the user message from the request
            data = json.loads(request.body)
            user_message = data.get("message", "")

            # Use the Gemini API
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(user_message)

            # Extract the chatbot's response text
            bot_response = (
                response.text if response.text else "I couldn't generate a response."
            )

            # Return JSON response
            return JsonResponse({"response": bot_response})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # Render the chat template for GET requests
    return render(request, "chat.html")
