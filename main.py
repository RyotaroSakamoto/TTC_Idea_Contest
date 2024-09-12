#ライブラリの読み込みと設定
import os
from io import StringIO

import chardet
import discord
from discord import app_commands
import fitz
import nest_asyncio
from openai import OpenAI

nest_asyncio.apply()

# APIキーとtokenの設定
openai_client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
DISCORD_TOKEN = os.environ["Discord_Bot_Key"]


#関数の定義
#default prompt func
def askQuestion(question="How large is the sun?"):
    completion = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role":
            "system",
            "content":
            "You are a teacher that gives simple useful answers to students."
        }, {
            "role": "user",
            "content": question
        }])

    return completion.choices[0].message.content


def print_hello():
    print("hello")


def img_add_furigana(url):
    completion = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role":
                "system",
                "content":
                "You are a teacher that gives simple useful answers to students."
            },
            {
                "role":
                "user",
                "content": [{
                    "type":
                    "text",
                    "text":
                    "画像を日本語に文字起こしし、漢字にふりがなを振って出力してください。\n出力例: ご飯(はん)を食(た)べる "
                }, {
                    "type": "image_url",
                    "image_url": {
                        "url": str(url),
                    }
                }]
            },
        ])

    return completion.choices[0].message.content


# #探索的データ分析を実行する関数
# def run_eda_analysis(csv_io):
#     prompt = f"""
#                         以下のCSVデータに対して探索的データ分析（EDA）を実行してください。データの確認、各統計量の確認、データに対する推察を段階的に実施してください。
#                         出力の条件:
#                         分析に使用したpythonコードを、ローカル環境で実行できるようにコードブロックで生成してください
#                         分析コードを実行し、実行結果をmarkdownとして整形してから出力して下さい
#                         {csv_io}
#                         """
#     completion = openai_client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are a perfect data analyst."
#             },
#             {
#                 "role": "user",
#                 "content": [{
#                     "type": "text",
#                     "text": f"{prompt}"
#                 }]
#             },
#         ])

#     return completion.choices[0].message.content


# PDFファイルをテキストに変換する関数
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


# テキストを特定の言語で要約する関数
def summarize_text(text, language):
    system_messages = {
        "kor": "Please summarize the following text in Korean:",
        "jp": "Please summarize the following text in Japanese:",
        "eng": "Please summarize the following text in English:",
        "ch": "Please summarize the following text in Chinese:"
    }

    system_message = system_messages.get(
        language, "Please summarize the following text in English:")

    completion = openai_client.chat.completions.create(model="gpt-4o",
                                                       messages=[{
                                                           "role":
                                                           "system",
                                                           "content":
                                                           system_message
                                                       }, {
                                                           "role":
                                                           "user",
                                                           "content":
                                                           text
                                                       }])
    return completion.choices[0].message.content


# 漢字にふりがなを追加する関数
def add_furigana(question):
    completion = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role":
            "system",
            "content":
            "Given a Japanese sentence, respond by adding furigana in parentheses next to all kanji characters."
        }, {
            "role": "user",
            "content": question
        }])
    return completion.choices[0].message.content


# 国ごとの文化を説明する関数
def explain_culture(question):
    completion = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role":
            "system",
            "content":
            "When a user provides a country name, respond with information about that country including its culture, population, GDP, and a brief description. The response should be in the same language as the user's question."
        }, {
            "role": "user",
            "content": question
        }])
    return completion.choices[0].message.content


# テキストを特定の言語に翻訳する関数
def translate_text(text, target_language):
    language_codes = {
        "kor": "Korean",
        "jp": "Japanese",
        "eng": "English",
        "ch": "Chinese"
    }

    target_language_name = language_codes.get(target_language, "English")

    completion = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role":
            "system",
            "content":
            f"Please translate the following text to {target_language_name}."
        }, {
            "role": "user",
            "content": text
        }])
    return completion.choices[0].message.content


help_messages = {
    "kor":
    ("**한자 후리가나 기능 (`-h`)**:\n"
     "- `-h`로 시작하는 문장을 입력하면, 봇이 한자 옆에 후리가나를 추가합니다.\n\n"
     "**국가별 문화 설명 기능 (`-b`)**:\n"
     "- `-b`로 시작하고 국가명을 입력하면, 해당 국가의 문화, 인구, GDP 등의 정보를 제공합니다.\n\n"
     "**PDF 요약 기능 (`-pdf`)**:\n"
     "- `-pdf` 뒤에 언어 코드(`kor`, `jp`, `eng`, `ch`)를 지정하고 PDF 파일을 첨부하면, 지정된 언어로 PDF 내용을 요약합니다.\n\n"
     "**번역 기능 (`-k`, `-j`, `-e`, `-ch`)**:\n"
     "- `-k`로 시작하는 문장은 한국어로, `-j`는 일본어로, `-e`는 영어로, `-ch`는 중국어로 번역됩니다."),
    "eng":
    ("**Kanji Furigana Feature (`-h`)**:\n"
     "- Starts with `-h` followed by a sentence, the bot will add furigana next to kanji characters.\n\n"
     "**Culture Explanation Feature (`-b`)**:\n"
     "- Starts with `-b` followed by a country name, the bot will provide information about that country's culture, population, GDP, etc.\n\n"
     "**PDF Summary Feature (`-pdf`)**:\n"
     "- Starts with `-pdf` followed by a language code (`kor`, `jp`, `eng`, `ch`) and attach a PDF file, the bot will summarize the content in the specified language.\n\n"
     "**Translation Feature (`-k`, `-j`, `-e`, `-ch`)**:\n"
     "- Starts with `-k` for Korean, `-j` for Japanese, `-e` for English, and `-ch` for Chinese translation."
     ),
    "jp":
    ("**漢字ふりがな機能（`-h`）**:\n"
     "- `-h` で始まる文章を入力すると、ボットが漢字の隣にふりがなを追加します。\n\n"
     "**国別文化説明機能（`-b`）**:\n"
     "- `-b` で始まり、続けて国の名前を入力すると、その国の文化、人口、GDPなどの情報を提供します。\n\n"
     "**PDF要約機能（`-pdf`）**:\n"
     "- `-pdf` の後に言語コード（`kor`、`jp`、`eng`、`ch`）を指定し、PDFファイルを添付すると、指定された言語でPDFの内容を要約します。\n\n"
     "**翻訳機能 (`-k`, `-j`, `-e`, `-ch`)**:\n"
     "- `-k` で始まる文は韓国語に、`-j` は日本語に、`-e` は英語に、`-ch` は中国語に翻訳されます。"),
    "ch":
    ("**汉字注音功能 (`-h`)**:\n"
     "- 以 `-h` 开头并跟随句子时，机器人会在汉字旁边添加注音。\n\n"
     "**国家文化说明功能 (`-b`)**:\n"
     "- 以 `-b` 开头并跟随国家名称时，机器人将提供该国家的文化、人口、GDP等信息。\n\n"
     "**PDF总结功能 (`-pdf`)**:\n"
     "- 以 `-pdf` 开头并跟随语言代码（`kor`、`jp`、`eng`、`ch`），并附加 PDF 文件时，机器人将根据指定语言总结内容。\n\n"
     "**翻译功能 (`-k`, `-j`, `-e`, `-ch`)**:\n"
     "- 以 `-k` 开头的句子将翻译为韩语，`-j` 为日语，`-e` 为英语，`-ch` 为中文。")
}


def main():

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)

    @client.event
    async def on_ready():
        print("起動完了")
        await tree.sync()  #スラッシュコマンドを同期

    @client.event
    async def on_message(message):
        # ボット自身のメッセージを無視します
        if message.author == client.user:
            return

        # 漢字ふりがな提供機能
        if message.content.startswith("-h"):
            question = message.content[3:]  # '-h ' 以降の質問を抽出
            furigana = add_furigana(question)
            await message.channel.send(furigana)

        # 国ごとの文化説明機能
        elif message.content.startswith("-b"):
            question = message.content[3:]  # '-b ' 以降の質問を抽出
            culture_info = explain_culture(question)
            await message.channel.send(culture_info)

        # PDF要約機能
        elif message.content.startswith("-pdf") and message.attachments:
            try:
                command_parts = message.content.split()
                if len(command_parts) != 2:
                    await message.channel.send(
                        "Please provide the correct command format, e.g., `-pdf kor`."
                    )
                    return

                language = command_parts[1].lower()
                valid_languages = ["kor", "jp", "eng", "ch"]

                if language not in valid_languages:
                    await message.channel.send(
                        "Supported languages are 'kor' for Korean, 'jp' for Japanese, 'eng' for English, and 'ch' for Chinese."
                    )
                    return

                attachment = message.attachments[0]
                if attachment.filename.endswith(".pdf"):
                    pdf_data = await attachment.read()  # PDF 파일 읽기
                    text = extract_text_from_pdf(
                        io.BytesIO(pdf_data))  # PDF 텍스트 추출
                    summary = summarize_text(text, language)  # 텍스트 요약

                    await message.channel.send(
                        f"Here is the summary of the PDF in {language}:\n\n{summary}"
                    )
                else:
                    await message.channel.send(
                        "Please upload a valid PDF file.")

            except Exception as e:
                await message.channel.send(f"An error occurred: {str(e)}")

        # 翻訳機能
        elif message.content.startswith("-k"):
            text = message.content[3:]
            translation = translate_text(text, "kor")
            await message.channel.send(translation)

        elif message.content.startswith("-j"):
            text = message.content[3:]
            translation = translate_text(text, "jp")
            await message.channel.send(translation)

        elif message.content.startswith("-e"):
            text = message.content[3:]
            translation = translate_text(text, "eng")
            await message.channel.send(translation)

        elif message.content.startswith("-ch"):
            text = message.content[3:]
            translation = translate_text(text, "ch")
            await message.channel.send(translation)

        # ヘルプ機能
        elif message.content.startswith("-?"):
            command_parts = message.content.split()
            if len(command_parts) != 2:
                await message.channel.send(
                    "Please provide the correct command format, e.g., `-? eng`."
                )
                return

            language = command_parts[1].lower()
            help_message = help_messages.get(language, help_messages["eng"])
            await message.channel.send(help_message)

    @tree.command(name="test", description="テストコマンドです。")
    async def test_command(interaction: discord.Interaction):
        await interaction.response.send_message(
            "てすと！")  #ephemeral=True→「これらはあなただけに表示されています」

    @tree.command(name="gpt", description="ChatGPTと対話を行います\n引数にプロンプトを入力してください")
    async def gpt(interaction: discord.Interaction, prompt: str):
        #プロンプトをgpt-4oに渡して出力を得る
        message_to_sent = askQuestion(prompt)
        #channelに結果を送信する
        await interaction.response.send_message(message_to_sent)

    @tree.command(name="img2f", description="添付された画像から文字を読み取り、ふりがなを付けて返信します。")
    async def img2f(interaction: discord.Interaction, img: discord.Attachment):
        await interaction.response.defer()
        message = img_add_furigana(img.url)
        # url = "https://cdn.discordapp.com/ephemeral-attachments/1282936421732323402/1282950560290570290/wdawdawadad.png?ex=66e13851&is=66dfe6d1&hm=5f4e5b5add506f1cdfb000797b23c175ef86451c4ac9d681af8f86dd0520b535&"
        print(img.url)
        print(type(img.url))
        embed = discord.Embed(
            title=f"{message}",
            color=0x00ff00,
            description=f"",
            url=img.url,
        )
        embed.set_image(url=img.url)  # 大きな画像タイルを設定できる

        await interaction.followup.send("", embed=embed)

    # #csvファイルの探索的データ分析
    # @tree.command(name="csv_analysis",
    #               description="csvファイルのデータから探索的データ分析を実行します。")
    # async def csv_analysis(interaction: discord.Integration,
    #                        csv_file: discord.Attachment):
    #     await interaction.response.defer()

    #     if csv_file.filename.endswith(".csv"):
    #         file_data = await csv_file.read()
    #         result = chardet.detect(file_data)
    #         encoding = result["encoding"]
    #         print(f"csv_files encoding is {encoding}")

    #         try:
    #             file_content = file_data.decode(encoding=encoding)
    #             print(f"csv_file: \n{file_content}")
    #             analysis_result = run_eda_analysis(file_content)

    #             if len(analysis_result) < 2000:
    #                 await interaction.followup.send(analysis_result,
    #                                                 split=True)
    #             else:
    #                 # analysis_result をテキストファイルとして保存し、ファイルとして送信
    #                 with StringIO() as text_file:
    #                     text_file.write(analysis_result)
    #                     text_file.seek(0)  # ファイルポインタを先頭に移動
    #                     await interaction.followup.send(file=discord.File(
    #                         text_file, filename="analysis_result.md"))

    #         except Exception as e:
    #             print(f"error: {e}")
    #             await interaction.followup.delete_message()

    #     else:
    #         await interaction.followup.send(f"error: {csv_file.filename=}")

    client.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
