import imaplib
import os
import email
import sys
import getpass
import time

class GmailAttachmentsDownloader:
    def __init__(self):
        self.initialize_variables()
        self.hello()

        # Retry login until successful or user quits
        while True:
            self.get_login()
            if self.attempt_login():
                break
            retry = input("\n🔁 Do you want to try logging in again? (y/n): ").lower().strip()
            if retry != 'y':
                print("\n👋 Exiting the program. Goodbye!")
                sys.exit()

        if not self.select_mailbox():
            print(f"\n📭 Could not select mailbox '{self.mailbox}' or it has no messages.")
            sys.exit()

        # Search loop until user wants to exit or results found
        while True:
            self.search_through_mailbox()
            if self.mail_count == 0:
                retry = input("\n🔁 No matching emails found. Would you like to search again? (y/n): ").lower().strip()
                if retry != 'y':
                    print("\n👋 Exiting the program. Goodbye!")
                    sys.exit()
            else:
                break

        if not self.confirm_download():
            print("\n🛑 User aborted the program.")
            sys.exit()

        self.parse_emails()

        print(f"✅ All done! Attachments saved in: {self.dest_folder}")

    def initialize_variables(self):
        self.usr = ""
        self.pwd = ""
        self.mail = None
        self.mailbox = "Inbox"
        self.mail_count = 0
        self.dest_folder = os.path.join(os.getcwd(), "attachments")
        self.data = []
        self.ids = []
        self.ids_list = []
        self.search_keyword = None

    def hello(self):
        print("\n📥 Welcome to Gmail Attachments Downloader")
        print("\n🛠️ Developed by Phyo Zin Wai\n")

    def get_login(self):
        print("🔐 Please enter your Gmail login credentials.")
        self.usr = input("Email: ")
        self.pwd = getpass.getpass("Password: ")

    def attempt_login(self):
        try:
            self.mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
            self.mail.login(self.usr, self.pwd)
            print("\n✅ \033[32mLogin successful!\033[0m")
            return True
        except imaplib.IMAP4.error as e:
            print(f"\n❌ \033[91mLogin failed: {e}\033[0m")
            return False

    def select_mailbox(self):
        try:
            status, count = self.mail.select(self.mailbox)
            if status == "OK":
                self.mail_count = int(count[0].decode("utf-8"))
                return True
            return False
        except Exception as e:
            print(f"\n❌ Error selecting mailbox: {e}")
            return False

    def search_through_mailbox(self):
        self.search_keyword = input("\n🔍 Enter keyword to search email subjects (leave empty to search all): ").strip()
        if self.search_keyword:
            escaped_keyword = self.search_keyword.replace('"', '\\"')
            search_criteria = f'SUBJECT "{escaped_keyword}"'
        else:
            search_criteria = "ALL"
        typ, self.data = self.mail.search(None, search_criteria)
        self.ids = self.data[0]
        self.ids_list = self.ids.split()
        self.mail_count = len(self.ids_list)
        print(f"\n📧 Found \033[32m{self.mail_count}\033[0m matching emails.")

    def confirm_download(self):
        answer = input(f"\n📂 Do you want to download attachments from these emails to {self.dest_folder}? (y/n): ").lower().strip()
        return answer == "y"

    def parse_emails(self):
        downloaded_count = 0
        for email_id in self.ids_list:
            _, email_data = self.mail.fetch(email_id, '(RFC822)')
            raw = email_data[0][1]

            try:
                msg = email.message_from_bytes(raw)
            except Exception:
                continue

            if msg.is_multipart():
                for part in msg.walk():
                    content_disposition = part.get("Content-Disposition")
                    if content_disposition and 'attachment' in content_disposition.lower():
                        filename = part.get_filename()
                        if filename:
                            os.makedirs(self.dest_folder, exist_ok=True)
                            file_path = os.path.join(self.dest_folder, filename)
                            with open(file_path, "wb") as f:
                                f.write(part.get_payload(decode=True))
                            print(f"📎 Saved attachment: \033[94m{filename}\033[0m")
                            downloaded_count += 1
            else:
                print("ℹ️ Skipped: Email is not multipart or has no attachments.")
        if downloaded_count == 0:
            print("\n📭 No attachments were found in the selected emails.")
        else:
            print(f"\n📁 Total attachments downloaded: \033[92m{downloaded_count}\033[0m\n")

if __name__ == "__main__":
    try:
        run = GmailAttachmentsDownloader()
    except KeyboardInterrupt:
        print("\n\n🛑 Program interrupted by user.")
        sys.exit(0)
