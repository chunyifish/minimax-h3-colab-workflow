# 影片片尾範本

本範本提供特寫、工具名單和標題卡的結構。它源自原作者的頻道範例；製作自己的影片時，請將頻道名稱、片名、特寫素材和工具名單換成實際內容。

## Colab 工作流

一般製片由 pipeline/template_colab/make_film.py 在 Colab VM 產生片尾。使用者只編輯 film.json，然後透過工作區執行：

~~~powershell
python cloud/colab_h3.py film pipeline/my_film ending
~~~

新片完整指令和其他人工關卡見 pipeline/template_colab/README.md。本機不直接執行 render_ending.py。

## 片尾內容

1. 使用本片實際畫面作特寫，名單只列實際使用的工具。
2. 列出使用 MiniMax Music 3 等工具前先閱讀其授權，並依要求標示工具與 AI 生成內容。
3. 標題改成自己的片名或頻道名，不要沿用原作者的品牌文字。
4. 每張卡最多列 3 行工具，避免字幕太小。
5. 片尾影片由 Colab 產生，通常為 1920×1080、24fps；成片聲音由主影片的組裝階段合併。

config_example.json 可參考卡片資料格式；實際片尾設定由 film.json 的 ending 欄位控制。