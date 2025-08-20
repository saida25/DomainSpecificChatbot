# chatbot_app/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_optional
import json
import uuid
import requests
from .models import ChatSession, ChatMessage

@login_optional
def chat_interface(request):
    """Main chat interface"""
    # Generate or get session ID
    session_id = request.session.get('chat_session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session['chat_session_id'] = session_id
        
        # Create chat session in database
        chat_session = ChatSession.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_id=session_id
        )
    
    return render(request, 'chat.html', {'session_id': session_id})

@csrf_exempt
def send_message(request):
    """Send message to Rasa and get response"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message')
            session_id = data.get('session_id')
            
            if not message or not session_id:
                return JsonResponse({'error': 'Missing message or session_id'}, status=400)
            
            # Get or create chat session
            chat_session, created = ChatSession.objects.get_or_create(
                session_id=session_id,
                defaults={'user': request.user if request.user.is_authenticated else None}
            )
            
            # Save user message
            user_message = ChatMessage.objects.create(
                session=chat_session,
                message=message,
                is_user=True
            )
            
            # Send message to Rasa server
            rasa_url = "http://localhost:5005/webhooks/rest/webhook"
            payload = {
                "sender": session_id,
                "message": message
            }
            
            try:
                response = requests.post(rasa_url, json=payload)
                response.raise_for_status()
                rasa_response = response.json()
                
                # Extract bot response
                bot_response = ""
                for response_item in rasa_response:
                    if 'text' in response_item:
                        bot_response += response_item['text'] + "\n"
                    if 'image' in response_item:
                        bot_response += f"[Image: {response_item['image']}]\n"
                
                bot_response = bot_response.strip()
                
                # Save bot response
                bot_message = ChatMessage.objects.create(
                    session=chat_session,
                    message=bot_response,
                    is_user=False
                )
                
                return JsonResponse({
                    'success': True,
                    'bot_response': bot_response,
                    'message_id': bot_message.id
                })
                
            except requests.exceptions.RequestException as e:
                # Fallback response if Rasa server is not available
                fallback_response = "I'm currently unavailable. Please try again later."
                
                bot_message = ChatMessage.objects.create(
                    session=chat_session,
                    message=fallback_response,
                    is_user=False
                )
                
                return JsonResponse({
                    'success': True,
                    'bot_response': fallback_response,
                    'message_id': bot_message.id
                })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def chat_history(request, session_id):
    """Get chat history for a session"""
    try:
        chat_session = ChatSession.objects.get(session_id=session_id)
        messages = ChatMessage.objects.filter(session=chat_session).order_by('timestamp')
        
        message_list = []
        for message in messages:
            message_list.append({
                'id': message.id,
                'message': message.message,
                'is_user': message.is_user,
                'timestamp': message.timestamp.isoformat(),
                'intent': message.intent,
                'confidence': message.confidence
            })
        
        return JsonResponse({
            'success': True,
            'messages': message_list,
            'session_id': session_id
        })
        
    except ChatSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)

@login_optional
def clear_chat(request, session_id):
    """Clear chat history for a session"""
    try:
        chat_session = ChatSession.objects.get(session_id=session_id)
        ChatMessage.objects.filter(session=chat_session).delete()
        
        return JsonResponse({'success': True})
        
    except ChatSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)