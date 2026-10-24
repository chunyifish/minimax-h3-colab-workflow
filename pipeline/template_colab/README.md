# Colab 多鏡短片範本

film.json 保存角色、場景、每鏡、台詞、配樂和片尾設定。Colab VM 執行 make_film.py 完成生圖、聲音、MiniMax H3、剪接和自審；本機只編輯設定、傳送素材及查看下載回來的成果。

## 使用方式

1. 確認完整 Colab 環境已啟動：python cloud/colab_h3.py start
2. 複製 pipeline/template_colab/ 到 pipeline/my_film/，修改 film.json。
3. 先在 Colab 產生文字讀本和時長估計，確認劇本節奏後再啟動模型生成：

~~~powershell
python cloud/colab_h3.py film pipeline/my_film read
~~~

檢查同步回來的 out/preview/讀本試映.mp4 和讀本_timeline.json。劇本通過後，繼續執行角色、場景和首幀階段；各 stage 都在 Colab 執行，out/ 結果同步回 pipeline/my_film/out/。

~~~powershell
python cloud/colab_h3.py film pipeline/my_film chars masters frames
~~~

人工關卡 1：查看 out/first/_sheet.jpg 和所有首幀。沒通過時修改描述或 seeds.frame_<鏡號>，再重跑 frames。

~~~powershell
python cloud/colab_h3.py film pipeline/my_film voices h3 amb
~~~

人工關卡 2：查看 out/review/clips_<鏡號>.jpg、H3 影片和聽寫結果。需要重拍時修改 seeds.h3_<鏡號>，或只重跑指定鏡頭：

~~~powershell
python cloud/colab_h3.py film pipeline/my_film h3 --env ONLY=S03
~~~

人工關卡 3：完成剪接和自審，最後播放完整影片：

~~~powershell
python cloud/colab_h3.py film pipeline/my_film edl music ending cut review
~~~

確認 out/cut/film_1080p.mp4 可播放、字幕和聲音符合預期後，再關閉 Colab：

~~~powershell
python cloud/colab_h3.py stop
~~~

不要直接在本機執行 make_film.py；它只在 Colab VM 上執行。範本會自動保留 out/ 已完成的檔案，中斷後可從相同 stage 繼續。

## film.json 欄位

| 欄位 | 用途 |
|---|---|
| title | 片名與片尾標題 |
| repo_dir | 本 repo 根目錄相對於影片資料夾的位置；複製到 pipeline/ 底下時使用預設值 |
| cine | 首幀共同的電影感、鏡頭、光線和調色描述 |
| set_sentence | 場景母版提示詞；{n} 代表場景圖編號 |
| frame_suffix | 首幀共同限制，例如不要文字或浮水印 |
| voice_mode | 預設 h3_ref，H3 參考角色音自行念；固定配音備案為 fixed |
| chars | 角色名稱、完整外觀、聲音設計、H3 音色與字幕顏色 |
| masters | 各場景空景母版提示詞 |
| shots | 鏡頭、出場角色、場景裁切、秒數、台詞、首幀與動作 |
| seeds | 角色、場景、首幀、H3 和角色聲音的重抽 seed |
| music | 配樂描述和候選 seed |
| mix | 台詞、配樂音量、響度和剪接設定 |
| ending | 片尾要用的特寫圖、工具名單與片名 |

每個 shot 的 action 由首幀姿勢開始，寫清楚動作開始、發展和結果；單鏡不超過 12 秒。畫面內台詞預設由 H3 使用角色參考音念出，完成後會聽寫並比對原文。只在 H3 多次念錯或需要精確聲畫同步時才使用 fixed 配音。

## 人工檢查

- 首幀階段：確認外觀、服裝、場景、手腳和畫面文字。
- H3 階段：確認角色一致、鏡頭穩定、表演符合 action，並聽寫每句台詞。
- review 階段：播放完整影片，檢查字幕、聲音、切點、黑畫面與片尾。
