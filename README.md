# BuzzerQA
BuzzerQAは人間向けクイズを模した日本語の短文質問応答形式のベンチマークです。大規模言語モデル(LLM)の日本語における事実性能力の評価に用いることを想定しています。

各問題はWikipedia記事を元に、LLMを用いた多段階処理によって作成しました。
問題の難易度によって2つに分かれており、より難しいBuzzerQA-hardは高性能モデル向け、より易しいBuzzerQA-easyは小型モデル向けとなっています。
また、BuzzerQA-easyよりも更に難易度が低い問題はベンチマークには含まれませんが、参考のためBuzzerQA-rejectedとして公開しています。
記事の要約および作問にはQwen3-32B (thinking mode)を、難易度の推定にはCALM3-22B-Chat, Gemma 3 27B IT, llm-jp-3.1-13b-instruct4, Phi-4, Qwen3-32B (thinking mode)を用いました。

# 変更履歴
## v1.1
不適当な問題の削除やより公平な条件での難易度推定を行い、再分類しました。内容が変更された問題はありません。
この結果、BuzzerQA-hardは1,370問、BuzzerQA-easyは966問となりました。

## v1.0
初期リリース


# 問題フォーマット
問題データはjsonオブジェクトの配列の形式を取ります。
各オブジェクトには"question", "answer", "a-id"の3つのkeyがあります。
"question"は問題文、"answer"は解答です。
"a-id"は各問題に割り振られたIDです。"buzzer-qa-*n*"(nは0以上の整数)となっており、rejectedを含めた全体で重複していません。

以下に例を示します。
```
{
"question": "頭頂部に水を必要とする皿があり、それが乾いたり割れたりすると力を失ったり死ぬとされる、中国の河伯信仰や水虎（スイコ）と関連が指摘されている、水神の零落した姿とされる存在は何でしょう？",
"answer": "河童",
"a-id": "buzzer-qa-1740"
}
```

# 解答と評価
## 解答
"question"に対する解答を"answer_llm"というkeyとして問題データに追加してください。

Qwen3-32Bを使用して解答する場合のサンプルコードが`code/answer_sample.py`です。
```
python answer_sample.py \
  --model_name Qwen/Qwen3-32B \
  --quiz_file ../BuzzerQA/BuzzerQA-easy-v1.1.json \
  --output_file ../BuzzerQA/BuzzerQA-easy-v1.1-answer_llm.json
```
- `--model_name`: 解答に用いるLLMのHugging Faceにおけるモデル名
- `--quiz_file`: 問題データのパス
- `--output_file`: 出力(解答データ)のパス

## 評価
"answer"と"answer_llm"が問題に対する解答として同一であるかをLLM-as-a-judgeで評価し、正答率をスコアとします。デフォルトではLLMとしてQwen3-32Bを用いています。

`code/score.py`を実行してください。
```
python score.py \
  --model_name Qwen/Qwen3-32B \
  --answer_file ../BuzzerQA/BuzzerQA-easy-v1.1-answer_llm.json \
  --output_file ../BuzzerQA/BuzzerQA-easy-v1.1-answer_llm-scored.json
```
- `--model_name`: 模範解答との一致判定に用いるLLMのHugging Faceにおけるモデル名
- `--answer_file`: 解答データのパス
- `--output_file`: 出力(採点データ)のパス

# 評価結果

v1.1を用いたいくつかのLLMの評価結果を記載します。

|モデル名                                           |hard   | easy   |
| ------------------------------------------------ | ------ | -------| 
| GPT-5.2 (reasoning.effort = medium)                               | 0.394     | 0.813 |
| GPT-5.2 (reasoning.effort = none)                       | 0.231 | 0.713     |
| GPT-5                        | 0.495     | 0.853     |
| GPT-5 mini                     | 0.195     | 0.653     |
| GPT-5 nano  | 0.079     | 0.413     |
| GPT-4o  | 0.191 | 0.649 |
| GPT-4o mini  | 0.031 | 0.281 |
| OpenAI o3  | 0.465 | 0.841 |
| Claude Opus 4.5  | 0.355 | 0.817 |
| Claude Sonnet 4.5 | 0.242 | 0.702 |
| Gemini 3 Pro | **0.704** | **0.911** |
| Gemini 3 Flash | 0.591 | 0.889 |
| Qwen3-8B (thinking mode) | 0.017 | 0.137 |
| Qwen3-8B (non-thinking mode) | 0.010 | 0.069 |
| Qwen3-32B (non-thinking mode)  | 0.016 | 0.136 |
| llm-jp-3.1-8x13b-instruct4  | 0.088 | 0.463 |
| Llama 3.3 Swallow 70B Instruct v0.4 | 0.095 | 0.517 |

# 参考文献
```
{sasaki-jsai2026,
    title = "人間向けクイズを模した高難易度日本語QAベンチマークの構築",
    author = "佐々木斗海 and 河原大輔",
    booktitle = "2026年度人工知能学会全国大会",
    year = "2026",
}
```

# ライセンス
本ベンチマークは [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) の下で公開しています。
