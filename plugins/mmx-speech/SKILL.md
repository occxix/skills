---
name: mmx-speech
description: Use mmx to synthesize speech via MiniMax TTS (speech-2.8-hd). Use when the user wants text-to-speech, voice narration, audiobook, podcast scripts, subtitle generation, or high-quality audio from text. Triggers on "TTS", "语音合成", "朗读", "配音", "旁白", "生成音频", "文字转语音".
---

# MiniMax 语音合成技能

使用 `mmx speech synthesize` 生成高质量语音（默认模型：`speech-2.8-hd`，上限 10000 字符）。

> **默认原则**：先问内容和感觉，再转成专业参数。不要一上来就问 voice ID。

---

## 工作流总览

```
用户描述需求
  ↓
【第一步】引导需求（4个问题）
  ↓
【第二步】选择音色
  ↓
【第三步】确认参数（语速/音质）
  ↓
【第四步】生成并验证
```

---

## 第一步：引导需求

| 问题 | 目的 |
|------|------|
| 这段文字是什么类型？（新闻播报/小说旁白/教程讲解/广告配音…） | 确定风格 |
| 想要男声还是女声？有什么气质要求？ | 选音色 |
| 语速偏快还是偏慢？（正常/讲故事慢/播报快） | 控制 speed |
| 需要字幕时间戳吗？（用于视频字幕对齐） | 是否加 --subtitles |

---

## 第二步：选择音色

### 中文常用音色

| 用户描述 | voice_id | 特点 |
|----------|----------|------|
| 播报/新闻/正式 | `Chinese (Mandarin)_News_Anchor` | 专业女播音腔 |
| 男播报/正式 | `Chinese (Mandarin)_Male_Announcer` | 沉稳播报男声 |
| 温柔/温暖女声 | `Chinese (Mandarin)_Warm_Girl` | 温暖少女 |
| 甜美女声 | `Chinese (Mandarin)_Sweet_Lady` | 甜美 |
| 御姐/成熟女 | `Chinese (Mandarin)_Mature_Woman` | 傲娇御姐 |
| 温润男声 | `Chinese (Mandarin)_Gentleman` | 温润绅士 |
| 抒情男声 | `Chinese (Mandarin)_Lyrical_Voice` | 抒情感 |
| 不羁/个性男 | `Chinese (Mandarin)_Unrestrained_Young_Man` | 潇洒不羁 |
| 萌/可爱 | `Chinese (Mandarin)_Cute_Spirit` | 憨憨萌兽 |
| 老人/长辈 | `Chinese (Mandarin)_Kind-hearted_Elder` | 花甲奶奶 |
| 古风/仙侠 | `female-yujie-jingpin` | 御姐精品版 |

### 英文常用音色

| 用途 | voice_id |
|------|----------|
| 旁白/叙述 | `English_expressive_narrator`（默认）|
| 温柔女声 | `Serene_Woman` |
| 可爱/活泼 | `Sweet_Girl` |

> 运行 `mmx speech voices --language chinese` 或 `--language english` 查看完整列表。

---

## 第三步：参数确认

### 音质预设

| 预设 | 用途 | 参数 |
|------|------|------|
| 标准（默认） | 日常配音 | `--format mp3 --sample-rate 32000 --bitrate 128000` |
| 高质量 | 正式发布 | `--format mp3 --sample-rate 44100 --bitrate 256000` |
| 无损 | 专业制作 | `--format wav --sample-rate 44100` |

### 语速参考

| 用户需求 | `--speed` 值 |
|----------|-------------|
| 慢（有声书/老人） | `0.7` |
| 偏慢（讲故事） | `0.85` |
| 正常 | `1.0`（默认，可不填）|
| 偏快（播报） | `1.15` |
| 快（广告） | `1.3` |

---

## 第四步：生成命令

```bash
# 基础用法
mmx speech synthesize \
  --text "你好，欢迎收听今天的播客。" \
  --voice "Chinese (Mandarin)_News_Anchor" \
  --out output.mp3 \
  --quiet

# 高质量 + 字幕
mmx speech synthesize \
  --text "这是一段旁白。" \
  --voice "Chinese (Mandarin)_Warm_Girl" \
  --speed 0.9 \
  --format mp3 \
  --sample-rate 44100 \
  --bitrate 256000 \
  --subtitles \
  --out output.mp3 \
  --quiet

# 从文件读取（长文本）
mmx speech synthesize \
  --text-file script.txt \
  --voice "English_expressive_narrator" \
  --out narration.mp3 \
  --quiet

# 流式输出（实时播放）
mmx speech synthesize \
  --text "Streaming audio test." \
  --stream | mpv --no-terminal -
```

### 字幕文件处理

加 `--subtitles` 后，输出 JSON 同时包含音频（base64）和字幕时间戳：

```bash
mmx speech synthesize \
  --text "第一句话。第二句话。" \
  --subtitles \
  --out audio_with_subs.mp3 \
  --output json --quiet > result.json

# 提取字幕
python3 -c "import json,sys; d=json.load(open('result.json')); print(json.dumps(d.get('subtitle_file','')))"
```

---

## 验证

```bash
ffprobe -v quiet -show_entries format=duration,size -of default=noprint_wrappers=1 output.mp3
```

---

## 长文本分段策略

`speech-2.8-hd` 上限 10000 字符。超出时按段落拆分：

```bash
# 分段生成后合并
mmx speech synthesize --text-file part1.txt --out p1.mp3 --quiet
mmx speech synthesize --text-file part2.txt --out p2.mp3 --quiet
ffmpeg -i "concat:p1.mp3|p2.mp3" -acodec copy merged.mp3
```

---

## 注意事项

- 默认模型：`speech-2.8-hd`（可用：`speech-2.6`、`speech-02`）
- `--subtitles` 与 `--stream` 不能同时使用
- 始终加 `--quiet` 避免进度条污染输出
- 长文本建议用 `--text-file`，避免 shell 转义问题
