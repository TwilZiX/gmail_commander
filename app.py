import imaplib
import smtplib
import email
import getpass
import subprocess

print("\n----------GMAIL COMMANDER----------\n")
user = input("E-mail: ")
password = getpass.getpass("Password: ")
imap_url = "imap.gmail.com"
smtp_url = "smtp.gmail.com"

print("\nProgram is already running, waiting for emails!\n")

try:
    # IMAP
    mail = imaplib.IMAP4_SSL(imap_url)
    mail.login(user, password)
    mail.select("INBOX")

    # SMTP
    s = smtplib.SMTP_SSL(smtp_url)
    s.login(user, password)

    old_id = "x"
    new_id = 0
    current_message = ""
    from_user = ""

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

            if (
                "plain" in content_type
                and email_message["Subject"].lower() == "command"
            ):
                current_message = part.get_payload(decode=True)
                current_message = current_message.rstrip().decode("utf-8")
                new_id = most_recent

            if old_id != new_id and old_id != "x":
                from_user = email_message["From"].split()
                from_user = from_user[-1][1:-1]

                response = subprocess.check_output(
                    current_message, shell=True, stderr=subprocess.STDOUT
                )
                msg = "Subject: {}\n\n{}".format(
                    "Response", email.message_from_bytes(response)
                )

                try:
                    s.sendmail(
                        user, from_user, msg,
                    )
                    print(20 * "*" + "\n")
                    print("Replied to: " + from_user)
                    print("Command: " + current_message.replace("\n", ""))
                    print("Result: " + response.decode("utf-8"))
                except:
                    print("Could not reply to: " + from_user)

            old_id = new_id
except:
    print("Could not log in!")
