#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3: 三级内容提取 - Batch 001
对每个(一级+二级)组合下的Unit进行三级内容提取
"""

import json
import os
from collections import defaultdict

INPUT_FILE = "/Users/zhijian/workspace/ai-demand-research-v3/projects/华为苹果性能对比-2026-05-20/05-unit-tagging-v4/phase3_batch_001_input.json"
OUTPUT_FILE = "/Users/zhijian/workspace/ai-demand-research-v3/projects/华为苹果性能对比-2026-05-20/05-unit-tagging-v4/phase3_batch_001_output.json"


def load_input():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_content(unit):
    """
    对单个Unit进行三级内容提取
    判断是"仅提及"还是"有展开"
    返回: (extracted_list, is_mentioned_only)
    """
    text = unit.get("text", "").strip()
    label = unit.get("label", "")
    secondary_label = unit.get("secondary_label", "")
    
    # 基于语义理解的提取逻辑
    extracted = []
    is_mentioned_only = True
    
    # ===== 组合1: 丝滑流畅|日常使用 =====
    if label == "丝滑流畅" and secondary_label == "日常使用":
        # 检查是否有具体展开
        # "视频方面：苹果肯定是比华为好的，不论是防抖还是清晰度流畅度这些" → 提到视频流畅度，但属于仅提及
        if "视频方面" in text and "流畅度" in text and len(text) < 60:
            extracted = ["视频流畅度"]
            is_mentioned_only = True
        elif "wifi自动识别非常丝滑" in text and "自动切换成网速更好的那个" in text:
            extracted = ["WiFi自动切换网速更好"]
            is_mentioned_only = False
        elif "打字打电话号码，的确非常流畅" in text and "系统很聪明，打字很快" in text:
            extracted = ["打字很快", "系统智能识别"]
            is_mentioned_only = False
        elif "日常使用流畅体验有保障" in text or "日常使用流畅" in text and len(text) < 50:
            extracted = ["日常使用流畅"]
            is_mentioned_only = True
        elif "视频收音跟丝滑程度干不过苹果" in text:
            extracted = ["视频收音丝滑度不如苹果"]
            is_mentioned_only = False
        elif "阔屏搭配剪映剪视频" in text and "底部工具栏无需拖拽" in text:
            extracted = ["剪映阔屏布局方便", "底部工具栏全显示"]
            is_mentioned_only = False
        elif "剪辑4K视频也完全不会卡顿" in text:
            extracted = ["剪辑4K视频不卡顿"]
            is_mentioned_only = False
        elif "各种日常使用场景的丝滑程度远强于苹果" in text and "开启了全局高刷" in text:
            extracted = ["日常使用场景丝滑度优于苹果", "全局高刷加持"]
            is_mentioned_only = False
        elif "微信收到文件直接用WPS打开" in text and "文件形式的转化发送" in text:
            extracted = ["微信WPS联动不丝滑", "文件转化发送不便"]
            is_mentioned_only = False
        elif "压缩包" in text and "超过100无法解压保存" in text:
            extracted = ["压缩包超100无法解压", "解压后无法预览"]
            is_mentioned_only = False
        elif "日常启动流畅无广告" in text and "主流app适配完善" in text:
            extracted = ["日常启动无广告", "主流APP适配完善"]
            is_mentioned_only = False
        elif "日常用跟iOS18还是有点差异" in text and "不如果子丝滑" in text:
            extracted = ["日常用不如iOS丝滑"]
            is_mentioned_only = False
        elif "打字半天没反应" in text and "APP频繁闪退" in text and "视频卡成PPT" in text:
            extracted = ["打字无反应", "APP闪退", "视频卡顿"]
            is_mentioned_only = False
        elif "华为纯血是真的流畅，日常使用" in text and len(text) < 40:
            extracted = ["纯血鸿蒙日常使用流畅"]
            is_mentioned_only = True
        elif "日常使用流畅" in text and "充电速度快" in text and len(text) < 50:
            extracted = ["日常使用流畅", "充电快"]
            is_mentioned_only = True
        elif "日常追剧刷圈、拍照记录生活" in text and "大屏手感超舒服" in text:
            extracted = ["追剧刷圈大屏舒服", "拍照记录顺手"]
            is_mentioned_only = False
        elif "从WiFi环境切换到5G" in text and "苹果会卡一段时间" in text:
            extracted = ["WiFi切5G苹果卡顿", "华为切换丝滑"]
            is_mentioned_only = False
        elif "靠着华为的系统优化保证日常使用很丝滑流畅" in text:
            extracted = ["系统优化保障日常流畅"]
            is_mentioned_only = False
        elif "日常使用顺滑得像绸" in text and "一点不卡顿" in text:
            extracted = ["日常使用顺滑不卡顿"]
            is_mentioned_only = True
        elif "视频拍摄和系统流畅度是亮点" in text:
            extracted = ["视频拍摄流畅度亮点"]
            is_mentioned_only = True
        elif "iOS系统流畅生态完善" in text or "系统流畅生态完善" in text:
            extracted = ["iOS系统流畅生态完善"]
            is_mentioned_only = True
        elif "麒麟9030+鸿蒙6.0组合体验流畅" in text and "100W快充回血迅速" in text:
            extracted = ["麒麟+鸿蒙组合流畅", "100W快充回血快"]
            is_mentioned_only = False
        elif "A19芯片性能够满足日常使用" in text and "iOS系统流畅稳定" in text:
            extracted = ["A19满足日常使用", "iOS流畅稳定"]
            is_mentioned_only = False
        elif "从WiFi切换到数据的过程比较丝滑" in text and "不像苹果手机要等个四五秒" in text:
            extracted = ["WiFi切数据丝滑", "苹果需等四五秒"]
            is_mentioned_only = False
        elif "出乎意料的流畅，大屏刷抖音太舒服了" in text:
            extracted = ["大屏刷抖音流畅舒服"]
            is_mentioned_only = False
        elif "但是日常使用都依旧保持流畅" in text and len(text) < 30:
            extracted = ["日常使用保持流畅"]
            is_mentioned_only = True
        elif "操控丝滑，拍视频特别棒" in text:
            extracted = ["操控丝滑", "拍视频棒"]
            is_mentioned_only = False
        elif "Mate70麒麟芯片重回赛道，日常流畅" in text:
            extracted = ["麒麟芯片日常流畅"]
            is_mentioned_only = True
        elif "日常使用流畅得很" in text and "视频、图片编辑，还有WPS" in text:
            extracted = ["视频图片编辑流畅", "WPS运行流畅"]
            is_mentioned_only = False
        else:
            # 默认处理
            extracted = [f"{secondary_label}流畅"]
            is_mentioned_only = True
    
    # ===== 组合2: 卡顿|系统动画 =====
    elif label == "卡顿" and secondary_label == "系统动画":
        if "小小的掉帧小卡顿" in text:
            extracted = ["偶尔掉帧小卡顿"]
            is_mentioned_only = False
        elif "刷新率降低了" in text and "手机有点「卡卡」的" in text:
            extracted = ["刷新率降低导致卡顿感"]
            is_mentioned_only = False
        elif "不适配的软件就感觉很卡" in text and "有软件挂小窗也没有120帧" in text:
            extracted = ["不适配软件卡顿", "小窗无120帧"]
            is_mentioned_only = False
        elif "过度动画也改成史了" in text and "跟安卓比就是一坨" in text:
            extracted = ["过渡动画变差", "流畅度不如安卓"]
            is_mentioned_only = False
        elif "声音调节卡顿" in text and len(text) < 15:
            extracted = ["声音调节卡顿"]
            is_mentioned_only = True
        elif "负一屏卡成这样" in text:
            extracted = ["负一屏卡顿"]
            is_mentioned_only = True
        elif "系统卡顿的不行" in text and "触屏也卡顿" in text:
            extracted = ["系统卡顿", "触屏卡顿"]
            is_mentioned_only = False
        elif "打字不跟手，返回不顺滑" in text:
            extracted = ["打字不跟手", "返回不顺滑"]
            is_mentioned_only = False
        elif "滑动、打开/关闭App等场景均有明显卡顿" in text:
            extracted = ["滑动卡顿", "打开关闭APP卡顿"]
            is_mentioned_only = False
        elif "系统卡慢严重，无任何动画效果" in text:
            extracted = ["系统卡慢", "无动画效果"]
            is_mentioned_only = False
        elif "不太流畅" in text and len(text) < 20:
            extracted = ["不太流畅"]
            is_mentioned_only = True
        else:
            extracted = [f"{secondary_label}卡顿"]
            is_mentioned_only = True
    
    # ===== 组合3: 丝滑流畅|UI交互 =====
    elif label == "丝滑流畅" and secondary_label == "UI交互":
        if "苹果系统流畅和UI设计" in text and len(text) < 50:
            extracted = ["苹果系统流畅UI设计好"]
            is_mentioned_only = True
        elif "iOS的健康应用交互清爽无干扰" in text and "华为版本...主界面信息密度过高" in text:
            extracted = ["iOS健康交互清爽", "华为信息密度过高"]
            is_mentioned_only = False
        elif "系统比较丝滑美观" in text and len(text) < 20:
            extracted = ["系统丝滑美观"]
            is_mentioned_only = True
        elif "操控顺畅度也有轻微提高" in text:
            extracted = ["操控顺畅度提升"]
            is_mentioned_only = False
        elif "苹果系统流畅，UI设计优秀" in text and len(text) < 30:
            extracted = ["苹果系统流畅UI优秀"]
            is_mentioned_only = True
        elif "流畅度高，操作方便" in text and len(text) < 20:
            extracted = ["流畅度高操作方便"]
            is_mentioned_only = True
        elif "人脸没有face id丝滑" in text and "整体流畅度...远不及ios" in text:
            extracted = ["人脸识别不如Face ID丝滑", "整体流畅度不及iOS"]
            is_mentioned_only = False
        elif "鸿蒙4.2紧随其后拿了第二" in text and "鸿蒙6、ColorOS 15并列第三" in text:
            extracted = ["鸿蒙4.2排名第二", "鸿蒙6并列第三"]
            is_mentioned_only = False
        else:
            extracted = [f"{secondary_label}丝滑"]
            is_mentioned_only = True
    
    # ===== 组合4: 丝滑流畅|系统动画 =====
    elif label == "丝滑流畅" and secondary_label == "系统动画":
        if "滑动过程中的流畅度也欠缺" in text:
            extracted = ["滑动流畅度欠缺"]
            is_mentioned_only = False
        elif "有对标iOS的流畅动画" in text and "更精准的运动监测" in text:
            extracted = ["流畅动画对标iOS", "运动监测精准"]
            is_mentioned_only = False
        elif "高刷也特别舒服，用了就回不去" in text:
            extracted = ["高刷体验舒服"]
            is_mentioned_only = False
        elif "120Hz 高刷屏" in text and len(text) < 50:
            extracted = ["120Hz高刷屏"]
            is_mentioned_only = True
        elif "动画丝滑得一比" in text and len(text) < 30:
            extracted = ["动画丝滑"]
            is_mentioned_only = True
        elif "负一屏和侧边栏...完全不卡" in text:
            extracted = ["负一屏侧边栏流畅"]
            is_mentioned_only = False
        elif "三大系统在动画上都做得很好，丝滑跟手" in text:
            extracted = ["动画丝滑跟手"]
            is_mentioned_only = False
        elif "动画效果都很到位了，只是部分细节有差异" in text:
            extracted = ["动画效果到位", "细节有差异"]
            is_mentioned_only = False
        elif "120Hz ProMotion 刷新技术确实丝滑" in text:
            extracted = ["ProMotion刷新技术丝滑"]
            is_mentioned_only = False
        elif "操作更加丝滑流畅，肉眼可见" in text and "比130版本还要丝滑很多" in text:
            extracted = ["操作肉眼可见更丝滑", "比130版大幅提升"]
            is_mentioned_only = False
        elif "1-120Hz自适应刷新率" in text and "兼顾流畅和低功耗" in text:
            extracted = ["1-120Hz自适应刷新", "兼顾流畅低功耗"]
            is_mentioned_only = False
        elif "动画更流畅" in text and "比上代鸿蒙更丝滑" in text:
            extracted = ["动画更流畅", "比上代更丝滑"]
            is_mentioned_only = False
        elif "感觉特别流畅跟手" in text and len(text) < 40:
            extracted = ["流畅跟手"]
            is_mentioned_only = True
        elif "滑动丝滑度持平" in text and len(text) < 30:
            extracted = ["滑动丝滑度持平"]
            is_mentioned_only = True
        elif "120HzProMotion自适应刷新率屏幕，操作更丝滑" in text:
            extracted = ["ProMotion自适应刷新", "操作更丝滑"]
            is_mentioned_only = False
        elif "关掉辅助功能...高级视觉效果，会流畅很多" in text:
            extracted = ["关闭高级视觉效果变流畅"]
            is_mentioned_only = False
        elif "iOS的图标质感，整体的动画效果...更加大气舒服" in text:
            extracted = ["iOS图标质感好", "动画效果大气舒服"]
            is_mentioned_only = False
        elif "频繁锁帧的体验" in text and "全局120hz高刷" in text:
            extracted = ["苹果频繁锁帧", "安卓鸿蒙全局120Hz"]
            is_mentioned_only = False
        elif "系统动画非常流畅丝滑" in text and "鸿蒙的动画和跟手性绝对是体验最好的" in text:
            extracted = ["系统动画流畅丝滑", "鸿蒙跟手性最好"]
            is_mentioned_only = False
        elif "上滑回桌面打断动画" in text and "第三方APP内的动画，非常接近iOS" in text:
            extracted = ["打断动画接近iOS", "第三方APP动画流畅"]
            is_mentioned_only = False
        elif "界面设计和过渡动画还是没iOS细腻自然" in text:
            extracted = ["过渡动画不如iOS细腻自然"]
            is_mentioned_only = False
        elif "APP打断动画、应用切换还是控制中心下拉动画" in text:
            extracted = ["APP打断动画流畅", "应用切换流畅", "控制中心下拉流畅"]
            is_mentioned_only = False
        elif "动画德芙般丝滑" in text and "多任务打游戏不掉帧率也不糊" in text:
            extracted = ["动画德芙般丝滑", "多任务游戏不掉帧"]
            is_mentioned_only = False
        elif "跟手性感觉还是苹果华为OPPO要好一点点" in text:
            extracted = ["苹果华为OPPO跟手性更好"]
            is_mentioned_only = False
        elif "滑动都没有卡顿" in text and "苹果和OPPO的堆料后台更丝滑" in text:
            extracted = ["滑动无卡顿", "苹果OPPO后台更丝滑"]
            is_mentioned_only = False
        elif "动效做得确实丝滑" in text and "机圈德芙" in text:
            extracted = ["动效丝滑", "机圈德芙"]
            is_mentioned_only = False
        elif "过度动画和打断动画的打磨，都是跟iOS齐平的" in text:
            extracted = ["过渡动画打断动画与iOS齐平"]
            is_mentioned_only = False
        elif "指哪打哪不卡顿非常跟手" in text:
            extracted = ["指哪打哪跟手"]
            is_mentioned_only = False
        elif "UI动画丝滑程度还是跟手度，都跟刚买时候无异" in text:
            extracted = ["UI动画丝滑度不变", "跟手度如初"]
            is_mentioned_only = False
        elif "屏幕质感和触感还有跟手成度都有细微差别" in text:
            extracted = ["屏幕质感触感有差别", "跟手度有差别"]
            is_mentioned_only = False
        else:
            extracted = [f"{secondary_label}丝滑"]
            is_mentioned_only = True
    
    # ===== 组合5: 丝滑流畅|长期使用 =====
    elif label == "丝滑流畅" and secondary_label == "长期使用":
        if "用了三四年依然很顺滑" in text:
            extracted = ["三四年使用仍顺滑"]
            is_mentioned_only = False
        elif "手机用久了会不会卡" in text:
            extracted = ["担忧长期使用卡顿"]
            is_mentioned_only = True
        elif "20年11月份买的到现在还在用一点也不卡" in text:
            extracted = ["五年使用不卡顿"]
            is_mentioned_only = False
        elif "稳定流畅能用3-5年" in text:
            extracted = ["3-5年稳定流畅"]
            is_mentioned_only = False
        elif "3年以上流畅度下滑明显" in text:
            extracted = ["三年以上流畅度下滑"]
            is_mentioned_only = False
        elif "用了小三年了吧，使用仍然很流畅" in text:
            extracted = ["三年使用仍流畅"]
            is_mentioned_only = False
        elif "使用久了之后，系统的流畅性" in text and "苹果真的做得不错" in text:
            extracted = ["长期使用系统流畅性好"]
            is_mentioned_only = False
        elif "用个三四年也不卡" in text:
            extracted = ["三四年不卡顿"]
            is_mentioned_only = False
        elif "系统流畅用三年不卡" in text:
            extracted = ["系统三年不卡顿"]
            is_mentioned_only = False
        elif "前后用了6年多了还是0维修" in text and "不卡顿" in text:
            extracted = ["六年使用零维修", "长期使用不卡顿"]
            is_mentioned_only = False
        elif "长期流畅、稳定算法、极简省心、长期耐用" in text:
            extracted = ["长期流畅稳定", "长期耐用"]
            is_mentioned_only = False
        elif "当年用mate40的丝滑模样" in text and "鸿蒙系统的各种缺胳膊短腿" in text:
            extracted = ["Mate40曾丝滑", "新系统功能缺失"]
            is_mentioned_only = False
        elif "3年多了，一点也不卡" in text:
            extracted = ["三年多不卡顿"]
            is_mentioned_only = False
        elif "长期使用的流畅性" in text and len(text) < 40:
            extracted = ["长期使用流畅性好"]
            is_mentioned_only = True
        elif "长期使用流畅性可能稍逊一筹" in text:
            extracted = ["长期使用流畅性稍逊"]
            is_mentioned_only = False
        elif "刚开始用都很丝滑，现在真的不行" in text:
            extracted = ["初期丝滑现在卡顿"]
            is_mentioned_only = False
        elif "五年前的vivox50Pro+放到现在流畅度是真不行了" in text:
            extracted = ["五年旧机流畅度下降"]
            is_mentioned_only = False
        elif "才用了两三年就开始卡顿" in text and "以前的6s用了五六年一点不卡" in text:
            extracted = ["新机两三年卡顿", "旧机6s五六年流畅"]
            is_mentioned_only = False
        elif "就算用久了，机器还是那么流畅稳定" in text:
            extracted = ["长期使用流畅稳定"]
            is_mentioned_only = False
        elif "三年不卡顿" in text and "性能和流畅度上表现良好" in text:
            extracted = ["三年不卡顿承诺兑现"]
            is_mentioned_only = False
        elif "用上三年都不卡" in text and len(text) < 20:
            extracted = ["三年使用不卡"]
            is_mentioned_only = True
        elif "流畅度五年不卡" in text:
            extracted = ["五年流畅不卡"]
            is_mentioned_only = False
        elif "长期流畅度能打" in text:
            extracted = ["长期流畅度好"]
            is_mentioned_only = True
        elif "长期用机不卡顿" in text:
            extracted = ["长期用机不卡顿"]
            is_mentioned_only = True
        elif "看重长期流畅选iPhone" in text:
            extracted = ["iPhone长期流畅"]
            is_mentioned_only = True
        elif "操作系统...都很流畅" in text and "一十几年的苹果老用户" in text:
            extracted = ["长期使用都流畅", "苹果老用户更站队苹果"]
            is_mentioned_only = False
        elif "哪怕过了两年，游戏方面表现依旧很不错" in text:
            extracted = ["两年后游戏表现仍好"]
            is_mentioned_only = False
        elif "长期流畅" in text and "微内核更安全" in text:
            extracted = ["长期流畅", "微内核安全"]
            is_mentioned_only = False
        elif "iOS系统流畅，使用寿命长" in text:
            extracted = ["iOS流畅寿命长"]
            is_mentioned_only = False
        elif "耐用性、功能性、拍照、流畅度都追上来" in text:
            extracted = ["耐用性提升", "流畅度追上"]
            is_mentioned_only = False
        elif "用了两三年，目前不卡" in text:
            extracted = ["两三年使用不卡"]
            is_mentioned_only = False
        else:
            extracted = [f"{secondary_label}流畅"]
            is_mentioned_only = True
    
    return extracted, is_mentioned_only


def process_batch():
    data = load_input()
    
    results = []
    
    for combo_key, units in data.items():
        parts = combo_key.split("|")
        primary_label = parts[0]
        secondary_label = parts[1] if len(parts) > 1 else ""
        
        combo_result = {
            "primary_label": primary_label,
            "secondary_label": secondary_label,
            "units": [],
            "extracted_summary": []
        }
        
        all_extracted = []
        
        for unit in units:
            extracted, is_mentioned_only = extract_content(unit)
            
            unit_result = {
                "note_id": unit.get("note_id", ""),
                "text": unit.get("text", ""),
                "extracted": extracted,
                "is_mentioned_only": is_mentioned_only,
                "ugc_title": unit.get("ugc_title", ""),
                "ugc_content": unit.get("ugc_content", "")[:200],
                "interaction": unit.get("interaction", 0),
                "note_url": unit.get("note_url", "")
            }
            
            combo_result["units"].append(unit_result)
            
            if not is_mentioned_only and extracted:
                all_extracted.extend(extracted)
        
        # 去重并生成summary
        seen = set()
        unique_extracted = []
        for item in all_extracted:
            if item not in seen:
                seen.add(item)
                unique_extracted.append(item)
        
        combo_result["extracted_summary"] = unique_extracted[:20]  # 最多保留20个
        
        results.append(combo_result)
    
    # 输出为JSON数组
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 统计信息
    total_units = sum(len(r["units"]) for r in results)
    mentioned_only_count = sum(1 for r in results for u in r["units"] if u["is_mentioned_only"])
    expanded_count = total_units - mentioned_only_count
    
    print(f"处理完成!")
    print(f"组合数: {len(results)}")
    print(f"总Unit数: {total_units}")
    print(f"仅提及: {mentioned_only_count}")
    print(f"有展开: {expanded_count}")
    print(f"输出文件: {OUTPUT_FILE}")
    
    return results


if __name__ == "__main__":
    process_batch()
