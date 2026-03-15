# Discord Music Bot

作者：Victor

此專案是以 Discord Bot 為核心的音樂播放系統，整合了 FastAPI 後端與 React 前端控制台。

系統提供三種操作介面：

- Discord Slash Commands（語音頻道控制）
- Web 前端控制台（播放控制、收藏管理、搜尋）
- REST API + WebSocket（給前端同步狀態）

## Demo

![Demo](./demo.gif)

## 主要功能

- 播放控制：播放、暫停、跳歌、指定歌曲、循環、隨機、音量
- YouTube 搜尋：支援關鍵字搜尋與網址點播
- 收藏清單：建立清單、加入歌曲、刪除歌曲、整份清單加入播放佇列
- 即時同步：WebSocket 推送播放狀態（清單、索引、模式、音量）
- Web 登入：透過 Discord `/web` 產生短效 JWT，換取 Session Cookie

## 文件分工

- 本檔：專案概覽、環境設定、啟動方式、Docker、Discord 指令
- API 詳細端點：[docs/API_ENDPOINTS.md](docs/API_ENDPOINTS.md)
- Discord 指令詳細說明：[docs/DISCORD_COMMANDS.md](docs/DISCORD_COMMANDS.md)

## 技術棧

| 層級 | 技術 |
|:-----|:-----|
| 前端 | React 19, React Router 7, Axios, SCSS, Vite |
| 後端 | FastAPI, Uvicorn, Discord\.py, asyncio |
| 音訊處理 | yt-dlp, FFmpeg, PyNaCl |
| 資料庫 | MongoDB（pymongo AsyncMongoClient） |
| 認證 | JWT（PyJWT）+ Session（Starlette SessionMiddleware） |
| 即時通訊 | WebSocket |


## 環境需求

- Python 3.11 以上
- Node.js 20 以上
- MongoDB 7 以上
- FFmpeg（本機執行後端時需要）

## 環境變數

### backend/.env

先複製 `backend/.env.example` 為 `backend/.env`。

| 變數 | 說明 |
|:-----|:-----|
| `DISCORD_TOKEN` | Discord Bot Token |
| `MANAGER_USER_ID` | 管理者使用者 ID（目前程式會讀取） |
| `SECRET_KEY` | JWT 簽章金鑰 |
| `SESSION_SECRET` | Session 簽章金鑰 |
| `DATABASE_URI` | MongoDB URI |
| `DATABASE_NAME` | MongoDB Database 名稱 |
| `FRONTEND_URL` | 前端網址（CORS 與 `/web` 連結用） |
| `API_HOST` | API 綁定位址（預設 127.0.0.1） |
| `API_PORT` | API 連接埠（預設 8000） |

### frontend/.env（開發）與 frontend/.env.production（正式）

| 變數 | 說明 |
|:-----|:-----|
| `VITE_API_BASE_URL` | REST API Base URL（需包含結尾 `/`） |
| `VITE_WS_URL` | WebSocket URL（例如 `ws://host:8000/playback/`） |

## 本機開發

### 1. 啟動 MongoDB

請先確認本機 MongoDB 正在執行，且 `DATABASE_URI` 可連線。

### 2. 啟動 backend

```bash
cd backend
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
```

```powershell
Copy-Item .env.example .env
python app.py
```

後端預設位址：`http://localhost:8000`

### 3. 啟動 frontend

```bash
cd frontend
npm install
```

```powershell
Copy-Item .env.example .env
npm run dev
```

前端預設位址：`http://localhost:5173`

## Docker

### 開發/測試模式

使用 `docker-compose.yml`：

```powershell
Copy-Item backend/.env.example backend/.env
Copy-Item frontend/.env.example frontend/.env
docker compose up --build
```

- Frontend：`http://localhost:5173`
- Backend：`http://localhost:8000`
- MongoDB：`localhost:27017`

### 正式模式

使用 `docker-compose.prod.yml`：

```powershell
Copy-Item backend/.env.example backend/.env
Copy-Item frontend/.env.example frontend/.env.production
# 依實際網域修改 frontend/.env.production

docker compose -f docker-compose.prod.yml up --build -d
```

- Frontend：`http://<server-ip>`
- Backend：`http://<server-ip>:8000`

## API 文件

完整端點、參數與 WebSocket payload 請見：

- [docs/API_ENDPOINTS.md](docs/API_ENDPOINTS.md)

## Discord 指令

完整說明（參數、回應行為、前置條件）請見：

- [docs/DISCORD_COMMANDS.md](docs/DISCORD_COMMANDS.md)

| 指令 | 說明 |
|:-----|:-----|
| `/join` | 連線到使用者所在語音頻道 |
| `/leave` | 中斷語音連線 |
| `/play <song> [choose]` | 播放網址或關鍵字搜尋結果 |
| `/pause` | 暫停播放 |
| `/resume` | 恢復播放 |
| `/skip` | 跳過目前歌曲 |
| `/skipto <number>` | 跳到指定曲目 |
| `/remove <number>` | 刪除指定曲目 |
| `/clear` | 清空播放佇列 |
| `/loop` | 切換循環播放 |
| `/shuffle` | 切換隨機播放 |
| `/queue` | 顯示播放清單 |
| `/info` | 顯示目前歌曲 |
| `/web` | 產生前端登入短效連結 |
| `/hello`、`/test` | 開發測試用指令 |

## 系統行為與限制

- `/web` 產生的 JWT 有效期為 1 分鐘
- 每位使用者最多建立 10 個收藏清單
- WebSocket 在前端採自動重連（最多 10 次）
- Bot 在語音頻道只剩自己時，60 秒後會自動離線並清除該 guild 播放狀態

## 授權

MIT License
