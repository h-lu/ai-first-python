#!/usr/bin/env python3
"""
LLM 简答题评分脚本
"""

import os
import json
import argparse
import requests
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def read_file(path):
    if os.path.exists(path):
        return open(path, "r", encoding="utf-8").read()
    return ""


def read_file_or_string(value):
    if os.path.exists(value):
        return open(value, "r", encoding="utf-8").read()
    return value


PROMPT_TEMPLATE = """你是严格且一致的助教，按提供的评分量表为学生的简答题评分。

评分规则：
- 严格依据量表中各评分项的 scoring_guide 进行评分
- 每个评分项只能给出 scoring_guide 中定义的整数分值（如 0, 1, 2, 3, 4）
- 不输出任何解释性文本；只输出 JSON

输出格式：
  {{
  "total": number (各项分数之和),
    "criteria": [
    {{"id": "评分项id", "score": 整数(必须是scoring_guide中定义的分值), "reason": "简短评语"}},
    ...
    ],
    "flags": [],
  "confidence": number(0-1, 评分置信度)
  }}

重要：
- score 必须是整数，只能是 scoring_guide 中定义的分值（如 0/1/2/3/4）
- 不要给出 2.5, 3.5 这样的中间值
- total 必须等于所有 criteria 的 score 之和
- 如果答案与题目无关或为空，total=0，并加 flag "need_review"

【题目】
<<<{question}>>>

【评分量表】
<<<{rubric}>>>

【学生答案】
<<<{answer}>>>
"""


def call_llm(url, key, model, prompt):
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "temperature": 0,
        "top_p": 1,
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"},
    }
    response = requests.post(url, headers=headers, json=data, timeout=(10, 60))
    response.raise_for_status()
    result = response.json()
    content = result.get("choices", [{}])[0].get("message", {}).get("content", "{}")
    return json.loads(content)


def main():
    parser = argparse.ArgumentParser(description="Grade short answer questions using LLM")
    parser.add_argument("--question", required=True, help="Path to question file")
    parser.add_argument("--answer", required=True, help="Path to answer file")
    parser.add_argument("--rubric", required=True, help="Path to rubric JSON file")
    parser.add_argument("--out", default="grade.json", help="Output JSON file")
    parser.add_argument("--summary", default="summary.md", help="Output summary markdown file")
    parser.add_argument("--model", default=os.getenv("LLM_MODEL", "deepseek-chat"))
    parser.add_argument("--api_url", default=os.getenv("LLM_API_URL", "https://api.deepseek.com/chat/completions"))
    parser.add_argument("--api_key", default=os.getenv("LLM_API_KEY", ""))
    args = parser.parse_args()

    if not args.api_key:
        print("Warning: LLM_API_KEY not set. LLM grading may fail.", file=sys.stderr)

    question = read_file_or_string(args.question).strip()
    answer = read_file(args.answer).strip()
    rubric_text = read_file(args.rubric).strip()

    if not question or not answer:
        resp = {
            "total": 0,
            "criteria": [],
            "flags": ["need_review", "empty_answer"],
            "confidence": 0.0,
        }
    else:
        try:
            prompt = PROMPT_TEMPLATE.format(question=question, rubric=rubric_text, answer=answer)
            resp = call_llm(args.api_url, args.api_key, args.model, prompt)
        except Exception as e:
            print(f"LLM grading failed: {e}", file=sys.stderr)
            resp = {
                "total": 0,
                "criteria": [],
                "flags": ["need_review", "llm_error"],
                "confidence": 0.0,
            }

    criteria = resp.get("criteria", [])
    if criteria:
        for c in criteria:
            c["score"] = round(float(c.get("score", 0)))
        resp["total"] = sum(c.get("score", 0) for c in criteria)

    try:
        rubric_data = json.loads(rubric_text)
        lo, hi = rubric_data.get("borderline_band", [None, None])
        total = float(resp.get("total", 0))
        flags = set(resp.get("flags", []))
        if lo is not None and hi is not None and lo <= total <= hi:
            flags.add("need_review")
        confidence = resp.get("confidence", 1.0)
        if confidence < 0.7:
            flags.add("need_review")
        resp["flags"] = sorted(list(flags))
    except Exception:
        pass

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(resp, f, ensure_ascii=False, indent=2)

    try:
        rubric_data = json.loads(rubric_text)
        max_score = rubric_data.get("max_score", 10)
    except Exception:
        max_score = 10

    lines = [
        "# 简答题评分",
        f"- **总分**：**{resp.get('total', 0):.2f} / {max_score}**",
        f"- **置信度**：{resp.get('confidence', 0):.2f}",
        f"- **标记**：{', '.join(resp.get('flags', [])) or '无'}",
        "",
        "## 分项评分",
    ]
    for criterion in resp.get("criteria", []):
        criterion_id = criterion.get("id", "")
        score = criterion.get("score", 0)
        reason = criterion.get("reason", "")
        lines.append(f"- **{criterion_id}**: {score} 分")
        if reason:
            lines.append(f"  - {reason}")

    with open(args.summary, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"LLM grading complete: {resp.get('total', 0):.2f}/{max_score}")


if __name__ == "__main__":
    main()

