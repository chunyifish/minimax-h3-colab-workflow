# AGENTS.md

本 repo 是 MiniMax H3 Colab 工作流（Codex 版）。唯一支援的模型執行環境是 Google Colab。

## 執行邊界

- 生圖、聲音、H3、配樂、放大、剪接與自審都在 Colab VM 執行。
- 本機只做文字設定、Colab CLI 控制、素材傳輸和成果檢視。
- 不提供或執行本機 GPU、混合本機與 Colab、本機 ComfyUI 或本機模型安裝流程。
- 使用 cloud/colab_h3.py film 執行製片 stage；make_film.py 只在 Colab VM 執行。
- 啟動前確認 Colab 額度與 MiniMax H3 授權條件。額度為 0、機房位置不明或出現授權提醒時先停止，不可繞過檢查。
- OAuth 授權碼、API key 和私人素材不得貼進聊天、文件或 Git。

## 製片關卡

先用 Colab `read` stage 產生文字試映，使用者確認劇本後才跑影像模型；遵守首幀、逐鏡影片和完整成片的人工檢查點。每個 film stage 完成後確認 out/ 已同步回工作區，再決定是否進入下一階段。停止 Colab 前確認重要成果已下載。
