# Discord Bot for Language Processing and EDA

## 前置き

このプロジェクトはTTC_Idea_Contestにて制作された現在制作途中であり、大規模な変更がある可能性があります。

## 概要

このプロジェクトは、Discord上で様々な言語処理機能と探索的データ分析(EDA)機能を提供するボットです。ユーザーはメッセージを通じてボットとやり取りし、翻訳や文化の説明、PDFの要約、漢字のふりがな追加、CSVファイルのEDAなど、幅広い機能を利用できます。

## 使用技術

- **Python**: メインのプログラム言語。
- **Discord.py**: Discordとのインターフェース用ライブラリ。
- **OpenAI API**: GPT-4を利用した自然言語処理機能。
- **fitz (PyMuPDF)**: PDF処理ライブラリ。
- **chardet**: 文字エンコーディング検出ライブラリ。

## 主な機能

1. **漢字ふりがな追加機能** (`-h`)

   - 日本語の文章内の漢字にふりがなを追加します。
2. **国ごとの文化説明機能** (`-b`)

   - 指定された国について、文化、人口、GDPなどを説明します。
3. **PDF要約機能** (`-pdf`)

   - PDFファイルをアップロードし、指定した言語（日本語、韓国語、英語、中国語）で内容を要約します。
4. **翻訳機能**

   - 指定したテキストを、韓国語（`-k`）、日本語（`-j`）、英語（`-e`）、中国語（`-ch`）に翻訳します。
5. **探索的データ分析機能** (`csv_analysis`)

   - CSVファイルに対して探索的データ分析（EDA）を実行し、結果を提供します。
6. **画像からのふりがな付け機能** (`img2f`)

   - アップロードされた画像のテキストを抽出し、ふりがなを追加して返答します。

## 環境変数の設定

以下の環境変数を設定する必要があります。

- `OPENAI_API_KEY`: OpenAI APIキー
- `Discord_Bot_Key`: Discord Botのトークン

## 実行方法

1. リポジトリをクローンします。

   ```
   git clone <repository_url>
   cd <repository_directory>
   ```
2. 必要なパッケージをインストールします。

   ```
   pip install -r requirements.txt
   ```
3. 環境変数を設定します。

   ```Bash

   #Linux,Mac
   export OPENAI_API_KEY=<your_openai_api_key>
   export Discord_Bot_Key=<your_discord_bot_key>
   ```
4. Botを実行します。

   ```
   python main.py
   ```

## コマンド一覧

- `-h <日本語文>`: 漢字にふりがなを追加。
- `-b <国名>`: 指定した国の文化や情報を提供。
- `-pdf <言語コード>`: PDFをアップロードして指定言語で要約。
- `-k <テキスト>`: 韓国語に翻訳。
- `-j <テキスト>`: 日本語に翻訳。
- `-e <テキスト>`: 英語に翻訳。
- `-ch <テキスト>`: 中国語に翻訳。
- `/csv_analysis <CSVファイル>`: アップロードしたCSVに対してEDA(簡易な探索的データ分析)を実行。
- `/img2f <画像>`: 画像内のテキストにふりがなを追加。


## 貢献

バグ報告や新機能の提案は、Issueにてお願いします。
