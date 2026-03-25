# BuzzerQA
BuzzerQAは日本語の短文質問応答形式のベンチマークです。大規模言語モデル(LLM)の日本語における事実性能力の評価に用いることを想定しています。

各問題はWikipedia記事を元に、LLMによって作成されました。

問題の難易度によって2つに分かれており、より難しいBuzzerQA-hardは高性能モデル向け、より易しいBuzzerQA-easyは小型モデル向けとなっています。

また、BuzzerQA-easyよりも更に難易度が低い問題はベンチマークには含まれませんが、参考のためBuzzerQA-rejectedとして公開しています。

## v1.1
発表時の問題に対し、不適当な問題の削除やより公平な条件での難易度推定を行い、再分類しました。内容が変更された問題はありません。

この結果、BuzzerQA-hardは1,370問、BuzzerQA-easyは966問となりました。


# 問題フォーマット
問題ファイルはjsonオブジェクトの配列の形式を取ります。
各オブジェクトには"question", "answer", "a-id"の3つのkeyがあります。
"question"は問題文、"answer"は解答です。
"a-id"は各問題に割り振られたIDです。"prod-*n*"(nは0以上の整数)となっており、rejectedを含めた全体で重複していません。

以下に1例を示します。
```
{
"question": "頭頂部に水を必要とする皿があり、それが乾いたり割れたりすると力を失ったり死ぬとされる、中国の河伯信仰や水虎（スイコ）と関連が指摘されている、水神の零落した姿とされる存在は何でしょう？",
"answer": "河童",
"a-id": "prod-1740"
}
```

# 解答と評価
## 解答
"question"に対する解答を"answer_llm"として、問題ファイルに保存してください。

Qwen3-32Bを使用する場合のサンプルファイルがanswer_sample.pyとしてあります。

## 評価
"answer"と"answer_llm"が問題に対する解答として同一であるかをLLM-as-a-judgeで評価し、正答率をスコアとします。デフォルトではLLMとしてQwen3-32Bを用いています。

score.pyを実行してください。

# 評価結果

v1.1を用いたいくつかのLLMの評価結果を記載します。

|モデル名                                           |hard   | easy   |
| ------------------------------------------------ | ------ | -------| 
| GPT-5.2 (reasoning.effort = medium)                               | 0.396     | 0.803 |
| GPT-5.2 (reasoning.effort = none)                       | 0.229 | 0.712     |
| GPT-5                        | 0.493     | 0.850     |
| GPT-5 mini                     | 0.187     | 0.638     |
| GPT-5 nano  | 0.080     | 0.419     |
| GPT-4o  | 0.187 | 0.638 |
| GPT-4o mini  | 0.033 | 0.291 |
| OpenAI o3  | 0.465 | 0.837 |
| Claude Opus 4.5  | 0.352 | 0.817 |
| Claude Sonnet 4.5 | 0.240 | 0.702 |
| Gemini 3 Pro | **0.699** | **0.910** |
| Gemini 3 Flash | 0.586 | 0.882 |
| Qwen3-8B (thinking mode) | 0.022 | 0.145 |
| Qwen3-8B (non-thinking mode) | 0.011 | 0.083 |
| Qwen3-32B (non-thinking mode)  | 0.019 | 0.145 |
| llm-jp-3.1-8x13b-instruct4  | 0.084 | 0.466 |
| Llama 3.3 Swallow 70B Instruct v0.4 | 0.102 | 0.512 |

# リファレンス
```
{sasaki-jsai2026,
    title = "人間向けクイズを模した高難易度日本語QAベンチマークの構築",
    author = "佐々木斗海 and 河原大輔",
    booktitle = "2026年度人工知能学会全国大会",
    year = "2026",
}
```

# ライセンス
本データセットは [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)の下で公開されています。
