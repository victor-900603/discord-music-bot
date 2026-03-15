# Discord 指令文件

本文件整理 `backend/cogs/player.py` 與 `backend/cogs/general.py` 的實際可用指令。

## 指令類型

- Slash Commands：使用 `/` 觸發，啟動時會同步到 Discord
- Prefix Command：使用 `?` 觸發（目前僅保留 `?latency`）

## 使用前置條件

多數音樂控制指令會先檢查使用者是否在語音頻道：

- 必須先加入任一語音頻道
- 若不在語音頻道，Bot 會拒絕執行

## Slash Commands 一覽

| 指令 | 參數 | 說明 |
|:-----|:-----|:-----|
| `/join` | 無 | 連線到你目前所在的語音頻道 |
| `/leave` | 無 | 離開目前語音頻道 |
| `/play` | `song: str`, `choose: True/False` | 播放網址或關鍵字搜尋結果 |
| `/pause` | 無 | 暫停播放 |
| `/resume` | 無 | 恢復播放 |
| `/skip` | 無 | 跳過目前歌曲 |
| `/skipto` | `number: int` | 跳到第 N 首歌曲（1-based） |
| `/remove` | `number: int` | 刪除第 N 首歌曲（1-based） |
| `/clear` | 無 | 清空目前伺服器播放清單 |
| `/loop` | 無 | 切換循環播放開關 |
| `/shuffle` | 無 | 切換隨機播放開關 |
| `/info` | 無 | 顯示目前歌曲資訊 |
| `/queue` | 無 | 顯示播放清單（分頁） |
| `/web` | 無 | 產生 Web 控制台登入連結 |
| `/hello` | 無 | 測試用指令 |
| `/test` | 無 | 測試用指令（含語音連線檢查） |

## 主要指令細節

### /play

參數：

- `song`：YouTube 連結或搜尋關鍵字
- `choose`：
- `False`：直接播放第一筆搜尋結果
- `True`：顯示搜尋結果互動按鈕，讓使用者選擇

行為：

- 當 `song` 是 URL，直接解析並加入播放佇列
- 當 `song` 是關鍵字，會走 YouTube 搜尋流程

### /skipto 與 /remove

- `number` 以 1 為第一首
- 如果曲號超出範圍，會回覆「指定曲目不存在」

### /loop

- 每次呼叫會切換開關狀態
- 若切換成開啟且目前未在播放，會嘗試啟動播放流程

### /shuffle

- 每次呼叫會切換開關狀態
- 開啟後播放順序由隨機序列控制

### /queue

- 顯示 Discord 互動式分頁清單
- 每頁 5 首，可透過按鈕翻頁

### /web

- 產生短效 JWT 登入連結並回傳給使用者
- 訊息為 ephemeral（僅自己可見）
- 訊息 30 秒後自動刪除

## Prefix Command

### ?latency

- 用途：回傳 Bot latency（毫秒）
- 定義位置：`backend/cogs/general.py`

## 事件行為

### 指令同步

- Bot 啟動時會執行 command sync
- Slash 指令若有變更，重啟後會重新同步

### 自動離線

- 當 Bot 所在語音頻道只剩 Bot 自己時
- 等待 60 秒後仍無其他成員，會自動停止播放並離線
- 同時清除該 guild 的播放清單狀態

## 相關檔案

- `backend/cogs/player.py`
- `backend/cogs/general.py`
- `backend/cogs/views.py`
- `backend/utils/playback.py`
- `backend/utils/playing_list.py`
