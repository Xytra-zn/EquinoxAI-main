import requests
from pyrogram import filters
from pyrogram.enums import ChatAction
from Equinox import Equinox

API_URL = "https://api-inference.huggingface.co/models/toloka/t5-large-for-text-aggregation"
headers = {"Authorization": "Bearer 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"}

def summarize_text(text):
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    output = response.json()
    if 'summary_text' in output:
        return output['summary_text']
    else:
        return None

@Equinox.on_message(filters.command("summarize","summaries"))
async def summarize_text_command(client, message):
    try:
        if len(message.command) < 2:
            if message.reply_to_message and message.reply_to_message.text:
                text = message.reply_to_message.text
                await Equinox.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
            else:
                await message.reply_text("Please provide the text you want to summarize.")
                return
        else:
            text = " ".join(message.command[1:])

        summary = summarize_text(text)
        if summary:
            await message.reply_text(summary)
        else:
            await message.reply_text("Failed to summarize the text.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")