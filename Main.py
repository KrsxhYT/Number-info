# pip install -r requirements.txt

import phonenumbers
from phonenumbers import (
    carrier, geocoder, timezone, number_type,
    is_valid_number, is_possible_number,
    is_emergency_number, is_carrier_specific,
    PhoneNumberFormat, NumberParseException,
    region_code_for_number, region_codes_for_country_code,
    format_number_for_mobile_dialing,
    can_be_internationally_dialled,
    is_valid_number_for_region
)
from colorama import Fore, Style, init
import os

init(autoreset=True)

def banner():
    print(Fore.MAGENTA + Style.BRIGHT + r"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃         📞 KRSXH PHONE ANALYZER     ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
""")

def type_to_str(t):
    import phonenumbers.phonenumberutil as putil
    mapping = {
        getattr(putil, "FIXED_LINE", -1): "📞 FIXED_LINE",
        getattr(putil, "MOBILE", -2): "📱 MOBILE",
        getattr(putil, "FIXED_LINE_OR_MOBILE", -3): "📱📞 MOBILE/FIXED",
        getattr(putil, "TOLL_FREE", -4): "🆓 TOLL_FREE",
        getattr(putil, "PREMIUM_RATE", -5): "💸 PREMIUM_RATE",
        getattr(putil, "SHARED_COST", -6): "🤝 SHARED_COST",
        getattr(putil, "VOIP", -7): "🌐 VOIP",
        getattr(putil, "PERSONAL_NUMBER", -8): "👤 PERSONAL_NUMBER",
        getattr(putil, "PAGER", -9): "📟 PAGER",
        getattr(putil, "UAN", -10): "🏢 UAN",
        getattr(putil, "VOICEMAIL", -11): "📤 VOICEMAIL",
    }
    return mapping.get(t, "❓ UNKNOWN")

def analyze_number(raw_input):
    try:
        p = phonenumbers.parse(raw_input, None)
        tz = timezone.time_zones_for_number(p)
        return {
            "📥 Entered Number": raw_input,
            "🔢 E.164": phonenumbers.format_number(p, PhoneNumberFormat.E164),
            "📞 National": phonenumbers.format_number(p, PhoneNumberFormat.NATIONAL),
            "🌍 International": phonenumbers.format_number(p, PhoneNumberFormat.INTERNATIONAL),
            "🧩 RFC3966": phonenumbers.format_number(p, PhoneNumberFormat.RFC3966),
            "📱 Mobile Dial": format_number_for_mobile_dialing(p, None, True),
            "🔢 Length": len(str(p.national_number)),
            "📌 Raw National": p.national_number,
            "🌎 Country": geocoder.description_for_number(p, "en"),
            "🏙️ Region": geocoder.description_for_number(p, "en"),
            "🌐 Country Code": p.country_code,
            "🗺️ Region Code": region_code_for_number(p),
            "🗂️ All Regions": ', '.join(region_codes_for_country_code(p.country_code)),
            "📡 Carrier": carrier.name_for_number(p, "en"),
            "📶 Carrier Specific": "✅" if is_carrier_specific(p) else "❌",
            "🔠 Type": type_to_str(number_type(p)),
            "💠 Type Code": number_type(p),
            "✅ Valid": "✅" if is_valid_number(p) else "❌",
            "❔ Possible": "✅" if is_possible_number(p) else "❌",
            "📞 Intl Dialable": "✅" if can_be_internationally_dialled(p) else "❌",
            "🧭 Region Valid": "✅" if is_valid_number_for_region(p, region_code_for_number(p)) else "❌",
            "🚨 Emergency": "✅" if is_emergency_number(raw_input, "IN") else "❌",
            "🔌 Extension": p.extension if p.extension else "None",
            "🇮🇹 Italian Leading Zero": "✅" if getattr(p, "italian_leading_zero", False) else "❌",
            "🕓 Timezones": ', '.join(tz) if tz else "N/A",
            "⏱️ Timezone Count": len(tz),
            "🕒 UTC Sample": tz[0] if tz else "N/A",
            "🔢 Prefix 3": str(p.national_number)[:3],
            "🔢 Suffix 4": str(p.national_number)[-4:],
            "🧬 Raw Object": str(p),
            "📚 Metadata Loaded": "✅" if getattr(phonenumbers.PhoneMetadata, "metadata", None) else "❌",
            "📦 Library": "phonenumbers Python",
            "🧠 Analyzed By": "@KrsxhPy"
        }
    except NumberParseException:
        return {"error": "❌ Invalid number format."}

def display(info):
    if "error" in info:
        print(Fore.RED + info["error"])
        return
    print(Fore.YELLOW + "\n📋 ANALYSIS REPORT")
    for k, v in info.items():
        print(f"{Fore.CYAN}{k:<26} ➜ {Fore.WHITE}{v}")

def save_to_txt(info):
    path = os.path.join(os.getcwd(), "KrsxhNumberReport.txt")
    with open(path, 'w', encoding='utf-8') as f:
        for k, v in info.items():
            f.write(f"{k}: {v}\n")
        f.write("\n🔍 Generated by: @KrsxhPy\n")
    print(Fore.GREEN + f"\n✅ Report saved at: {path}")

def main():
    banner()
    num = input(Fore.LIGHTBLUE_EX + "📞 Enter number (with country code): ").strip()
    info = analyze_number(num)
    display(info)
    if "error" not in info:
        save_to_txt(info)

if __name__ == "__main__":
    main()
