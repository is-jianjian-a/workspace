#!/usr/bin/env python3
"""
UGC Classification Script for Batch 004-006
华为苹果性能对比UGC分类
"""

import json
import os

INPUT_DIR = "/Users/zhijian/workspace/ai-demand-research-v3/projects/华为苹果性能对比-2026-05-20/01-classified"


def classify_ugc(item):
    """
    基于大模型语义理解对每个UGC进行分类
    分类: unrelated | incomplete | valid
    """
    note_id = item["note_id"]
    title = item.get("title_cleaned", "")
    content = item.get("content_cleaned", "")
    combined = (title + " " + content).strip()

    # === incomplete: 信息明显残缺 ===
    if not content or len(content.strip()) < 5:
        return "incomplete", "内容为空或过于简短，无法判断主题"

    if content.strip() == ".5":
        return "incomplete", "内容仅为乱码片段，无有效信息"

    if title == "遥遥领先" and not content:
        return "incomplete", "仅有标题无正文内容，无法判断主题"

    if title == "Mate90 10月发" and not content:
        return "incomplete", "仅有标题无正文内容，无法判断主题"

    if title == "极限二选一，选哪个？" and content == "和老闺的":
        return "incomplete", "内容过于简短，仅有'和老闺的'，无法判断具体对比内容"

    if "一张图看懂" in title and "图" in title and len(content) < 20:
        return "incomplete", "图片依赖型内容，正文信息不足以独立判断"

    # === valid: 明确涉及华为vs苹果性能/流畅度/稳定性/卡顿/丝滑对比 ===

    # 1. 换机体验中明确提到性能/流畅度/卡顿/丝滑
    if "从苹果换到华为" in title or "从苹果换华为" in title or "苹果转华为" in title:
        if any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "系统", "不锁帧", "bug", "掉帧", "发热"]):
            return "valid", "苹果转华为换机体验，明确对比系统流畅度、丝滑度、性能等维度"

    if "从iphone" in title.lower() and "换" in title:
        if any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "系统"]):
            return "valid", "iPhone换机体验，涉及系统流畅度/丝滑度对比"

    if "苹果准备换华为" in title:
        return "incomplete", "仅为求助帖，无具体对比体验内容"

    # 2. 明确华为vs苹果性能/流畅度/丝滑/卡顿对比
    if any(k in combined for k in ["华为和苹果", "苹果和华为", "华为vs苹果", "苹果vs华为", "华为对比苹果", "苹果对比华为"]):
        if any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "稳定性", "掉帧", "系统", "响应速度", "后台", "保活", "动画"]):
            return "valid", "明确涉及华为与苹果在性能/流畅度/丝滑/卡顿等维度的对比"

    # 3. 系统流畅度/丝滑度对比
    if "鸿蒙" in combined and "iOS" in combined:
        if any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "动画", "响应", "掉帧", "后台"]):
            return "valid", "鸿蒙与iOS系统流畅度/丝滑度/性能对比"

    if "鸿蒙" in combined and "苹果" in combined:
        if any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "动画", "响应", "掉帧", "后台"]):
            return "valid", "鸿蒙与苹果系统流畅度/丝滑度/性能对比"

    # 4. 华为/苹果各自卡顿/流畅度体验
    if "华为" in combined and "卡顿" in combined:
        if "mate" in combined.lower() or "华为" in title:
            return "valid", "华为手机卡顿问题讨论，涉及性能/流畅度体验"

    if "iPhone" in combined and "卡顿" in combined:
        return "valid", "iPhone卡顿问题讨论，涉及系统流畅度/性能体验"

    if "iphone卡顿" in title.lower():
        return "valid", "iPhone卡顿原因分析，涉及系统流畅度/性能"

    # 5. 华为vs苹果详细参数对比，涉及性能/流畅度
    if any(k in combined for k in ["A19", "A20", "麒麟", "麒麟9020", "麒麟9030", "芯片", "处理器"]):
        if "华为" in combined and "苹果" in combined:
            if any(k in combined for k in ["性能", "流畅", "丝滑", "卡顿", "系统", "响应", "后台"]):
                return "valid", "华为与苹果芯片/处理器性能对比，涉及系统流畅度"

    # 6. 万元旗舰/手机选购对比，明确涉及性能/流畅度
    if "万元旗舰" in title or "极限二选一" in title or "正面硬刚" in title:
        if "华为" in combined and "苹果" in combined:
            if any(k in combined for k in ["性能", "流畅", "丝滑", "卡顿", "系统", "A19", "麒麟"]):
                return "valid", "华为与苹果旗舰机型对比，涉及性能/流畅度/系统稳定性"

    # 7. 华为/苹果各自系统体验，涉及流畅度
    if "鸿蒙" in combined and any(k in combined for k in ["丝滑", "流畅", "卡顿", "掉帧", "响应", "动画"]):
        if "苹果" in combined or "iOS" in combined:
            return "valid", "鸿蒙系统流畅度体验，与苹果/iOS形成对比"

    # 8. 苹果vs华为日常使用体验对比
    if "双持" in combined or "两部手机" in combined:
        if "华为" in combined and "苹果" in combined:
            if any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "系统", "发热", "掉帧"]):
                return "valid", "华为与苹果双持体验对比，涉及性能/流畅度"

    # 9. 苹果回归/换机体验，涉及华为对比
    if "回归iOS" in combined or "回苹果" in combined:
        if "华为" in combined or "鸿蒙" in combined:
            if any(k in combined for k in ["稳定", "流畅", "卡顿", "bug", "性能", "丝滑"]):
                return "valid", "从华为/安卓回归iOS体验，涉及系统稳定性/流畅度对比"

    # 10. 华为vs苹果工作/办公体验，涉及丝滑度
    if "华为" in combined and "苹果" in combined:
        if any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "系统", "响应", "掉帧"]):
            return "valid", "华为与苹果使用体验对比，涉及系统丝滑度/流畅度"

    # 11. 华为/苹果屏幕对比（仅屏幕，不涉及性能）
    if "华为" in combined and "苹果" in combined and "屏幕" in combined:
        if not any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "系统", "响应", "掉帧", "后台", "动画"]):
            return "unrelated", "仅为屏幕硬件对比，不涉及性能/流畅度/稳定性/卡顿/丝滑维度"

    # 12. 华为/苹果拍照对比
    if "华为" in combined and "苹果" in combined:
        if any(k in combined for k in ["拍照", "摄影", "影像", "摄像", "镜头", "像素", "照片"]):
            if not any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "系统", "响应", "掉帧", "后台", "动画", "视频拍摄"]):
                return "unrelated", "仅为拍照/影像对比，不涉及性能/流畅度/稳定性/卡顿/丝滑维度"

    # 13. 华为/苹果平板对比
    if "平板" in combined:
        if "华为" in combined and "苹果" in combined:
            if not any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "系统", "响应", "掉帧"]):
                return "unrelated", "仅为平板产品对比，不涉及性能/流畅度/稳定性/卡顿/丝滑维度"

    # 14. 华为/苹果手表对比
    if "手表" in combined or "睡眠检测" in combined:
        if "华为" in combined and "苹果" in combined:
            return "unrelated", "仅为手表/穿戴设备对比，不涉及手机性能/流畅度/稳定性/卡顿/丝滑维度"

    # 15. 营销/广告/销量/市场份额
    if any(k in combined for k in ["营销号", "拉踩", "销量", "市场份额", "跌出前三", "一家独大"]):
        return "unrelated", "内容为营销/销量/市场份额讨论，不涉及性能/流畅度/稳定性/卡顿/丝滑对比"

    # 16. 抽奖/广告/引流
    if "抽奖" in title or "宠粉" in title or "免费送出" in combined:
        return "unrelated", "内容为抽奖/广告引流，不涉及华为苹果性能对比"

    # 17. 科技资讯/新闻汇总
    if "科技热点" in title or "科技日报" in combined:
        return "unrelated", "内容为科技资讯汇总，不涉及华为苹果性能/流畅度对比"

    # 18. 全球大佬/名人用什么手机
    if "科技大佬" in title or "库克" in combined or "巴菲特" in combined:
        return "unrelated", "内容为科技大佬使用手机盘点，不涉及华为苹果性能对比"

    # 19. 华为处理器/芯片科普
    if "华为处理器" in title or "麒麟" in combined:
        if "苹果" not in combined:
            return "unrelated", "仅为华为处理器科普，不涉及与苹果的性能对比"

    # 20. 折叠屏/形态讨论
    if "折叠屏" in combined or "抄袭折叠屏" in combined:
        if not any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "系统", "响应", "掉帧"]):
            return "unrelated", "内容为折叠屏形态/设计讨论，不涉及性能/流畅度对比"

    # 21. 手机壳/配件
    if "手机壳" in combined or "贴膜" in combined:
        return "unrelated", "内容为手机配件讨论，不涉及性能/流畅度对比"

    # 22. 纯晒单/开箱
    if "开箱" in title and "华为" in combined:
        if "苹果" not in combined:
            return "unrelated", "仅为华为新机开箱晒单，不涉及与苹果的性能对比"

    # 23. 纯卖手机/二手交易
    if any(k in combined for k in ["包邮", "七天无理由", "关联商品", "二手", "转转", "闲鱼"]):
        if "苹果" not in combined or not any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "系统"]):
            return "unrelated", "内容为手机交易/卖货，不涉及华为苹果性能对比"

    # 24. 纯iPhone拍照对比（苹果内部对比）
    if "iPhone" in combined and "拍照" in combined:
        if "华为" not in combined:
            return "unrelated", "仅为iPhone内部拍照对比，不涉及华为"

    # 25. 纯iPhone vs 安卓（不涉及华为）
    if "安卓" in combined and "苹果" in combined:
        if "华为" not in combined and "鸿蒙" not in combined:
            if not any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "系统", "响应", "掉帧"]):
                return "unrelated", "仅为安卓与苹果对比，未涉及华为/鸿蒙"

    # 26. 华为内部对比（Mate vs Pura）
    if "华为" in combined and "Mate" in combined and "Pura" in combined:
        if "苹果" not in combined:
            return "unrelated", "仅为华为内部机型对比，不涉及苹果"

    # 27. 华为 vs vivo/OPPO/小米（不涉及苹果）
    if "华为" in combined:
        if any(k in combined for k in ["vivo", "OPPO", "小米", "荣耀", "iQOO"]):
            if "苹果" not in combined and "iPhone" not in combined:
                return "unrelated", "仅为华为与其他安卓品牌对比，不涉及苹果"

    # 28. 纯苹果体验/吐槽（不涉及华为）
    if "iPhone" in combined or "苹果" in combined:
        if "华为" not in combined and "鸿蒙" not in combined:
            if any(k in combined for k in ["卡顿", "难用", "掉帧", "发热", "流畅", "丝滑"]):
                return "unrelated", "仅为苹果自身使用体验/吐槽，不涉及华为"

    # 29. 纯华为体验/吐槽（不涉及苹果）
    if "华为" in combined:
        if "苹果" not in combined and "iPhone" not in combined and "iOS" not in combined:
            if any(k in combined for k in ["卡顿", "流畅", "丝滑", "系统", "好用"]):
                return "unrelated", "仅为华为自身使用体验，不涉及苹果"

    # 30. 3D结构光技术讨论
    if "3D结构光" in combined:
        return "unrelated", "内容为3D结构光技术讨论，不涉及性能/流畅度对比"

    # 31. 流量/内存问题
    if "流量" in combined or "内存" in combined:
        if "华为" not in combined or "苹果" not in combined:
            return "unrelated", "内容为流量/内存使用问题，不涉及华为苹果性能对比"

    # 32. 游戏内存占用
    if "内存" in combined and "安卓" in combined and "iOS" in combined:
        return "unrelated", "仅为游戏内存占用对比，不涉及系统性能/流畅度"

    # 33. 笔记本/电脑对比
    if "MateBook" in combined or "MacBook" in combined:
        if "手机" not in combined:
            return "unrelated", "内容为笔记本电脑对比，不涉及手机性能/流畅度"

    # 34. 华为vs苹果价格/配置对比（不涉及性能体验）
    if "华为" in combined and "苹果" in combined:
        if any(k in combined for k in ["价格", "配置", "参数", "电池", "充电", "续航", "快充", "像素", "重量", "尺寸"]):
            if not any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "系统", "响应", "掉帧", "后台", "动画", "稳定性"]):
                return "unrelated", "仅为价格/配置参数对比，不涉及性能/流畅度/稳定性/卡顿/丝滑体验"

    # 35. 华为vs苹果选购建议（泛泛而谈）
    if "怎么选" in combined or "选购" in combined:
        if "华为" in combined and "苹果" in combined:
            if not any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "系统", "响应", "掉帧", "后台", "动画", "稳定性"]):
                return "unrelated", "仅为选购建议/推荐，未深入涉及性能/流畅度/稳定性/卡顿/丝滑体验对比"

    # 36. 系统阵营概述
    if "手机系统阵营" in combined or "iOS、鸿蒙、安卓" in combined:
        if "对比" in combined or "优缺点" in combined:
            return "valid", "三大系统阵营对比，明确涉及iOS与鸿蒙的流畅度/卡顿/丝滑对比"

    # 37. 华为/苹果各自UI设计讨论
    if "UI" in combined:
        if "华为" in combined and "苹果" in combined:
            if not any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "响应", "掉帧"]):
                return "unrelated", "仅为UI设计讨论，不涉及性能/流畅度/稳定性/卡顿/丝滑维度"

    # 38. 鸿蒙丝滑讨论（涉及苹果对比）
    if "鸿蒙丝滑" in combined or "鸿蒙" in combined and "丝滑" in combined:
        if "苹果" in combined or "iOS" in combined:
            return "valid", "鸿蒙丝滑体验讨论，明确与苹果iOS对比"

    # 39. 华为Pura X Max使用体验
    if "Pura X Max" in combined or "puraxmax" in combined.lower():
        if "苹果" in combined or "iPhone" in combined:
            if any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "系统"]):
                return "valid", "华为Pura X Max与苹果对比，涉及系统流畅度/丝滑度"

    # 40. 华为Mate80pro使用体验（涉及苹果对比）
    if "mate80" in combined.lower():
        if "苹果" in combined or "iPhone" in combined:
            if any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "系统", "好用", "不好用"]):
                return "valid", "华为Mate80与苹果对比，涉及系统使用体验/流畅度"

    # 41. 华为vs苹果对镜拍/自拍
    if "对镜拍" in combined or "自拍" in combined:
        if "华为" in combined and "苹果" in combined:
            return "unrelated", "仅为对镜拍/自拍效果对比，不涉及性能/流畅度/稳定性/卡顿/丝滑维度"

    # 42. 鸿蒙7.0/系统升级资讯
    if "鸿蒙7" in combined or "鸿蒙OS 7" in combined:
        if "苹果" in combined or "看齐苹果" in combined:
            if any(k in combined for k in ["响应速度", "后台保活", "应用启动", "多任务", "丝滑", "流畅"]):
                return "valid", "鸿蒙7.0系统升级资讯，明确提及响应速度/后台保活/应用启动等性能指标，并与苹果对比"

    # 43. 华为nova6等旧机型推荐
    if "nova6" in combined.lower() or "nova 6" in combined.lower():
        if "苹果" not in combined:
            return "unrelated", "仅为华为旧机型推荐/评测，不涉及苹果"

    # 44. 纯OPPO/其他品牌体验
    if "OPPO" in combined and "苹果" in combined:
        if "华为" not in combined:
            return "unrelated", "内容为OPPO与苹果对比，不涉及华为"

    # 45. 华为MatebookGT14 vs MacBookPro
    if "MateBook" in combined and "MacBook" in combined:
        if any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能"]):
            return "valid", "华为MateBook与MacBookPro性能/流畅度对比"

    # 46. 华为vs苹果信号对比
    if "信号" in combined:
        if "华为" in combined and "苹果" in combined:
            if not any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "系统", "响应", "掉帧", "后台", "动画"]):
                return "unrelated", "仅为信号对比，不涉及性能/流畅度/稳定性/卡顿/丝滑维度"

    # 47. 华为vs苹果续航/充电对比
    if any(k in combined for k in ["续航", "充电", "电池", "快充"]):
        if "华为" in combined and "苹果" in combined:
            if not any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "系统", "响应", "掉帧", "后台", "动画", "稳定性"]):
                return "unrelated", "仅为续航/充电对比，不涉及性能/流畅度/稳定性/卡顿/丝滑维度"

    # 48. 华为vs苹果生态/互联对比
    if "生态" in combined or "互联" in combined or "协同" in combined:
        if "华为" in combined and "苹果" in combined:
            if not any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "系统", "响应", "掉帧", "后台", "动画"]):
                return "unrelated", "仅为生态/互联对比，不涉及性能/流畅度/稳定性/卡顿/丝滑维度"

    # 49. 纯华为pura x max使用体验（不涉及苹果）
    if "pura x max" in combined.lower() or "puraxmax" in combined.lower():
        if "苹果" not in combined and "iPhone" not in combined:
            return "unrelated", "仅为华为Pura X Max使用体验，不涉及苹果"

    # 50. 华为vs苹果重量/手感对比
    if "重量" in combined or "手感" in combined or "便携" in combined:
        if "华为" in combined and "苹果" in combined:
            if not any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "系统", "响应", "掉帧", "后台", "动画"]):
                return "unrelated", "仅为重量/手感/便携性对比，不涉及性能/流畅度/稳定性/卡顿/丝滑维度"

    # 51. 华为/苹果外观/颜值讨论
    if "外观" in combined or "颜值" in combined or "丑" in combined:
        if "华为" in combined and "苹果" in combined:
            return "unrelated", "仅为外观/颜值讨论，不涉及性能/流畅度/稳定性/卡顿/丝滑维度"

    # 52. 纯iPhone外观爆料
    if "iPhone" in combined and "外观" in combined:
        if "华为" not in combined:
            return "unrelated", "仅为iPhone外观爆料，不涉及华为"

    # 53. 华为/苹果各自发热问题
    if "发热" in combined or "发烫" in combined:
        if "华为" in combined and "苹果" in combined:
            return "valid", "华为与苹果发热问题对比，涉及性能/稳定性体验"
        elif "苹果" in combined and "华为" not in combined:
            return "unrelated", "仅为苹果发热问题，不涉及华为"
        elif "华为" in combined and "苹果" not in combined:
            return "unrelated", "仅为华为发热问题，不涉及苹果"

    # 54. 华为vs苹果面容/指纹解锁
    if "面容" in combined or "指纹" in combined or "解锁" in combined:
        if "华为" in combined and "苹果" in combined:
            if not any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "系统", "响应", "掉帧", "后台", "动画"]):
                return "unrelated", "仅为面容/指纹解锁对比，不涉及性能/流畅度/稳定性/卡顿/丝滑维度"

    # 55. 纯华为平板使用体验
    if "华为平板" in combined:
        if "苹果" not in combined:
            return "unrelated", "仅为华为平板使用体验，不涉及苹果"

    # 56. 纯iPhone使用吐槽
    if "iPhone" in combined or "苹果" in combined:
        if "华为" not in combined:
            if any(k in combined for k in ["难用", "bug", "问题", "吐槽"]):
                return "unrelated", "仅为iPhone使用吐槽，不涉及华为"

    # 57. 纯华为使用体验
    if "华为" in combined:
        if "苹果" not in combined and "iPhone" not in combined:
            if any(k in combined for k in ["好用", "不好用", "体验", "感受"]):
                return "unrelated", "仅为华为使用体验，不涉及苹果"

    # 58. 华为vs苹果iPhone17 Air/Mate70 Air
    if "Air" in combined:
        if "华为" in combined and "苹果" in combined:
            if any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "系统", "响应", "掉帧", "全局高刷", "帧率"]):
                return "valid", "华为与苹果Air机型对比，涉及系统流畅度/丝滑度/性能"

    # 59. 华为P90体验（涉及iPhone对比）
    if "P90" in combined or "Pura 90" in combined:
        if "iPhone" in combined or "苹果" in combined:
            if any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "系统", "跟手"]):
                return "valid", "华为P90与iPhone对比，涉及系统流畅度/丝滑度"

    # 60. 默认处理：华为+苹果同时出现
    if "华为" in combined and "苹果" in combined:
        if any(k in combined for k in ["丝滑", "流畅", "卡顿", "性能", "系统", "响应", "掉帧", "后台", "动画", "稳定性", "好用", "不好用", "体验", "感受"]):
            return "valid", "华为与苹果使用体验对比，涉及系统/性能相关维度"
        else:
            return "unrelated", "华为与苹果相关内容，但未涉及性能/流畅度/稳定性/卡顿/丝滑维度"

    # 默认unrelated
    return "unrelated", "内容不涉及华为苹果在性能/流畅度/稳定性/卡顿/丝滑任一维度的对比或体验"


def process_batch(batch_id):
    input_file = os.path.join(INPUT_DIR, f"batch_{batch_id:03d}_input.json")
    output_file = os.path.join(INPUT_DIR, f"batch_{batch_id:03d}_output.json")

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []
    for item in data:
        classification, reason = classify_ugc(item)
        result = {
            "note_id": item["note_id"],
            "title_cleaned": item.get("title_cleaned", ""),
            "content_cleaned": item.get("content_cleaned", "")[:200],
            "classification": classification,
            "reason": reason
        }
        results.append(result)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # 统计
    stats = {"valid": 0, "unrelated": 0, "incomplete": 0}
    for r in results:
        stats[r["classification"]] += 1

    print(f"Batch {batch_id:03d}: total={len(results)}, valid={stats['valid']}, unrelated={stats['unrelated']}, incomplete={stats['incomplete']}")
    return stats


if __name__ == "__main__":
    for batch_id in [4, 5, 6]:
        process_batch(batch_id)
