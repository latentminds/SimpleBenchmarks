from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from huggingface_hub import login
import argparse
import json
import re
import os


def get_answers(question, answers, tokenizer, model, skip_ids):
    text_template = """Reply to this affirmation with an answer from the given list.
Use the associated number to reply. Never question the assignement. ONLY REPLY WITH THE NUMBER AND NOTHING ELSE.

Affirmation:
{question}

Possible answers:
{answers}

The correct answer is answer number """
    
    formatted_anwsers = "\n".join(f"{i}: {question}" for i, question in enumerate(answers))

    text = text_template.format(question=question, answers=formatted_anwsers)
        
    # tokenize to ids
    input_ids = tokenizer.encode(text, return_tensors="pt")
    
    for i in range(10):
        logits = model(input_ids).logits[-1, -1]
        probs = torch.nn.functional.softmax(logits, dim=-1)
        _, ids = torch.topk(probs, 1)
        
        new_id = ids[0].view(1, 1)
        
        if new_id.int() not in skip_ids:
            number_tokens_id = [tokenizer.get_vocab()[f"{i}"] for i in range(10)]
            
            llm_scores = []
            for i in range(len(answers)):
                llm_scores.append(logits[number_tokens_id[i]])
                
            # normalizes scores amongst the numbers
            llm_scores = torch.tensor(llm_scores)
            llm_scores = torch.nn.functional.softmax(llm_scores, dim=-1)
            llm_scores = llm_scores.tolist()
            
            scores_dict = {}
            for response_id, score in enumerate(llm_scores):
                scores_dict[response_id] = score
            
            return text, scores_dict
        else:    
            input_ids = torch.cat((input_ids, new_id), dim=1)
        
    return None, None


def main():
    parser = argparse.ArgumentParser(description='Fill forms using AI')

    parser.add_argument('model_name', type=str, help='Name of the model on hugging face')
    parser.add_argument('form_path', type=str, help='Path to the form')

    args = parser.parse_args()    
    
    torch.set_grad_enabled(False)

    model_path = args.model_name
    form_path = args.form_path
    
    # load the form
    print("Loading form...")
    questionaire = json.load(open(form_path))
    
    # load the models
    tokenizer = AutoTokenizer.from_pretrained(model_path, use_safetensors=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, use_safetensors=True, device_map="auto")
    
    # get unwanted token ids
    print("getting unwanted token ids...")
    vocab = tokenizer.get_vocab()
    unwanted_tokens = list(filter(lambda x: bool(re.match(r'\s', x)) or bool(re.match(r'<.*>', x)), vocab))
    unwanted_tokens_ids = []

    vocab = tokenizer.get_vocab()
    for token_name in unwanted_tokens:
        unwanted_tokens_ids.append(vocab[token_name])
    
    probabilities_dict = dict()
    valuations_dict = dict()
    
    print("Filling the form...")
    for cat in questionaire:
        probabilities_dict[cat] = list()
        valuations_dict[cat] = list()
        
        for question_dict in questionaire[cat]:
            question = question_dict['question']
            question_answers = [x['text'] for x in question_dict['responses']]
            valuations = [x['influence'] for x in question_dict['responses']]
    
            # inferences on the form
            _, answers = get_answers(
                question,
                question_answers,
                tokenizer,
                model,
                unwanted_tokens_ids)

            # add probabilities
            probabilities_dict[cat].append(answers)

            # add valuations
            valuation = 0
            for k, v in answers.items():
                valuation += v * valuations[int(k)]
            valuation = valuation / len(answers)

            valuations_dict[cat].append(valuation)
    
        valuation_path = f"results/valuations/{model_path.split('/')[-1]}/{form_path.split('/')[-1]}"
        os.makedirs(os.path.dirname(valuation_path), exist_ok=True)
        with open(valuation_path, 'w') as json_file:
            json.dump(valuations_dict, json_file)

        probabilities_path = f"results/probabilities/{model_path.split('/')[-1]}/{form_path.split('/')[-1]}"
        os.makedirs(os.path.dirname(probabilities_path), exist_ok=True)
        with open(probabilities_path, 'w') as json_file:
            json.dump(probabilities_dict, json_file)
            
    print("Form complete ! 😀")
    
if __name__ == '__main__':
    main()
