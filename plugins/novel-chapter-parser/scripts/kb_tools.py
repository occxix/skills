"""
小说章节解析器 - 知识库工具函数
"""

import os
import re
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

TEXT_ENCODINGS = ("utf-8-sig", "utf-8", "gb18030", "gbk", "big5", "cp1252")


def _cjk_count(text: str) -> int:
    return sum(1 for char in text if "\u4e00" <= char <= "\u9fff")


def _mojibake_score(text: str) -> int:
    markers = ("Ã", "Â", "¤", "¥", "¦", "§", "¨", "©", "ª", "«", "¬", "®", "¯", "å", "æ", "ç", "è", "é")
    return sum(text.count(marker) for marker in markers)


def repair_common_mojibake(text: str) -> str:
    """修复常见的 UTF-8 被按 cp1252/latin1 误读后保存的乱码。"""
    if _mojibake_score(text) < 5:
        return text

    candidates = []
    for encoding in ("cp1252", "latin1"):
        try:
            repaired = text.encode(encoding).decode("utf-8")
            candidates.append(repaired)
        except UnicodeError:
            continue

    if not candidates:
        return text

    best = max(candidates, key=lambda item: (_cjk_count(item), -_mojibake_score(item)))
    if _cjk_count(best) > _cjk_count(text) and _mojibake_score(best) < _mojibake_score(text):
        return best
    return text


def read_text_auto(path: str | Path) -> str:
    """自动识别常见文本编码并读取，返回已尽量修复乱码的文本。"""
    path = Path(path)
    logger.debug(f"读取文件: {path}")

    try:
        data = path.read_bytes()
    except Exception as e:
        logger.error(f"读取文件失败 {path}: {str(e)}")
        raise

    last_error = None

    for encoding in TEXT_ENCODINGS:
        try:
            text = repair_common_mojibake(data.decode(encoding))
            logger.debug(f"使用编码 {encoding} 读取成功")
            return text
        except UnicodeDecodeError as exc:
            last_error = exc
            continue

    if last_error:
        logger.error(f"无法识别文件编码 {path}, 尝试过的编码: {TEXT_ENCODINGS}")
        raise last_error
    return ""


def write_text_utf8(path: str | Path, content: str):
    """统一以 UTF-8 写入文本，避免后续中文乱码。"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    logger.debug(f"写入文件: {path} (大小: {len(content)} 字符)")
    path.write_text(content, encoding="utf-8", newline="\n")


def append_text_utf8(path: str | Path, content: str):
    """统一以 UTF-8 追加文本。"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    logger.debug(f"追加文件: {path} (追加大小: {len(content)} 字符)")
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(content)


def safe_file_name(name: str) -> str:
    """生成安全的文件名，去除特殊字符。"""
    invalid_chars = '<>:"/\\|?*'
    for c in invalid_chars:
        name = name.replace(c, '')
    # 替换空格和特殊符号
    name = re.sub(r'[\s]+', '_', name)
    # 限制长度
    return name[:100].strip('_')


def find_knowledge_base(base_path: str | Path) -> Optional[Path]:
    """查找知识库目录。"""
    base_path = Path(base_path)
    logger.debug(f"查找知识库: {base_path}")

    # 直接检查当前目录
    if (base_path / "0_预处理").exists():
        return base_path

    # 检查子目录
    for subdir in base_path.iterdir():
        if subdir.is_dir() and (subdir / "0_预处理").exists():
            logger.info(f"找到知识库: {subdir}")
            return subdir

    return None


# 知识库目录结构
KB_STRUCTURE = {
    "0_预处理": {},
    "1_写作手法": {},
    "2_世界观与环境": {
        "地域库": {},
        "组织库": {},
        "世界观总览.md": "template"
    },
    "3_人物体系": {},
    "4_剧情与事件": {},
    "5_关系网络": {},
    "6_动态演变与主题": {},
    "7_变化日志": {
        "人物变化日志.md": "template",
        "组织变化日志.md": "template",
        "地域变化日志.md": "template",
        "剧情与子剧情变化.md": "template",
        "关系变化日志.md": "template",
        "总变化时间线.md": "template"
    },
    "8_章节总结": {},
    "9_关键记忆点": {
        "高能语录记录.md": "template",
        "关键内心和思想变化记录.md": "template",
        "剧情转折记录.md": "template"
    }
}


def init_knowledge_base(base_path: str, novel_name: str) -> Dict[str, Any]:
    """
    初始化小说知识库目录结构
    
    Args:
        base_path: 基础路径
        novel_name: 小说名称
    
    Returns:
        创建结果
    """
    kb_path = Path(base_path) / f"小说解析器知识库（《{novel_name}》）"
    
    if kb_path.exists():
        return {
            "success": False,
            "message": f"知识库已存在: {kb_path}",
            "path": str(kb_path)
        }
    
    created_dirs = []
    created_files = []
    
    def create_structure(parent: Path, structure: dict, prefix: str = ""):
        for name, content in structure.items():
            item_path = parent / name
            if isinstance(content, dict):
                # 目录
                item_path.mkdir(parents=True, exist_ok=True)
                created_dirs.append(str(item_path.relative_to(kb_path)))
                if content:
                    create_structure(item_path, content, f"{prefix}{name}/")
            elif content == "template":
                # 模板文件
                item_path.parent.mkdir(parents=True, exist_ok=True)
                write_text_utf8(item_path, "")
                created_files.append(str(item_path.relative_to(kb_path)))
    
    kb_path.mkdir(parents=True, exist_ok=True)
    create_structure(kb_path, KB_STRUCTURE)
    
    return {
        "success": True,
        "message": f"知识库创建成功",
        "path": str(kb_path),
        "created_dirs": created_dirs,
        "created_files": created_files
    }


def get_chapter_preprocess_path(kb_path: str, chapter_num: int) -> Path:
    """获取预处理文件路径"""
    return Path(kb_path) / "0_预处理" / f"第{chapter_num:02d}章预处理.md"


def get_chapter_summary_path(kb_path: str, chapter_num: int) -> Path:
    """获取章节总结文件路径"""
    return Path(kb_path) / "8_章节总结" / f"第{chapter_num:02d}章总结.md"


def get_entity_path(kb_path: str, entity_type: str, entity_name: str) -> Path:
    """获取实体文件路径"""
    type_map = {
        "人物": "3_人物体系",
        "地域": "2_世界观与环境/地域库",
        "组织": "2_世界观与环境/组织库",
        "剧情": "4_剧情与事件",
        "关系": "5_关系网络"
    }
    dir_name = type_map.get(entity_type, entity_type)
    return Path(kb_path) / dir_name / f"{entity_name}.md"


def get_change_log_path(kb_path: str, log_type: str) -> Path:
    """获取变化日志路径"""
    log_map = {
        "人物": "人物变化日志.md",
        "组织": "组织变化日志.md",
        "地域": "地域变化日志.md",
        "剧情": "剧情与子剧情变化.md",
        "关系": "关系变化日志.md"
    }
    filename = log_map.get(log_type, f"{log_type}变化日志.md")
    return Path(kb_path) / "7_变化日志" / filename


def get_timeline_path(kb_path: str) -> Path:
    """获取总变化时间线路径"""
    return Path(kb_path) / "7_变化日志" / "总变化时间线.md"


def get_key_memory_path(kb_path: str, memory_type: str) -> Path:
    """获取关键记忆点文件路径"""
    memory_map = {
        "高能语录": "高能语录记录.md",
        "内心思想": "关键内心和思想变化记录.md",
        "剧情转折": "剧情转折记录.md"
    }
    filename = memory_map.get(memory_type, f"{memory_type}记录.md")
    return Path(kb_path) / "9_关键记忆点" / filename


# 模板内容
PREPROCESS_TEMPLATE = """# 第{chapter:02d}章 预处理（纯提取）

**章节基本信息**
- 标题：
- 字数：
- 时间/地点：
- 章节起始行号：第{start_line}行
- 章节结尾行号：第{end_line}行

**提取内容**

**人物**
- 人物名：描述（能力、性格、外貌、关键行为）

**组织**
- 组织名：描述（地位、与主角关系）

**地域**
- 地域名：描述（特点、氛围）

**剧情与事件**
- 主事件：
- 关键细节：

**关系**
- A → B：关系描述

**世界观提示**
- 新增/提及设定：

**伏笔/象征**
- 伏笔：
- 象征：

**关键记忆点候选**
- 高能语录：原句/概述
- 关键内心和思想变化：描述
- 剧情转折：描述
"""

QUERY_REPORT_TEMPLATE = """# 第{chapter:02d}章 查询报告

**当前知识库状态（查询前）**
- 实体名：状态描述（新增 / 已存在 / 需要更新）

**需要更新的实体**
- 地域：xxx（新增）
- 组织：xxx（新增）
- 人物：xxx（新增/更新）

**需要写入关键记忆点**
- 高能语录：xxx
- 关键内心和思想变化：xxx
- 剧情转折：xxx

**是否需要调用历史时间线？** → 是/否（原因）
**是否需要调用之前章节总结？** → 是/否（原因）
**是否需要调用关键记忆点？** → 是/否（原因）

查询完成，可直接进入操作3更新。
"""

ENTITY_TEMPLATE = """# {name}

## 1. 当前状态
- 首次出现：第{chapter}章
- 身份/类型：
- 特点：
- 能力/设定：
- 最新状态：（本章关键变化）

## 2. 变化时间线
- 第{chapter}章：具体变化描述
"""

CHAPTER_SUMMARY_TEMPLATE = """# 第{chapter:02d}章 总结

**章节基本信息**
- 章节标题：
- 字数：
- 核心事件：

**1. 写作手法与叙事技巧**

**2. 世界观与环境设定**

**3. 人物体系**

**4. 剧情与事件体系**

**5. 关系网络**

**6. 动态演变与主题**

**本章贡献**：

**待关注**：

**关键记忆点**：
- 高能语录：
- 关键内心和思想变化：
- 剧情转折：

**来源**：第{chapter:02d}章原文 + 知识库查询
"""

CHANGE_LOG_ENTRY = """
### 第{chapter:02d}章

**{entity_name}**
- 变化：{change_desc}
- 来源：第{chapter:02d}章
"""

TIMELINE_ENTRY = """
## 第{chapter:02d}章

### 人物变化
- 

### 组织变化
- 

### 地域变化
- 

### 剧情进展
- 

### 关系变化
- 

---
"""

KEY_MEMORY_ENTRY = """
### 第{chapter:02d}章

- 内容：{content}
"""
