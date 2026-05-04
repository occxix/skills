#!/usr/bin/env python3
"""
批量处理小说章节
用法: /parse-chapters <起始章> <结束章> <小说原文路径> [知识库路径]
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 添加脚本路径
SCRIPTS_PATH = Path(__file__).parent
if str(SCRIPTS_PATH) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_PATH))

from parse_chapter import ChapterParser
from kb_tools import find_knowledge_base


def batch_parse_chapters(start_chapter: int, end_chapter: int, source_path: str, kb_path: str = None) -> Dict[str, Any]:
    """
    批量处理多个章节

    Args:
        start_chapter: 起始章节号
        end_chapter: 结束章节号
        source_path: 小说原文路径
        kb_path: 知识库路径（可选）

    Returns:
        处理结果统计
    """
    if start_chapter > end_chapter:
        start_chapter, end_chapter = end_chapter, start_chapter

    logger.info(f"开始批量处理章节: {start_chapter} - {end_chapter}")

    # 查找知识库路径
    if not kb_path:
        kb_path = find_knowledge_base(os.getcwd())
        if not kb_path:
            return {
                "success": False,
                "error": "未找到知识库，请先运行 /init-novel 初始化知识库，或手动指定知识库路径"
            }

    kb_path = Path(kb_path)
    logger.info(f"使用知识库: {kb_path}")

    # 初始化解析器
    parser = ChapterParser(str(kb_path), source_path)

    results = {
        "total": end_chapter - start_chapter + 1,
        "success": 0,
        "failed": 0,
        "chapters": []
    }

    # 逐个处理章节
    for chapter_num in range(start_chapter, end_chapter + 1):
        logger.info(f"正在处理第 {chapter_num}/{end_chapter} 章")
        try:
            result = parser.parse_chapter(chapter_num)
            if result.get("success", True):
                results["success"] += 1
                results["chapters"].append({
                    "chapter": chapter_num,
                    "status": "success",
                    "result": result
                })
                logger.info(f"第 {chapter_num} 章处理完成")
            else:
                results["failed"] += 1
                results["chapters"].append({
                    "chapter": chapter_num,
                    "status": "failed",
                    "error": result.get("error", "未知错误")
                })
                logger.error(f"第 {chapter_num} 章处理失败: {result.get('error')}")
        except Exception as e:
            results["failed"] += 1
            results["chapters"].append({
                "chapter": chapter_num,
                "status": "failed",
                "error": str(e)
            })
            logger.exception(f"第 {chapter_num} 章处理异常")

    logger.info(f"批量处理完成: 成功 {results['success']} 章, 失败 {results['failed']} 章, 总计 {results['total']} 章")
    return results


def main():
    """命令行入口"""
    if len(sys.argv) < 4:
        print("用法: python parse_chapters.py <起始章> <结束章> <小说原文路径> [知识库路径]")
        print("示例: python parse_chapters.py 1 10 ./novel.txt ./novel-knowledge-base")
        sys.exit(1)

    try:
        start_chapter = int(sys.argv[1])
        end_chapter = int(sys.argv[2])
    except ValueError:
        print("错误: 章节号必须是整数")
        sys.exit(1)

    source_path = sys.argv[3]
    kb_path = sys.argv[4] if len(sys.argv) > 4 else None

    # 检查源文件是否存在
    if not Path(source_path).exists():
        print(f"错误: 小说原文件/目录不存在: {source_path}")
        sys.exit(1)

    # 执行批量处理
    results = batch_parse_chapters(start_chapter, end_chapter, source_path, kb_path)

    # 输出结果
    print(f"\n📊 批量处理结果统计:")
    print(f"总章节数: {results['total']}")
    print(f"✅ 成功: {results['success']}")
    print(f"❌ 失败: {results['failed']}")
    print(f"成功率: {results['success'] / results['total'] * 100:.1f}%")

    if results['failed'] > 0:
        print("\n❌ 失败的章节:")
        for chapter in results['chapters']:
            if chapter['status'] == 'failed':
                print(f"  - 第 {chapter['chapter']} 章: {chapter['error']}")

    if results['success'] > 0:
        print(f"\n📝 已处理的章节会在 0_预处理/ 目录下生成对应的预处理和查询报告文件")
        print("请根据报告内容完成后续的知识库更新操作")

    # 有失败的章节时返回非零退出码
    sys.exit(results['failed'] > 0)


if __name__ == "__main__":
    main()