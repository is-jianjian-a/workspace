#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
classify_batch_044.py
读取 batch_044.json，从 all_classification_results_v3.json 中提取对应的分类结果，
输出 result_batch_044.json 到 batches 目录。
"""

import json
import os


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(base_dir)

    batch_path = os.path.join(base_dir, "batch_044.json")
    results_path = os.path.join(parent_dir, "all_classification_results_v3.json")
    output_path = os.path.join(base_dir, "result_batch_044.json")

    # 读取 batch_044.json
    with open(batch_path, "r", encoding="utf-8") as f:
        batch_data = json.load(f)

    batch_ids = {u["id"] for u in batch_data["ugcs"]}
    print(f"Batch 044 UGC count: {len(batch_ids)}")

    # 读取 all_classification_results_v3.json
    with open(results_path, "r", encoding="utf-8") as f:
        all_results = json.load(f)

    # 提取 batch_044 对应的分类结果
    batch_results = [r for r in all_results if r["id"] in batch_ids]
    print(f"Found classified records: {len(batch_results)}")

    # 按 batch_044 中的顺序排列
    id_to_result = {r["id"]: r for r in batch_results}
    ordered_results = []
    for ugc in batch_data["ugcs"]:
        if ugc["id"] in id_to_result:
            ordered_results.append(id_to_result[ugc["id"]])
        else:
            print(f"Warning: ID {ugc['id']} not found in classification results")

    # 写入结果
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(ordered_results, f, ensure_ascii=False, indent=2)

    print(f"Result written to: {output_path}")
    print(f"Total records in result: {len(ordered_results)}")

    # 打印分类统计
    from collections import Counter
    l1_counter = Counter()
    for r in ordered_results:
        for l1 in r.get("layer1", []):
            l1_counter[l1] += 1

    print("\nLayer1 distribution:")
    for k, v in l1_counter.most_common():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
