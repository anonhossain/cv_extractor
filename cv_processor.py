import os
import re
from pdfminer.high_level import extract_text

class CVProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    @staticmethod
    def extract_candidate_name_from_filename(file_path):
        return os.path.splitext(os.path.basename(file_path))[0]

    @staticmethod
    def extract_pattern(text, pattern, split_by_reference=True):
        compiled_pattern = re.compile(pattern)
        all_matches = compiled_pattern.findall(text)

        reference_matches = []
        if split_by_reference:
            reference_pattern = re.compile(r'references?|REFERENCES?', re.IGNORECASE)
            split_text = reference_pattern.split(text, 1)
            if len(split_text) > 1:
                reference_matches = compiled_pattern.findall(split_text[1])

        return all_matches, reference_matches

    @staticmethod
    def format_phone_number(phone_number):
        # Remove unwanted characters (like spaces, dashes, or leading `-`)
        phone_number = re.sub(r'[^\d]', '', phone_number)

        # Ensure the number starts with `880` or add it if missing
        if phone_number.startswith('880'):
            return f'+{phone_number}'
        elif phone_number.startswith('0'):
            return f'+880{phone_number[1:]}'
        else:
            return f'+880{phone_number}'

    def process_cv(self, file_path):
        text = extract_text(file_path)

        # Extract candidate name
        candidate_name = self.extract_candidate_name_from_filename(file_path)

        # Patterns
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        phone_pattern = r'\+?880[-\s]?\d{4}[-\s]?\d{6}|\d{5}[-\s]?\d{6}'

        # Extract emails and phone numbers
        emails, ref_emails = self.extract_pattern(text, email_pattern)
        phones, ref_phones = self.extract_pattern(text, phone_pattern)

        # Format phone numbers
        phones = [self.format_phone_number(phone) for phone in phones]
        ref_phones = [self.format_phone_number(phone) for phone in ref_phones]

        # Candidate data
        candidate_email = emails[0] if emails else "N/A"
        candidate_phone = phones[0] if phones else "N/A"
        ref_email1 = ref_emails[0] if len(ref_emails) > 0 else "N/A"
        ref_email2 = ref_emails[1] if len(ref_emails) > 1 else "N/A"
        ref_phone1 = ref_phones[0] if len(ref_phones) > 0 else "N/A"
        ref_phone2 = ref_phones[1] if len(ref_phones) > 1 else "N/A"

        return {
            "name": candidate_name,
            "email": candidate_email,
            "phone": candidate_phone,
            "ref_email1": ref_email1,
            "ref_email2": ref_email2,
            "ref_phone1": ref_phone1,
            "ref_phone2": ref_phone2,
        }
