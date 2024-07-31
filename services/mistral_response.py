from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from configs.config_param import model, api_key, new_dict
from fuzzywuzzy import process, fuzz
import numpy as np

client = MistralClient(api_key=api_key,timeout=50)


# The `FuzzyMatch` class provides methods for fuzzy matching lists, extracting top five matched key
# components, and retrieving content based on indexes.
class FuzzyMatch:
    @staticmethod
    def fuzzy_match_lists(list1, dict2):
        print(">fuzzy_match_lists",end="")
        results = {}
        for key, texts in dict2.items():
            if texts := texts[0]:
                scores = []
                for text in list1:
                    matches = process.extract(text, texts, scorer=fuzz.ratio)
                    best_match = matches[0]  # Most relevant match
                    scores.append(best_match[1])  # Append the score of the best match
                average_score = np.mean(scores) if scores else 0
                if average_score > 80:
                    results[key] = {
                        'average_score': average_score,
                        'element_count': len(texts),
                        'matches': [(text, process.extract(text, texts, scorer=fuzz.ratio)[0]) for text in list1]}
        return results
    @staticmethod
    def get_top_five_matched_key_components(results):
        print(">get_top_five_matched_key_components",end="")
        return sorted(results.items(), key=lambda item: item[1]['average_score'], reverse=True)[:5]
    
    @staticmethod
    def give_indexes_from_keycomponents(values: list, threshold=5)->list: #example:- values ["effect", "person unaware of exact income amount", "income diversion"]
        print(">give_indexes_from_keycomponents",end="")
        top_five_component = FuzzyMatch.get_top_five_matched_key_components(FuzzyMatch.fuzzy_match_lists(values,new_dict))
        print("top_five_component==>>", top_five_component)
        return list(map(lambda x: x[0],  top_five_component   )) if top_five_component else None
    
    @staticmethod
    def get_content_from_index(values: list):
        print(">get_content_from_index",end="")
        indexed_components=FuzzyMatch.give_indexes_from_keycomponents(values)
        return list(map(lambda index: (index,new_dict.get(index)[1][:new_dict.get(index)[1].find("\n")]),indexed_components)) if  indexed_components else None

class MistralAiConversation:
    @staticmethod
    def get_key_components_from_text(text:str)->list:
        print(">get_key_components_from_text",end="")
        return eval(client.chat(
            model=model,
            response_format={"type": "json_object"},
            messages=[
                ChatMessage(role="user", content=f"""Just give key_components = [ ] break down the question into key components give vector representation "{text}" only Give python list code. Nothing else. do not give variable name and "=" sign just value. make question shorter""")],).choices[0].message.content)
    
    @staticmethod
    def write_valid_response_according_prompt(text:str)->list:
        print(">write_valid_response_according_prompt",end="")
        result = client.chat(
            model=model,
            response_format={"type": "json_object"},
            messages=[
                ChatMessage(role="user", content=f"""'{text}' check this question is it relate to tax laws in India or not if yes than say please ask question it more clearly if not than give response ask only question for undertand indian consitutions""")],)
        print("result==>", result)
        return result.choices[0].message.content
    
    
    @staticmethod
    def get_one_qa_from_list(user_text:str,indexed_side_text)->bool:
        print(">get_one_qa_from_list",end="")
        return eval(client.chat(
            model=model,
            response_format={"type": "json_object"},
            messages=[
                ChatMessage(role="user", content=f"""this is first question "{user_text}" this is second question "{indexed_side_text}" if this two String contain same question or simileraty is very high that return True else False only in Capitalize""")],).choices[0].message.content.capitalize())

    @staticmethod
    def get_answer_from_dict_make_it_informative(index:int):
        print(">get_answer_from_dict_make_it_informative",end="")
        text_getted =new_dict.get(index)[1]
        word_index = text_getted.find("\n")
        return text_getted[word_index:]
        # return client.chat(
        #     model=model,
        #     response_format={"type": "json_object"},
        #     messages=[
        #         ChatMessage(role="user", content=f"""'{text_getted[word_index:]}' Just Give Answer from this string if string if it contains else 'please ask another question this is not in my database'""")],).choices[0].message.content
    
    @staticmethod
    def verify_each_query_and_get_answer(values,user_input):
        print(">verify_each_query_and_get_answer",end="")
        # for i,each in enumerate(values):
        #     print("index============>>>>>>>>>",i)
        #     if MistralAiConversation.get_one_qa_from_list(each[1],user_input):
        #         final_val = each[0]
        #         break
        return values[0][0]
    
    @staticmethod
    def user_to_server_conversation_flow(user_input:str):
        print(">user_to_server_conversation_flow",end="")
        if verify_each := FuzzyMatch.get_content_from_index(MistralAiConversation.get_key_components_from_text(user_input)):
            return MistralAiConversation.get_answer_from_dict_make_it_informative(MistralAiConversation.verify_each_query_and_get_answer(verify_each,user_input))
        else:
            print("else")
            return MistralAiConversation.write_valid_response_according_prompt(user_input)
        