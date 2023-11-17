import imaplib
import email
import re
import os
import logging
import time

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
print("Script Directory:", script_dir)

# Configure logging for the phishing_detection.py script
log_file_path = os.path.join(script_dir, 'phishing_detection.log')
logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

log_file_path = r'C:\Users\jtcha\phishing_detection.log'

logging.getLogger().handlers[0].flush()

def locate_email_domains_file():
    # Get the current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full file path
    email_domains_file = os.path.join(script_dir, 'Email_domains.txt')
    return email_domains_file

def load_valid_domains(filename):
    valid_domains = set()
    with open(filename, 'r') as file:
        for line in file:
            domain = line.strip().lower()
            valid_domains.add(domain)
    return valid_domains

# Locate and load the valid domains
email_domains_file = locate_email_domains_file()
valid_domains_set = load_valid_domains(email_domains_file)

def is_valid_email(email):
    # Improved email validation regex pattern
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_pattern, email):
        # Split the email address to extract the domain part
        _, domain = email.split('@')
        # Check if the domain is in the set of valid domains
        return domain.lower() in valid_domains_set
    return False

def extract_email_headers(email_content):
    # Parse the email content
    msg = email.message_from_string(email_content)
    # Get the "From" address and "Reply-To" address (if available)
    from_address = msg.get("From", "")
    reply_to_address = msg.get("Reply-To", "")
    # Get the authentication results (SPF, DKIM, DMARC)
    spf_result = msg.get("Authentication-Results", "").lower()
    dkim_result = msg.get("DKIM-Signature", "").lower()
    dmarc_result = msg.get("DMARC-Authentication-Results", "").lower()

    return from_address, reply_to_address, spf_result, dkim_result, dmarc_result

def is_phishing_email(email_content):
    # Define phishing keywords to check in the email content
    phishing_keywords = ['urgent', 'account', 'password', 'login', 'security', 'username']

    # Convert email content to lowercase for case-insensitive matching
    email_content_lower = email_content.lower()

    # Use word boundaries in the regex to avoid matching partial words
    regex = re.compile(r'\b(?:' + '|'.join(map(re.escape, phishing_keywords)) + r')\b')

    # Check if any phishing keyword is found in the email content
    phishing_detected = bool(regex.search(email_content_lower))

    # If any phishing keyword is found, check for valid keywords
    if phishing_detected:
        # Define valid keywords for account validation emails (case-insensitive)
        valid_keywords = ['confirmation', 'verification', 'code', 'token', 'verify']
        # Check if any valid keyword is present in the email content (case-insensitive)
        valid_present = any(word.lower() in email_content_lower for word in valid_keywords)

        # If any valid keyword is present, return False (not phishing)
        if valid_present:
            return False

        # If no valid keyword is present, return True for phishing
        return True

    # Extract email headers
    from_address, reply_to_address, spf_result, dkim_result, dmarc_result = extract_email_headers(email_content)

    # Check for suspicious indicators in the email headers
    if not is_valid_email(from_address) or not is_valid_email(reply_to_address):
        return True  # Suspicious "From" or "Reply-To" addresses

    # Check for failed SPF, DKIM, or DMARC authentication
    if "fail" in spf_result or "fail" in dkim_result or "fail" in dmarc_result:
        return True  # Failed authentication indicates suspicious email

    # If none of the phishing indicators are found, return False
    return False

def log_phishing_attempt(email_content):
    # Log the details of the phishing attempt
    logging.info("Phishing Attempt Detected:")
    logging.info("Content: %s", email_content)
    print("Logging Attempt")
    
# New function for processing Gmail emails and performing phishing detection
def process_gmail_emails(username, password):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")

    try:
        mail.login(username, password)  # Use the application-specific password here
        mail.select("inbox")

    # Connect to Gmail IMAP server
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        
    except imaplib.IMAP4.error as e:
        print("IMAP Error:", e)

    finally:
        mail.logout()

    # Login to the Gmail account
    mail.login('chancellorjarrett@gmail.com', 'p#W3rw4@wa86jto8r5GXo$gFLhwYL#f9')

    # Select the mailbox to monitor (INBOX in this case)
    mail.select('INBOX')

    # Loop to continuously check for new emails
    while True:
        # Search for new emails
        status, email_ids = mail.search(None, 'UNSEEN')

        if status == 'OK':
            # Get the list of email IDs
            email_id_list = email_ids[0].split()

            # Process each email
            for email_id in email_id_list:
                # Fetch the email content
                status, email_data = mail.fetch(email_id, '(RFC822)')
                if status == 'OK':
                    msg = email.message_from_bytes(email_data[0][1])
                    email_content = msg.get_payload(decode=True).decode('utf-8')
                    # Perform phishing detection on the email content
                    if is_phishing_email(email_content):
                        # Log phishing attempt to the existing phishing_detection.log file
                        logger.warning("Potential phishing email detected.")
                        logger.info("Email Content: %s", email_content)
                        # You can implement actions like sending an alert or moving the email to a specific folder here

        # Sleep for a short time before checking for new emails again
        time.sleep(60)  # Change the time interval as per your preference

if __name__ == "__main__":
    # Get user input for the email content
    email_from = input("Enter the email address: ")
    email_subject = input("Enter the email subject: ")
    email_content = input("Enter the email content: ")

    # Check if the provided email is valid and not a phishing attempt
    if is_valid_email(email_from) and not is_phishing_email(email_content):
        print("Valid email for account validation. Processing...")
        time.sleep(5)  # Introduce a 5-second delay before printing the result
        print("The entered email is valid!")
    else:
        print("Potential phishing email. Blocking or sending an alert...")
        # Log the phishing attempt
        log_phishing_attempt(email_content)