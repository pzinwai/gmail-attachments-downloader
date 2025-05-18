# Gmail Attachments Downloader

📎 📥 A simple Python program to log in to your Gmail account via IMAP, search for emails by subject keyword, and download attachments from those emails to a local folder.

---

## Features

- Secure login with Gmail (using App Password recommended)
- Search emails by subject keyword or download from all emails
- Download all attachments from matching emails
- Save attachments in a local `attachments` folder
- Retry login and search until successful or user quits

---

## Prerequisites

- Python 3.x installed
- Internet connection

---

## How to Create a Gmail App Password

Due to Google's security policies, using your regular Gmail password with IMAP may fail if 2-Step Verification is enabled or if "Less secure app access" is disabled. The recommended way is to create an **App Password**:

1. **Enable 2-Step Verification** on your Google account if you haven't already:
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Under **"Signing in to Google"**, click **2-Step Verification** and follow the steps.

2. **Generate an App Password:**
   - Go to [App Passwords](https://myaccount.google.com/apppasswords) (you must be signed in)
   - Select **Mail** as the app and **Other (Custom name)** as the device (you can name it e.g. "GmailAttachmentDownloader")
   - Click **Generate**
   - Copy the 16-character password generated (without spaces)

3. Use this app password instead of your normal Gmail password when prompted by the program.

---

## Installation

1. Clone or download this repository.
   ```bash
   git clone https://github.com/pzinwai/gmail-attachment-downloader.git
   cd gmail-attachment-downloader
   ```
2. Install any dependencies (standard Python libraries used, no extra packages needed).

3. Run the program:
   ```bash
   python app.py
   ```

## 💡 What You'll Be Prompted For

1. Gmail Email – enter your full email address

2. Password – enter the App Password (not your regular Gmail password)

3. Search Keyword – enter a keyword to filter emails by subject (or press Enter to select all)

4. Download Confirmation – confirm you want to save attachments

Attachments will be saved in the local `attachments/` folder automatically.

## Notes

1. Only attachments from emails matching your search keyword will be downloaded.

2. Emails without attachments or non-multipart emails are skipped.

3. You can retry login or searches as many times as needed.

4. Interrupt the program anytime with `Ctrl + C`.


## Troubleshooting

`Login failed`: Make sure you are using an app password, not your regular Gmail password.

`No attachments found`: Try a different search keyword or check if emails have attachments.

`IMAP access issues`: Ensure IMAP is enabled in your Gmail settings (Gmail Settings > Forwarding and POP/IMAP > Enable IMAP).

## License
This project is provided as-is, feel free to modify and use it as you like.

## Contact
Developed by [Phyo Zin Wai](https://www.phyozinwai.com)

Happy attachment downloading!