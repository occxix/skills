"""
处理单章小说

用法: /parse-chapter <章节号> <小说原文路径>
"""

import os
import sys
import re
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

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

from kb_tools import (
    get_chapter_preprocess_path,
    get_chapter_summary_path,
    get_entity_path,
    get_change_log_path,
    get_timeline_path,
    get_key_memory_path,
    read_text_auto,
    write_text_utf8,
    append_text_utf8,
    safe_file_name,
    find_knowledge_base,
    PREPROCESS_TEMPLATE,
    QUERY_REPORT_TEMPLATE,
    ENTITY_TEMPLATE,
    CHAPTER_SUMMARY_TEMPLATE,
    CHANGE_LOG_ENTRY,
    TIMELINE_ENTRY,
    KEY_MEMORY_ENTRY
)


class ChapterParser:
    """章节解析器"""
    
    def __init__(self, kb_path: str, source_path: str):
        """
        初始化
        
        Args:
            kb_path: 知识库路径
            source_path: 小说原文路径
        """
        self.kb_path = Path(kb_path)
        self.source_path = Path(source_path)
        self.chapter_num = 0
        self.chapter_content = ""
        self.chapter_start_line = 0
        self.chapter_end_line = 0
        self.preprocess_data = {}
    
    def parse_chapter(self, chapter_num: int) -> Dict[str, Any]:
        """
        解析指定章节（执行三次操作）
        
        Args:
            chapter_num: 章节号
        
        Returns:
            处理结果
        """
        self.chapter_num = chapter_num
        
        # 读取章节内容
        self.chapter_content = self._read_chapter(chapter_num)
        if not self.chapter_content:
            return {"success": False, "error": f"无法读取第{chapter_num}章"}
        
        results = {
            "chapter": chapter_num,
            "operation1": None,
            "operation2": None,
            "operation3": None
        }
        
        # 操作1：生成预处理
        results["operation1"] = self._operation1_preprocess()
        
        # 操作2：查询知识库
        results["operation2"] = self._operation2_query()
        
        # 操作3：更新知识库（由用户/LLM执行）
        results["operation3"] = {
            "status": "pending",
            "message": "请根据预处理和查询结果，完成知识库更新"
        }
        
        return results
    
    def _read_chapter(self, chapter_num: int) -> str:
        """读取章节内容"""
        if self.source_path.is_file():
            # 单文件小说
            content = read_text_auto(self.source_path)
            return self._extract_chapter(content, chapter_num)
        else:
            # 多文件小说
            chapter_file = self.source_path / f"第{chapter_num:02d}章.txt"
            if chapter_file.exists():
                content = read_text_auto(chapter_file)
                self.chapter_start_line = 1
                self.chapter_end_line = len(content.splitlines()) or 1
                return content
            # 尝试其他命名
            for pattern in [f"第{chapter_num}章*.txt", f"*{chapter_num}*.txt"]:
                matches = list(self.source_path.glob(pattern))
                if matches:
                    content = read_text_auto(matches[0])
                    self.chapter_start_line = 1
                    self.chapter_end_line = len(content.splitlines()) or 1
                    return content
        return ""
    
    def _extract_chapter(self, content: str, chapter_num: int) -> str:
        """从长文本中提取指定章节"""
        # 阿拉伯数字转中文数字映射
        num_map = {
            '0': '零', '1': '一', '2': '二', '3': '三', '4': '四',
            '5': '五', '6': '六', '7': '七', '8': '八', '9': '九'
        }

        # 生成中文数字表示
        def num_to_chinese(n: int) -> str:
            if n == 0:
                return '零'
            digits = list(str(n))
            units = ['', '十', '百', '千', '万']
            result = []
            for i, d in enumerate(reversed(digits)):
                if d != '0':
                    result.append(num_map[d] + units[i])
                elif result and result[-1][0] != '零':
                    result.append('零')
            if len(result) > 1 and result[-1] == '一' and result[-2] == '十':
                result = result[:-1]
            return ''.join(reversed(result)).rstrip('零')

        chinese_num = num_to_chinese(chapter_num)

        # 目标章节匹配模式（按优先级排序）
        target_patterns = [
            # 标准中文章节
            rf'^\s*第\s*{chapter_num}\s*章\s*[^\n]*',
            rf'^\s*第\s*{chinese_num}\s*章\s*[^\n]*',
            # 其他章节格式
            rf'^\s*第\s*{chapter_num}\s*节\s*[^\n]*',
            rf'^\s*第\s*{chapter_num}\s*回\s*[^\n]*',
            rf'^\s*第\s*{chapter_num}\s*卷\s*[^\n]*',
            # 数字开头的章节
            rf'^\s*{chapter_num}\s*[\.、]\s*[^\n]*',
            rf'^\s*{chapter_num}\s*[^\n]*',
            # 英文格式
            rf'^Chapter\s+{chapter_num}\b[^\n]*',
            rf'^Episode\s+{chapter_num}\b[^\n]*',
            rf'^Part\s+{chapter_num}\b[^\n]*',
        ]

        # 任意章节匹配模式（用于查找章节边界）
        any_chapter_patterns = [
            r'^\s*第\s*\d+\s*章\s*[^\n]*',
            r'^\s*第\s*[一二三四五六七八九十百千]+\s*章\s*[^\n]*',
            r'^\s*第\s*\d+\s*节\s*[^\n]*',
            r'^\s*第\s*\d+\s*回\s*[^\n]*',
            r'^\s*第\s*\d+\s*卷\s*[^\n]*',
            r'^\s*\d+\s*[\.、]\s*[^\n]*',
            r'^Chapter\s+\d+\b[^\n]*',
            r'^Episode\s+\d+\b[^\n]*',
            r'^Part\s+\d+\b[^\n]*',
        ]

        lines = content.split('\n')
        start_idx = -1
        end_idx = len(lines)

        # 查找章节开始位置
        for i, line in enumerate(lines):
            for pattern in target_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    start_idx = i
                    logger.debug(f"找到章节开始位置: 第{i+1}行, 内容: {line.strip()}")
                    break
            if start_idx != -1:
                break

        if start_idx == -1:
            logger.warning(f"未找到第{chapter_num}章的开始位置")
            return ""

        # 查找章节结束位置（下一个章节开始）
        for i in range(start_idx + 1, len(lines)):
            if any(re.search(pattern, lines[i], re.IGNORECASE) for pattern in any_chapter_patterns):
                end_idx = i
                logger.debug(f"找到章节结束位置: 第{i+1}行, 下一章内容: {lines[i].strip()}")
                break

        self.chapter_start_line = start_idx + 1
        self.chapter_end_line = end_idx
        chapter_content = '\n'.join(lines[start_idx:end_idx])

        logger.info(f"成功提取第{chapter_num}章: {self.chapter_start_line}-{self.chapter_end_line}行, 共{len(chapter_content)}字符")
        return chapter_content
    
    def _operation1_preprocess(self) -> Dict[str, Any]:
        """
        操作1：生成预处理文件（纯提取）

        只读本章原文，不查询知识库、不做任何判断
        """
        preprocess_path = get_chapter_preprocess_path(str(self.kb_path), self.chapter_num)
        preprocess_path.parent.mkdir(parents=True, exist_ok=True)

        # 自动提取章节信息
        auto_extracted = self._auto_extract_content(self.chapter_content)
        logger.info(f"自动提取到 {len(auto_extracted.get('characters', []))} 个人物, {len(auto_extracted.get('organizations', []))} 个组织")

        # 填充模板
        template = PREPROCESS_TEMPLATE.format(
            chapter=self.chapter_num,
            start_line=self.chapter_start_line or "X",
            end_line=self.chapter_end_line or "Y"
        )

        # 替换模板中的占位内容
        if auto_extracted.get('title'):
            template = template.replace('- 标题:', f'- 标题: {auto_extracted["title"]}')
        if auto_extracted.get('word_count'):
            template = template.replace('- 字数:', f'- 字数: {auto_extracted["word_count"]}')
        if auto_extracted.get('time_location'):
            template = template.replace('- 时间/地点:', f'- 时间/地点: {auto_extracted["time_location"]}')

        # 填充提取的实体
        if auto_extracted.get('characters'):
            characters_section = '\n'.join(f'- {name}: {desc}' for name, desc in auto_extracted['characters'].items())
            template = template.replace('**人物**\n- 人物名: 描述（能力、性格、外貌、关键行为）', f'**人物**\n{characters_section}')

        if auto_extracted.get('organizations'):
            orgs_section = '\n'.join(f'- {name}: {desc}' for name, desc in auto_extracted['organizations'].items())
            template = template.replace('**组织**\n- 组织名: 描述（地位、与主角关系）', f'**组织**\n{orgs_section}')

        if auto_extracted.get('locations'):
            locations_section = '\n'.join(f'- {name}: {desc}' for name, desc in auto_extracted['locations'].items())
            template = template.replace('**地域**\n- 地域名: 描述（特点、氛围）', f'**地域**\n{locations_section}')

        if auto_extracted.get('events'):
            events_section = '\n'.join(f'- {event}' for event in auto_extracted['events'])
            template = template.replace('**剧情与事件**\n- 主事件:\n- 关键细节:', f'**剧情与事件**\n{events_section}')

        write_text_utf8(preprocess_path, template)

        return {
            "status": "created",
            "file": str(preprocess_path),
            "message": f"已创建预处理模板，自动提取了{len(auto_extracted.get('characters', []))}个人物，{len(auto_extracted.get('organizations', []))}个组织",
            "auto_extracted": auto_extracted
        }

    def _auto_extract_content(self, content: str) -> Dict[str, Any]:
        """自动提取章节内容中的关键信息。"""
        result = {
            'title': '',
            'word_count': len(content),
            'time_location': '',
            'characters': {},
            'organizations': {},
            'locations': {},
            'events': [],
            'relationships': [],
            'world_settings': [],
            'foreshadowing': [],
            'key_quotes': []
        }

        if not content:
            return result

        lines = [line.strip() for line in content.split('\n') if line.strip()]
        if lines:
            # 提取章节标题（第一行通常是标题）
            result['title'] = lines[0][:100]

        # 预定义的组织后缀
        org_suffixes = ['派', '教', '宗', '门', '寺', '观', '宫', '阁', '楼', '会', '盟', '族', '帮', '谷',
                       '府', '城', '国', '殿', '院', '司', '局', '部', '所', '社', '团', '队', '组', '军',
                       '营', '连', '班', '盟', '联', '协', '学', '宫']

        # 预定义的地点后缀
        loc_suffixes = ['城', '市', '镇', '村', '庄', '岛', '山', '峰', '岭', '谷', '河', '江', '湖', '海',
                       '洋', '湾', '港', '关', '口', '岸', '原', '野', '森', '林', '洞', '穴', '府', '宅',
                       '院', '楼', '阁', '殿', '寺', '观', '庙', '塔', '桥', '路', '街', '巷', '里', '坊']

        # 提取人物（基于常见的称呼模式）
        name_patterns = [
            r'([一-龥]{2,4})[说道|问|答|喊|叫|笑|哭|怒|喜|悲|惊|怕]',
            r'([一-龥]{2,4})[先生|小姐|夫人|太太|公公|婆婆|叔叔|阿姨|哥哥|弟弟|姐姐|妹妹]',
            r'([一-龥]{2,4})[掌门|帮主|教主|宫主|阁主|楼主|队长|团长|连长|营长|司令]',
        ]

        for pattern in name_patterns:
            matches = re.findall(pattern, content)
            for name in matches:
                if len(name) >= 2 and name not in result['characters']:
                    # 简单描述
                    result['characters'][name] = '待补充'

        # 提取组织
        for suffix in org_suffixes:
            pattern = r'([一-龥]{2,6}' + suffix + ')'
            matches = re.findall(pattern, content)
            for org in matches:
                if org not in result['organizations']:
                    result['organizations'][org] = '待补充'

        # 提取地点
        for suffix in loc_suffixes:
            pattern = r'([一-龥]{2,6}' + suffix + ')'
            matches = re.findall(pattern, content)
            for loc in matches:
                if loc not in result['locations']:
                    result['locations'][loc] = '待补充'

        # 提取关键事件（简单基于句子长度和关键词）
        keywords = ['决定', '计划', '开始', '结束', '成功', '失败', '发现', '发明', '创建', '毁灭',
                   '死亡', '出生', '结婚', '离婚', '背叛', '忠诚', '战斗', '谈判', '交易', '约定',
                   '承诺', '誓言', '诅咒', '祝福', '预言', '秘密', '真相', '谎言', '欺骗', '信任']

        sentences = re.split(r'[。！？；\n]', content)
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:
                for keyword in keywords:
                    if keyword in sentence:
                        result['events'].append(sentence[:200])
                        break

        # 提取关键语录（引号中的内容）
        quote_pattern = r'["“]([^"”]+)["”]'
        quotes = re.findall(quote_pattern, content)
        for quote in quotes:
            if len(quote) > 5 and len(quote) < 200:
                result['key_quotes'].append(quote)

        logger.debug(f"自动提取完成: {len(result['characters'])} 人物, {len(result['organizations'])} 组织, {len(result['locations'])} 地点, {len(result['events'])} 事件")
        return result
    
    def _operation2_query(self) -> Dict[str, Any]:
        """
        操作2：查询知识库（只查询、不修改）
        
        根据预处理内容查询相关实体状态
        """
        # 读取预处理文件
        preprocess_path = get_chapter_preprocess_path(str(self.kb_path), self.chapter_num)
        if not preprocess_path.exists():
            return {
                "status": "error",
                "message": "预处理文件不存在，请先完成操作1"
            }
        
        # 生成查询报告模板
        query_report_path = self.kb_path / "0_预处理" / f"第{self.chapter_num:02d}章查询报告.md"
        
        report_content = QUERY_REPORT_TEMPLATE.format(chapter=self.chapter_num)
        
        # 添加查询指引
        report_content += "\n\n---\n**查询指引**\n\n"
        report_content += "请根据预处理中的实体，查询以下位置：\n"
        report_content += f"- 人物实体: `3_人物体系/`\n"
        report_content += f"- 地域实体: `2_世界观与环境/地域库/`\n"
        report_content += f"- 组织实体: `2_世界观与环境/组织库/`\n"
        report_content += f"- 历史时间线: `7_变化日志/总变化时间线.md`\n"
        report_content += f"- 之前章节总结: `8_章节总结/`\n"
        report_content += f"- 关键记忆点: `9_关键记忆点/`\n"
        
        write_text_utf8(query_report_path, report_content)
        
        return {
            "status": "created",
            "file": str(query_report_path),
            "message": f"已创建查询报告模板，请完成知识库查询"
        }
    
    def create_entity_file(self, entity_type: str, entity_name: str) -> str:
        """
        操作3辅助：创建/更新实体文件
        
        Args:
            entity_type: 实体类型（人物/地域/组织/剧情/关系）
            entity_name: 实体名称
        
        Returns:
            文件路径
        """
        entity_path = get_entity_path(str(self.kb_path), entity_type, entity_name)
        entity_path.parent.mkdir(parents=True, exist_ok=True)
        
        if entity_path.exists():
            # 追加变化时间线
            content = read_text_auto(entity_path)
            
            # 在变化时间线末尾追加
            timeline_entry = f"\n- 第{self.chapter_num}章：具体变化描述\n"
            if "## 2. 变化时间线" in content:
                content = content.rstrip() + timeline_entry
            else:
                content += f"\n\n## 2. 变化时间线{timeline_entry}"
            
            write_text_utf8(entity_path, content)
        else:
            # 创建新实体文件
            template = ENTITY_TEMPLATE.format(
                name=entity_name,
                chapter=self.chapter_num
            )
            write_text_utf8(entity_path, template)
        
        return str(entity_path)
    
    def append_change_log(self, log_type: str, entity_name: str, change_desc: str):
        """
        操作3辅助：追加变化日志
        
        Args:
            log_type: 日志类型（人物/组织/地域/剧情/关系）
            entity_name: 实体名称
            change_desc: 变化描述
        """
        log_path = get_change_log_path(str(self.kb_path), log_type)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        entry = CHANGE_LOG_ENTRY.format(
            chapter=self.chapter_num,
            entity_name=entity_name,
            change_desc=change_desc
        )
        
        if log_path.exists():
            append_text_utf8(log_path, entry)
        else:
            write_text_utf8(log_path, f"# {log_type}变化日志\n{entry}")
    
    def append_timeline(self, content: str):
        """
        操作3辅助：追加总变化时间线
        
        Args:
            content: 时间线内容
        """
        timeline_path = get_timeline_path(str(self.kb_path))
        timeline_path.parent.mkdir(parents=True, exist_ok=True)
        
        entry = TIMELINE_ENTRY.format(chapter=self.chapter_num)
        
        if timeline_path.exists():
            append_text_utf8(timeline_path, content)
        else:
            write_text_utf8(timeline_path, f"# 总变化时间线\n\n{content}")

    def append_key_memory(self, memory_type: str, content: str):
        """
        操作3辅助：追加关键记忆点

        Args:
            memory_type: 记忆点类型（高能语录/内心思想/剧情转折）
            content: 记忆点内容
        """
        memory_path = get_key_memory_path(str(self.kb_path), memory_type)
        memory_path.parent.mkdir(parents=True, exist_ok=True)

        entry = KEY_MEMORY_ENTRY.format(
            chapter=self.chapter_num,
            content=content
        )

        if memory_path.exists():
            append_text_utf8(memory_path, entry)
        else:
            write_text_utf8(memory_path, f"# {memory_path.stem}\n{entry}")
    
    def create_chapter_summary(self, content: str = None):
        """
        操作3辅助：创建章节总结
        
        Args:
            content: 总结内容（可选，默认使用模板）
        """
        summary_path = get_chapter_summary_path(str(self.kb_path), self.chapter_num)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        
        if content:
            template = content
        else:
            template = CHAPTER_SUMMARY_TEMPLATE.format(chapter=self.chapter_num)
        
        write_text_utf8(summary_path, template)
        
        return str(summary_path)


def main():
    """命令行入口"""
    if len(sys.argv) < 3:
        print("用法: python parse_chapter.py <章节号> <小说原文路径> [知识库路径]")
        print("示例: python parse_chapter.py 1 ./novel.txt ./知识库")
        sys.exit(1)
    
    chapter_num = int(sys.argv[1])
    source_path = sys.argv[2]
    kb_path = sys.argv[3] if len(sys.argv) > 3 else os.getcwd()
    
    # 查找知识库
    kb_dir = Path(kb_path)
    if not (kb_dir / "0_预处理").exists():
        # 尝试查找子目录
        for subdir in kb_dir.iterdir():
            if subdir.is_dir() and (subdir / "0_预处理").exists():
                kb_path = str(subdir)
                break
    
    parser = ChapterParser(kb_path, source_path)
    result = parser.parse_chapter(chapter_num)
    
    print(f"\n📖 第{chapter_num}章处理结果:")
    print(f"\n操作1（预处理）: {result['operation1']['status']}")
    print(f"  📄 文件: {result['operation1']['file']}")
    
    print(f"\n操作2（查询）: {result['operation2']['status']}")
    print(f"  📄 文件: {result['operation2']['file']}")
    
    print(f"\n操作3（更新）: {result['operation3']['status']}")
    print(f"  💡 {result['operation3']['message']}")


if __name__ == "__main__":
    main()
