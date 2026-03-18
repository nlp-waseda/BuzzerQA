# BuzzerQA
BuzzerQAは日本語の短文質問応答形式のベンチマークです。大規模言語モデル(LLM)の日本語における事実性能力の評価に用いることを想定しています。

各問題はWikipedia記事を元に、LLMによって作成されました。

問題の難易度によって2つに分かれており、より難しいBuzzerQA-hardは高性能モデル向け、より易しいBuzzerQA-easyは小型モデル向けとなっています。
BuzzerQA-hardは1,388問、BuzzerQA-easyは1,033問からなります。

また、BuzzerQA-easyよりも更に難易度が低い問題はベンチマークには含まれませんが、参考のためBuzzerQA-rejectedとして公開しています。

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
"answer"と"answer_llm"が問題に対する解答として同一であるかをLLM-as-a-judgeで評価し、正答率をスコアとします。

score.pyを実行してください。

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
