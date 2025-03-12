# Telegram Private Channel Media Downloader

A Python script that automatically downloads media files from private Telegram channels you are a member of. The script filters messages from a specified date and saves all media attachments to organized local directories.

## Changes

- Checks if the file size and the downloaded file size are equal
- Saves the last downloaded message id to skip already downloaded medias
- Uses the logging  module to display more information
- Added delay to avoid rate limites
- Fixed some minor bugs

## Features

- Downloads media files from private Telegram channels
- Organizes downloads by channel name
- Includes progress bars for both overall progress and individual file downloads
- Skips existing files to avoid duplicates
- Sanitizes filenames to prevent system compatibility issues
- Filters messages by date
- Handles download errors gracefully

## Prerequisites

- Python 3.6 or higher
- Telegram API credentials (api_id and api_hash)
- Active Telegram account
- Member access to the private channels you want to download from

## Required Python Packages

```bash
pip install telethon tqdm
```

## Setup

1. First, obtain your Telegram API credentials:
   - Go to https://my.telegram.org/apps
   - Log in with your phone number
   - Create a new application if you haven't already
   - Note down your `api_id` and `api_hash`

2. Clone or download this script to your local machine.

3. Configure the script by replacing the placeholder values at the top of the script:
   ```python
   api_id = 'your_api_id'        # Replace with your API ID
   api_hash = 'your_api_hash'    # Replace with your API Hash
   phone_number = 'your_phone_number'  # Include country code
   ```

4. (Optional) Modify the start date filter if needed:
   ```python
   start_date = datetime(2024, 4, 1, tzinfo=timezone.utc)
   ```

## Usage

1. Run the script:
   ```bash
   python telegram_downloader.py
   ```

2. On first run, you'll be prompted to:
   - Enter your phone number
   - Enter the verification code sent to your Telegram account
   - (Optionally) Enter your 2FA password if enabled

3. The script will then:
   - Fetch all your private channels
   - Create a directory structure for downloads
   - Download media files from messages after the specified start date
   - Show progress bars for the download process

## Directory Structure

Downloads are organized as follows:
```
downloads/
├── Channel_Name_1/
│   ├── file1.jpg
│   ├── file2.pdf
│   └── ...
├── Channel_Name_2/
│   ├── file1.mp4
│   └── ...
└── ...
```

## Features Explained

### File Sanitization
- The script sanitizes channel names and filenames to ensure compatibility across different operating systems
- Special characters are removed or replaced
- Spaces and common punctuation are preserved

### Progress Tracking
- Overall progress bar shows the number of messages being processed
- Individual file progress bars show download progress with size and speed
- Clear console output indicates current channel and file being processed

### Error Handling
- Gracefully handles download failures
- Skips existing files to prevent duplicates
- Continues operation even if individual downloads fail

### Date Filtering
- Only downloads media from messages after the specified start date
- Helps manage download size and focus on recent content
- Can be modified to use different date ranges

## Limitations

- Only downloads from private channels (channels without a public username)
- Requires membership in the channels
- Subject to Telegram's rate limits and restrictions
- Downloads all media types (no filtering by file type)

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Safety Note

Please ensure you have permission to download and store media content from the channels you're accessing. Respect copyright and intellectual property rights when using this tool.

## Troubleshooting

1. **Authentication Issues**
   - Ensure your API credentials are correct
   - Check if your phone number is in the correct format
   - Verify your Telegram account is active and not restricted

2. **Download Errors**
   - Check your internet connection
   - Verify you have sufficient disk space
   - Ensure you have write permissions in the download directory

3. **Rate Limiting**
   - If you encounter rate limits, the script will handle them automatically
   - Consider adding delays between downloads if needed

## Support

For issues, questions, or contributions, please open an issue in the repository.
