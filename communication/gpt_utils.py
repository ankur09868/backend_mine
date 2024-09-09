from communication.models import Conversation
from openai import OpenAI
import os



def generate_reply_from_conversation(conversation_id, platform):
    try:
        # Retrieve the conversation object
        conversation = Conversation.objects.get(conversation_id=conversation_id)
        
        # Access the messages field (which is a single text string)
        messages_text = conversation.messages
        
        # Split the messages into a list based on your delimiter
        # Assuming messages are separated by newlines
        messages_list = messages_text.split('\n')  # Adjust splitting logic as needed
        
        # Extract the latest message from the list
        if messages_list:
            latest_message = messages_list[-1].strip()  # Get the last message
            full_conversation = "\n".join(messages_list)  # Combine all messages for context
        else:
            return "No messages found in this conversation."

        # Prepare the GPT prompt based on the platform
        if platform == "whatsapp":
            system_content = "You are a helpful assistant for generating casual WhatsApp messages."
        elif platform == "instagram":
            system_content = "You are a helpful assistant for generating engaging Instagram DM responses."
        elif platform == "email":
            system_content = "You are a professional assistant for generating email responses."
        else:
            return "Unsupported platform for generating a reply."

        # Initialize OpenAI client
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Generate a response from GPT using both the full conversation and latest message
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": f"Here is the full conversation:\n{full_conversation}\n\nLatest message:\n{latest_message}\n\nGenerate a reply based on the above context and latest message."}
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Extract the generated reply
        gpt_reply = response.choices[0].message.content.strip()

        return gpt_reply

    except Conversation.DoesNotExist:
        return "Conversation with the given ID does not exist."
    except Exception as e:
        return f"An error occurred: {str(e)}"

    except Conversation.DoesNotExist:
        return "Conversation with the given ID does not exist."
    except Exception as e:
        return f"An error occurred: {str(e)}"
def prepare_gpt_prompt(sentiment_score, channel, topics=None):
    # Define tone and message components based on sentiment score
    if sentiment_score < 1.0:
        tone = "deeply empathetic and compassionate"
        additional_notes = (
            "The customer is likely experiencing significant distress or dissatisfaction. "
            "Craft a response that deeply acknowledges their feelings, expresses genuine concern, "
            "and provides specific, actionable assistance to address their issues."
        )
    elif sentiment_score < 2.0:
        tone = "empathetic and understanding"
        additional_notes = (
            "The customer may be experiencing frustration or sadness. Acknowledge their emotions, "
            "show understanding, and offer clear, actionable help to resolve their concerns."
        )
    elif sentiment_score < 3.0:
        tone = "supportive and reassuring"
        additional_notes = (
            "The customer might need reassurance and support. Emphasize that you are here to assist, "
            "and provide comforting guidance or solutions. Ensure your message is encouraging and helpful."
        )
    elif sentiment_score < 4.0:
        tone = "positive and uplifting"
        additional_notes = (
            "The customer has a generally positive outlook. Maintain a friendly and optimistic tone, "
            "and encourage continued engagement or action. Highlight positive aspects and express enthusiasm."
        )
    else:
        tone = "enthusiastic and encouraging"
        additional_notes = (
            "The customer is highly satisfied or positive. Use a very upbeat and motivating tone, "
            "celebrate their positive experience, and encourage further interaction or action."
        )

    # Customize message based on the communication channel
    if channel == "email":
        channel_specifics = (
            "Craft an email that is professional yet warm. Start with a friendly greeting, "
            "acknowledge the customer's recent interaction or query, and offer assistance or next steps."
        )
    elif channel == "whatsapp":
        channel_specifics = (
            "Craft a WhatsApp message that is conversational and to the point. Use a friendly and informal tone, "
            "and offer quick assistance or a clear next step."
        )
    elif channel == "instagram":
        channel_specifics = (
            "Craft an Instagram DM that is engaging and concise. Use a friendly and approachable tone, "
            "suitable for social media interaction. Offer help or a call to action."
        )
    else:
        channel_specifics = (
            "Craft a message suitable for the chosen communication channel. Keep the tone friendly and appropriate for the medium."
        )

    # Format topics for the prompt if they exist
    topics_info = f"- Relevant topics identified: {', '.join(topics)}." if topics else "- No specific topics identified."

    return f"""
    Craft a personalized {channel} message for a customer based on the following guidelines:

    - The sentiment score is {sentiment_score:.2f}, which indicates a {tone} approach is needed.
    - Channel: {channel}.
    
    Message Requirements:
    - {channel_specifics}
    - The tone should be {tone}.
    - Start with a warm greeting.
    - Address the customer in a friendly and approachable manner.
    - Avoid mentioning specific details like sentiment score directly.
    - Show appreciation for the customer's interaction and express a willingness to assist if needed.

    Additional Notes:
    - {additional_notes}
    {topics_info}
    """
