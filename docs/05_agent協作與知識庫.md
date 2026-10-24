# 05 Codex 協作與工作紀錄

Codex 依照 repo 根目錄 AGENTS.md 和本文件協助製片。使用者工作區只負責文字設定、CLI 控制、素材傳輸和成品檢視；模型推論與影音後製全部在 Colab VM 執行。

## Codex 入口

- repo 根目錄 AGENTS.md 定義 Colab-only 的工作規則。
- 單支影片可將 agent/AGENTS.md範本.md 複製到影片資料夾並命名為 AGENTS.md。
- Codex 開工前讀取當前劇本、PROGRESS.md、製作紀錄.md 和相關規則；不要假設先前 stage 已完成。
- 每個 Colab stage 完成後，記錄命令、下載結果、檢查結果、限制和下一步。

## 知識分層

| 層級 | 內容 |
|---|---|
| Codex 入口 | AGENTS.md、單片 AGENTS.md、PROGRESS.md |
| 工作規則 | docs/01 至 docs/07 |
| 技能 | agent/skills/codex-ai-drama/ 與來源授權 NOTICE.md |
| 每片紀錄 | 劇本.md、film.json、製作紀錄.md、Colab 回傳的 out/ |

同一項規則只保留一份詳細說明；其他文件連結到該來源。清楚區分「已閱讀」、「已安裝」、「已在 Colab 執行」和「使用者已驗收」。

## Colab 工作規範

- 執行前先用 cloud/colab_h3.py check 確認登入、額度和工作階段。
- 額度為 0 時不可執行 start；地區或授權提醒未解決時停止，不可繞過。
- 使用 cloud/colab_h3.py film 執行製片 stage，不要在本機直接執行 make_film.py。
- 每個 stage 的輸出先同步回工作區並檢查，再進下一個 stage。
- 呼叫 start、長時間保留 VM 或開始影片生成前，向使用者清楚說明將使用 Colab 資源。
- OAuth 授權碼和 API key 不得讀取、轉貼、印出或寫入 Git。
- 交付前播放完整影片並完成 docs/04_自審清單.md。

## 每支片交接

製片資料夾建議保存劇本.md、film.json、PROGRESS.md、製作紀錄.md 和 out/。停止 Colab 前確認素材、首幀、逐鏡影片、自審結果和成片已下載。

早期技術測試數字不代表目前 Colab 的速度、額度或費用；以帳戶目前顯示和實際雲端執行結果為準。
