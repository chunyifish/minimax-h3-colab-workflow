# MiniMax H3 Colab 工作流（Codex 版）

這是以 Google Colab 為唯一模型執行環境的 MiniMax H3 影片製作工作流。原始專案與授權資訊見 [第三方聲明](THIRD_PARTY_NOTICES.md)；本 fork 的 GitHub 名稱為 minimax-h3-colab-workflow。

## 執行原則

- 生圖、角色參考音、H3 影片、配樂、放大、剪接、字幕與自審全部在 Colab 雲端執行。
- Codex 與使用者在工作區撰寫劇本、調整 film.json、查看下載回來的階段成果，並用 Colab CLI 指揮雲端工作。
- 本機電腦只需能執行 Colab CLI、連網、編輯文字檔及下載／查看成果；不需要 NVIDIA 顯卡、模型權重或本機 ComfyUI。
- 不支援本機 GPU、混合本機與 Colab 的生成流程。

## 開始前

需要可用的 Colab 運算額度。Google AI 方案、學生優惠或 Colab 登入狀態本身不代表帳號一定有可用額度；先執行額度檢查。若餘額是 0，先處理帳戶資格或額度，不要啟動 GPU。

Windows 上安裝與登入 Colab CLI、處理授權頁和常見錯誤，請照 [Codex／Colab CLI 跨電腦連線指南](COLAB_CLI_跨電腦連線指南.md)。OAuth 授權碼只貼回啟動登入的 Terminal，不要貼到聊天、文件或截圖。

## 快速流程

在工作區 Terminal 安裝並登入後：

~~~powershell
python cloud/colab_h3.py check
~~~

確認帳號有可用額度，並讀取啟動前的授權與地區提醒。符合帳戶條件且使用者決定開始後，啟動完整雲端環境：

~~~powershell
python cloud/colab_h3.py start
~~~

複製範本，修改新資料夾裡的 film.json：

~~~powershell
Copy-Item pipeline/template_colab pipeline/my_film -Recurse
~~~

先在 Colab 產生文字讀本，確認劇情節奏後再生成影像。此階段不呼叫生成模型，但 Colab 工作階段仍會依帳戶方案計算資源使用：

~~~powershell
python cloud/colab_h3.py film pipeline/my_film read
~~~

檢查同步回來的 `pipeline/my_film/out/preview/讀本試映.mp4` 和 `讀本_timeline.json`。劇本通過後再執行下列影像階段：

以下指令會把製片資料夾上傳到 Colab，在 Colab 執行指定階段，並把 out/ 成果下載回同一個工作區資料夾：

~~~powershell
python cloud/colab_h3.py film pipeline/my_film chars masters frames
~~~

檢查下載回來的角色圖、場景圖與首幀，確認後再生成聲音與影片：

~~~powershell
python cloud/colab_h3.py film pipeline/my_film voices h3 amb
~~~

檢查每鏡影片與自審結果，再完成剪接、配樂、片尾與成片：

~~~powershell
python cloud/colab_h3.py film pipeline/my_film edl music ending cut review
~~~

完成下載後關閉 Colab 工作階段：

~~~powershell
python cloud/colab_h3.py stop
~~~

需要確認工作階段時使用 python cloud/colab_h3.py status。詳細操作、限制與故障排除見 [cloud/README.md](cloud/README.md)。

## 目錄

- [AGENTS.md](AGENTS.md)：本 repo 給 Codex 的 Colab-only 工作規則。
- [AGENT_SETUP.md](AGENT_SETUP.md)：第一次使用的簡要步驟。
- [cloud/README.md](cloud/README.md)：Colab CLI、完整生成、額度與故障排除。
- [COLAB_CLI_跨電腦連線指南.md](COLAB_CLI_跨電腦連線指南.md)：Windows CLI 安裝與 Google 授權。
- [docs/colab-resources.md](docs/colab-resources.md)：Colab 額度與雲端運算資源管理。
- [docs/02_端到端流程.md](docs/02_端到端流程.md)：影片製作階段與人工檢查點。
- [pipeline/template_colab/README.md](pipeline/template_colab/README.md)：film.json 欄位與範本操作。
- [docs/03_規則與踩坑.md](docs/03_規則與踩坑.md)、[docs/04_自審清單.md](docs/04_自審清單.md)：生成規則與成片檢查。

範本、工具與範例素材依各自授權使用。使用模型前請讀 [第三方聲明](THIRD_PARTY_NOTICES.md)，並遵守模型授權、Colab 條款與內容標示要求。
