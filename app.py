import imaplib
import email
import os
import getpass

print("----------GMAIL COMMANDER----------\n")
user = input("E-mail: ")
password = getpass.getpass("Password: ")
imap_url = "imap.gmail.com"

print()

mail = imaplib.IMAP4_SSL(imap_url)
mail.login(user, password)
mail.select("INBOX")

old_message = ""
current_message = ""

while True:
    result, data = mail.uid("search", None, "ALL")
    inbox_item_list = data[0].split()

    most_recent = inbox_item_list[-1]

    result2, email_data = mail.uid("fetch", most_recent, "(RFC822)")
    raw_email = email_data[0][1].decode("utf-8")
    email_message = email.message_from_string(raw_email)

    for part in email_message.walk():
        if part.get_content_maintype() == "multipart":
            continue
        filename = part.get_filename()
        content_type = part.get_content_type()

        if "plain" in content_type and email_message["Subject"] == "command":
            current_message = part.get_payload()

        if old_message != current_message:
            os.system(current_message[:-2])
            print("\n" + 100 * "-" + "\n")
            old_message = current_message

