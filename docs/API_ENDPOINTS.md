# API 端點說明

本文件整理後端 FastAPI 實際提供的端點與參數。

- 服務預設位址：`http://localhost:8000`
- API 文件：`/docs`（Swagger UI）、`/openapi.json`
- 認證方式：JWT 換 Session（Cookie）

## 認證流程

1. 在 Discord 執行 `/web` 取得短效 token 連結。
2. 前端將 token 送到 `POST /auth/`。
3. 後端驗證 token 後把 `guild_id`、`channel_id`、`user_id` 寫入 Session。
4. 之後 API 透過 Session Cookie 辨識使用者。

## 認證（Auth）

### POST /auth/
以 Discord `/web` 產生的 token 建立 Session。

Request Body:

```json
{
  "token": "<jwt-token>"
}
```

Response:

```json
{
  "message": "Session is set",
  "user": "username",
  "guild": "guild-name"
}
```

### GET /auth/
取得目前 Session 對應使用者資訊（需已登入）。

### DELETE /auth/
刪除目前 Session（登出）。

## 健康檢查

### GET /health
回傳 API 與 Bot 目前狀態。

Response 範例：

```json
{
  "status": "ok",
  "bot_ready": true,
  "guild_count": 3,
  "active_playlists": 2
}
```

## 搜尋（Search）

### GET /search/?keyword=<關鍵字>
搜尋 YouTube 影片。

## 播放清單（Playlist）

### GET /playlist/
取得目前伺服器播放清單、目前索引與模式。

### POST /playlist/?id=<id>&mode=<song|favorite>
加入歌曲或整份收藏清單到播放佇列。

- `mode=song`：`id` 視為 YouTube `videoId`
- `mode=favorite`：`id` 視為收藏清單 ID

### DELETE /playlist/?index=<0-based index>
移除指定索引的歌曲。

### PUT /playlist/move/?from_index=<0-based>&to_index=<0-based>
調整播放清單順序。

## 播放控制（Playback）

### GET /playback/play/
播放或恢復播放。

### GET /playback/pause/
暫停播放。

### GET /playback/skipto/?index=<0-based index>
跳到指定索引歌曲。

### GET /playback/loop/
切換循環播放。

### GET /playback/shuffle/
切換隨機播放。

### GET /playback/volume/?value=<0.0~1.0>
設定音量（0.0 到 1.0）。

## 收藏清單（Favorites）

### GET /favorites/
取得目前使用者收藏清單列表。

### POST /favorites/?name=<name>
建立收藏清單。

### DELETE /favorites/{id}/
刪除收藏清單。

### GET /favorites/{favorite_id}/songs/
取得指定收藏清單的歌曲。

### POST /favorites/{favorite_id}/song/
加入歌曲至收藏。

Request Body:

```json
{
  "id": "youtube-video-id",
  "title": "song title",
  "channel": "channel name",
  "thumbnail": "https://..."
}
```

### DELETE /favorites/{favorite_id}/song/{song_id}/
從收藏清單移除歌曲。

## WebSocket

### WS /playback/
每秒檢查播放狀態，資料變更時推送播放資料。

Payload 範例：

```json
{
  "is_playing": true,
  "songs": [
    {
      "title": "song",
      "webpage_url": "https://www.youtube.com/watch?v=...",
      "thumbnail": "https://...",
      "channel": "channel"
    }
  ],
  "current_index": 0,
  "loop": false,
  "shuffle": false,
  "volume": 0.5
}
```

## 常見錯誤碼

- `401`：Session 無效或 token 無效
- `404`：找不到資源，或使用者不在語音頻道
- `500`：伺服器內部錯誤
