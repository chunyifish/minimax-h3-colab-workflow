# Colab 資源與本機需求

## 本機工作區

本機電腦只負責 Codex 對話、文字編輯、Colab CLI、素材傳輸和查看下載回來的影片。不需要 NVIDIA 顯卡、CUDA、ComfyUI、模型權重或大量模型儲存空間。

保留足夠空間存放原始素材、工作區和下載回來的成品即可。大模型在 Colab VM 下載和使用；VM 關閉後其暫存內容會消失，重要成果必須先由 CLI 同步回 repo。

## Colab 帳戶與運算資源

生成工作需要 Colab 可用運算額度。先執行 python cloud/colab_h3.py check，確認帳戶的 balance 和作用中工作階段。Google 方案名稱、學生優惠、登入成功都不能單獨證明有可用額度；以帳戶目前顯示為準。

Colab 的 GPU、價格、額度和可用時間會變動。開始前查看 Google 帳戶的最新額度與費率。完整安裝會下載模型並準備語音、生圖、H3、配樂與後製環境；保留同一個 VM 連續完成各 stage，可免去重新安裝。停止 VM 前先確認 out/ 已下載。

## 使用授權與地區

啟動 MiniMax H3 前，閱讀第三方模型授權，並留意 Colab CLI 顯示的機房位置。若 CLI 提醒地區不適用或無法確認位置，先停止並核對授權，不要繞過提醒。細節與操作方式見 [cloud/README.md](../cloud/README.md)。