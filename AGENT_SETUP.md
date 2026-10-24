# Codex 與 Colab 工作區設定

本 repo 的影像、聲音、影片、配樂與後製都在 Google Colab 執行。Codex 使用本機工作區管理劇本、film.json、上傳與下載；不在本機安裝模型、不使用本機顯卡。

## 1. 本機只安裝 Colab CLI

Windows 初次設定和 Google OAuth 步驟請照 [COLAB_CLI_跨電腦連線指南.md](COLAB_CLI_跨電腦連線指南.md)。本機需要 Python 3.12、uv、Git 和網路連線；不需要 CUDA、NVIDIA 驅動、ComfyUI 或大型模型磁碟空間。

OAuth 授權須由使用者在瀏覽器完成，授權碼只輸入啟動該次登入流程的同一個 Terminal。Codex 不讀取或代貼授權碼。

## 2. 檢查帳戶和啟動前條件

在 repo 根目錄執行：

~~~powershell
python cloud/colab_h3.py check
~~~

確認 Colab 帳戶有可用運算額度，並閱讀 CLI 顯示的 H3 授權／機房提醒。額度為 0 時不要啟動 GPU；如地區未知或授權提醒未解決，先停止並確認授權條件，不要繞過提示。

## 3. 啟動完整 Colab 環境

全流程需要生圖、配音、H3、配樂與後製環境，使用完整安裝：

~~~powershell
python cloud/colab_h3.py start
~~~

只在明確只要 H3 渲染、且素材與 spec 已備妥時才使用 H3-only 安裝；一般製片請用完整安裝。Colab VM 是暫存環境，開始生成前檢查帳戶額度和素材備份。

## 4. 製作新片

1. 複製 pipeline/template_colab/ 到 pipeline/<片名>/，只在工作區編輯劇本與 film.json。
2. 先執行 `python cloud/colab_h3.py film pipeline/<片名> read`，檢查同步回來的文字讀本和時長估計；劇本通過後才花額度生成影像。
3. 在 Colab 執行 chars、masters、frames，再檢查同步回來的 out/first/_sheet.jpg。人工確認通過後才進入影片生成。
4. 在 Colab 執行 voices、h3、amb；檢查同步回來的逐鏡抽格和聽寫結果。
5. 確認後在 Colab 執行 edl、music、ending、cut、review；最後播放下載回來的完整成片。

完整命令與重跑方式見 [pipeline/template_colab/README.md](pipeline/template_colab/README.md)。執行階段時使用 cloud/colab_h3.py film pipeline/<片名> <stage...>；不要直接在本機執行 make_film.py。

## 5. 成品下載與關機

每個 film 指令會把 Colab 的 out/ 同步回該片工作區資料夾。完成成片下載並確認檔案可播放後，執行 python cloud/colab_h3.py stop。Colab 運算額度會隨工作階段和 GPU 使用而變動；長時間審片時用 status 確認機器狀態，不要讓不需要的工作階段持續執行。

## 給 Codex 的工作規則

- 所有模型推論和重型影音處理只在 Colab 執行。
- 使用者的本機只作為控制端、文字編輯端和成果檢視端。
- 不提供本機顯卡等級、VRAM、RAM 或本機生成分流方案。
- 不印出 OAuth 碼、API key 或其他憑證。
- 遵守人工關卡：劇本、首幀、逐鏡影片、完整成片都要等使用者檢視。
