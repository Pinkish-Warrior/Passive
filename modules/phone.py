# Looks up carrier, location, and type for a phone number.
# Uses the phonenumbers library (bundled data — no API key or network call needed).
# Number must include the country code (e.g. +33612345678).

import phonenumbers
from phonenumbers import geocoder, carrier, PhoneNumberType

TYPE_LABELS = {
    PhoneNumberType.MOBILE:               "mobile",
    PhoneNumberType.FIXED_LINE:           "fixed line",
    PhoneNumberType.FIXED_LINE_OR_MOBILE: "fixed line or mobile",
    PhoneNumberType.TOLL_FREE:            "toll-free",
    PhoneNumberType.PREMIUM_RATE:         "premium rate",
    PhoneNumberType.SHARED_COST:          "shared cost",
    PhoneNumberType.VOIP:                 "VoIP",
    PhoneNumberType.PERSONAL_NUMBER:      "personal number",
    PhoneNumberType.PAGER:                "pager",
    PhoneNumberType.UAN:                  "UAN",
    PhoneNumberType.VOICEMAIL:            "voicemail",
    PhoneNumberType.UNKNOWN:              "unknown",
}


def lookup_phone(number: str) -> str:
    try:
        parsed = phonenumbers.parse(number, None)
    except phonenumbers.NumberParseException as e:
        raise ValueError(f"Could not parse phone number: {e}")

    valid     = phonenumbers.is_valid_number(parsed)
    formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    region    = phonenumbers.region_code_for_number(parsed) or "N/A"
    location  = geocoder.description_for_number(parsed, "en") or "N/A"
    carrier_name = carrier.name_for_number(parsed, "en") or "N/A"
    number_type  = TYPE_LABELS.get(phonenumbers.number_type(parsed), "unknown")

    return (
        f"Phone:    {formatted}\n"
        f"Valid:    {'yes' if valid else 'no'}\n"
        f"Type:     {number_type}\n"
        f"Country:  {region}\n"
        f"Location: {location}\n"
        f"Carrier:  {carrier_name}"
    )
