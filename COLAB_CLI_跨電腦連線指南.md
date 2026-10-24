# Codex＋Google Colab CLI 連線指南（Windows）

最後更新：2026-10-24

本指南協助 Windows 上的 Codex 工作區連接 Google Colab。所有模型和影音工作都在 Colab VM 執行；本機只執行 Colab CLI、傳送檔案和檢視成果，不需要 NVIDIA 顯卡或本機模型。每台電腦都要在自己的 Terminal 完成登入。不要複製舊電腦的 OAuth 憑證，也不要把一次性授權碼貼到聊天、文件或截圖。

本 repo 的 cloud/colab_h3.py 會直接呼叫官方 Colab CLI 管理工作階段、上傳、下載與關機，不需要另外安裝 Colab MCP。

## 開始前檢查

- 先執行 cloud/colab_h3.py check 查看登入狀態、運算餘額和作用中工作階段；check 不會啟動 GPU。
- 帳戶方案名稱不保證有可用 Colab 額度。若 balance 為 0，先確認帳戶目前的 Colab 額度和資格，不要執行 start。
- 啟動前閱讀 MiniMax H3 的現行授權條款及 CLI 顯示的機房位置。若位置不明或顯示授權提醒，先停止並核對，不要繞過提醒。

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

1. 在 Google 帳戶的 Colab／方案頁面確認目前可用額度。方案標籤或登入成功本身不能證明帳戶有可用額度。
2. 額度為 0 時不要執行 start。等帳戶顯示可用額度後再繼續。
3. 啟動時查看 CLI 顯示的機房位置，並遵守 MiniMax H3 現行授權。遇到排除地區或位置不明時停止，不要移除或繞過提醒。
4. cloud/colab_h3.py start 會啟動雲端 GPU 並使用帳戶資源；開始前先確認帳戶額度和授權條件。

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
