import asyncio
import io
import requests
from PIL import Image
from pyrogram import filters
from pyrogram.enums import ChatAction
from Equinox import Equinox

API_URL = "https://api-inference.huggingface.co/models/dataautogpt3/ProteusV0.2"
API_URL2 = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": "Bearer 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"}

async def generate_image(prompt):
    try:
        payload = {"inputs": prompt}
        response = requests.post(API_URL, headers=headers, json=payload)
        image_bytes = response.content
        return image_bytes
    except:
        payload = {"inputs": prompt}
        response = requests.post(API_URL2, headers=headers, json=payload)
        image_bytes = response.content
        return image_bytes

@Equinox.on_message(filters.command("imagine","draw","create"))
async def generate_images_command(client, message):
    try:
        if len(message.command) == 1:
            await message.reply_text("Please provide a prompt for generating the images.")
            return

        prompt = " ".join(message.command[1:])
        await Equinox.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
        # Generate four images asynchronously
        image_tasks = [generate_image(prompt) for _ in range(4)]
        image_bytes_list = await asyncio.gather(*image_tasks)

        for image_bytes in image_bytes_list:
            if image_bytes:
                image = Image.open(io.BytesIO(image_bytes))
                # Sending the image to the user
                image_io = io.BytesIO()
                image.save(image_io, format='PNG')
                image_io.seek(0)
                await Equinox.send_photo(chat_id=message.chat.id, photo=image_io, caption="Image generated sucessfully!")      
            else:
                await message.reply_text("Sorry, failed to generate one of the images.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")