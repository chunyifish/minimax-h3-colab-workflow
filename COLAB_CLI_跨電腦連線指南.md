# Colab CLI 跨電腦連線指南（Windows／MiniMax H3）

最後更新：2026-10-24

本指南供另一台 Windows 電腦上的 Codex 與使用者接手本專案。Colab CLI 登入只在本機設定憑證；新電腦必須自行登入。不要複製舊電腦的 OAuth 憑證，也不要把一次性授權碼貼到聊天、文件或截圖。

本 repo 的 cloud/colab_h3.py 會直接呼叫 Colab CLI 來管理 session、上傳、下載與關機；這個工作流程不需要另外安裝 Colab MCP。

## 目前檢查結果

- 目前工作區的 Colab CLI 0.7.5 已登入；執行 cloud/colab_h3.py check 顯示 0.00 compute units、使用率 0.00/hr、0 個作用中工作階段。
- Colab 付費服務頁也顯示 0 個運算單元；Google One 頁面顯示 AI Pro，但家庭群組頁要求「設定家庭群組」。畫面沒有顯示 AI Pro 是否為免費學生試用，因此試用狀態尚未確認。
- 如果是免費學生試用，額度為 0 很可能是方案資格限制，而不是 CLI 登入故障。Google 說 AI Pro 的 Colab 額度須為家庭方案管理者，且 Google One 試用會員不適用。請以目前帳戶的會員／付款詳情確認試用狀態。
- 尚未啟動 Colab GPU、安裝 H3 或生成影片。
- cloud/colab_h3.py 已有 H3 地區保護：偵測到授權排除地區或無法確認國家時，會停止並關閉該 Colab session。

## 1. 在另一台電腦準備工作區

若尚未取得 repo，可從工作區父資料夾執行：

~~~powershell
git clone https://github.com/chunyifish/minimax-h3-colab-workflow.git
~~~

先確認電腦已安裝 Python 3.12 和 uv。uv 安裝方式見 [uv 官方安裝說明](https://docs.astral.sh/uv/getting-started/installation/)。

## 2. Windows PowerShell 安裝 Colab CLI

以下做法把 CLI、快取、暫存與登入設定放在 Git repo 外的工作區父資料夾。若 PowerShell 目前位於包含 minimax-h3-colab-workflow 子資料夾的工作區：

~~~powershell
$WorkRoot = (Get-Location).Path
$RepoRoot = Join-Path $WorkRoot "minimax-h3-colab-workflow"
~~~

若 PowerShell 已在 repo 根目錄，改用：

~~~powershell
$RepoRoot = (Get-Location).Path
$WorkRoot = Split-Path $RepoRoot -Parent
~~~

選好路徑後，在同一個 PowerShell 視窗執行：

~~~powershell
if (-not (Test-Path (Join-Path $RepoRoot "cloud\colab_h3.py"))) {
    throw "RepoRoot 不正確；請確認 cloud\colab_h3.py 存在。"
}

$CliRoot = Join-Path $WorkRoot ".colab-cli-venv2"
$CliPython = Join-Path $CliRoot "Scripts\python.exe"
$CliScripts = Join-Path $CliRoot "Scripts"
$env:USERPROFILE = Join-Path $WorkRoot ".colab-cli-profile"
$env:TEMP = Join-Path $WorkRoot ".tmp"
$env:TMP = $env:TEMP
$env:TMPDIR = $env:TEMP
$LocalDirs = @($env:USERPROFILE, $env:TEMP, (Join-Path $WorkRoot ".uv-cache"))
New-Item -ItemType Directory -Force -Path $LocalDirs | Out-Null

uv venv $CliRoot --python 3.12
uv --cache-dir (Join-Path $WorkRoot ".uv-cache") pip install --python $CliPython --link-mode=copy "google-colab-cli==0.7.5"
$env:Path = $CliScripts + ";" + $env:Path
Set-Location $RepoRoot
& $CliPython cloud/colab_cli_windows_patch.py
colab version
~~~

這是本專案在 Windows 上使用的隔離安裝方式。新開 PowerShell 視窗時，環境變數和 PATH 不會自動沿用。之後每次開新 Terminal，先把路徑改成該電腦的工作區位置，再執行：

~~~powershell
$WorkRoot = "C:\path\to\workspace"
$RepoRoot = Join-Path $WorkRoot "minimax-h3-colab-workflow"
$CliRoot = Join-Path $WorkRoot ".colab-cli-venv2"
$CliPython = Join-Path $CliRoot "Scripts\python.exe"
$CliScripts = Join-Path $CliRoot "Scripts"
$env:USERPROFILE = Join-Path $WorkRoot ".colab-cli-profile"
$env:TEMP = Join-Path $WorkRoot ".tmp"
$env:TMP = $env:TEMP
$env:TMPDIR = $env:TEMP
$env:Path = $CliScripts + ";" + $env:Path
Set-Location $RepoRoot
~~~

## 3. 使用者完成 Google 授權

在已設定好環境變數和 PATH 的 PowerShell 執行：

~~~powershell
colab usage
~~~

若 CLI 尚未登入，它會啟動 Google 授權流程。若瀏覽器沒有自動開啟，從正在執行命令的 Terminal 複製授權網址到瀏覽器；在瀏覽器選擇有 Colab 權益的 Google 帳戶，並把一次性授權碼輸入到**啟動這次 colab usage 的同一個、正在等待輸入的 Terminal**。Codex 不應讀取、複製或代貼授權碼。

曾遇到的畫面與判斷：

- 授權頁可能標示 Google Cloud／gcloud CLI。只依照目前這次登入流程操作；授權碼仍是機密，不要貼到聊天或截圖。
- 若 Terminal 沒有顯示授權網址、也沒有提示正在等待授權碼，先確認命令在哪個 Terminal 執行；確認沒有另一個流程仍在等待後，再於正確 Terminal 執行 colab usage。
- 如果畫面上是空白的 PowerShell 提示符，表示該 Terminal 當下沒有等待中的 CLI 命令。先確認正確的 Terminal 分頁，再執行 colab usage；不要把授權碼貼到空白提示符或另一個任意視窗。
- 不要同時開多個 colab usage 登入流程。若授權逾時或已失效，在確認舊流程已結束後重新執行，使用新產生的授權碼。
- 不要因授權頁提到 gcloud 就在另一個視窗手動執行不相關的登入流程。

授權完成後，查詢版本與額度：

~~~powershell
colab usage
& $CliPython cloud/colab_h3.py check
~~~

check 是連線／額度檢查，不會啟動 GPU。記錄版本、Current balance、Usage rate 與 Active assignments。登入成功但 balance 為 0，代表帳號目前沒有可用 Colab 運算單元；不要把它誤判成 OAuth 失敗。

## 4. 啟動 H3 前的必要檢查

1. 在 Google One 會員或付款詳情確認學生優惠是否仍在免費試用期，以及該帳戶是否符合家庭方案管理者資格。Colab 頁面顯示 AI Pro 本身不足以證明有 Colab 額度。
2. Colab 額度為 0 時先不要執行 start。Google Colab FAQ 說，無正數運算單元的免費 managed runtime 不允許主要繞過 notebook UI 操作網頁介面，且可能隨時被終止；本 repo 的影片生成流程使用 ComfyUI 網頁介面。
3. H3 授權限制美國、歐盟、英國及南韓。Colab 分配的機房位置可能每次不同；repo 的保護程式會在位置遭排除或無法確認時停止並關閉 session。不要移除或繞過這道保護。
4. cloud/colab_h3.py start 會申請 GPU 並消耗運算單元。必須先確認額度、機房／授權條件與使用者的資源使用決定，再開始。

符合條件並獲使用者決定開始後，repo 的 H3-only 流程為：

~~~powershell
& $CliPython cloud/colab_h3.py start --h3-only
~~~

工作完成且不再需要該機器時：

~~~powershell
& $CliPython cloud/colab_h3.py stop
~~~

批次生成、下載與全雲端流程請依 [cloud/README.md](cloud/README.md) 操作。

## 5. 踩坑與處理方式

| 現象 | 處理方式 |
|---|---|
| Windows 執行 colab 出現 No module named termios | 官方 CLI 不支援 Windows 互動終端模組；用本 repo 的 cloud/colab_cli_windows_patch.py 修補已安裝套件，再執行 colab version。更新 CLI 後需重新修補。colab console 和 colab ssh 仍不可用，本 repo 不需要這兩個命令。 |
| 安裝時遇到使用者目錄、快取或暫存權限錯誤 | 使用本指南的工作區本機 .uv-cache、.tmp、.colab-cli-profile，並在 uv 安裝時使用 --link-mode=copy。不要把認證資料放進 Git repo。 |
| 新 Terminal 找不到 colab 或要求重新登入 | 每個新 PowerShell 都要重新設定 venv 的 Scripts PATH 和 .colab-cli-profile 對應的 USERPROFILE；登入資料不會自動跟隨其他電腦或另一個設定目錄。 |
| Terminal 只有空白提示符、找不到授權網址 | 先確認命令是否在另一個 Terminal 分頁等待。若沒有等待中的流程，再在正確分頁執行 colab usage。只有明確正在等待授權碼的原 Terminal 才能接收該碼。 |
| CLI 已登入，額度仍是 0 | 檢查方案是否為免費學生試用，以及家庭方案管理者資格；Colab 頁面與 CLI 都顯示 0 時，重做 OAuth 通常不會增加額度。 |
| Connection was lost 或 Timeout waiting for reply | Colab CLI 呼叫可能短暫斷線；repo helper 有有限次重試。先用 python cloud/colab_h3.py status 確認 session，避免在不確定上一個工作是否仍運行時重複啟動付費工作。 |
| Git 提示 detected dubious ownership | 這是 repo 資料夾擁有者與目前 Windows 使用者不同的安全檢查，不是 Colab 登入問題。不要直接加全域 safe.directory；如需讀取 Git 狀態，可用一次性的 git -c "safe.directory=$RepoRoot" -C "$RepoRoot" status --short。 |

## 官方資料與 repo 內文件

- [Google AI Pro 的 Colab 額度與資格](https://support.google.com/googleone/answer/14534406?hl=zh-TW)
- [Google Colab FAQ：運算單元與 managed runtime 限制](https://research.google.com/colaboratory/faq.html)
- [本 repo 的 Colab H3 操作說明](cloud/README.md)
- [本 repo 的 Windows CLI 修補程式](cloud/colab_cli_windows_patch.py)
