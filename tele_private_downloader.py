import os
import logging
import time
from datetime import datetime, timezone
from telethon.sync import TelegramClient
from telethon.tl.types import Channel
from telethon.utils import get_display_name
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# Replace these with your own values
api_id = 'your_api_id'  # Replace with your API ID
api_hash = 'your_api_hash'  # Replace with your API Hash
phone_number = 'your_phone_number'  # Replace with your phone number, including country code


# Base download directory
base_download_dir = "downloads"
os.makedirs(base_download_dir, exist_ok=True)

# File to store the last downloaded message ID
offset_file = os.path.join(base_download_dir, "last_downloaded.txt")

# Start date for filtering messages
start_date = datetime(2022, 5, 18, tzinfo=timezone.utc)

def sanitize_filename(filename):
    """Sanitize the filename to make it safe for the filesystem."""
    return "".join(c for c in filename if c.isalnum() or c in " ._-").strip()


def download_files_with_progress(client, message, file_path):
    """Download media files with a progress bar."""
    with tqdm(total=message.file.size, unit='B', unit_scale=True, desc=f"Downloading {os.path.basename(file_path)}") as pbar:
        def progress_callback(current, total):
            pbar.update(current - pbar.n)

        try:
            client.download_media(message.media, file_path, progress_callback=progress_callback)
            pbar.close()
            return True  # Download successful
        except Exception as e:
            pbar.close()
            logger.error(f"Failed to download {file_path}: {e}")
            return False  # Download failed

def get_last_downloaded_id():
    """Read the last downloaded message ID from the offset file."""
    if os.path.exists(offset_file):
        with open(offset_file, "r") as f:
            return int(f.read().strip())
    return None  # No offset file found

def update_last_downloaded_id(message_id):
    """Update the last downloaded message ID in the offset file."""
    with open(offset_file, "w") as f:
        f.write(str(message_id))



def download_files_from_private_channels():
    """Download media files from private Telegram channels."""
    with TelegramClient('my-session', api_id, api_hash) as client:
        logger.info("Fetching private channels...")

        dialogs = client.get_dialogs()
        private_channels = [
            dialog.entity for dialog in dialogs if isinstance(dialog.entity, Channel) and dialog.entity.username is None
        ]

        if not private_channels:
            logger.info("No private channels found.")
            return

        logger.info(f"Found {len(private_channels)} private channels.")

        for channel in private_channels:
            channel_name = sanitize_filename(get_display_name(channel))
            channel_dir = os.path.join(base_download_dir, channel_name)

            os.makedirs(channel_dir, exist_ok=True)
            logger.info(f"\nProcessing channel: {channel_name}")

            # Get the last downloaded message ID for this channel
            last_downloaded_id = get_last_downloaded_id()

            # Ensure offset_id is not None
            offset_id = last_downloaded_id if last_downloaded_id is not None else 0

            try:
                messages = client.iter_messages(channel, offset_date=start_date, offset_id=offset_id, reverse=True)
            except Exception as e:
                logger.error(f"Error fetching messages from {channel_name}: {e}")
                continue

            for message in tqdm(messages, desc=f"Messages in {channel_name}", unit="msg"):
                if not hasattr(message, 'media') or message.media is None:
                    logger.debug(f"Skipping message {message.id}: No media found.")
                if not hasattr(message, 'file') or message.file is None:
                    logger.debug(f"Skipping message {message.id}: File attribute missing.")
                    continue  # Skip messages without a file attribute

                file_name = sanitize_filename(message.file.name or f"file_{message.id}")
                file_path = os.path.join(channel_dir, file_name)

                # Check if the file already exists and compare sizes
                if os.path.exists(file_path):
                    existing_size = os.path.getsize(file_path)
                    if existing_size == message.file.size:
                        logger.debug(f"File already exists and is the same size, skipping: {file_path}")
                        update_last_downloaded_id(message.id)  # Update offset even if file exists
                        continue  # Skip if the file exists and sizes match
                    else:
                        logger.info(f"File exists but size differs, downloading: {file_path}")
                else:
                    logger.info(f"File does not exist, downloading: {file_path}")

                # Download the file
                if download_files_with_progress(client, message, file_path):
                    update_last_downloaded_id(message.id)  # Update offset after successful download
                time.sleep(1)  # Add a delay to avoid rate limits

if __name__ == "__main__":
    download_files_from_private_channels()
