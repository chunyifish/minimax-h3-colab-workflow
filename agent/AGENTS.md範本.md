# <影片專案名稱>

> Codex 專案入口。將本檔放在影片資料夾並命名為 AGENTS.md。
> 本 repo 的生成環境只有 Google Colab；本機工作區負責編輯、CLI 控制、傳輸與檢視，不執行模型。

## 專案資訊

- 片名：
- 影片規格：16:9、24fps；單鏡不超過 12 秒。
- 角色與場景設定：film.json。
- 進度記錄：PROGRESS.md、製作紀錄.md。

## 必讀文件

- repo 根目錄 AGENTS.md
- docs/02_端到端流程.md
- docs/03_規則與踩坑.md
- docs/04_自審清單.md
- pipeline/template_colab/README.md

## Colab 執行規則

- 劇本、角色設定和 film.json 可在本機工作區編輯。
- 角色圖、場景圖、首幀、角色音、H3 影片、配樂、放大、剪接和自審都在 Colab VM 執行。
- 使用 python cloud/colab_h3.py film <影片資料夾> <stage...> 上傳設定、在 Colab 執行並下載 out/。
- 不要直接在本機執行 make_film.py，也不要安裝本機模型或啟動本機 ComfyUI。
- 呼叫 start 前確認額度與授權提醒；額度為 0 或地區條件未確認時先停止。
- 不把 OAuth 授權碼、API key 或私人素材寫入 Git 或聊天。

## 人工關卡

1. 劇本和鏡表：使用者確認後才開始生圖。
2. 首幀總覽：使用者確認後才開始 H3。
3. 每鏡影片與聽寫：使用者確認後才剪接。
4. 完整成片：交付前請使用者播放確認。

## 交接紀錄

每次完成一個 stage，更新 PROGRESS.md 和製作紀錄.md，記錄 Colab 命令、輸出路徑、檢查結果、尚未完成項目和下一步。關機前確認 out/ 已下載回工作區。