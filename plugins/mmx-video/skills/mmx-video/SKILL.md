---
name: mmx-video
description: Use mmx to generate videos via MiniMax Hailuo models. Use when the user wants to generate video clips, text-to-video, image-to-video, subject reference video, or start-end frame interpolation. Triggers on "生成视频", "文生视频", "图生视频", "Hailuo", "视频片段", "T2V", "I2V", "video generate".
---

# MiniMax 视频生成技能

使用 `mmx video generate` 生成视频片段（默认 6 秒，768P）。

> **默认原则**：先引导用户描述画面，再转成专业提示词。视频生成耗时较长（1-3 分钟），提前告知用户。

---

## 工作流总览

```
用户描述需求
  ↓
【第一步】引导需求（4个问题）
  ↓
【第二步】选择模型和模式
  ↓
【第三步】转换提示词
  ↓
【第四步】生成并下载
```

---

## 第一步：引导需求

| 问题 | 目的 |
|------|------|
| 视频里想展示什么画面/场景？ | 核心内容 |
| 有参考图片吗？（首帧/末帧/角色参考图） | 决定模式 |
| 镜头怎么运动？（静止/推进/旋转/跟拍…） | 运镜描述 |
| 对速度或画质有要求吗？（快速出图 vs 高质量） | 选模型 |

---

## 第二步：选择模型和模式

| 场景 | 模型 | 标志 |
|------|------|------|
| 纯文字生视频（标准质量） | `MiniMax-Hailuo-2.3`（默认） | 无额外标志 |
| 纯文字生视频（快速出图） | `MiniMax-Hailuo-2.3-Fast` | `--model MiniMax-Hailuo-2.3-Fast` |
| 图片作为首帧（图生视频） | `MiniMax-Hailuo-2.3` | `--first-frame 图片路径` |
| 首帧+末帧插值（SEF模式） | `Hailuo-02`（自动切换） | `--first-frame + --last-frame` |
| 角色一致性视频 | `S2V-01`（自动切换） | `--subject-image 角色图片` |

### 模型对比

| | Hailuo-2.3（默认） | Hailuo-2.3-Fast |
|---|---|---|
| 速度 | 标准（~90-180s） | 更快（~30-60s） |
| 质量 | 更细腻 | 略低 |
| 适合 | 正式用途 | 快速预览 |

---

## 第三步：提示词转换

### 提示词结构（推荐格式）

```
[主体描述] [动作/状态] [场景/环境] [运镜指令] [氛围/风格]
```

### 运镜词汇表

| 用户描述 | 提示词 |
|----------|--------|
| 不动 | `Static shot.` / `Fixed camera.` |
| 慢推近 | `Slow push in.` / `Dolly zoom.` |
| 环绕 | `360-degree orbit.` |
| 跟拍 | `Tracking shot.` |
| 俯视 | `Aerial view.` / `Bird's-eye view.` |
| 上升 | `Camera rises slowly.` |
| 第一人称 | `POV shot.` |

### 风格词汇表

| 风格 | 提示词 |
|------|--------|
| 电影感 | `cinematic, shallow depth of field, dramatic lighting` |
| 纪录片 | `documentary style, natural lighting` |
| 动漫 | `anime style, vibrant colors` |
| 写实 | `photorealistic, 8K, ultra-detailed` |
| 梦幻 | `dreamy, soft bokeh, pastel tones` |

---

## 第四步：生成命令

```bash
# 文字生视频（标准，等待完成后下载）
mmx video generate \
  --prompt "A woman walks through a cherry blossom forest. Slow tracking shot. Cinematic." \
  --download output.mp4 \
  --quiet

# 快速出图（Hailuo-2.3-Fast）
mmx video generate \
  --model MiniMax-Hailuo-2.3-Fast \
  --prompt "一只猫在阳光下伸懒腰。静止镜头。" \
  --download cat.mp4 \
  --quiet

# 图生视频（首帧）
mmx video generate \
  --prompt "The person walks forward into the mist." \
  --first-frame person.jpg \
  --download walk.mp4 \
  --quiet

# SEF 首末帧插值（自动切换 Hailuo-02）
mmx video generate \
  --prompt "Smooth transition from dawn to dusk." \
  --first-frame dawn.jpg \
  --last-frame dusk.jpg \
  --download timelapse.mp4 \
  --quiet

# 角色一致性（自动切换 S2V-01）
mmx video generate \
  --prompt "A detective walks into a rainy street." \
  --subject-image character.jpg \
  --download detective.mp4 \
  --quiet

# 异步模式（立即返回 task ID，后台处理）
TASK=$(mmx video generate \
  --prompt "Ocean waves at sunset." \
  --async --quiet | python3 -c "import sys,json; print(json.load(sys.stdin).get('taskId',''))" 2>/dev/null)
echo "Task ID: $TASK"

# 查询进度
mmx video task get --task-id "$TASK" --output json --quiet

# 下载完成的视频
mmx video download --task-id "$TASK" --out ocean.mp4
```

---

## 等待策略

| 场景 | 推荐方式 |
|------|---------|
| 单个视频，可等待 | `--download 文件名`（默认轮询等待） |
| 批量生成 | `--async` 获取 task ID，轮询检查 |
| CI/自动化 | `--async --non-interactive` |

---

## 提示词最佳实践

1. **用英文提示词**：效果通常优于中文（模型训练偏英文）
2. **句号结尾**：每个描述元素用句号分隔
3. **明确运镜**：不写运镜 = 随机，建议始终指定
4. **避免文字/logo**：模型不善于在视频中渲染文字
5. **6 秒限制**：当前 Hailuo 系列固定 6 秒，复杂叙事需分段生成后拼接

---

## 注意事项

- 默认模型：`MiniMax-Hailuo-2.3`（768P, 6s）
- `--last-frame` 必须与 `--first-frame` 同时使用
- 生成耗时：标准 90-180 秒，Fast 30-60 秒
- 内容审核：暴力/成人内容会触发过滤器（exit code 10）
- 始终加 `--quiet` 避免进度条干扰
