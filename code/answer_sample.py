from transformers import AutoModelForCausalLM, AutoTokenizer
import gzip
import json
import os
import re

model_name = "Qwen/Qwen3-32B"
quiz_file="../BuzzerQA/BuzzerQA-easy-v1.1.json"
output_file="../BuzzerQA/BuzzerQA-easy-v1.1-answer_llm.json"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def return_prompts(question_block):
    prompts = f"""以下の質問に解答してください。解答は文ではなく名詞などできる限り簡潔にしてください。また、解説等は含めず、答えのみを出力してください。
{question_block}
"""
    return prompts

def answer_quizzes(quizzes,output_file):
    for quiz in quizzes:
        question_block = f"質問: {quiz['question']}\n"
        print(question_block)
        prompt = return_prompts(question_block)
        messages = [
            {"role": "user", "content": prompt},
        ]
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=32768
        )
        output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 

        try:
            index = len(output_ids) - output_ids[::-1].index(151668)
        except ValueError:
            index = 0

        thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
        content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

        quiz["answer_llm"] = content
        print("thinking content:", thinking_content)
        print("content:", content)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(quizzes, f, ensure_ascii=False, indent=2)

def load_quizzes(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    quizzes = load_quizzes(quiz_file)  
    answer_quizzes(quizzes,output_file)
