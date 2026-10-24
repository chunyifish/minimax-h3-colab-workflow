# pipeline：在 Colab 製作影片

新片請複製 template_colab/，修改 film.json，然後用 cloud/colab_h3.py film 在 Colab 執行。模型生成、後製、自審都在 Colab VM；工作區只負責編輯、傳輸和查看回傳成果。

## 新片流程

1. 在 Colab 啟動完整環境：python cloud/colab_h3.py start
2. 複製 pipeline/template_colab/ 到 pipeline/<片名>/，修改 film.json。
3. 在 Colab 產生文字試映：python cloud/colab_h3.py film pipeline/<片名> read。檢查同步回來的 out/preview/讀本試映.mp4 和讀本_timeline.json，劇本通過後才繼續。
4. 生成角色、場景和首幀：python cloud/colab_h3.py film pipeline/<片名> chars masters frames
5. 查看同步回來的 out/first/_sheet.jpg；人工確認後才繼續。
6. 生成參考音、H3 鏡頭和環境音：python cloud/colab_h3.py film pipeline/<片名> voices h3 amb
7. 查看 out/review/clips_*.jpg 和聽寫結果；需要重做時修改 seed，或用 --env ONLY=S03 只重做指定鏡頭。
8. 確認鏡頭後完成剪接與自審：python cloud/colab_h3.py film pipeline/<片名> edl music ending cut review
9. 播放 out/cut/film_1080p.mp4，確認成片後執行 python cloud/colab_h3.py stop。

每次 film 指令會把製片資料夾上傳、在 Colab 執行指定 stage，再把 out/ 同步回工作區。

新片只從 template_colab/ 開始；本 repo 不附帶本機 GPU 或桌面剪輯軟體的替代範例。
