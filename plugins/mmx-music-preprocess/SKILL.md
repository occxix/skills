---
name: mmx-music-preprocess
description: 使用 MiniMax API 提取音频特征和歌词预处理。当用户想要分析音频文件、提取歌曲特征、预处理翻唱素材，或提到"音频预处理"、"提取特征"、"music_cover_preprocess"、"音频分析"时使用。
---

# MiniMax 音频预处理技能

通过 MiniMax `music_cover_preprocess` API 提取音频特征和歌词，为后续翻唱生成做准备。

---

## API 说明

**端点**: `https://api.minimaxi.com/v1/music_cover_preprocess`

**功能**:
- 提取音频特征（节奏、调性、结构等）
- 通过 ASR 提取歌词
- 返回预处理结果用于后续 `music_cover` 生成

---

## 使用场景

| 场景 | 说明 |
|------|------|
| 翻唱准备 | 提取原曲特征和歌词，用于 `mmx music cover` |
| 音频分析 | 获取歌曲的 BPM、调性、结构信息 |
| 歌词提取 | 从音频中自动识别歌词（ASR） |
| 特征导出 | 导出特征数据用于其他音乐工具 |

---

## 前置条件

```bash
# 获取 API Key（从 mmx 配置）
API_KEY=$(cat ~/.mmx/config.json | grep -o '"api_key": *"[^"]*"' | sed 's/"api_key": *"\([^"]*\)"/\1/')

# 或手动设置
API_KEY="sk-xxxxx"
```

---

## 基础调用

### 从 URL 预处理

```bash
curl -s --request POST \
  --url https://api.minimaxi.com/v1/music_cover_preprocess \
  --header "Authorization: Bearer $API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "music-cover",
    "audio_url": "https://example.com/song.mp3"
  }' | jq .
```

### 从本地文件预处理

```bash
# 本地文件需先转为 base64
AUDIO_BASE64=$(base64 -w 0 local_song.mp3)

curl -s --request POST \
  --url https://api.minimaxi.com/v1/music_cover_preprocess \
  --header "Authorization: Bearer $API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "music-cover",
    "audio_data": "'"$AUDIO_BASE64"'"
  }' | jq .
```

---

## 返回格式

```json
{
  "preprocess_id": "preprocess_xxx",
  "audio_features": {
    "bpm": 120,
    "key": "C major",
    "duration": 180.5,
    "structure": ["intro", "verse", "chorus", "bridge", "outro"]
  },
  "lyrics": "提取的歌词文本...",
  "lyrics_with_tags": "[Verse]\n歌词...\n[Chorus]\n歌词...",
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

---

## 工作流

```
用户提供音频
    ↓
【第一步】确认音频来源（URL 或本地文件）
    ↓
【第二步】调用 preprocess API
    ↓
【第三步】解析返回结果
    ↓
【第四步】展示特征 + 歌词给用户
    ↓
【第五步】保存预处理结果（可选）
    ↓
【第六步】对接 mmx-music cover（可选）
```

---

## 第一步：确认音频来源

询问用户：

> 请提供音频文件：
> - **URL 方式**：直接提供音频链接（mp3/wav/flac，6秒～6分钟，最大 50MB）
> - **本地文件**：提供本地路径，我会转为 base64

---

## 第二步：调用 API

### URL 方式（推荐）

```bash
# 直接调用
RESULT=$(curl -s --request POST \
  --url https://api.minimaxi.com/v1/music_cover_preprocess \
  --header "Authorization: Bearer $API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "music-cover",
    "audio_url": "'"$AUDIO_URL"'"
  }')

# 解析
echo "$RESULT" | jq .
```

### 本地文件方式

```bash
# Windows (PowerShell)
AUDIO_BASE64=[Convert]::ToBase64String([IO.File]::ReadAllBytes("local_song.mp3"))

# Linux/macOS
AUDIO_BASE64=$(base64 -w 0 local_song.mp3)

# 调用
RESULT=$(curl -s --request POST \
  --url https://api.minimaxi.com/v1/music_cover_preprocess \
  --header "Authorization: Bearer $API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "music-cover",
    "audio_data": "'"$AUDIO_BASE64"'"
  }')
```

---

## 第三步：解析返回结果

```bash
# 提取关键信息
BPM=$(echo "$RESULT" | jq -r '.audio_features.bpm // "unknown"')
KEY=$(echo "$RESULT" | jq -r '.audio_features.key // "unknown"')
DURATION=$(echo "$RESULT" | jq -r '.audio_features.duration // 0')
LYRICS=$(echo "$RESULT" | jq -r '.lyrics // ""')
LYRICS_TAGGED=$(echo "$RESULT" | jq -r '.lyrics_with_tags // ""')
PREPROCESS_ID=$(echo "$RESULT" | jq -r '.preprocess_id // ""')

# 检查状态
STATUS=$(echo "$RESULT" | jq -r '.base_resp.status_code')
if [ "$STATUS" != "0" ]; then
  ERROR_MSG=$(echo "$RESULT" | jq -r '.base_resp.status_msg')
  echo "预处理失败: $ERROR_MSG"
  exit 1
fi
```

---

## 第四步：展示结果

展示格式：

```
## 音频特征分析结果

| 属性 | 值 |
|------|-----|
| BPM | 120 |
| 调性 | C major |
| 时长 | 3:00 |
| 结构 | intro → verse → chorus → bridge → outro |

## 提取歌词

（展示歌词内容，如有结构标签则分段展示）

预处理 ID: preprocess_xxx
```

---

## 第五步：保存预处理结果

```bash
# 保存到 JSON 文件
echo "$RESULT" > preprocess_result.json

# 或保存歌词单独文件
echo "$LYRICS_TAGGED" > extracted_lyrics.txt

# 保存特征摘要
cat > audio_features.md << EOF
# 音频特征分析

- BPM: $BPM
- 调性: $KEY
- 时长: $(printf '%02d:%02d' $((${DURATION%.*}/60)) $((${DURATION%.*}%60)))
- 预处理 ID: $PREPROCESS_ID

## 歌词

$LYRICS_TAGGED
EOF
```

---

## 第六步：对接翻唱生成

预处理结果可直接用于 `mmx music cover`：

```bash
# 使用预处理结果生成翻唱
mmx music cover \
  --prompt "民谣风格，木吉他，温暖男声" \
  --audio-file original.mp3 \
  --lyrics-file extracted_lyrics.txt \
  --format wav \
  --out folk_cover.wav \
  --quiet
```

或使用 URL：

```bash
mmx music cover \
  --prompt "古风仙侠，清冷女声，洞箫古筝" \
  --audio "$AUDIO_URL" \
  --lyrics "$LYRICS_TAGGED" \
  --format wav \
  --out gufeng_cover.wav \
  --quiet
```

---

## 错误处理

| 状态码 | 含义 | 处理建议 |
|--------|------|---------|
| 1000 | 内部错误 | 重试或联系支持 |
| 1001 | 参数错误 | 检查 audio_url/audio_data |
| 1002 | 音频格式不支持 | 确保是 mp3/wav/flac |
| 1003 | 音频时长超限 | 确保 6秒～6分钟 |
| 1004 | 文件过大 | 确保 < 50MB |
| 429 | 限额 | 等待或升级计划 |

```bash
# 错误检测
STATUS_CODE=$(echo "$RESULT" | jq -r '.base_resp.status_code')
if [ "$STATUS_CODE" != "0" ]; then
  STATUS_MSG=$(echo "$RESULT" | jq -r '.base_resp.status_msg')
  echo "预处理失败 (code: $STATUS_CODE): $STATUS_MSG"
  
  # 根据错误码给建议
  case $STATUS_CODE in
    1002) echo "请使用 mp3/wav/flac 格式";;
    1003) echo "音频时长需在 6秒～6分钟之间";;
    1004) echo "文件大小需 < 50MB";;
    429)  echo "已达限额，请稍后重试";;
  esac
fi
```

---

## 注意事项

- 音频时长：6秒～6分钟
- 文件大小：最大 50MB
- 支持格式：mp3, wav, flac
- 模型：`music-cover`（预处理专用）
- 预处理结果有效期：建议立即使用，避免过期
- ASR 歌词可能不完全准确，建议人工校验后再用于翻唱

---

## 与 mmx-music 技能联动

预处理完成后，可无缝对接 `mmx-music` 技能的翻唱流程：

1. 用本技能提取歌词和特征
2. 用户确认/修改歌词
3. 调用 `mmx music cover` 生成翻唱版本
4. 参考 mmx-music 技能的「翻唱模式」章节进行后续操作