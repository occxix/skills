---
name: mmx-image-wizard
description: >
  一站式 MiniMax 图片生成封装脚本 mmx-image 的技能入口。
  适用场景：（1）文生图（t2i）；（2）人物转换风格（i2i，保持同一人物特征）；（3）水印自动检测与裁剪；（4）参考图含 UI 元素时自动预清洗。
  当用户说"生成图片"、"画一张图"、"把照片转成古风"、"人物换装"、或直接提供参考图要求 AI 基于该人物生成新图时使用此技能。
triggers:
  - 生成图片
  - 画一张
  - 文生图
  - 换装
  - 转换风格
  - 把照片转成
  - i2i
  - character reference
  - 人物转换
license: MIT
metadata:
  version: "1.0"
  category: media-generation
---

# mmx-image-wizard

## 一句话概述

`mmx-image` 封装脚本位于 `/root/.local/bin/mmx-image`，自动处理：正确的 mmx 参数、参考图预清洗、水印检测与裁剪、输出路径解析。

## 快速使用

```bash
# 文生图
mmx-image gen "日落海边，cinematic"

# 人物风格转换（保持同一人物特征）
mmx-image i2i "同一人穿上汉服" /path/to/photo.jpg --out /tmp/hanfu.png

# 多张变体
mmx-image gen "动漫风女孩" -n 3 --out /tmp/girls.png
```

## 核心参数（mmx image CLI 正确版本）

| 需求 | 正确写法 | 易错写法 |
|------|---------|---------|
| 输出路径 | `--out /path.jpg` | `--output`（不存在） |
| 人物参考 | `--subject-ref "type=character,image=/path.jpg"` | `--input-image`、`--ref-image`（不存在） |

## 完整自动化流程

```
用户请求
   ↓
预清洗参考图（含 UI 元素 → 自动裁剪主体）
   ↓
生成（prompt 自动追加 "no text, no watermark..."）
   ↓
水印检测（mmx vision）
   ↓ 有水印 → ffmpeg 裁剪右下角 12%
   ↓ 无水印 → 直接使用
   ↓
交付干净图片
```

## 水印处理（水印在生成阶段预防，不在生成后裁）

**预防（推荐）：** prompt 结尾追加 `, no text, no watermark, no logo, no letters`

**后处理（自动，由 mmx-image 脚本调用）：**
```bash
# 手动检测
mmx vision describe --image /path.jpg \
  --prompt "Are there any text, watermark, logo, or letters in this image?" --quiet

# 手动裁剪（右下角水印）
ffmpeg -i /path.jpg -vf "crop=iw:ih*0.88:0:0" -update 1 /path_clean.jpg
```

## 参考图含 UI 元素时

参考图如果是截图/视频帧（含状态栏、弹幕、用户名等），先用 ffmpeg 预清洗：

```bash
# 裁剪掉边缘 UI，保留中心主体
ffmpeg -i /path/to/screenshot.jpg \
  -vf "crop=iw*0.75:ih*0.78:iw*0.12:ih*0.08" \
  -update 1 /path/to/clean_ref.jpg
```

## 详细文档

完整内容见：`references/image-guide.md`（路径解析、故障排除、完整 Pipeline 代码）

## 依赖

- `mmx` CLI（`/root/.hermes/node/bin/mmx`）
- `ffmpeg`（水印裁剪）
- `bash` >= 4.0

## 验证脚本是否可用

```bash
mmx-image --help
```
