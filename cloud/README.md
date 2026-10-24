# Google Colab 全雲端工作流（Codex 版）

本 repo 唯一支援的生成環境是 Google Colab。Codex 在使用者工作區編輯劇本與 film.json、呼叫 Colab CLI、檢視下載回來的成果；Colab VM 負責安裝模型、生成影像與聲音、執行 H3、剪接和自審。本機不需要 NVIDIA 顯卡、CUDA、ComfyUI 或模型權重。

## 1. 使用條件

- Google 帳戶必須有可用的 Colab 運算額度。登入成功或看到 Google AI 方案不保證有額度；以 colab usage 的 balance 為準。balance 為 0 時不要執行 start。
- 確認 MiniMax H3 授權條款適用於這次使用，並留意 CLI 啟動時顯示的機房地區資訊。若出現排除地區或無法確認位置的提醒，先停止並核對條款；不要繞過提醒。
- Colab 資源和運算額度由 Google 帳戶、方案與當下供應狀況決定。開始前檢查帳戶頁面，不要依賴舊的價格或 GPU 數字。
- 使用者的電腦只需能執行 Colab CLI、編輯文字檔、上傳素材和播放下載結果。

Windows 的 CLI 安裝與 OAuth 操作見 [跨電腦連線指南](../COLAB_CLI_跨電腦連線指南.md)。

## 2. 檢查、啟動與額度

在 repo 根目錄執行：

~~~powershell
python cloud/colab_h3.py check
~~~

這只查詢 CLI、帳戶額度和可用工作階段，不啟動 GPU。登入使用者自己在啟動 colab usage 的 Terminal 完成。授權碼不可貼到 Codex 聊天。

完整流程需要 Qwen 生圖、Breeze 角色參考音、MiniMax H3、Music 3、語音辨識與後製環境。啟動完整安裝：

~~~powershell
python cloud/colab_h3.py start
~~~

完整安裝完成後，工作階段可供多次 film 指令重用。H3-only 安裝只適合已有素材且只要遠端 H3 渲染的特定工作，不是一般教學流程。

## 3. 在 Colab 完成整支影片

複製 pipeline/template_colab/ 到 pipeline/<片名>/，編輯該資料夾的 film.json。這些文字檔和素材由本機 CLI 上傳；make_film.py 和所有模型階段都在 Colab VM 執行。

先在 Colab 產生文字讀本和每鏡時長估計，檢查劇情節奏後再啟動模型生成。讀本階段不呼叫生成模型，但 Colab 工作階段仍依帳戶方案計算資源使用：

~~~powershell
python cloud/colab_h3.py film pipeline/my_film read
~~~

檢查同步回來的 `pipeline/my_film/out/preview/讀本試映.mp4` 和 `讀本_timeline.json`，通過後再生成角色、場景與首幀：

~~~powershell
python cloud/colab_h3.py film pipeline/my_film chars masters frames
~~~

此階段完成後，out/ 會下載回 pipeline/my_film/out/。檢查角色定妝照、場景母版和 out/first/_sheet.jpg；首幀未通過前不要啟動後續影片生成。

人工確認後生成角色參考音、H3 鏡頭和需要的環境音：

~~~powershell
python cloud/colab_h3.py film pipeline/my_film voices h3 amb
~~~

檢查 out/review/clips_*.jpg、聽寫結果和每鏡成品。需要重拍時，修改 film.json 的 seed 或設定 ONLY，再使用相同 film 指令重跑相應 stage。

逐鏡檢查通過後，在 Colab 完成剪接、配樂、片尾和自審：

~~~powershell
python cloud/colab_h3.py film pipeline/my_film edl music ending cut review
~~~

最後播放本機同步回來的 out/cut/film_1080p.mp4，確認聲音、字幕和畫面後再交付。

已有 h3_shot spec 的批次工作可用 cloud/colab_h3.py batch；一般新片請使用 film 全流程。

## 4. 工作階段管理

~~~powershell
python cloud/colab_h3.py status
python cloud/colab_h3.py keepalive --minutes 30
python cloud/colab_h3.py stop
~~~

只在正在審片或準備下一個 stage 時保留 VM；keepalive 也會使用帳戶資源。完成下載與驗收後執行 stop。VM 是暫存工作區，關閉後模型和未同步資料會消失；film 指令下載的 out/ 會留在本機 repo。

若連線逾時或出現 Connection was lost，先執行 status 確認上一個工作是否仍在 Colab 執行，再決定是否重試，避免重複啟動生成。

## 5. 常見問題

| 現象 | 處理方式 |
|---|---|
| Windows CLI 出現 No module named termios | 依跨電腦連線指南執行 cloud/colab_cli_windows_patch.py；更新 CLI 後重新套用修補。 |
| Terminal 沒看到授權網址或輸入提示 | 在目前工作的 Terminal 分頁執行 colab usage；授權碼只輸入該命令正在等待的同一個 Terminal。 |
| 已登入但 balance 為 0 | 登入成功不等於有運算額度。檢查 Google One／Colab 方案資格與額度，額度可用前不要執行 start。 |
| Colab CLI 逾時或連線中斷 | 先執行 status；確認舊工作狀態後再重試。 |
| Git Bash 把 /content 路徑改寫成 Windows 路徑 | 用 PowerShell 執行本 repo 指令；Windows CLI 指南也提供對應做法。 |
| 機房位置提醒或位置不明 | 停止 H3 工作，查看 MiniMax 授權與 CLI 提醒；不要移除或繞過檢查。 |

## 6. 參考

- [Windows 跨電腦 Colab CLI 指南](../COLAB_CLI_跨電腦連線指南.md)
- [Colab CLI Windows 修補程式](colab_cli_windows_patch.py)
- [MiniMax H3 與第三方模型授權摘要](../THIRD_PARTY_NOTICES.md)
- [Google Colab FAQ](https://research.google.com/colaboratory/faq.html)
