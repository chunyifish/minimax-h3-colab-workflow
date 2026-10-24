# 07 在 Colab 建立角色與首幀

角色定妝照、場景母版和首幀都由 Colab VM 上的 Qwen 模型生成。使用者只在本機編輯 film.json、查看同步回來的圖片並做人工確認；不需要安裝本機生圖軟體或顯卡。

## 1. 建立新片資料夾

複製 pipeline/template_colab/ 到 pipeline/<片名>/，修改 film.json 的角色、場景、每鏡描述與 seed。角色外觀描述要完整而固定，包含年齡、臉、髮型、眼鏡、上衣與下半身；每一張首幀都會引用同一份描述。

## 2. 在 Colab 生成

確認完整雲端環境已啟動後執行：

~~~powershell
python cloud/colab_h3.py film pipeline/my_film chars masters frames
~~~

此命令會上傳製片資料夾，在 Colab 生成角色圖、場景母版、首幀，然後把 out/ 同步回本機。

## 3. 人工檢查

查看 out/chars/、out/masters/、out/first/_sheet.jpg 與各首幀。檢查角色外觀是否一致、手腳是否正常、場景方向是否正確、畫面有沒有文字或浮水印。未通過的鏡頭，在 film.json 調整描述或 seed，再用相同 Colab 指令重跑 frames。

## 4. 角色和場景一致性

- 先生成單張清楚的半身角色參考照，再讓首幀使用角色參考照與場景裁切圖。
- 同一場景的鏡頭共用場景母版，避免窗戶、黑板和主要家具位置跳動。
- 每張首幀寫清楚景別、角色位置、姿勢、表情和鏡頭方向。
- 畫面中需要閱讀的中文字後製疊加，不要求生成模型畫出正確文字。

首幀通過後，再執行 voices、h3、amb 階段。範本欄位與人工檢查點見 [pipeline/template_colab/README.md](../pipeline/template_colab/README.md)。