from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionSendPrice(Action):
    def name(self) -> Text:
        return "action_send_price"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message.get("text", "").lower()
        phone_pricing = {
            "oppo a18 4/64gb": {"brand": "oppo", "lock_solution": "O-Guard", "bei": 300000, "kianzio": 90000, "siku": 1700, "wiki": 11900, "mwezi": 51000},
            "oppo a18 4/128gb": {"brand": "oppo", "lock_solution": "O-Guard", "bei": 350000, "kianzio": 108000, "siku": 2000, "wiki": 14000, "mwezi": 60000},
            "oppo a38 4/128gb": {"brand": "oppo", "lock_solution": "O-Guard", "bei": 440000, "kianzio": 132000, "siku": 2400, "wiki": 16800, "mwezi": 72000},
            "oppo a58 6/128gb": {"brand": "oppo", "lock_solution": "O-Guard", "bei": 510000, "kianzio": 153000, "siku": 2700, "wiki": 18900, "mwezi": 81000},
            "oppo a58 8/128gb": {"brand": "oppo", "lock_solution": "O-Guard", "bei": 590000, "kianzio": 177000, "siku": 3100, "wiki": 21700, "mwezi": 93000},
            "oppo a3x 4/64gb": {"brand": "oppo", "lock_solution": "O-Guard", "bei": 330000, "kianzio": 99000, "siku": 1900, "wiki": 13300, "mwezi": 57000},
            "oppo a3x 4/128gb": {"brand": "oppo", "lock_solution": "O-Guard", "bei": 399000, "kianzio": 119700, "siku": 2200, "wiki": 15400, "mwezi": 66000},
            "vivo y28 8/256gb": {"brand": "vivo", "lock_solution": "V-Trust", "bei": 559000, "kianzio": 167700, "siku": 3000, "wiki": 21000, "mwezi": 90000},
            "vivo y18 6/128gb": {"brand": "vivo", "lock_solution": "V-Trust", "bei": 390000, "kianzio": 117000, "siku": 2200, "wiki": 15400, "mwezi": 66000},
            "vivo y03 4/128gb": {"brand": "vivo", "lock_solution": "V-Trust", "bei": 332000, "kianzio": 99600, "siku": 1900, "wiki": 13300, "mwezi": 57000},
            "vivo y03 4/64gb": {"brand": "vivo", "lock_solution": "V-Trust", "bei": 289000, "kianzio": 86700, "siku": 1700, "wiki": 11900, "mwezi": 51000},
            "vivo y19s 6/128gb": {"brand": "vivo", "lock_solution": "V-Trust", "bei": 380000, "kianzio": 114000, "siku": 2100, "wiki": 14700, "mwezi": 63000},
            "samsung a05 4/128gb": {"brand": "samsung", "lock_solution": "Trustonic", "bei": 325000, "kianzio": 97500, "siku": 1900, "wiki": 13300, "mwezi": 57000},
            "samsung a05 4/64gb": {"brand": "samsung", "lock_solution": "Trustonic", "bei": 300000, "kianzio": 90000, "siku": 1700, "wiki": 11900, "mwezi": 51000},
            "samsung a05s 4/64gb": {"brand": "samsung", "lock_solution": "Trustonic", "bei": 355000, "kianzio": 106500, "siku": 2000, "wiki": 14000, "mwezi": 60000},
            "samsung a05s 4/128gb": {"brand": "samsung", "lock_solution": "Trustonic", "bei": 380000, "kianzio": 114000, "siku": 2100, "wiki": 14700, "mwezi": 63000},
            "infinix note 30 pro 8/256gb": {"brand": "infinix", "lock_solution": "Pay Trigger", "bei": 480000, "kianzio": 144000, "siku": 2600, "wiki": 18200, "mwezi": 78000},
            "infinix smart 8 3/64gb": {"brand": "infinix", "lock_solution": "Pay Trigger", "bei": 269000, "kianzio": 80700, "siku": 1600, "wiki": 11200, "mwezi": 48000},
            "infinix smart 9 4/128gb": {"brand": "infinix", "lock_solution": "Pay Trigger", "bei": 328000, "kianzio": 98400, "siku": 1900, "wiki": 13300, "mwezi": 57000},
            "infinix hot50i 4g/128gb": {"brand": "infinix", "lock_solution": "Pay Trigger", "bei": 340000, "kianzio": 102000, "siku": 1900, "wiki": 13300, "mwezi": 57000},
            "infinix hot 40i 8/256gb": {"brand": "infinix", "lock_solution": "Pay Trigger", "bei": 333000, "kianzio": 99900, "siku": 1900, "wiki": 13300, "mwezi": 57000},
            "infinix hot 50 pro+ 8/256gb": {"brand": "infinix", "lock_solution": "Pay Trigger", "bei": 590000, "kianzio": 177000, "siku": 3100, "wiki": 21700, "mwezi": 93000},
            "tecno camon 30s 128gb/6gb": {"brand": "tecno", "lock_solution": "Pay Trigger", "bei": 580000, "kianzio": 174000, "siku": 3100, "wiki": 21600, "mwezi": 93000},
            "tecno spark 30c 128gb/4gb": {"brand": "tecno", "lock_solution": "Pay Trigger", "bei": 330000, "kianzio": 99000, "siku": 1900, "wiki": 13300, "mwezi": 57000},
            "realme c61 6/128gb": {"brand": "realme", "lock_solution": "Think Adams", "bei": 350000, "kianzio": 105000, "siku": 2000, "wiki": 14000, "mwezi": 60000},
            "realme c61 6/256gb": {"brand": "realme", "lock_solution": "Think Adams", "bei": 360000, "kianzio": 108000, "siku": 2000, "wiki": 14000, "mwezi": 60000},
            "realme note 50 4/128gb": {"brand": "realme", "lock_solution": "Think Adams", "bei": 290000, "kianzio": 87000, "siku": 1700, "wiki": 11900, "mwezi": 51000},
            "realme note 50 6/64gb": {"brand": "realme", "lock_solution": "Think Adams", "bei": 250000, "kianzio": 75000, "siku": 1500, "wiki": 10500, "mwezi": 45000},
            "honor x7b 8/256gb": {"brand": "honor", "lock_solution": "Think Adams", "bei": 500000, "kianzio": 150000, "siku": 2700, "wiki": 18900, "mwezi": 81000},
            "honor x6b 256gb/6gb": {"brand": "honor", "lock_solution": "Think Adams", "bei": 400000, "kianzio": 120000, "siku": 2200, "wiki": 15400, "mwezi": 66000},
            "honor x6b 128gb/6gb": {"brand": "honor", "lock_solution": "Think Adams", "bei": 365000, "kianzio": 109500, "siku": 2000, "wiki": 14000, "mwezi": 60000},
            "honor x5plus 64gb/4gb": {"brand": "honor", "lock_solution": "Think Adams", "bei": 280000, "kianzio": 84000, "siku": 1700, "wiki": 11900, "mwezi": 51000},
            "hisense e70 pro 128gb/4gb": {"brand": "hisense", "lock_solution": "Think Adams", "bei": 280000, "kianzio": 84000, "siku": 1700, "wiki": 11900, "mwezi": 51000},
            "hisense e71 64gb/4gb": {"brand": "hisense", "lock_solution": "Think Adams", "bei": 250000, "kianzio": 75000, "siku": 1500, "wiki": 10500, "mwezi": 45000},
            "zte a35 4g/64gb": {"brand": "zte", "lock_solution": "Think Adams", "bei": 250000, "kianzio": 75000, "siku": 1500, "wiki": 10500, "mwezi": 45000},
            "zte a55 4g/128gb": {"brand": "zte", "lock_solution": "Think Adams", "bei": 290000, "kianzio": 87000, "siku": 1700, "wiki": 11900, "mwezi": 51000}
        }

        # Check for specific model match
        for model in phone_pricing:
            if model in user_message:
                pricing = phone_pricing[model]
                response = (f"Bei ya {model.upper()} (Lock Solution: {pricing['lock_solution']}):\n"
                            f"- Bei ya Kuuzia: TZS {pricing['bei']:,}\n"
                            f"- Kianzio: TZS {pricing['kianzio']:,}\n"
                            f"- Malipo ya Siku: TZS {pricing['siku']:,}\n"
                            f"- Malipo ya Wiki: TZS {pricing['wiki']:,}\n"
                            f"- Malipo ya Mwezi: TZS {pricing['mwezi']:,}\n"
                            f"Unahitaji msaada zaidi, nipo kukusaidia.")
                dispatcher.utter_message(text=response)
                return []

        # Check for brand match
        brands = ["oppo", "vivo", "samsung", "infinix", "tecno", "realme", "honor", "hisense", "zte"]
        user_brand = next((brand for brand in brands if brand in user_message), None)
        
        if user_brand:
            models = [model for model, info in phone_pricing.items() if info["brand"] == user_brand]
            if models:
                response = f"Bei za simu za {user_brand.upper()} (Lock Solution: {phone_pricing[models[0]]['lock_solution']}):\n\n"
                for model in models:
                    pricing = phone_pricing[model]
                    response += (f"{model.upper()}:\n"
                                 f"- Bei ya Kuuzia: TZS {pricing['bei']:,}\n"
                                 f"- Kianzio: TZS {pricing['kianzio']:,}\n"
                                 f"- Malipo ya Siku: TZS {pricing['siku']:,}\n"
                                 f"- Malipo ya Wiki: TZS {pricing['wiki']:,}\n"
                                 f"- Malipo ya Mwezi: TZS {pricing['mwezi']:,}\n\n")
                response += "Unahitaji msaada zaidi, nipo kukusaidia."
                dispatcher.utter_message(text=response)
                return []

        # Fallback for no model or brand
        response = ("Samahani, sijaona modeli au brand uliyotaja. Tafadhali taja modeli, k.m. 'OPPO A18 4/64GB', au brand, k.m. 'OPPO', au uliza 'Bei za simu' kwa orodha yote. "
                    "Unahitaji msaada zaidi, nipo kukusaidia.")
        dispatcher.utter_message(text=response)
        return []

class ActionLockPhone(Action):
    def name(self) -> Text:
        return "action_lock_phone"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message.get("text", "").lower()
        lock_types = ["v-trust", "pay trigger", "o-guard", "trustonic", "think adams"]
        brands = ["oppo", "vivo", "samsung", "infinix", "tecno", "itel", "phillips", "realme", "honor", "zte"]

        # Check for specific lock type
        requested_lock = next((lock for lock in lock_types if lock in user_message), None)
        requested_brand = next((brand for brand in brands if brand in user_message), None)

        if requested_lock == "v-trust":
            response = ("Lock Solution ya V-Trust inatumika kwa simu za Vivo. Hatua za kulock:\n"
                        "a) Hakikisha simu ni mpya na haijawashwa.\n"
                        "b) Fungua boksi, fuata hatua za kuwasha simu.\n"
                        "c) Usiunganishe intaneti kabla ya kuweka IMEI ya kwanza kwenye mfumo (hakikisha IMEI sahihi).\n"
                        "d) Unganisha simu na intaneti thabiti.\n"
                        "e) Bonyeza kitufe cha kutuma AUTH CODE kwenye portal.\n"
                        "f) Fuata hatua za kuwasha simu hadi iwake kabisa.\n"
                        "g) Katika ubao wa taarifa, pata CODE ya V-Trust, iandike kwenye portal.\n"
                        "h) Thibitisha Code kwenye portal, bonyeza CODE kusanikisha V-Trust.\n"
                        "i) Kubali hatua zote hadi ujumbe 'UIDHINISHO UMEFANIKIWA (ACTIVATION SUCCESS)' uonekane, bonyeza OK.\n"
                        "j) Rudi kwenye portal kuthibitisha Lock Solution.\n"
                        "Unahitaji msaada zaidi, nipo kukusaidia.")
            dispatcher.utter_message(text=response)
            return []

        if requested_lock == "pay trigger":
            response = ("Lock Solution ya Pay Trigger inatumika kwa simu za Transsion (Tecno, Infinix, Itel, Phillips). Hatua za kulock:\n"
                        "a) Fungua boksi la simu.\n"
                        "b) Washa simu.\n"
                        "c) Kataa machaguo yasiyo ya lazima yanayoweza kuchelewesha kuwaka.\n"
                        "d) Kubali machaguo yanayohusisha ruhusa za leseni na mifumo.\n"
                        "e) Kamilisha mipangilio hadi uone aplikesheni za simu.\n"
                        "f) Unganisha simu na intaneti kusanikisha Lock Solution.\n"
                        "g) Kubali hatua zote kwa kubonyeza vitufe sahihi.\n"
                        "h) Baada ya kusanikisha Pay Trigger, rudi kwenye portal kuthibitisha Lock Solution.\n"
                        "Unahitaji msaada zaidi, nipo kukusaidia.")
            dispatcher.utter_message(text=response)
            return []

        if requested_lock == "o-guard":
            response = ("Lock Solution ya O-Guard inatumika kwa simu za Oppo. Hatua za kulock:\n"
                        "a) Fungua boksi la simu.\n"
                        "b) Washa simu.\n"
                        "c) Kataa machaguo yasiyo ya lazima yanayoweza kuchelewesha kuwaka.\n"
                        "d) Kubali machaguo yanayohusisha ruhusa za leseni na mifumo.\n"
                        "e) Kamilisha mipangilio hadi uone aplikesheni za simu.\n"
                        "f) Unganisha simu na intaneti kusanikisha Lock Solution.\n"
                        "g) Kubali hatua zote kwa kubonyeza vitufe sahihi.\n"
                        "h) Baada ya kusanikisha O-Guard, rudi kwenye portal kuthibitisha Lock Solution.\n"
                        "Unahitaji msaada zaidi, nipo kukusaidia.")
            dispatcher.utter_message(text=response)
            return []

        if requested_lock == "trustonic":
            response = ("Lock Solution ya Trustonic inatumika kwa simu za Samsung. Hatua za kulock:\n"
                        "Tafadhali fuata maagizo ya mfumo wa mauzo wa Onfon Microfinance. Kwa sasa, hatua za kina za Trustonic hazijapatikana. Rudi kwenye portal kwa maelezo zaidi au wasiliana na timu ya msaada.\n"
                        "Unahitaji msaada zaidi, nipo kukusaidia.")
            dispatcher.utter_message(text=response)
            return []

        if requested_lock == "think adams":
            response = ("Lock Solution ya Think Adams inatumika kwa simu za Realme, Honor, ZTE, na zingine. Hatua za kulock:\n"
                        "a) Washa simu.\n"
                        "b) Bonyeza mara 5-7 katika display ambayo haijaandikwa kitu ili kufungua Camera.\n"
                        "c) Skani QR Code iliyopo kwenye portal.\n"
                        "d) Unganisha simu na Wi-Fi.\n"
                        "e) Kubali hatua zinazofuata hadi simu inapofikia hatua ya mwisho ili kuinstall lock solution.\n"
                        "f) Hakikisha Think Adams DPC imekuwa installed kwenye simu ya mteja pamoja na Aplikesheni ya Onfon Microfinance.\n"
                        "g) Ingia kwenye Think Adams DPC na urefresh app hadi itakapokuonesha “Last Sync” yenye tarehe na muda ambao umelock simu.\n"
                        "h) Baada ya kuona tarehe na muda kwenye Lock Solution, rudi kwenye Portal ili kuconfirm Lock solution.\n"
                        "i) Hakikisha Lock na Loan vinasoma Active kabla ya kumpatia mteja simu yake.\n"
                        "Unahitaji msaada zaidi, nipo kukusaidia.")
            dispatcher.utter_message(text=response)
            return []

        if requested_brand == "vivo":
            response = ("Ili kulock simu ya Vivo (inatumia V-Trust):\n"
                        "a) Hakikisha simu ni mpya na haijawashwa.\n"
                        "b) Fungua boksi, fuata hatua za kuwasha simu.\n"
                        "c) Usiunganishe intaneti kabla ya kuweka IMEI ya kwanza kwenye mfumo (hakikisha IMEI sahihi).\n"
                        "d) Unganisha simu na intaneti thabiti.\n"
                        "e) Bonyeza kitufe cha kutuma AUTH CODE kwenye portal.\n"
                        "f) Fuata hatua za kuwasha simu hadi iwake kabisa.\n"
                        "g) Katika ubao wa taarifa, pata CODE ya V-Trust, iandike kwenye portal.\n"
                        "h) Thibitisha Code kwenye portal, bonyeza CODE kusanikisha V-Trust.\n"
                        "i) Kubali hatua zote hadi ujumbe 'UIDHINISHO UMEFANIKIWA (ACTIVATION SUCCESS)' uonekane, bonyeza OK.\n"
                        "j) Rudi kwenye portal kuthibitisha Lock Solution.\n"
                        "Unahitaji msaada zaidi, nipo kukusaidia.")
            dispatcher.utter_message(text=response)
            return []

        if requested_brand in ["infinix", "tecno", "itel", "phillips"]:
            response = (f"Ili kulock simu ya {requested_brand.capitalize()} (inatumia Pay Trigger):\n"
                        "a) Fungua boksi la simu.\n"
                        "b) Washa simu.\n"
                        "c) Kataa machaguo yasiyo ya lazima yanayoweza kuchelewesha kuwaka.\n"
                        "d) Kubali machaguo yanayohusisha ruhusa za leseni na mifumo.\n"
                        "e) Kamilisha mipangilio hadi uone aplikesheni za simu.\n"
                        "f) Unganisha simu na intaneti kusanikisha Lock Solution.\n"
                        "g) Kubali hatua zote kwa kubonyeza vitufe sahihi.\n"
                        "h) Baada ya kusanikisha Pay Trigger, rudi kwenye portal kuthibitisha Lock Solution.\n"
                        "Unahitaji msaada zaidi, nipo kukusaidia.")
            dispatcher.utter_message(text=response)
            return []

        if requested_brand == "oppo":
            response = ("Ili kulock simu ya Oppo (inatumia O-Guard):\n"
                        "a) Fungua boksi la simu.\n"
                        "b) Washa simu.\n"
                        "c) Kataa machaguo yasiyo ya lazima yanayoweza kuchelewesha kuwaka.\n"
                        "d) Kubali machaguo yanayohusisha ruhusa za leseni na mifumo.\n"
                        "e) Kamilisha mipangilio hadi uone aplikesheni za simu.\n"
                        "f) Unganisha simu na intaneti kusanikisha Lock Solution.\n"
                        "g) Kubali hatua zote kwa kubonyeza vitufe sahihi.\n"
                        "h) Baada ya kusanikisha O-Guard, rudi kwenye portal kuthibitisha Lock Solution.\n"
                        "Unahitaji msaada zaidi, nipo kukusaidia.")
            dispatcher.utter_message(text=response)
            return []

        if requested_brand == "samsung":
            response = ("Ili kulock simu ya Samsung (inatumia Trustonic):\n"
                        "Tafadhali fuata maagizo ya mfumo wa mauzo wa Onfon Microfinance. Kwa sasa, hatua za kina za Trustonic hazijapatikana. Rudi kwenye portal kwa maelezo zaidi au wasiliana na timu ya msaada.\n"
                        "Unahitaji msaada zaidi, nipo kukusaidia.")
            dispatcher.utter_message(text=response)
            return []

        if requested_brand in ["realme", "honor", "zte"]:
            response = (f"Ili kulock simu ya {requested_brand.capitalize()} (inatumia Think Adams):\n"
                        "a) Washa simu.\n"
                        "b) Bonyeza mara 5-7 katika display ambayo haijaandikwa kitu ili kufungua Camera.\n"
                        "c) Skani QR Code iliyopo kwenye portal.\n"
                        "d) Unganisha simu na Wi-Fi.\n"
                        "e) Kubali hatua zinazofuata hadi simu inapofikia hatua ya mwisho ili kuinstall lock solution.\n"
                        "f) Hakikisha Think Adams DPC imekuwa installed kwenye simu ya mteja pamoja na Aplikesheni ya Onfon Microfinance.\n"
                        "g) Ingia kwenye Think Adams DPC na urefresh app hadi itakapokuonesha “Last Sync” yenye tarehe na muda ambao umelock simu.\n"
                        "h) Baada ya kuona tarehe na muda kwenye Lock Solution, rudi kwenye Portal ili kuconfirm Lock solution.\n"
                        "i) Hakikisha Lock na Loan vinasoma Active kabla ya kumpatia mteja simu yake.\n"
                        "Unahitaji msaada zaidi, nipo kukusaidia.")
            dispatcher.utter_message(text=response)
            return []

        # Fallback for unrecognized specific queries
        response = ("Samahani, sijaona brand au lock type uliyotaja. Taja brand (k.m., Realme) au lock type (k.m., Think Adams) kwa maelezo ya hatua za kulock, au uliza 'lock solutions zote' kwa maelezo yote. "
                    "Unahitaji msaada zaidi, nipo kukusaidia.")
        dispatcher.utter_message(text=response)
        return []
