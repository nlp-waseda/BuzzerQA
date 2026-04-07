from transformers import AutoModelForCausalLM, AutoTokenizer
import gzip
import json
import os
import re
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="LLMで解答と模範解答の一致判定")
    parser.add_argument(
        "--model_name",
        type=str,
        default="Qwen/Qwen3-32B",
        help="模範解答との一致判定に用いるLLMのHugging Faceにおけるモデル名"
    )
    parser.add_argument(
        "--quiz_file",
        type=str,
        default="../BuzzerQA/BuzzerQA-easy-v1.1-answer_llm.json",
        help="解答データのパス"
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default=None,
        help="出力(採点データ)のパス"
    )
    return parser.parse_args()

def return_prompts(question_block):
    prompts = f"""模範解答とLLMの解答が一致しているかを判定してください。一致している場合は"correct"、異なる場合は"incorrect"と答えてください。それ以外の返答は行わないでください。
なお、表記揺れだと考えられる場合は一致していると判定してください。例えば「コンピュータ」と「コンピューター」のようにカタカナ語における長音の有無や、「富士山」と「ふじさん」のように表記方法の違いは一致しているとみなします。
{question_block}
"""
    return prompts

def score_quizzes(quizzes, model, tokenizer, output_file):
    correct_count = 0
    incorrect_count = 0

    for quiz in quizzes:
        question_block = f"模範解答: {quiz['answer']}\nLLMの解答: {quiz['answer_llm']}\n"
        print(question_block)
        prompt = return_prompts(question_block)

        messages = [{"role": "user", "content": prompt}]
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

        generated_ids = model.generate(**model_inputs, max_new_tokens=32768, top_k=1)
        output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()

        try:
            index = len(output_ids) - output_ids[::-1].index(151668)
        except ValueError:
            index = 0

        content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip()

        result = re.sub(r'[^a-z]', '', content.lower())
        quiz["result_llm"] = result

        if result == "correct":
            correct_count += 1
        elif result == "incorrect":
            incorrect_count += 1

    total = correct_count + incorrect_count
    score = correct_count / total if total > 0 else 0

    print(f"correct: {correct_count}")
    print(f"incorrect: {incorrect_count}")
    print(f"score: {score:.4f}")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(quizzes, f, ensure_ascii=False, indent=2)

def load_quizzes(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def make_default_output_path(input_path):
    base, ext = os.path.splitext(input_path)
    return f"{base}_scored{ext}"

if __name__ == "__main__":
    args = parse_args()

    output_file = args.output_file if args.output_file else make_default_output_path(args.quiz_file)

    print("model_name:", args.model_name)
    print("quiz_file:", args.quiz_file)
    print("output_file:", output_file)

    model = AutoModelForCausalLM.from_pretrained(
        args.model_name,
        torch_dtype="auto",
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)

    quizzes = load_quizzes(args.quiz_file)
    score_quizzes(quizzes, model, tokenizer, output_file)
