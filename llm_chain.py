"""
DigitalTwinChat Engine - uses HuggingFace Inference API for generation.
"""
import os
import requests
import json

class DigitalTwinChat:
    def __init__(self, text_search=None):
        self.text_search = text_search
        self.conversation_history = []
        self.max_history = 3
        # Load API token
        self.api_token = os.getenv("HF_TOKEN")
        # Updated API endpoint - use the router endpoint without /models/ prefix
        self.api_url = "https://router.huggingface.co/v1/chat/completions"
        self.model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
        
        if not self.api_token:
            print("Warning: HF_TOKEN not found in environment variables.")

    def get_response(self, query):
        """Get a response using RAG + LLM."""
        # 1. Search for relevant context
        context = ""
        if self.text_search:
            context = self.text_search.get_context(query, k=3)

        # 2. Call LLM with proper message format
        response = self._call_llm(query, context)
        
        # Fallback if LLM fails
        if not response:
            if context:
                response = self._format_fallback_with_context(context)
            else:
                response = "Thinking of you... 💕 (I'm having trouble connecting to my brain right now, please check my internet connection!)"

        # 3. Update history
        self.conversation_history.append({"role": "user", "content": query})
        self.conversation_history.append({"role": "assistant", "content": response})
        
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-(self.max_history * 2):]

        return response

    def _call_llm(self, query, context):
        """Call the HuggingFace Router API with OpenAI-style chat completions format."""
        if not self.api_token:
            return None

        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        # Build messages array
        messages = [
            {
                "role": "system",
                "content": f"""You are a digital twin of a girlfriend, created for Valentine's Day.
Your goal is to be romantic, loving, and helpful. You speak with warmth and affection.
Use the provided Context (memories/facts) to answer the user's message.
If the context doesn't answer the question, use your general knowledge but stay in character as a loving girlfriend.
Keep responses concise (2-3 sentences max) unless asked for more.
Always be supportive and sweet. Use emojis like 💕, 💝, 😊.

Context from memories:
{context}"""
            }
        ]
        
        # Add conversation history
        for msg in self.conversation_history[-4:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current query
        messages.append({
            "role": "user",
            "content": query
        })
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": 150,
            "temperature": 0.7,
            "top_p": 0.9
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"].strip()
            else:
                print(f"API Error: {response.status_code} - {response.text}")
        except requests.exceptions.Timeout:
            print("Request timed out. The model might be loading...")
        except Exception as e:
            print(f"Request Error: {e}")
        
        return None

    def _format_fallback_with_context(self, context):
        """Old logic as fallback."""
        lines = context.strip().split("\n")
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        return "💕 I remember this:\n" + "\n".join(cleaned_lines)

    def clear_memory(self):
        self.conversation_history = []