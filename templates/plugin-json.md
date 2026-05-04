---
name: plugin-json
description: Claude Code 插件配置模板
type: json
usage: 复制并修改字段值
---

{
  "name": "{{plugin-name}}",
  "version": "1.0.0",
  "description": "{{插件描述}}",
  "author": {
    "name": "{{作者名}}",
    "url": "{{作者URL}}"
  },
  "homepage": "{{项目主页}}",
  "repository": "{{仓库地址}}",
  "license": "MIT",
  "keywords": [
    "{{关键词1}}",
    "{{关键词2}}"
  ],
  "minimum_claude_version": "1.8.0",
  "skills": "./skills/"
}