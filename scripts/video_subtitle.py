#!/usr/bin/env python3
"""
Video Subtitle Extractor — supports Bilibili and YouTube.
Usage:
    python video_subtitle.py <URL_or_ID> [--output FILE] [--format FORMAT] [--lang LANG]
Examples:
    # Bilibili
    python video_subtitle.py BV12ZDuBwEhX
    python video_subtitle.py https://www.bilibili.com/video/BV12ZDuBwEhX/
    python video_subtitle.py BV12ZDuBwEhX --srt --output subs.srt

    # YouTube
    python video_subtitle.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
    python video_subtitle.py dQw4w9WgXcQ
    python video_subtitle.py https://youtu.be/dQw4w9WgXcQ --lang zh-Hans
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.parse
import os
import subprocess
import math


# ============================================================
# Shared utilities
# ============================================================

def format_timestamp(seconds: float) -> str:
    seconds = max(0, seconds)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def detect_platform(input_str: str) -> str:
    """Detect video platform or web page from URL or ID pattern."""
    s = input_str.strip()
    if re.search(r'bilibili\.com', s) or re.match(r'^BV[a-zA-Z0-9]+$', s):
        return 'bilibili'
    if re.search(r'youtube\.com|youtu\.be', s) or re.match(r'^[a-zA-Z0-9_-]{11}$', s):
        return 'youtube'
    # Fallback: try BV pattern
    if re.search(r'BV[a-zA-Z0-9]+', s):
        return 'bilibili'
    # If it looks like a URL and not a video platform → treat as web page
    if re.match(r'https?://', s):
        return 'web'
    raise ValueError(f"Cannot detect platform from: {input_str}")


def output_result(entries: list, args, extra_meta: dict = None):
    """Format and output subtitle entries. entries = [{start, end, content}, ...]"""
    if args.format == 'srt':
        lines = []
        for i, e in enumerate(entries, 1):
            lines.append(str(i))
            lines.append(f"{format_timestamp(e['start'])},000 --> {format_timestamp(e['end'])},000")
            lines.append(e['content'])
            lines.append('')
        text = '\n'.join(lines)
    elif args.format == 'json':
        formatted = []
        for e in entries:
            formatted.append({
                'start': format_timestamp(e['start']),
                'end': format_timestamp(e['end']),
                'start_sec': round(e['start'], 1),
                'end_sec': round(e['end'], 1),
                'content': e['content'],
            })
        text = json.dumps(formatted, ensure_ascii=False, indent=2)
    elif args.format == 'text-only':
        text = '\n'.join(e['content'] for e in entries)
    elif args.format == 'vtt':
        lines = ['WEBVTT', '']
        for e in entries:
            lines.append(f"{format_timestamp(e['start'])}.000 --> {format_timestamp(e['end'])}.000")
            lines.append(e['content'])
            lines.append('')
        text = '\n'.join(lines)
    elif args.format == 'raw':
        text = json.dumps(entries, ensure_ascii=False, indent=2)
    else:
        # Default: plain text with timestamps
        lines = []
        for e in entries:
            lines.append(f"[{format_timestamp(e['start'])} - {format_timestamp(e['end'])}] {e['content']}")
        text = '\n'.join(lines)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            if extra_meta:
                f.write(f"# Platform: {extra_meta.get('platform', 'unknown')}\n")
                f.write(f"# Title: {extra_meta.get('title', '')}\n")
                f.write(f"# Author: {extra_meta.get('author', '')}\n")
                if extra_meta.get('language'):
                    f.write(f"# Language: {extra_meta['language']}\n")
                f.write(f"# Entries: {len(entries)}\n\n")
            f.write(text)
        print(f"Saved to {args.output}", file=sys.stderr)
    else:
        if extra_meta and args.format not in ('json', 'raw', 'srt', 'vtt'):
            print(f"# Platform: {extra_meta.get('platform', 'unknown')}", file=sys.stderr)
            print(f"# Title: {extra_meta.get('title', '')}", file=sys.stderr)
            print(f"# Author: {extra_meta.get('author', '')}", file=sys.stderr)
            if extra_meta.get('language'):
                print(f"# Language: {extra_meta['language']}", file=sys.stderr)
            print(f"# Entries: {len(entries)}", file=sys.stderr)
            print("---", file=sys.stderr)
        print(text)


# ============================================================
# Skill Report — 视频内容八级分类：A报告/B技能/C演示/D教程/E玩法文档/F知识库/G娱乐梗/H引流
# ============================================================

# ---------- B (Skill): 工作流/技能类关键词 ----------
B_KEYWORDS_ZH = [
    '步骤', '第一步', '第二步', '第三步', '首先', '然后', '接着', '最后',
    '安装', '配置', '下载', '设置', '运行', '执行', '输入', '输出',
    '教程', '方法', '流程', '工作流', '自动化',
    'skill', '配置', '模板', '脚本', '命令', '工具',
]

B_KEYWORDS_EN = [
    'step', 'first', 'then', 'next', 'finally', 'install', 'setup',
    'download', 'configure', 'run', 'execute', 'command',
    'script', 'tool', 'workflow', 'automate',
    'tutorial', 'guide', 'how to',
]

# ---------- C (Demo): 实现/构建类关键词 ----------
C_KEYWORDS_ZH = [
    # 编码实现
    '代码', '源码', '源代码', '实现', '开发', '构建', '编写',
    '函数', '组件', '类', '接口', '数据',
    '算法', '逻辑', '渲染', '动画', '交互',
    # 框架/库/平台
    'three.js', 'unity', 'unreal', 'webgl', 'glsl', 'canvas',
    'react', 'vue', 'node', 'python', 'html', 'css', 'javascript',
    'npm', 'pip', 'yarn', 'github', '仓库', '项目',
    # 产物/效果
    'demo', '示例', '演示', '展示', '效果', '原型', 'prototype',
    '界面', 'ui', '画面', '图形', 'graphics',
    '游戏', '玩法', '关卡', '场景',
    '网站', '网页', 'web', 'app', '工具', '插件', 'plugin',
    # 实现细节
    '尺寸', '大小', '宽度', '高度', '颜色', '位置',
    '点击', '拖拽', '滚动', '鼠标', '键盘',
    '生成', '创建', 'build', 'deploy', '发布',
]

C_KEYWORDS_EN = [
    'demo', 'example', 'code', 'source', 'implement', 'implementation',
    'build', 'create', 'develop', 'construct',
    'function', 'component', 'class', 'algorithm', 'logic',
    'render', 'animation', 'interaction', 'interface',
    'game', 'app', 'web', 'tool', 'plugin', 'prototype',
    'three.js', 'shader', 'canvas', 'webgl',
    'github', 'project', 'repository', 'npm', 'pip',
    'ui', 'ux', 'layout', 'design', 'graphics',
    'click', 'drag', 'scroll', 'mouse', 'keyboard',
    'generate', 'create', 'build',
]

# ---------- D (Tutorial): 教程/教育类关键词 ----------
D_KEYWORDS_ZH = [
    # 教学概念
    '教学', '教程', '学习', '理解', '入门', '基础', '概念',
    '原理', '理论', '定义', '特性', '特征', '本质', '核心',
    '讲解', '介绍', '概述', '总结', '回顾', '结论', '归纳',
    '例子', '比如', '例如', '举例', '类比',
    # 结构词
    '什么是', '是什么', '为什么', '原因', '因为', '所以',
    '对比', '区别', '不同', '差异', '优缺点',
    '适用', '场景', '用途', '应用', '常见',
    '注意', '注意事项', '建议', '推荐', '技巧',
    # 教育场景
    '知识点', '知识', '框架', '体系', '分类', '类型',
    '初学者', '新手', '进阶', '高阶',
    '课时', '章节', '模块', '大纲', '目录',
    # 讲解结构
    '第一个', '第二个', '首先', '其次', '然后', '最后',
    '一方面', '另一方面', '总的来说', '总而言之',
]

D_KEYWORDS_EN = [
    'tutorial', 'learn', 'teach', 'education', 'educational',
    'course', 'lesson', 'curriculum', 'training',
    'concept', 'principle', 'theory', 'theoretical', 'definition',
    'what is', 'introduction', 'overview', 'explain', 'explanation',
    'example', 'for example', 'for instance', 'e.g.',
    'beginner', 'basic', 'fundamental', 'essential',
    'understanding', 'understand', 'comprehend', 'knowledge',
    'summary', 'conclusion', 'review', 'recap', 'wrap-up',
    'difference', 'comparison', 'contrast', 'pros and cons',
    'advantage', 'disadvantage',
    'use case', 'scenario', 'application',
    'guide', 'walkthrough', 'reference',
    'first', 'second', 'finally', 'overall',
]

# ---------- B + C 都沾边的技术词（辅助判断） ----------
TECH_BOOST = [
    'python', 'javascript', 'typescript', 'html', 'css', 'bash',
    'git', 'docker', 'node', 'api', 'model', 'ai', 'llm',
    'whisper', 'asr', 'funasr', 'claude', 'openai',
    'video', 'audio', 'subtitle', '字幕', '剪辑', '口播',
    '编辑器', 'vscode', 'code', 'terminal',
]

# ---------- E (Game Design Doc): 玩法文档/游戏设计类关键词 ----------
E_KEYWORDS_ZH = [
    # 核心玩法（仅保留游戏特有用语）
    '玩法', '战斗', '对战', '回合', '策略',
    '升级', '养成', '收集', '合成', '建造',
    '关卡', '地图', 'boss', 'BOSS',
    '数值', '属性', '伤害', '血量', '攻击', '防御', '冷却',
    '玩家', '奖励', '成就',
    # 游戏类型
    'rpg', 'slg', 'slots', 'casino', '博彩', '棋牌',
    '卡牌', '放置', '经营', '塔防', '射击', '动作',
    '休闲', '益智', '解谜', '竞速', '体育',
    '抽卡', '开箱', '扭蛋', '氪金', '付费',
    '副本', 'raid', 'pvp', 'pve', '组队',
    # 游戏资产
    '美术', '动画', '特效', '音效', '音乐',
    '模型', '贴图', '材质', 'shader',
    '技能', '天赋', '装备', '武器', '道具',
    '金币', '钻石', '体力', '能量',
]

E_KEYWORDS_EN = [
    'gameplay', 'combat', 'battle', 'strategy',
    'player', 'level', 'damage', 'health', 'mana',
    'reward', 'achievement', 'quest',
    'rpg', 'slg', 'slots', 'casino', 'puzzle',
    'boss', 'raid', 'pvp', 'pve',
    'loot', 'craft', 'upgrade', 'skill tree',
    'character', 'class', 'race', 'faction',
    'weapon', 'armor', 'item', 'inventory',
    'currency', 'gold', 'diamond', 'energy',
    'respawn', 'spawn', 'cooldown', 'buff', 'debuff',
]

# ---------- F (Knowledge Base): 知识库/归档类关键词 ----------
F_KEYWORDS_ZH = [
    # 知识/百科
    '知识', '百科', '文档', '资料', '信息', '数据',
    '参考', '手册', '指南', '规范', '标准', '协议',
    '历史', '背景', '来源', '起源', '发展', '演变',
    # 记录/归档
    '记录', '档案', '存储', '保存', '备份', '归档',
    '日志', '笔记', '摘要', '摘录', '收录',
    # 概念/理论
    '概念', '定义', '术语', '名词', '解释',
    '原理', '理论', '基础', '根本', '本质',
    '分类', '类型', '种类', '范畴', '领域',
    # 技术/方法
    '技术', '方法', '方法论', '流程', '框架',
    '架构', '模式', '模板', '范式',
    '最佳实践', '经验', '总结', '心得',
]

F_KEYWORDS_EN = [
    'knowledge', 'wiki', 'documentation', 'reference',
    'manual', 'guide', 'standard', 'specification',
    'history', 'background', 'origin', 'evolution',
    'archive', 'record', 'storage', 'backup',
    'concept', 'definition', 'terminology', 'glossary',
    'principle', 'theory', 'fundamental', 'essential',
    'taxonomy', 'classification', 'category',
    'methodology', 'framework', 'pattern', 'paradigm',
    'best practice', 'lesson', 'summary',
]

# ---------- G (Entertainment): 娱乐/梗/名场面类关键词 ----------
G_KEYWORDS_ZH = [
    # 搞笑/段子
    '搞笑', '好笑', '幽默', '段子', '笑话', '喜剧',
    '名场面', '经典', '梗', '玩梗', '吐槽', '翻车',
    '尴尬', '社死', '打脸', '真香', '啪啪打脸',
    # 名人
    '罗永浩', '雷军', '马云', '马化腾', '周鸿祎',
    # 反应
    '笑死', '笑喷', '笑哭', '笑出声',
    '哈哈哈', '哈哈哈哈', '笑到',
    # 鬼畜/二次创作
    '鬼畜', '魔性', '洗脑', '上头',
    '表情包', '截图', '素材',
    # 情绪
    '感动', '泪目', '暖心', '扎心', '崩溃',
    '上头', '上瘾', '停不下来',
]

G_KEYWORDS_EN = [
    'funny', 'hilarious', 'lol', 'lmao', 'rofl',
    'meme', 'classic', 'iconic', 'legendary',
    'awkward', 'cringe', 'embarrassing',
    'comedy', 'comic', 'satire', 'parody',
    'viral', 'trending', 'epic', 'fail',
]

# ---------- H (Traffic): 引流/传播性类关键词 ----------
H_KEYWORDS_ZH = [
    # 传播/热度
    '爆款', '热门', '火爆', '刷屏', '上热门',
    '流量', '引流', '涨粉', '吸粉', '圈粉',
    '关注', '订阅', '转发', '分享', '推荐',
    # 内容类型
    '短视频', '抖音', '快手', '小红书', '视频号',
    '直播', '带货', '开箱', '测评', '试吃',
    # 推荐算法
    '算法', '推荐', '推送', '曝光', '点击率',
    '完播率', '互动', '评论', '弹幕', '点赞',
    # 争议性
    '争议', '辩论', '吵架', '撕逼', '怼',
    '喷', '黑', '洗白', '反转', '神反转',
    # 抓眼球
    '震惊', '竟然', '居然', '万万没想到',
    '揭秘', '内幕', '真相', '别错过',
    '99%', '你一定', '必看', '收藏',
    # 受众
    '玩家', '观众', '粉丝', '网友', '大众',
    '围观', '吃瓜', '看热闹',
]

H_KEYWORDS_EN = [
    'viral', 'trending', 'popular', 'trend',
    'traffic', 'followers', 'subscribe', 'share',
    'controversy', 'debate', 'hot take',
    'shocking', 'surprising', 'crazy', 'insane',
    'must watch', 'don\'t miss', 'you won\'t believe',
    'challenge', 'reaction', 'review', 'unboxing',
    'short video', 'tiktok', 'reel', 'shorts',
]


def analyze_video_type(entries: list, meta: dict) -> dict:
    """
    八级分类分析：
      A (report)        — 仅出分析报告（必出）
      B (skill)         — 可以做出可复用的技能
      C (demo)          — 可以做出DEMO（小工具/小玩法/原型）
      D (tutorial)      — 可以部署为教程/学习资源
      E (gamedesign)    — 可以做成玩法文档/游戏设计案
      F (knowledgebase) — 可以归档做知识库
      G (entertainment) — 娱乐/梗/名场面/有梗价值
      H (traffic)       — 引流素材/能吸引流量

    优先级：C > B > E > G > H > F > D > A
    """
    # Build full text
    text_zh = ' '.join(e['content'] for e in entries)
    text_lower = text_zh.lower()
    total_words = len(text_zh)
    duration = meta.get('duration', 0)
    duration_min = duration / 60

    # ============================================================
    # B 类评分 (Skill) — 满分 100
    # ============================================================
    b_wf_count = 0
    b_wf_found = []
    for kw in B_KEYWORDS_ZH:
        cnt = text_zh.count(kw)
        if cnt > 0:
            b_wf_count += cnt
            b_wf_found.append((kw, cnt))
    for kw in B_KEYWORDS_EN:
        cnt = text_lower.count(kw)
        if cnt > 0:
            b_wf_count += cnt
            b_wf_found.append((kw, cnt))

    # B: Numbered steps
    b_steps = 0
    b_steps += len(re.findall(r'第[一二三四五六七八九十\d]+[步个]', text_zh))
    b_steps += len(re.findall(r'[Ss]tep\s*\d+', text_lower))
    b_steps += len(re.findall(r'^\d+[\.\)]\s', text_lower, re.MULTILINE))

    # B: Sub-scores
    b_wf_score = min(40, b_wf_count * 2)
    b_step_score = min(30, b_steps * 6)
    b_tech_boost = min(20, text_lower.count('skill') * 5 + text_lower.count('工具') * 3 + text_lower.count('automate') * 5)
    b_duration_score = 10 if 3 <= duration_min <= 30 else (5 if 1 <= duration_min <= 60 else 0)
    b_score_total = b_wf_score + b_step_score + b_tech_boost + b_duration_score

    b_wf_found.sort(key=lambda x: -x[1])

    # ============================================================
    # C 类评分 (Demo) — 满分 100
    # ============================================================
    c_imp_count = 0
    c_imp_found = []
    for kw in C_KEYWORDS_ZH:
        cnt = text_zh.count(kw)
        if cnt > 0:
            c_imp_count += cnt
            c_imp_found.append((kw, cnt))
    for kw in C_KEYWORDS_EN:
        cnt = text_lower.count(kw)
        if cnt > 0:
            c_imp_count += cnt
            c_imp_found.append((kw, cnt))

    # C: Tech boost (count overlapping tech terms)
    c_tech_count = 0
    c_tech_found = []
    for kw in TECH_BOOST:
        cnt = text_lower.count(kw)
        if cnt > 0:
            c_tech_count += cnt
            c_tech_found.append((kw, cnt))

    # C: Code/implementation density
    total_terms = max(1, len(entries))
    c_density = c_imp_count / total_terms

    # C: Sub-scores
    c_imp_score = min(50, c_imp_count * 2)
    c_tech_score = min(30, c_tech_count * 1.5)
    c_density_score = min(10, c_density * 20)
    c_duration_score = 10 if 1 <= duration_min <= 20 else (5 if 0.5 <= duration_min <= 60 else 0)
    c_score_total = c_imp_score + c_tech_score + c_density_score + c_duration_score

    c_imp_found.sort(key=lambda x: -x[1])
    c_tech_found.sort(key=lambda x: -x[1])

    # ============================================================
    # D 类评分 (Tutorial) — 满分 100
    # ============================================================
    d_edu_count = 0
    d_edu_found = []
    for kw in D_KEYWORDS_ZH:
        cnt = text_zh.count(kw)
        if cnt > 0:
            d_edu_count += cnt
            d_edu_found.append((kw, cnt))
    for kw in D_KEYWORDS_EN:
        cnt = text_lower.count(kw)
        if cnt > 0:
            d_edu_count += cnt
            d_edu_found.append((kw, cnt))

    # D: Explanation density (edu keywords per entry)
    d_density = d_edu_count / max(1, len(entries))

    # D: Structure indicators (总结, 首先, 总的来说, first, finally, etc.)
    d_structure = 0
    d_structure += len(re.findall(r'总结|归纳|回顾|总的来说|总而言之', text_zh))
    d_structure += len(re.findall(r'首先|其次|然后|最后|第一|第二|第三', text_zh))
    d_structure += len(re.findall(r'\bfirst\b|\bsecond\b|\bfinally\b|\boverall\b|\bsummary\b', text_lower))

    # D: Sub-scores
    d_edu_score = min(40, d_edu_count * 1.5)
    d_density_score = min(30, d_density * 30)
    d_structure_score = min(20, d_structure * 3)
    d_duration_score = 10 if 5 <= duration_min <= 45 else (5 if 2 <= duration_min <= 60 else 0)
    d_score_total = d_edu_score + d_density_score + d_structure_score + d_duration_score

    d_edu_found.sort(key=lambda x: -x[1])

    # ============================================================
    # E 类评分 (Game Design) — 满分 100
    # ============================================================
    e_game_count = 0
    e_game_found = []
    for kw in E_KEYWORDS_ZH:
        cnt = text_zh.count(kw)
        if cnt > 0:
            e_game_count += cnt
            e_game_found.append((kw, cnt))
    for kw in E_KEYWORDS_EN:
        cnt = text_lower.count(kw)
        if cnt > 0:
            e_game_count += cnt
            e_game_found.append((kw, cnt))

    # E: Keyword density
    e_density = e_game_count / max(1, len(entries))

    # E: Sub-scores
    e_game_score = min(50, e_game_count * 1.5)
    e_density_score = min(30, e_density * 25)
    e_duration_score = 20 if 3 <= duration_min <= 60 else (10 if 1 <= duration_min <= 120 else 0)
    e_score_total = e_game_score + e_density_score + e_duration_score

    e_game_found.sort(key=lambda x: -x[1])

    # ============================================================
    # F 类评分 (Knowledge Base) — 满分 100
    # ============================================================
    f_kb_count = 0
    f_kb_found = []
    for kw in F_KEYWORDS_ZH:
        cnt = text_zh.count(kw)
        if cnt > 0:
            f_kb_count += cnt
            f_kb_found.append((kw, cnt))
    for kw in F_KEYWORDS_EN:
        cnt = text_lower.count(kw)
        if cnt > 0:
            f_kb_count += cnt
            f_kb_found.append((kw, cnt))

    # F: Density
    f_density = f_kb_count / max(1, len(entries))

    # F: Sub-scores
    f_kb_score = min(50, f_kb_count * 1.5)
    f_density_score = min(30, f_density * 25)
    f_duration_score = 20 if 5 <= duration_min <= 120 else (10 if 2 <= duration_min <= 180 else 0)
    f_score_total = f_kb_score + f_density_score + f_duration_score

    f_kb_found.sort(key=lambda x: -x[1])

    # ============================================================
    # G 类评分 (Entertainment) — 满分 100
    # ============================================================
    g_ent_count = 0
    g_ent_found = []
    for kw in G_KEYWORDS_ZH:
        cnt = text_zh.count(kw)
        if cnt > 0:
            g_ent_count += cnt
            g_ent_found.append((kw, cnt))
    for kw in G_KEYWORDS_EN:
        cnt = text_lower.count(kw)
        if cnt > 0:
            g_ent_count += cnt
            g_ent_found.append((kw, cnt))

    # G: Short video bonus (snackable content = more entertaining)
    g_short_bonus = 20 if duration_min < 1 else (15 if duration_min < 2 else (10 if duration_min < 5 else 0))
    # G: Density
    g_density = g_ent_count / max(1, len(entries))
    # G: Sub-scores
    g_kw_score = min(40, g_ent_count * 3)
    g_density_score = min(25, g_density * 20)
    g_duration_score = min(35, g_short_bonus)
    g_score_total = g_kw_score + g_density_score + g_duration_score

    g_ent_found.sort(key=lambda x: -x[1])

    # ============================================================
    # H 类评分 (Traffic) — 满分 100
    # ============================================================
    h_traffic_count = 0
    h_traffic_found = []
    for kw in H_KEYWORDS_ZH:
        cnt = text_zh.count(kw)
        if cnt > 0:
            h_traffic_count += cnt
            h_traffic_found.append((kw, cnt))
    for kw in H_KEYWORDS_EN:
        cnt = text_lower.count(kw)
        if cnt > 0:
            h_traffic_count += cnt
            h_traffic_found.append((kw, cnt))

    # H: Cross-boost from entertainment (funny content drives traffic)
    h_ent_boost = min(15, g_score_total * 0.15)
    # H: Short duration (snackable = shareable)
    h_short_score = 10 if duration_min < 2 else (5 if duration_min < 5 else 0)
    # H: Sub-scores
    h_kw_score = min(50, h_traffic_count * 2)
    h_ent_boost_score = h_ent_boost
    h_duration_bonus = h_short_score
    h_score_total = h_kw_score + h_ent_boost_score + h_duration_bonus

    h_traffic_found.sort(key=lambda x: -x[1])

    # ============================================================
    # 最终判断 (优先级: C > B > E > G > H > F > D > A)
    # ============================================================
    # C 门槛：≥45 分且实现关键词不低于技术词（确保真的有实现内容）
    c_threshold = 45
    c_is_demo = c_score_total >= c_threshold and c_imp_count >= max(3, c_tech_count * 0.3)

    # B 门槛：≥45 分
    b_threshold = 45
    b_is_skill = b_score_total >= b_threshold

    # E 门槛：≥40 分
    e_threshold = 40
    e_is_gamedesign = e_score_total >= e_threshold

    # F 门槛：≥40 分
    f_threshold = 40
    f_is_kb = f_score_total >= f_threshold

    # G 门槛：≥35 分（娱乐类门槛稍低，因为不是刚需）
    g_threshold = 35
    g_is_entertainment = g_score_total >= g_threshold

    # H 门槛：≥40 分
    h_threshold = 40
    h_is_traffic = h_score_total >= h_threshold

    # D 门槛：≥45 分
    d_threshold = 45
    d_is_tutorial = d_score_total >= d_threshold

    # 优先级判断 (C > B > E > G > H > F > D > A)
    if c_is_demo:
        recommendation = "C"
        confidence = "high" if c_score_total >= 65 else "medium"
        primary_score = round(c_score_total, 1)
    elif b_is_skill:
        recommendation = "B"
        confidence = "high" if b_score_total >= 65 else "medium"
        primary_score = round(b_score_total, 1)
    elif e_is_gamedesign:
        recommendation = "E"
        confidence = "high" if e_score_total >= 65 else "medium"
        primary_score = round(e_score_total, 1)
    elif g_is_entertainment:
        recommendation = "G"
        confidence = "high" if g_score_total >= 65 else "medium"
        primary_score = round(g_score_total, 1)
    elif h_is_traffic:
        recommendation = "H"
        confidence = "high" if h_score_total >= 65 else "medium"
        primary_score = round(h_score_total, 1)
    elif f_is_kb:
        recommendation = "F"
        confidence = "high" if f_score_total >= 65 else "medium"
        primary_score = round(f_score_total, 1)
    elif d_is_tutorial:
        recommendation = "D"
        confidence = "high" if d_score_total >= 65 else "medium"
        primary_score = round(d_score_total, 1)
    else:
        recommendation = "A"
        confidence = "low"
        primary_score = max(round(b_score_total, 1), round(c_score_total, 1), round(d_score_total, 1),
                            round(e_score_total, 1), round(f_score_total, 1), round(g_score_total, 1),
                            round(h_score_total, 1))

    # Build label
    label_map = {
        "A": "A (REPORT)", "B": "B (SKILL)", "C": "C (DEMO)", "D": "D (TUTORIAL)",
        "E": "E (GAMEDESIGN)", "F": "F (KNOWLEDGE BASE)", "G": "G (ENTERTAINMENT)", "H": "H (TRAFFIC)"
    }
    score_label = label_map.get(recommendation, "A (REPORT)")

    report = {
        "recommendation": recommendation,
        "recommendation_label": score_label,
        "confidence": confidence,
        "score_detail": {
            "B_skill": {
                "score": round(b_score_total, 1),
                "breakdown": {
                    "workflow_keywords": round(b_wf_score, 1),
                    "numbered_steps": round(b_step_score, 1),
                    "tech_boost": round(b_tech_boost, 1),
                    "duration": b_duration_score,
                },
                "top_keywords": [k for k, _ in b_wf_found[:8]],
                "total_hits": b_wf_count,
                "step_count": b_steps,
            },
            "C_demo": {
                "score": round(c_score_total, 1),
                "breakdown": {
                    "implementation_keywords": round(c_imp_score, 1),
                    "technical_boost": round(c_tech_score, 1),
                    "keyword_density": round(c_density_score, 1),
                    "duration": c_duration_score,
                },
                "top_implementation": [k for k, _ in c_imp_found[:8]],
                "top_technical": [k for k, _ in c_tech_found[:6]],
                "total_hits": c_imp_count,
            },
            "D_tutorial": {
                "score": round(d_score_total, 1),
                "breakdown": {
                    "educational_keywords": round(d_edu_score, 1),
                    "explanation_density": round(d_density_score, 1),
                    "structure": round(d_structure_score, 1),
                    "duration": d_duration_score,
                },
                "top_keywords": [k for k, _ in d_edu_found[:8]],
                "total_hits": d_edu_count,
                "structure_count": d_structure,
            },
            "E_gamedesign": {
                "score": round(e_score_total, 1),
                "breakdown": {
                    "game_keywords": round(e_game_score, 1),
                    "density": round(e_density_score, 1),
                    "duration": e_duration_score,
                },
                "top_keywords": [k for k, _ in e_game_found[:8]],
                "total_hits": e_game_count,
            },
            "F_knowledgebase": {
                "score": round(f_score_total, 1),
                "breakdown": {
                    "knowledge_keywords": round(f_kb_score, 1),
                    "density": round(f_density_score, 1),
                    "duration": f_duration_score,
                },
                "top_keywords": [k for k, _ in f_kb_found[:8]],
                "total_hits": f_kb_count,
            },
            "G_entertainment": {
                "score": round(g_score_total, 1),
                "breakdown": {
                    "keywords": round(g_kw_score, 1),
                    "density": round(g_density_score, 1),
                    "short_bonus": g_short_bonus,
                },
                "top_keywords": [k for k, _ in g_ent_found[:8]],
                "total_hits": g_ent_count,
            },
            "H_traffic": {
                "score": round(h_score_total, 1),
                "breakdown": {
                    "keywords": round(h_kw_score, 1),
                    "ent_boost": round(h_ent_boost_score, 1),
                    "short_bonus": h_duration_bonus,
                },
                "top_keywords": [k for k, _ in h_traffic_found[:8]],
                "total_hits": h_traffic_count,
            },
        },
        "meta": {
            "platform": meta.get('platform', ''),
            "title": meta.get('title', ''),
            "author": meta.get('author', ''),
            "duration_seconds": duration,
            "subtitle_entries": len(entries),
            "total_words": total_words,
        },
    }

    return report


# ============================================================
# Bilibili
# ============================================================

class BilibiliExtractor:
    @staticmethod
    def extract_bvid(input_str: str) -> str:
        m = re.match(r'^(BV[a-zA-Z0-9]+)$', input_str.strip())
        if m:
            return m.group(1)
        m = re.search(r'(BV[a-zA-Z0-9]+)', input_str)
        if m:
            return m.group(1)
        raise ValueError(f"Cannot extract BV number from: {input_str}")

    @staticmethod
    def api_get(url: str, extra_headers: dict = None) -> dict:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.bilibili.com/',
        }
        if extra_headers:
            headers.update(extra_headers)
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode('utf-8'))

    def extract(self, input_str: str, args) -> tuple:
        """Returns (entries, meta_dict). entries = [{start, end, content}, ...]"""
        bvid = self.extract_bvid(input_str)

        # Get video info
        info = self.api_get(f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}')
        if info.get('code') != 0:
            raise RuntimeError(f"API error: {info.get('message', 'unknown')}")
        data = info['data']
        title = data.get('title', '')
        owner = data.get('owner', {}).get('name', '')
        duration = data.get('duration', 0)
        pages = data.get('pages', [])

        print(f"Platform: Bilibili", file=sys.stderr)
        print(f"BV: {bvid}", file=sys.stderr)
        print(f"Title: {title}", file=sys.stderr)
        print(f"UP: {owner}", file=sys.stderr)
        print(f"Duration: {duration}s", file=sys.stderr)

        # Find cid
        target_page = args.page
        if target_page > len(pages):
            print(f"Warning: Page {target_page} not found, using page 1", file=sys.stderr)
            target_page = 1
        cid = pages[target_page - 1]['cid']
        page_title = pages[target_page - 1].get('part', '')
        print(f"Page {target_page}: cid={cid} ({page_title})", file=sys.stderr)

        # Get subtitles
        extra_headers = {}
        if args.cookie:
            extra_headers['Cookie'] = args.cookie

        # Try player v2 API
        url1 = f'https://api.bilibili.com/x/player/v2?bvid={bvid}&cid={cid}'
        d1 = self.api_get(url1, extra_headers)
        subs = d1.get('data', {}).get('subtitle', {}).get('list', [])

        # Fallback: dm view API
        if not subs:
            url2 = f'https://api.bilibili.com/x/v2/dm/view?oid={cid}&type=1'
            d2 = self.api_get(url2, extra_headers)
            subs = d2.get('data', {}).get('subtitle', {}).get('subtitles', [])

        if not subs:
            print("No subtitles found.", file=sys.stderr)
            raise RuntimeError(
                "No subtitles found. Possible reasons:\n"
                "  1. Video has no AI/CC subtitles\n"
                "  2. Video requires login (use --cookie)\n"
                "  3. Use --trigger-ai to auto-enable AI subtitles via browser"
            )

        print(f"Found {len(subs)} subtitle(s)", file=sys.stderr)
        for s in subs:
            print(f"  - {s.get('lan', '?')}: {s.get('lan_doc', '')}", file=sys.stderr)

        # Prefer Chinese AI subtitle
        chosen = None
        for s in subs:
            if s.get('lan') == 'ai-zh':
                chosen = s
                break
        if not chosen:
            chosen = subs[0]

        sub_url = chosen.get('subtitle_url', '')
        if sub_url.startswith('//'):
            sub_url = 'https:' + sub_url
        if sub_url.startswith('http://'):
            sub_url = 'https://' + sub_url[7:]

        print(f"Downloading subtitle...", file=sys.stderr)
        sub_data = self.api_get(sub_url)
        body = sub_data.get('body', [])

        entries = []
        for item in body:
            entries.append({
                'start': item.get('from', 0),
                'end': item.get('to', 0),
                'content': item.get('content', ''),
            })

        meta = {
            'platform': 'bilibili',
            'title': title,
            'author': owner,
            'duration': duration,
            'bvid': bvid,
            'language': chosen.get('lan_doc', ''),
        }
        return entries, meta


# ============================================================
# YouTube
# ============================================================

class YouTubeExtractor:
    def extract(self, input_str: str, args) -> tuple:
        """Returns (entries, meta_dict)."""
        video_id = self._extract_video_id(input_str)

        try:
            from youtube_transcript_api import YouTubeTranscriptApi
        except ImportError:
            raise RuntimeError(
                "youtube-transcript-api is not installed.\n"
                "Run: pip install youtube-transcript-api"
            )

        # Determine languages
        languages = None
        if args.lang:
            languages = [args.lang]
        else:
            languages = ['zh-Hans', 'zh-Hant', 'zh', 'en']

        ytt_api = YouTubeTranscriptApi()

        # List available transcripts
        try:
            transcript_list = ytt_api.list(video_id)
            print(f"Platform: YouTube", file=sys.stderr)
            print(f"Video ID: {video_id}", file=sys.stderr)

            # Show available transcripts
            print("Available subtitles:", file=sys.stderr)
            for t in transcript_list:
                tag = " [AI]" if t.is_generated else " [CC]"
                translatable = " (translatable)" if t.is_translatable else ""
                print(f"  - {t.language_code}: {t.language}{tag}{translatable}", file=sys.stderr)

            # Find matching transcript
            transcript = transcript_list.find_transcript(languages)
        except Exception as e:
            # Fallback: try fetch directly
            print(f"List failed ({e}), trying direct fetch...", file=sys.stderr)
            try:
                transcript_data = ytt_api.fetch(video_id, languages=languages)
                entries = []
                for snippet in transcript_data:
                    entries.append({
                        'start': snippet.start,
                        'end': snippet.start + snippet.duration,
                        'content': snippet.text,
                    })
                print(f"Got {len(entries)} entries", file=sys.stderr)
                meta = {
                    'platform': 'youtube',
                    'title': '',
                    'author': '',
                    'video_id': video_id,
                    'language': getattr(transcript_data, 'language', ''),
                }
                return entries, meta
            except Exception as e2:
                raise RuntimeError(
                    f"Failed to get YouTube transcript: {e2}\n"
                    f"  Try: --lang en  or  --lang zh-Hans"
                )

        print(f"Using: {transcript.language} ({transcript.language_code})", file=sys.stderr)

        # Fetch
        fetched = transcript.fetch()
        entries = []
        for snippet in fetched:
            entries.append({
                'start': snippet.start,
                'end': snippet.start + snippet.duration,
                'content': snippet.text,
            })

        print(f"Got {len(entries)} entries", file=sys.stderr)

        meta = {
            'platform': 'youtube',
            'title': '',
            'author': '',
            'video_id': video_id,
            'language': f"{transcript.language} ({transcript.language_code})",
        }

        return entries, meta

    @staticmethod
    def _extract_video_id(input_str: str) -> str:
        """Extract YouTube video ID from URL or raw ID."""
        s = input_str.strip()
        # Direct video ID (11 chars)
        if re.match(r'^[a-zA-Z0-9_-]{11}$', s):
            return s
        # Standard URL
        m = re.search(r'[?&]v=([a-zA-Z0-9_-]{11})', s)
        if m:
            return m.group(1)
        # Short URL
        m = re.search(r'youtu\.be/([a-zA-Z0-9_-]{11})', s)
        if m:
            return m.group(1)
        # Embed URL
        m = re.search(r'embed/([a-zA-Z0-9_-]{11})', s)
        if m:
            return m.group(1)
        raise ValueError(f"Cannot extract YouTube video ID from: {input_str}")


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description='Extract subtitles from Bilibili and YouTube videos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Bilibili
  python video_subtitle.py BV12ZDuBwEhX
  python video_subtitle.py https://www.bilibili.com/video/BV12ZDuBwEhX/
  python video_subtitle.py BV12ZDuBwEhX --srt -o subs.srt

  # YouTube
  python video_subtitle.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
  python video_subtitle.py dQw4w9WgXcQ
  python video_subtitle.py https://youtu.be/dQw4w9WgXcQ --lang zh-Hans

Output formats:
  default   Plain text with timestamps: [00:01 - 00:05] Hello world
  srt       SRT subtitle format
  vtt       WebVTT subtitle format
  json      JSON with readable timestamps
  raw       Raw JSON (start/end as seconds)
  text-only Text only, no timestamps
        """)

    parser.add_argument('input', help='Video URL or ID (BV number / YouTube video ID / full URL)')
    parser.add_argument('--output', '-o', help='Output file path (default: stdout)')
    parser.add_argument('--format', '-f', default='default',
                        choices=['default', 'srt', 'vtt', 'json', 'raw', 'text-only'],
                        help='Output format (default: plain text with timestamps)')
    parser.add_argument('--lang', '-l', help='Preferred language code (YouTube only, e.g. zh-Hans, en, ja)')
    parser.add_argument('--page', '-p', type=int, default=1, help='Page number for multi-part Bilibili videos (default: 1)')
    parser.add_argument('--cookie', type=str, default='', help='Cookie string for login-required videos')
    parser.add_argument('--asr', action='store_true',
                        help='Fallback to Whisper ASR when no subtitles found (downloads audio + transcribes)')
    parser.add_argument('--asr-model', default='base',
                        choices=['tiny', 'base', 'small', 'medium', 'large-v3'],
                        help='Whisper model for ASR fallback (default: base)')
    parser.add_argument('--asr-lang', default=None,
                        help='Language hint for ASR (e.g. zh, en, ja). Auto-detect if not set.')

    # ======== Vision Mode (expensive, uses visual AI) ========
    parser.add_argument('--vision', '-V', action='store_true',
                        help='[VISION MODE] Extract key frames for AI visual analysis (uses LLM tokens per frame)')
    parser.add_argument('--vision-dir', type=str, default='',
                        help='Output directory for extracted frames (default: auto temp dir)')
    parser.add_argument('--vision-max-frames', type=int, default=0,
                        help='Max key frames (default: auto-calculate from video duration, or 0 for auto)')

    # ======== Skill Report ========
    parser.add_argument('--skill-report', '-R', action='store_true',
                        help='Generate skill feasibility report: analyze if video content can be turned into a reusable skill')

    args = parser.parse_args()

    try:
        # Auto-detect platform
        platform = detect_platform(args.input)
        print(f"Detected platform: {platform}", file=sys.stderr)

        entries = None
        meta = {}

        # ======== Web Page Mode ========
        # If platform is 'web', use web_analyzer instead of video extraction
        if platform == 'web':
            print(f"Platform: Web Page", file=sys.stderr)
            web_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web_analyzer.py')
            web_cmd = [
                sys.executable, web_script, args.input,
                '-f', 'json',
            ]
            web_result = subprocess.run(web_cmd, capture_output=True, text=True, timeout=30)

            if web_result.returncode == 0:
                try:
                    web_entries = json.loads(web_result.stdout.strip())
                    entries = []
                    for item in web_entries:
                        entries.append({
                            'start': 0,
                            'end': 0,
                            'content': item.get('content', ''),
                        })
                    meta = {
                        'platform': 'web',
                        'title': args.input,
                        'author': '',
                        'duration': 0,
                    }
                    print(f"Extracted {len(entries)} paragraphs from web page", file=sys.stderr)
                except json.JSONDecodeError:
                    print("Warning: Could not parse web content as JSON", file=sys.stderr)
            else:
                print(f"Web analysis failed: {web_result.stderr[-200:]}", file=sys.stderr)
                sys.exit(1)

        # Step 1: Try API subtitle extraction (video platforms only) / skip for web
        if platform == 'web':
            pass  # Already handled above
        else:
            try:
                if platform == 'bilibili':
                    extractor = BilibiliExtractor()
                elif platform == 'youtube':
                    extractor = YouTubeExtractor()
                else:
                    raise ValueError(f"Unsupported platform: {platform}")

                entries, meta = extractor.extract(args.input, args)

            except RuntimeError as e:
                if 'No subtitles found' in str(e) or 'Subtitles are disabled' in str(e) or 'TranscriptsDisabled' in str(e):
                    print(f"\nNo subtitles available via API.", file=sys.stderr)
                    if args.asr:
                        print("Falling back to Whisper ASR...", file=sys.stderr)
                    else:
                        print("Tip: Add --asr to fallback to Whisper speech recognition.", file=sys.stderr)
                        sys.exit(1)
                else:
                    raise

        # Step 2: If no entries and --asr enabled, use Whisper
        if not entries:
            if args.asr:
                print("Falling back to Whisper ASR...", file=sys.stderr)
            else:
                print("No subtitle entries found.", file=sys.stderr)
                print("Tip: Add --asr to fallback to Whisper speech recognition.", file=sys.stderr)
                sys.exit(1)

        if entries:
            output_result(entries, args, meta)

            # ======== Skill Report (runs after subtitle extraction) ========
            if args.skill_report:
                report = analyze_video_type(entries, meta)
                
                print("\n" + "="*60, file=sys.stderr)
                print("  分析完成，以下是我的建议：", file=sys.stderr)
                print("="*60, file=sys.stderr)
                
                rec = report['recommendation']
                emoji = {"C": "🎮", "B": "⚙️", "E": "📝", "G": "😂", "H": "🔥", "F": "🗂", "D": "📚", "A": "💬"}
                label = {"C": "DEMO", "B": "技能", "E": "玩法文档", "G": "娱乐梗", "H": "引流素材", "F": "知识库", "D": "教程", "A": "报告"}
                desc = {
                    "C": "这个内容有实现细节，可以做一个交互原型出来",
                    "B": "这个内容有完整的工作流/方法，可以做成可复用的Skill",
                    "E": "这个内容有游戏机制/系统设计结构，可以输出玩法文档",
                    "G": "这个内容有趣/有梗，适合做娱乐向输出",
                    "H": "这个内容有流量潜力，可以做成引流素材",
                    "F": "这个内容有知识/参考价值，可以归档到知识库",
                    "D": "这个内容有教育结构，可以部署为教程",
                    "A": "这个内容不适合做技能/DEMO/教程等，仅输出分析报告",
                }
                
                print(f"  {emoji[rec]} 推荐方向：{label[rec]}", file=sys.stderr)
                print(f"  {desc.get(rec, '')}", file=sys.stderr)
                print(f"\n  当然也可以选择其他方向：", file=sys.stderr)
                print(f"  🎮 C(DEMO)  ⚙️ B(技能)  📝 E(玩法文档)  😂 G(娱乐梗)", file=sys.stderr)
                print(f"  🔥 H(引流)  🗂 F(知识库)  📚 D(教程)  💬 A(报告)", file=sys.stderr)
                print(f"\n  告诉我想做哪个方向，我来执行。", file=sys.stderr)

                # Output full JSON to stdout
                print(json.dumps(report, ensure_ascii=False, indent=2))

        elif args.asr:
            # Import and run ASR module
            asr_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'video_asr.py')

            # Use temp file for JSON output (avoids progress/JSON mix in stdout)
            import tempfile
            tmp_json = tempfile.NamedTemporaryFile(
                mode='w', suffix='.json', delete=False, encoding='utf-8'
            )
            tmp_json_path = tmp_json.name
            tmp_json.close()

            try:
                cmd = [
                    sys.executable, asr_script, args.input,
                    '-f', 'json', '-o', tmp_json_path,
                    '--model', args.asr_model,
                ]
                if args.asr_lang:
                    cmd.extend(['--lang', args.asr_lang])
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

                if result.returncode != 0:
                    print(result.stderr, file=sys.stderr)
                    sys.exit(result.returncode)

                # Read JSON from temp file
                asr_entries = None
                with open(tmp_json_path, 'r', encoding='utf-8') as f:
                    asr_entries = json.load(f)

                if asr_entries:
                    # Re-format and output
                    class AsrArgs:
                        format = args.format
                        output = args.output
                    output_result(asr_entries, AsrArgs())

                    # Skill report on ASR entries
                    if args.skill_report:
                        asr_meta = {
                            'platform': detect_platform(args.input),
                            'title': '',
                            'author': '',
                            'duration': 0,
                        }
                        report = analyze_video_type(asr_entries, asr_meta)
                        print("\n" + "="*60, file=sys.stderr)
                        print("  分析完成，以下是我的建议：", file=sys.stderr)
                        print("="*60, file=sys.stderr)
                        
                        rec = report['recommendation']
                        emoji = {"C": "🎮", "B": "⚙️", "E": "📝", "G": "😂", "H": "🔥", "F": "🗂", "D": "📚", "A": "💬"}
                        label = {"C": "DEMO", "B": "技能", "E": "玩法文档", "G": "娱乐梗", "H": "引流素材", "F": "知识库", "D": "教程", "A": "报告"}
                        desc = {
                            "C": "这个内容有实现细节，可以做一个交互原型出来",
                            "B": "这个内容有完整的工作流/方法，可以做成可复用的Skill",
                            "E": "这个内容有游戏机制/系统设计结构，可以输出玩法文档",
                            "G": "这个内容有趣/有梗，适合做娱乐向输出",
                            "H": "这个内容有流量潜力，可以做成引流素材",
                            "F": "这个内容有知识/参考价值，可以归档到知识库",
                            "D": "这个内容有教育结构，可以部署为教程",
                            "A": "这个内容不适合做技能/DEMO/教程等，仅输出分析报告",
                        }
                        
                        print(f"  {emoji[rec]} 推荐方向：{label[rec]}", file=sys.stderr)
                        print(f"  {desc.get(rec, '')}", file=sys.stderr)
                        print(f"\n  当然也可以选择其他方向：", file=sys.stderr)
                        print(f"  🎮 C(DEMO)  ⚙️ B(技能)  📝 E(玩法文档)  😂 G(娱乐梗)", file=sys.stderr)
                        print(f"  🔥 H(引流)  🗂 F(知识库)  📚 D(教程)  💬 A(报告)", file=sys.stderr)
                        print(f"\n  告诉我想做哪个方向，我来执行。", file=sys.stderr)
                        print(f"  你可以选择执行：B技能/C演示/D教程/E玩法文档/F知识库/G娱乐梗/H引流素材", file=sys.stderr)
                        print(json.dumps(report, ensure_ascii=False, indent=2))
                else:
                    print("Error: ASR produced no output", file=sys.stderr)
                    sys.exit(1)

            finally:
                if os.path.exists(tmp_json_path):
                    os.unlink(tmp_json_path)

        # ======== Vision Mode ========
        # Runs AFTER subtitle extraction. Extracts key frames for AI visual analysis.
        if args.vision:
            print("\n" + "="*60, file=sys.stderr)
            print("[VISION MODE] Extracting key frames for visual analysis...", file=sys.stderr)
            print("="*60, file=sys.stderr)
            if args.vision_max_frames > 0:
                print(f"Frame limit: {args.vision_max_frames} (use --vision-max-frames N to adjust)", file=sys.stderr)
            else:
                print("Frame count: auto (based on video duration)", file=sys.stderr)
            
            # Vision mode needs yt-dlp and Pillow. Use the current Python by
            # default; allow callers to override it without hardcoding a local path.
            python_path = os.environ.get('AI_DAILIAN_PYTHON') or sys.executable
            if not os.path.exists(python_path):
                python_path = sys.executable

            vision_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'video_vision.py')
            vision_cmd = [
                python_path, vision_script, args.input,
            ]
            
            if args.vision_max_frames > 0:
                vision_cmd.extend(['--max-frames', str(args.vision_max_frames)])
            
            if args.vision_dir:
                vision_cmd.extend(['--output-dir', args.vision_dir])
            
            vision_result = subprocess.run(vision_cmd, capture_output=True, text=True, timeout=600)
            
            if vision_result.returncode == 0:
                # Print vision script's progress logs first
                if vision_result.stderr:
                    for line in vision_result.stderr.split('\n'):
                        line = line.strip()
                        if line:
                            print(f"  {line}", file=sys.stderr)
                
                # Parse the JSON output from video_vision.py (last block after ---)
                stdout_output = vision_result.stdout
                if '---' in stdout_output:
                    json_part = stdout_output.split('---')[-1].strip()
                    try:
                        vision_data = json.loads(json_part)
                        total_mb = vision_data.get('total_size_mb', 0)
                        total_frames = vision_data.get('total_frames', 0)
                        
                        print(f"\n{'='*60}", file=sys.stderr)
                        print(f"[VISION READY]", file=sys.stderr)
                        print(f"{'='*60}", file=sys.stderr)
                        print(f"  Frames:        {total_frames} 张", file=sys.stderr)
                        print(f"  Disk size:     {total_mb:.1f} MB", file=sys.stderr)
                        print(f"  Output dir:    {vision_data.get('output_dir', '?')}", file=sys.stderr)
                        print(f"  Contact sheet: {vision_data.get('contact_sheet', 'N/A')}", file=sys.stderr)
                        print(f"{'='*60}", file=sys.stderr)
                        print(f"  ⚠ 这些文件不会被自动删除。看完后手动删掉以释放空间。", file=sys.stderr)
                        print(f"{'='*60}", file=sys.stderr)
                    except json.JSONDecodeError:
                        print("Warning: Could not parse vision output JSON", file=sys.stderr)
                else:
                    print(vision_result.stdout, file=sys.stderr)
            else:
                print(f"Vision extraction failed (exit {vision_result.returncode})", file=sys.stderr)
                if vision_result.stderr:
                    print(vision_result.stderr[-500:], file=sys.stderr)

    except Exception as e:
        import traceback
        print(f"Error: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
