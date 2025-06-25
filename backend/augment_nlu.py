import yaml
import random
from pathlib import Path

def load_nlu(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_nlu(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)
    print(f"Saved {file_path}")

def generate_variations(base_example, intent, lang="en"):
    if lang == "en":
        templates = [
            "What is {}?", "Tell me about {}.", "How does {} work?", "Explain {} in detail.",
            "Can you help with {}?", "What’s the process for {}?", "How to {}?",
            "Give me details on {}.", "What are the steps for {}?", "I need info on {}.",
            "How do I handle {}?", "What’s {} all about?", "Show me how to {}.",
            "Can you explain {}?", "What do I do for {}?"
        ]
    else:  # sw
        templates = [
            "{} ni nini?", "Nawezaje {}?", "Jinsi ya {}?", "Elezea {} kwa undani.",
            "Unaweza kunisaidia na {}?", "Mchakato wa {} ni upi?", "Nifanye nini kwa {}?",
            "Toa maelezo ya {}.", "Hatua za {} ni zipi?", "Nihitaji taarifa za {}.",
            "Jinsi ya kushughulikia {}?", "{} inahusu nini?", "Nionyeshe jinsi ya {}.",
            "Unaweza kuelezea {}?", "Nifanye nini ili {}?"
        ]
    
    variations = [template.format(base_example if lang == "en" else base_example.lower()) for template in templates]
    
    if intent == "ask_sales_process":
        variations.extend([
            f"How to register a {base_example} customer?" if lang == "en" else f"Jinsi ya kusajili mteja wa {base_example.lower()}?",
            f"What’s the {base_example} sales process?" if lang == "en" else f"Mchakato wa mauzo ya {base_example.lower()} ni upi?"
        ])
    elif intent == "ask_payment_methods":
        variations.extend([
            f"Can I pay {base_example} with M-Pesa?" if lang == "en" else f"Ninaweza kulipa {base_example.lower()} kwa M-Pesa?",
            f"What’s the payment method for {base_example}?" if lang == "en" else f"Njia ya malipo ya {base_example.lower()} ni ipi?"
        ])
    elif intent == "phone_pricing":
        variations.extend([
            f"How much is the {base_example}?" if lang == "en" else f"Bei ya {base_example.lower()} ni kiasi gani?",
            f"What’s the price of {base_example}?" if lang == "en" else f"Kianzio cha {base_example.lower()} ni kiasi gani?"
        ])
    
    return variations

def augment_nlu(nlu_data, target_count=1000):
    augmented_nlu = {"version": "3.1", "nlu": []}
    
    for intent_data in nlu_data["nlu"]:
        intent = intent_data["intent"]
        examples = intent_data["examples"].split("\n- ")[1:]  # Skip first empty
        examples = [ex.strip() for ex in examples if ex.strip()]
        
        en_examples = [ex for ex in examples if not any(w in ex.lower() for w in ["ni", "ya", "jinsi", "nawezaje"])]
        sw_examples = [ex for ex in examples if any(w in ex.lower() for w in ["ni", "ya", "jinsi", "nawezaje"])]
        
        new_examples = set(examples)
        for ex in en_examples[:10]:  # Limit to avoid performance issues
            new_examples.update(generate_variations(ex, intent, "en"))
        for ex in sw_examples[:10]:
            new_examples.update(generate_variations(ex, intent, "sw"))
        
        # Fill to target_count efficiently
        while len(new_examples) < target_count and (en_examples or sw_examples):
            base_ex = random.choice(en_examples if random.random() < 0.5 and en_examples else sw_examples)
            lang = "en" if base_ex in en_examples else "sw"
            variations = generate_variations(base_ex, intent, lang)
            new_examples.update(variations[:5])  # Add fewer variations per iteration
        
        new_examples = list(new_examples)[:target_count]
        
        augmented_nlu["nlu"].append({
            "intent": intent,
            "examples": "- " + "\n- ".join(new_examples)
        })
    
    return augmented_nlu

def main():
    nlu_path = "data/nlu.yml"
    if not Path(nlu_path).exists():
        print(f"{nlu_path} not found.")
        return
    
    nlu_data = load_nlu(nlu_path)
    augmented_nlu = augment_nlu(nlu_data)
    save_nlu(augmented_nlu, "data/nlu.yml")

if __name__ == "__main__":
    main()