# lyrics_generation API 测试报告

测试日期：2026-05-04

## API 基本信息

- **端点**：`https://api.minimaxi.com/v1/lyrics_generation`
- **模式**：`write_full_song` | `edit`
- **认证**：Bearer Token（从 ~/.mmx/config.json 获取）

## 中文歌词生成测试

### 测试结果汇总

| # | prompt | 结果 | 语言 |
|---|--------|------|------|
| 1 | `"中文歌词，一首关于夏日海边的轻快情歌"` | ❌ | 英文 |
| 2 | `"Chinese lyrics only. 中文歌词。一首关于夏日海边的轻快情歌，流行风格"` | ✅ | 中文 |
| 3 | `"Chinese lyrics only. 中文歌词。古风仙侠，讲述星落凡间的故事，空灵悲情"` | ✅ | 中文 |
| 4 | `"全部用中文创作歌词。古风仙侠风格，讲述一颗星星坠落凡间爱上凡人的故事"` | ❌ | 英文 |
| 5 | `"请用中文写歌词。夏日海边，轻快情歌，流行风格，男女对唱"` | ❌ | 英文 |
| 6 | `"写一首中文流行歌曲，关于城市夜晚的孤独"` | ❌ | 英文 |

### 成功率

- 总测试：6 次
- 中文成功：2 次
- 成功率：**33%**

### 最有效 prompt 格式

```
"Chinese lyrics only. 中文歌词。[主题描述]"
```

**关键要素**：
1. 开头必须 `Chinese lyrics only.`
2. 紧接 `中文歌词。` 双重强调
3. 然后是主题描述

### 失败 prompt 特征

- 仅用"中文歌词"开头 → 失败
- 用"全部用中文创作歌词" → 失败
- 用"请用中文写歌词" → 失败
- 用"写一首中文..." → 失败

### 结论

API 对中文 prompt 理解不稳定。最可靠方式：
1. 使用 `"Chinese lyrics only. 中文歌词。"` 开头
2. 多次尝试（最多 3 次）
3. 若仍失败，改用 mmx-lyrics 技能（mmx text chat）

---

## 成功案例

### 案例 1：雨夜的思念

**prompt**：
```
"Chinese lyrics only. 中文歌词。一首关于夏日海边的轻快情歌，流行风格"
```

**返回**：
```json
{
  "song_title": "雨夜的思念",
  "style_tags": "ballad, emotional, reflective, pop",
  "lyrics": "[Intro]\n\n[Verse]\n雨滴敲打着玻璃窗\n像你温柔的声响\n寂寞在午夜滋长\n思念拉长\n回忆却模糊了模样\n\n[Pre-Chorus]\n想问你是否安好\n却怕打扰\n这沉默的信号\n\n[Chorus]\n雨夜的思念在飘\n像断线的风筝找不到\n曾经的拥抱\n已变成遥远的歌谣\n..."
}
```

**注意**：prompt 要求"夏日海边"，返回"雨夜的思念"，主题偏离。

### 案例 2：月光下的约定

**prompt**：
```
"Chinese lyrics only. 中文歌词。古风仙侠，讲述星落凡间的故事，空灵悲情"
```

**返回**：
```json
{
  "song_title": "月光下的约定",
  "style_tags": "mandopop, ballad, romantic, melancholic",
  "lyrics": "[Intro]\n\n[Verse]\n月光洒满了窗台\n思念涌上了心海\n想你的时候醒来\n却只剩下空白\n..."
}
```

**注意**：prompt 要求"古风仙侠"，返回风格标签为 "mandopop, ballad"，非古风。

---

## edit 模式测试

### 测试命令

```bash
curl -s --request POST \
  --url https://api.minimaxi.com/v1/lyrics_generation \
  --header "Authorization: Bearer $API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"mode": "edit", "prompt": "改得更欢快", "lyrics": "[Verse]\n月光落在空荡的房间\n你的气息还留在枕边"}'
```

### 返回

```json
{
  "song_title": "Untitled Song",
  "style_tags": "Pop, Ballad",
  "lyrics": "[Verse]\nI'm not sure what to say\nBut I'll try my best anyway"
}
```

**结论**：edit 模式对中文歌词编辑不可靠，会返回英文。

---

## API 返回结构

```json
{
  "song_title": "歌曲标题",
  "style_tags": "风格标签（逗号分隔）",
  "lyrics": "完整歌词（含结构标签）",
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `song_title` | string | AI 生成的歌曲标题 |
| `style_tags` | string | 风格标签，逗号分隔 |
| `lyrics` | string | 歌词内容，已含 [Verse] [Chorus] 等标签 |
| `base_resp.status_code` | int | 0=成功，其他=错误 |
| `base_resp.status_msg` | string | 状态消息 |

---

## 错误处理

| status_code | 含义 | 处理 |
|-------------|------|------|
| 0 | 成功 | 正常处理 |
| 1004 | 认证失败 | 检查 API Key |
| 2013 | 参数错误 | 检查 mode 值 |

---

## 推荐使用策略

### 1. 快速生成（可接受主题偏离）

使用 API，prompt 格式：
```
"Chinese lyrics only. 中文歌词。[主题]"
```

多次尝试，最多 3 次。

### 2. 精细控制（需准确主题/风格）

使用 mmx-lyrics 技能：
```bash
mmx text chat --system "你是一位专业词作人" --message "[详细要求]"
```

### 3. 混合策略

1. API 生成初稿
2. mmx text chat 精细修改
3. 传给 mmx-music 合成

---

## 局限性总结

1. **语言不稳定**：中文 prompt 成功率仅 33%
2. **主题偏离**：prompt 要求"夏日海边"，返回"雨夜思念"
3. **风格不准**：prompt 要求"古风仙侠"，返回"mandopop"
4. **edit 模式不可靠**：中文歌词编辑会返回英文

**适用场景**：快速生成歌词初稿，不要求精确控制主题和风格。