# lyrics_generation API Prompt 模板

## write_full_song 模式

### 中文歌词模板（推荐）

```
"Chinese lyrics only. 中文歌词。[主题]，[风格]，[情绪]"
```

**示例**：

```bash
# 流行情歌
curl -s --request POST \
  --url https://api.minimaxi.com/v1/lyrics_generation \
  --header "Authorization: Bearer $API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"mode": "write_full_song", "prompt": "Chinese lyrics only. 中文歌词。一首关于夏日海边的轻快情歌，流行风格"}'

# 古风仙侠
curl -s --request POST \
  --url https://api.minimaxi.com/v1/lyrics_generation \
  --header "Authorization: Bearer $API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"mode": "write_full_song", "prompt": "Chinese lyrics only. 中文歌词。古风仙侠，讲述星落凡间的故事，空灵悲情"}'

# 城市孤独
curl -s --request POST \
  --url https://api.minimaxi.com/v1/lyrics_generation \
  --header "Authorization: Bearer $API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"mode": "write_full_song", "prompt": "Chinese lyrics only. 中文歌词。城市夜晚的孤独，轻柔忧郁，流行风格"}'
```

### 英文歌词模板

```
"[Theme], [Style], [Mood]"
```

**示例**：

```bash
# Electronic pop
curl -s --request POST \
  --url https://api.minimaxi.com/v1/lyrics_generation \
  --header "Authorization: Bearer $API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"mode": "write_full_song", "prompt": "A summer beach love song, upbeat pop, tropical vibes"}'

# Cinematic ballad
curl -s --request POST \
  --url https://api.minimaxi.com/v1/lyrics_generation \
  --header "Authorization: Bearer $API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"mode": "write_full_song", "prompt": "A song about star falling to earth, cinematic, ethereal, melancholic"}'
```

---

## edit 模式

### 基础模板

```bash
curl -s --request POST \
  --url https://api.minimaxi.com/v1/lyrics_generation \
  --header "Authorization: Bearer $API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"mode": "edit", "prompt": "[修改指令]", "lyrics": "[原歌词]"}'
```

### 修改指令示例

| 指令 | 用途 |
|------|------|
| `"改得更欢快"` | 调整情绪 |
| `"押韵更自然"` | 优化韵脚 |
| `"增加古风意象"` | 添加风格元素 |
| `"translate to Chinese"` | 尝试翻译（不稳定） |

**注意**：edit 模式对中文歌词不可靠，可能返回英文。

---

## Prompt 结构建议

### 必要元素

1. **语言声明**：`Chinese lyrics only. 中文歌词。`（中文歌词必需）
2. **主题**：歌曲核心内容
3. **风格**：音乐流派
4. **情绪**：情感基调

### 可选元素

- 结构要求：`"七字句为主"`
- 人声要求：`"男女对唱"`
- 具体意象：`"包含月光、海浪"`

### 完整 prompt 示例

```
"Chinese lyrics only. 中文歌词。夏日海边邂逅的爱情，流行风格，轻快甜蜜，男女对唱，包含海浪、阳光意象"
```

---

## API Key 获取模板

```bash
# 从 mmx 配置读取
API_KEY=$(cat ~/.mmx/config.json | grep -o '"api_key": *"[^"]*"' | sed 's/"api_key": *"\([^"]*\)"/\1/')

# 或直接查看
mmx config show --output json | jq -r '.api_key'
```

---

## 结果解析模板

```bash
# 调用 API 并解析
RESULT=$(curl -s --request POST \
  --url https://api.minimaxi.com/v1/lyrics_generation \
  --header "Authorization: Bearer $API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"mode": "write_full_song", "prompt": "..."}')

# 提取字段（需要 jq）
TITLE=$(echo "$RESULT" | jq -r '.song_title')
STYLE=$(echo "$RESULT" | jq -r '.style_tags')
LYRICS=$(echo "$RESULT" | jq -r '.lyrics')

# 检查状态
STATUS=$(echo "$RESULT" | jq -r '.base_resp.status_code')
if [ "$STATUS" = "0" ]; then
  echo "生成成功"
  echo "标题：$TITLE"
  echo "风格：$STYLE"
  echo "$LYRICS"
else
  echo "生成失败：$(echo "$RESULT" | jq -r '.base_resp.status_msg')"
fi
```

---

## 与 mmx-music 协作模板

```bash
# 1. 生成歌词
LYRICS=$(curl -s --request POST \
  --url https://api.minimaxi.com/v1/lyrics_generation \
  --header "Authorization: Bearer $API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"mode": "write_full_song", "prompt": "Chinese lyrics only. 中文歌词。夏日海边情歌"}' \
  | jq -r '.lyrics')

# 2. 保存歌词
echo "$LYRICS" > lyrics.txt

# 3. 生成音乐
mmx music generate \
  --prompt "流行，轻快，夏日海边" \
  --lyrics-file lyrics.txt \
  --vocals "清亮女声" \
  --genre "pop" \
  --mood "upbeat" \
  --bpm 100 \
  --format mp3 \
  --out summer_song.mp3 \
  --quiet
```