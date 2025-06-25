import pdfplumber
import yaml
import re
from pathlib import Path
try:
    from pdf2image import convert_from_path
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

def extract_text_from_pdf(pdf_path):
    try:
        # Try pdfplumber for text-based PDFs
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            if text.strip():
                return text
        # Fallback to OCR if available
        if OCR_AVAILABLE:
            print(f"Using OCR for {pdf_path}")
            images = convert_from_path(pdf_path)
            text = ""
            for image in images:
                text += pytesseract.image_to_string(image, lang='eng+swa') + "\n"
            return text
        return ""
    except Exception as e:
        print(f"Error extracting {pdf_path}: {e}")
        return ""

def generate_nlu_data(text):
    # Broader patterns to capture more content
    patterns = {
        "ask_sales_process": r"(Sales|Mchakato|Mauzo|Register|Sajili|NIDA|OTP|IMEI|STK|Loan|Customer|Portal).*?([^\n.]+)",
        "ask_payment_methods": r"(Payment|Malipo|Lipa|M-Pesa|Bank|Cash|Loan|Installment).*?([^\n.]+)",
        "ask_maintenance": r"(Maintenance|Matengenezo|Warranty|Waranti|Repair|Tengeneza|Service).*?([^\n.]+)",
        "ask_lost_phone": r"(Lost|Potea|Missing|Simu\s*Iliyopotea|Stolen|Report).*?([^\n.]+)",
        "lock_phone": r"(Lock|Kulock|V-Trust|Pay\s*Trigger|O-Guard|Trustonic|Think\s*Adams|Vivo|Tecno|Oppo|Samsung|Realme).*?([^\n.]+)",
        "phone_pricing": r"(\w+\s*\w*)\s*[:,]\s*(\d+[,\d]*\s*TZS|Initial|Weekly|Monthly|Payment|Bei|Kianzio)"
    }
    
    nlu_data = {"version": "3.1", "nlu": []}
    
    # Base examples
    base_examples = {
        "greet": ["Hello", "Hi", "Good morning", "Hey there", "Can you say hello to me?", "Habari", "Mambo", "Sala", "Habari za leo", "Jambo msaidizi", "Greet", "Say hi", "Salamu"],
        "ask_sales_process": ["How do I sell?", "Sales process", "What’s the steps to register a customer?", "Tell me how to start selling a phone today", "Steps", "Register", "Mauzo", "Nawezaje kufanya mauzo?", "Hatua za mauzo ni zipi?", "Jinsi ya kusajili mteja?", "Nifanye nini kuanza mauzo?", "Explain the whole sales process to me in detail", "Mchakato", "Sajili", "How to add a loan in the portal?", "How to verify NIDA number?", "How to send OTP for sales?", "How to enter IMEI for a phone?", "What is STK push for payment?"],
        "ask_payment_methods": ["Payment", "How to pay?", "What are the payment methods?", "Tell me how a customer can pay their loan", "Can you pay with M-Pesa?", "Lipa", "Mteja anawezaje kulipa?", "Njia za malipo?", "Jinsi ya kulipa mkopo?", "Explain all payment options available", "Malipo", "Payment options", "Kulipa"],
        "ask_maintenance": ["Maintenance", "Where to fix the phone?", "What does warranty cover?", "How do I get the phone repaired?", "Is there free maintenance?", "Matengenezo", "Matengenezo yafanyika wapi?", "Waranti inajumuisha nini?", "Jinsi ya kutengeneza simu?", "Tell me about phone maintenance process", "Warranty", "Repair", "Tengeneza"],
        "ask_lost_phone": ["Lost", "What if phone is missing?", "How do I report a lost phone?", "Customer says phone is gone, what now?", "Steps for lost phone", "Potea", "Nifanye nini simu ikipotea?", "Simu imepotea", "Jinsi ya kushughulikia simu iliyopotea?", "Tell me what to do if a phone gets lost", "Lost phone", "Hatua za simu kupotea", "Missing"],
        "ask_bot_identity": ["Who", "Who are you?", "What’s your name?", "Are you a bot?", "Tell me about yourself", "Nani", "Wewe ni nani?", "Jina lako ni nani?", "Wewe ni bot?", "Explain who you are", "Identity", "Nani wewe", "Bot"],
        "lock_phone": ["How to lock a Vivo phone?", "How to use V-Trust for locking?", "Steps to lock a Tecno phone", "How to install Pay Trigger?", "How to lock an Oppo phone?", "What is O-Guard for Oppo?", "How to lock a Samsung phone?", "How to use Trustonic?", "How to lock a Realme phone with Think Adams?", "Jinsi ya kulock simu ya Vivo?", "Hatua za kulock simu ya Tecno?", "V-Trust ni nini?", "Pay Trigger inatumikaje?"],
        "sync_users": ["Sync portal users", "Update user data in portal", "Synchronize customer data", "Run sync_portal_users", "Sync users with portal", "Sasisha data ya wateja", "Sync data kwenye portal"],
        "phone_pricing": ["What is the price of Tecno Camon 30S?", "How much is the initial payment for Realme C61?", "What are the weekly payments for Honor X7B?", "Tell me about ZTE A35 pricing", "How much is the monthly payment for Tecno Spark 30C?", "Bei ya simu ya Tecno ni kiasi gani?", "Kianzio cha Realme C61 ni kiasi gani?", "Malipo ya wiki ya Honor X7B?"]
    }
    
    # Generate examples from PDFs
    for intent, pattern in patterns.items():
        examples = set(base_examples.get(intent, []))
        for match in re.finditer(pattern, text, re.IGNORECASE):
            keyword, content = match.groups()
            examples.update([
                f"What is {content}?" if intent != "phone_pricing" else f"How much is {content}?",
                f"Tell me about {content}.",
                f"Explain {content} in detail.",
                f"Jinsi ya {content.lower()}?" if intent != "phone_pricing" else f"Bei ya {content} ni nini?",
                f"Nawezaje {content.lower()}?" if intent != "phone_pricing" else f"Kiasi cha {content} ni kiasi gani?"
            ])
        nlu_data["nlu"].append({"intent": intent, "examples": "- " + "\n- ".join(examples)})
    
    # Add static intents
    for intent in ["greet", "ask_bot_identity", "sync_users"]:
        nlu_data["nlu"].append({"intent": intent, "examples": "- " + "\n- ".join(base_examples[intent])})
    
    return nlu_data

def generate_domain_data(text):
    # Responses
    responses = {
        "utter_greet": [
            {"text": "Habari! Mimi ni OnfonMobile TZ, msaidizi wako wa mauzo ya simu. Nawezaje kukusaidia leo?"},
            {"text": "Hello! I'm OnfonMobile TZ, your phone sales assistant. How can I help you today?"}
        ],
        "utter_ask_bot_identity": [
            {"text": "Mimi ni OnfonMobile TZ, bot ya kusaidia mauzo ya simu. Unaweza kuniuliza chochote!"},
            {"text": "I'm OnfonMobile TZ, a bot to help with phone sales. Ask me anything!"}
        ],
        "utter_sync_users": [
            {"text": "Data ya wateja imesawazishwa kwa mafanikio na portal."},
            {"text": "User data synchronized successfully with the portal."}
        ]
    }
    
    # Patterns for responses
    patterns = {
        "utter_ask_sales_process": r"(Sales|Mchakato|Mauzo|Register|Sajili|NIDA|OTP|IMEI|STK|Loan|Customer|Portal).*?([^\n.]+)",
        "utter_ask_payment_methods": r"(Payment|Malipo|Lipa|M-Pesa|Bank|Cash|Loan|Installment).*?([^\n.]+)",
        "utter_ask_maintenance": r"(Maintenance|Matengenezo|Warranty|Waranti|Repair|Tengeneza|Service).*?([^\n.]+)",
        "utter_ask_lost_phone": r"(Lost|Potea|Missing|Simu\s*Iliyopotea|Stolen|Report).*?([^\n.]+)",
        "utter_lock_phone": r"(Lock|Kulock|V-Trust|Pay\s*Trigger|O-Guard|Trustonic|Think\s*Adams|Vivo|Tecno|Oppo|Samsung|Realme).*?([^\n.]+)",
        "utter_phone_pricing": r"(\w+\s*\w*)\s*[:,]\s*(\d+[,\d]*\s*TZS|Initial|Weekly|Monthly|Payment|Bei|Kianzio)"
    }
    
    for utter, pattern in patterns.items():
        utter_responses = []
        for match in re.finditer(pattern, text, re.IGNORECASE):
            _, content = match.groups()
            utter_responses.extend([
                {"text": content.strip()},
                {"text": content.strip().lower()}  # Swahili version
            ])
        responses[utter] = utter_responses or [
            {"text": f"Tafadhali toa maelezo zaidi kuhusu {utter.replace('utter_', '')}."},
            {"text": f"Please provide more details about {utter.replace('utter_', '')}."}
        ]
    
    domain_data = {
        "version": "3.1",
        "intents": ["greet", "ask_sales_process", "ask_payment_methods", "ask_maintenance", "ask_lost_phone", "ask_bot_identity", "lock_phone", "sync_users", "phone_pricing"],
        "responses": responses,
        "session_config": {
            "session_expiration_time": 60,
            "carry_over_slots_to_new_session": True
        }
    }
    return domain_data

def save_yaml(data, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)
    print(f"Saved {filepath}")

def main():
    pdf_paths = ["MwongozoMauzo.pdf", "vianzio.pdf"]
    all_text = ""
    
    for pdf_path in pdf_paths:
        if Path(pdf_path).exists():
            text = extract_text_from_pdf(pdf_path)
            all_text += text + "\n"
        else:
            print(f"PDF not found: {pdf_path}")
    
    if all_text:
        nlu_data = generate_nlu_data(all_text)
        domain_data = generate_domain_data(all_text)
        
        save_yaml(nlu_data, "data/nlu.yml")
        save_yaml(domain_data, "domain.yml")
    else:
        print("No text extracted from PDFs.")

if __name__ == "__main__":
    main()