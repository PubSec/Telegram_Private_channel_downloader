from telethon.sync import TelegramClient
from telethon.tl.types import Channel
from telethon.utils import get_display_name
from datetime import datetime, timezone
import os
from tqdm import tqdm  # Progress bar library

# Replace these with your own values
api_id = 'your_api_id'  # Replace with your API ID
api_hash = 'your_api_hash'  # Replace with your API Hash
phone_number = 'your_phone_number'  # Replace with your phone number, including country code

base_download_dir = "downloads"

os.makedirs(base_download_dir, exist_ok=True)

# Specify the start date for filtering messages (with UTC timezone)
start_date = datetime(2024, 4, 1, tzinfo=timezone.utc)  # Messages from April 2024 onwards

def sanitize_filename(filename):
    return "".join(c for c in filename if c.isalnum() or c in " ._-").strip()

def download_files_with_progress(client, message, file_path):
    with tqdm(total=message.file.size, unit='B', unit_scale=True, desc=f"Downloading {os.path.basename(file_path)}") as pbar:
        def progress_callback(current, total):
            pbar.update(current - pbar.n)

        try:
            client.download_media(message.media, file_path, progress_callback=progress_callback)
            pbar.close()
        except Exception as e:
            pbar.close()
            print(f"Failed to download {file_path}: {e}")

def download_files_from_private_channels():
    with TelegramClient('session_name', api_id, api_hash) as client:
        print("Fetching private channels...")

        dialogs = client.get_dialogs()

        private_channels = [
            dialog.entity for dialog in dialogs if isinstance(dialog.entity, Channel) and dialog.entity.username is None
        ]

        if not private_channels:
            print("No private channels found.")
            return

        print(f"Found {len(private_channels)} private channels.")

        for channel in private_channels:
            channel_name = sanitize_filename(get_display_name(channel))
            channel_dir = os.path.join(base_download_dir, channel_name)

            os.makedirs(channel_dir, exist_ok=True)
            print(f"\nProcessing channel: {channel_name}")

            messages = [
                msg for msg in client.iter_messages(channel) 
                if msg.media and msg.date >= start_date
            ]

            if not messages:
                print(f"No media found in {channel_name} from April 2024 onwards.")
                continue

            for message in tqdm(messages, desc=f"Messages in {channel_name}", unit="msg"):
                file_path = os.path.join(channel_dir, sanitize_filename(message.file.name or f"file_{message.id}"))
                if os.path.exists(file_path):
                    print(f"File already exists, skipping: {file_path}")
                else:
                    download_files_with_progress(client, message, file_path)

if __name__ == "__main__":
    download_files_from_private_channels()
