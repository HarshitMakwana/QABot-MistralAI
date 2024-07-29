from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from configs.config_param import model, api_key

client = MistralClient(api_key=api_key)

class MistralAiConversation:
    def get_key_components_from_text(text:str)->list:
        return eval(client.chat(
            model=model,
            response_format={"type": "json_object"},
            messages=[
                ChatMessage(role="user", content=f"""Just give key_components = [ ] break down the question into key components give vector representation "{text}" only Give python list code. Nothing else. do not give variable name and "=" sign just value. make question shorter""")],).message.content)
    def get_one_qa_from_list(index_list:list)->str:
        return None
    def get_top_five_qa_from_list():
        return None
    def detect_out_of_context_queries():
        return None