# BuzzerQA
BuzzerQAは日本語の短文質問応答形式のベンチマークです。大規模言語モデル(LLM)の日本語における事実性能力の評価に用いることを想定しています。

各問題はWikipedia記事を元に、LLMによって作成されました。

問題の難易度によって2つに分かれており、より難しいBuzzerQA-hardは高性能モデル向け、より易しいBuzzerQA-easyは小型モデル向けとなっています。
BuzzerQA-hardは1,388問、BuzzerQA-easyは1,033問からなります。

また、BuzzerQA-easyよりも更に難易度が低い問題はベンチマークには含まれませんが、参考のためBuzzerQA-rejectedとして公開しています。

# フォーマット
問題ファイルはjsonオブジェクトの配列の形式を取ります。
各オブジェクトには"question", "answer", "a-id"の3つのkeyがあります。
"question"の値は問題文です。
"answer"の値は解答です。
"a-id"

# リファレンス

# ライセンス
