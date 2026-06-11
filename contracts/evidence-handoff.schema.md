# gg-dailian 证据交接合约

跨技能与跨模块的统一证据分层 schema。下游消费者可通过该合约消费上游产出的证据索引，无需重做源采集。

## 证据索引条目

```json
{
  "evidence_id": "E001",
  "source_id": "video_01",
  "source_type": "video_file | video_url | screenshot | web_page | local_audio | user_text | user_context",
  "timestamp": "00:03:15.000",
  "time_range": "00:03:10-00:03:25",
  "frame_id": "F045",
  "image_id": null,
  "region": "top-right HUD",
  "visible_text": "Claim reward",
  "observed_fact": "玩家点击胜利结算后立即出现双倍奖励按钮",
  "event_type": "reward_claim | hook_peak | feature_exposure | feature_unlock | first_use | failure_signal | confusion_signal | monetization_prompt | decision_point | shareable_moment | control_release | loop_closure | access_blocked",
  "supports_judgment": "商业化打断发生在首轮胜利反馈之前",
  "confidence": 0.88,
  "uncertainty_note": "",
  "extraction_method": "frame_sample | ocr | page_metadata | direct_observation | user_provided"
}
```

## 来源锚点

```json
{
  "source_type": "video_url | local_file | web_page | screenshot | text",
  "analysis_date": "2026-06-10",
  "title": "原始标题或文件名",
  "url": "https://... 或 本地文件，无公开 URL",
  "creator": "作者/UP主 或 unknown",
  "duration": "201s 或 null",
  "evidence_level": "完整正文/字幕确认 | 元信息确认 | 页面可见内容判断 | 封面/关键帧判断 | 文件名/URL弱线索",
  "access_notes": "可访问 | 需登录 | 平台限制 | 已下架"
}
```

## 价值判断卡

```json
{
  "value_type": "method | learning | case | expression | visual | production | knowledge | entertainment",
  "value_summary": "一句话核心价值",
  "target_audience": ["游戏设计师", "独立开发者"],
  "recommended_artifact": "SOP | 教程 | 展示页 | 知识笔记 | 模板集 | 对比表",
  "threshold_judgment": "pass | thin | stop",
  "next_step": "建议下一步动作"
}
```
