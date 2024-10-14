import re

def extract_session_id(session_str : str):
    match = re.search(r"sessions/(.*?)/contexts", session_str)

    if match:
        extracted_string = match.group(1)
        return extracted_string

    return ""

def get_dict_to_str(food_dict:dict):
    return ', '.join([f"{v} {k}" for k, v in food_dict.items()])

if __name__ == "__main__":
    print(get_dict_to_str({"samosa":2,"pizza":1}))
    print(extract_session_id("projects/pandeyjichatbot-lsdq/agent/sessions/6af3edd6-7ca4-b1df-7472-779a3e08acf9/contexts/ongoing-order"))