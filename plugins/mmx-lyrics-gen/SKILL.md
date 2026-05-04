---
name: mmx-lyrics-gen
description: 使用 MiniMax lyrics_generation API 直接生成歌词。当用户需要快速生成完整歌词、已有歌词需要修改润色时使用。触发词："生成歌词"、"写歌词"、"lyrics generation"、"歌词润色"、"修改歌词"。适合快速歌词生成场景，比 mmx-lyrics 更轻量。
---

# MiniMax 歌词生成 API 技能

直接调用 `/v1/lyrics_generation` API 生成或编辑歌词。

> **与 mmx-lyrics 区别**：此技能直接调用歌词生成 API，更快速轻量。mmx-lyrics 通过 mmx text chat 精细创作，适合需要精细控制的场景。

---

## API 概览

| 模式 | 用途 | 输入 |
|------|------|------|
| `write_full_song` | 根据主题生成完整歌词 | `prompt`（主题描述） |
| `edit` | 编辑/润色已有歌词 | `prompt`（修改指令） + `lyrics`（原歌词） |

---

## 工作流

```
用户请求
  ↓
判断需求类型
  ├─ 新创作 → write_full_song
  └─ 修改已有 → edit
  ↓
调用 API
  ↓
展示结果 + 确认
  ↓
保存到文件（可选）
```

---

## 第一步：判断需求

| 用户说 | 模式 | 示例 |
|--------|------|------|
| "帮我写一首关于X的歌词" | `write_full_song` | prompt = "一首关于夏日海边的轻快情歌" |
| "生成歌词，主题是X" | `write_full_song` | prompt = 主题描述 |
| "把这段歌词改得更X" | `edit` | prompt = "改得更欢快" + lyrics = 原歌词 |
| "润色这段歌词" | `edit` | prompt = "润色，押韵更自然" + lyrics = 原歌词 |

---

## 第二步：调用 API

### write_full_song 模式

```bash
curl -s --request POST \
  --url https://api.minimaxi.com/v1/lyrics_generation \
  --header "Authorization: Bearer $API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"mode": "write_full_song", "prompt": "主题描述"}'
```

**prompt 建议**：
- 包含主题 + 风格 + 情绪
- 示例：`"一首关于夏日海边的轻快情歌"`、`"古风仙侠，讲述星落凡间的故事"`

### edit 模式

```bash
curl -s --request POST \
  --url https://api.minimaxi.com/v1/lyrics_generation \
  --header "Authorization: Bearer $API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"mode": "edit", "prompt": "修改指令", "lyrics": "原歌词内容"}'
```

**prompt 建议**：
- 明确修改方向
- 示例：`"改得更欢快"`、`"押韵更自然"`、`"增加古风意象"`

---

## 第三步：解析结果

API 返回格式：

```json
{
  "song_title": "Digital Echoes",
  "style_tags": "electronic, futuristic, introspective, pop",
  "lyrics": "[Intro]\n\n[Verse]\n...\n[Chorus]\n...",
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

提取字段：
- `song_title`：歌曲标题
- `style_tags`：风格标签
- `lyrics`：完整歌词（已含结构标签）

---

## 第四步：展示并确认

展示格式：

```
【歌曲标题】{song_title}
【风格】{style_tags}

【歌词】
{lyrics}

---
是否满意？
- 回复"确认" → 保存到文件
- 回复"修改" + 具体要求 → 用 edit 模式调整
- 回复"重写" → 重新生成
```

---

## 第五步：保存到文件（可选）

用户确认后保存：

```bash
# 文件名：{song_title}_lyrics.txt
cat > 歌曲名_lyrics.txt << 'EOF'
[Intro]
...
[Verse]
...
EOF
```

---

## API Key 获取

从 mmx 配置读取：

```bash
API_KEY=$(cat ~/.mmx/config.json | grep -o '"api_key": *"[^"]*"' | sed 's/"api_key": *"\([^"]*\)"/\1/')
```

或直接查看：

```bash
mmx config show
```

---

## 注意事项

### 中文歌词生成

**必须使用以下 prompt 格式**：
```
"Chinese lyrics only. 中文歌词。[主题描述]"
```

**实测结论**：
- ✅ `Chinese lyrics only. 中文歌词。` 开头 → 中文歌词
- ❌ 其他格式（"中文歌词"、"请用中文"等） → 英文歌词

### API 局限性（2026-05-04 实测）

| 问题 | 现象 | 影响 |
|------|------|------|
| **主题偏离** | prompt 要求"星落凡间"，返回"星空誓言" | 无法精确控制故事内容 |
| **风格偏离** | prompt 要求"古风仙侠"，返回 mandopop/pop | 无法精确控制音乐风格 |
| **歌名忽略** | prompt 指定"落星引"，返回其他歌名 | 无法指定歌曲标题 |
| **意象忽略** | prompt 要求"霜月孤鸿"，返回现代城市意象 | 无法强制使用特定意象 |
| **结构简化** | prompt 要求完整结构，返回简化版 | 无法控制段落数量 |
| **韵脚忽略** | prompt 要求"ang/iang韵"，返回其他韵脚 | 无法控制押韵规则 |

**测试记录**：

| prompt | 返回歌名 | 返回风格 | 主题匹配 |
|--------|---------|---------|---------|
| `"Chinese lyrics only. 中文歌词。古风仙侠。星落凡间故事..."` | 星辰大海的约定 | Mandopop | ❌ 偏离 |
| `"Chinese lyrics only. 中文歌词。歌名：落星引。古风仙侠..."` | 月光下的约定 | mandopop | ❌ 偏离 |
| `"Chinese lyrics only. 中文歌词。古风仙侠叙事长歌。歌名必须叫：落星引..."` | 月光下的低语 | dream pop | ❌ 偏离 |
| `"Chinese lyrics only. 中文歌词。古风仙侠。星落凡间故事..."` | 星空下的誓言 | pop | ❌ 偏离 |

### 适用场景

**适合**：
- 快速生成流行情歌初稿
- 不要求精确控制主题/风格/歌名
- 接受多次尝试获取可用结果

**不适合**：
- 古风仙侠等特定风格创作
- 需要指定歌名/意象/韵脚
- 需要精确控制故事内容
- edit 模式修改中文歌词（不稳定）

### 解决方案

1. **中文歌词**：必须用 `Chinese lyrics only. 中文歌词。` 开头
2. **精确创作**：改用 `mmx-lyrics` 技能（`mmx text chat` 更可控）
3. **多次尝试**：最多 3 次，接受偏离结果
4. **人工调整**：生成后用 `mmx text chat` 修改偏离内容

---

## 与 mmx-lyrics 技能协作

1. **快速初稿**：用此技能 `write_full_song` 生成初稿
2. **精细调整**：用 mmx-lyrics 的 `mmx text chat` 精细修改
3. **音乐合成**：传给 mmx-music 技能生成音频

---

## 示例命令

### 生成中文歌词

```bash
curl -s --request POST \
  --url https://api.minimaxi.com/v1/lyrics_generation \
  --header "Authorization: Bearer $API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"mode": "write_full_song", "prompt": "中文歌词，一首关于夏日海边的轻快情歌"}'
```

### 编辑歌词

```bash
curl -s --request POST \
  --url https://api.minimaxi.com/v1/lyrics_generation \
  --header "Authorization: Bearer $API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"mode": "edit", "prompt": "增加古风意象，押韵更工整", "lyrics": "[Verse]\n月光落在空荡的房间\n你的气息还留在枕边"}'
```