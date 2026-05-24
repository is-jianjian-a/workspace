#!/usr/bin/env python3
"""
Phase 3 v2: 三级内容提取脚本
对每个(一级+二级)组合下的Unit进行三级内容提取

规则：
1. 判断Unit是否"仅提及"二级标签场景，还是有"展开讲具体内容"
2. "仅提及"：只提到场景，没有具体细节/例子/数据
3. "有展开"：除了场景外，还有具体细节、例子、对比、感受、数据等
"""

import json
import re


def extract_third_level(text, primary_label, secondary_label):
    """
    对单个Unit进行三级内容提取
    返回: (extracted_list, is_mentioned_only)
    """
    extracted = []
    is_mentioned_only = True

    # ========== 丝滑流畅 | 系统 ==========
    if primary_label == "丝滑流畅" and secondary_label == "系统":
        # 先检查是否有具体展开的内容
        expand_patterns = [
            (r"鸿蒙[^，。！]*?丝滑", "鸿蒙系统丝滑"),
            (r"iOS[^，。！]*?丝滑", "iOS系统丝滑"),
            (r"系统[^，。！]*?丝滑", "系统丝滑"),
            (r"系统[^，。！]*?流畅", "系统流畅"),
            (r"系统[^，。！]*?不卡", "系统不卡"),
            (r"系统[^，。！]*?卡顿", "系统卡顿"),
            (r"掉帧", "掉帧"),
            (r"不跟手", "不跟手"),
            (r"响应快", "响应快"),
            (r"响应慢", "响应慢"),
            (r"反应快", "反应快"),
            (r"反应慢", "反应慢"),
            (r"全局高刷", "全局高刷"),
            (r"120Hz", "120Hz高刷"),
            (r"傻快", "傻快"),
            (r"触控[^，。！]*?采样", "触控采样率"),
            (r"触控[^，。！]*?延迟", "触控延迟"),
            (r"跟手[^，。！]*?", "跟手"),
            (r"顺滑[^，。！]*?", "顺滑"),
            (r"不卡[^，。！]*?", "不卡"),
            (r"卡顿[^，。！]*?", "卡顿"),
            (r"流畅[^，。！]*?", "流畅"),
            (r"丝滑[^，。！]*?", "丝滑"),
        ]
        for pattern, label in expand_patterns:
            if re.search(pattern, text):
                if label not in extracted:
                    extracted.append(label)
                is_mentioned_only = False

        # 如果没有提取到具体内容，检查是否仅泛泛提及
        if len(extracted) == 0:
            # 泛泛提及的模式
            vague_patterns = [
                r"系统[^，。！]*?(?:流畅|丝滑|顺滑|不卡|卡顿|卡)",
                r"(?:流畅|丝滑|顺滑|不卡|卡顿|卡)[^，。！]*?系统",
            ]
            for vp in vague_patterns:
                if re.search(vp, text):
                    is_mentioned_only = True
                    break
            else:
                # 连泛泛提及都不是
                is_mentioned_only = True

    # ========== 丝滑流畅 | 系统动画 ==========
    elif primary_label == "丝滑流畅" and secondary_label == "系统动画":
        expand_patterns = [
            (r"动画[^，。！]*?丝滑", "动画丝滑"),
            (r"动画[^，。！]*?流畅", "动画流畅"),
            (r"动画[^，。！]*?顺滑", "动画顺滑"),
            (r"动画[^，。！]*?卡顿", "动画卡顿"),
            (r"动画[^，。！]*?掉帧", "动画掉帧"),
            (r"打断动画", "打断动画"),
            (r"过渡动画", "过渡动画"),
            (r"返回动画", "返回动画"),
            (r"切换动画", "切换动画"),
            (r"开屏动画", "开屏动画"),
            (r"灵动岛[^，。！]*?动画", "灵动岛动画"),
            (r"灵动岛[^，。！]*?回收", "灵动岛回收动画"),
            (r"多任务[^，。！]*?动画", "多任务动画"),
            (r"后台[^，。！]*?动画", "后台动画"),
            (r"应用[^，。！]*?动画", "应用动画"),
            (r"窗口[^，。！]*?动画", "窗口动画"),
            (r"非线性动画", "非线性动画"),
            (r"线性动画", "线性动画"),
            (r"帧率[^，。！]*?稳定", "帧率稳定"),
            (r"帧率[^，。！]*?抽", "帧率抽帧"),
            (r"不抽不卡", "帧率稳定不卡"),
            (r"掉帧", "掉帧"),
            (r"抽帧", "抽帧"),
            (r"卡帧", "卡帧"),
        ]
        for pattern, label in expand_patterns:
            if re.search(pattern, text):
                if label not in extracted:
                    extracted.append(label)
                is_mentioned_only = False

        if len(extracted) == 0:
            vague_patterns = [
                r"动画[^，。！]*?(?:流畅|丝滑|顺滑|卡顿|掉帧|卡)",
                r"(?:流畅|丝滑|顺滑|卡顿|掉帧|卡)[^，。！]*?动画",
            ]
            for vp in vague_patterns:
                if re.search(vp, text):
                    is_mentioned_only = True
                    break

    # ========== 丝滑流畅 | UI交互 ==========
    elif primary_label == "丝滑流畅" and secondary_label == "UI交互":
        expand_patterns = [
            (r"UI[^，。！]*?丝滑", "UI丝滑"),
            (r"UI[^，。！]*?流畅", "UI流畅"),
            (r"UI[^，。！]*?设计", "UI设计"),
            (r"交互[^，。！]*?丝滑", "交互丝滑"),
            (r"交互[^，。！]*?流畅", "交互流畅"),
            (r"操作[^，。！]*?丝滑", "操作丝滑"),
            (r"操作[^，。！]*?流畅", "操作流畅"),
            (r"操作[^，。！]*?顺滑", "操作顺滑"),
            (r"侧滑返回", "侧滑返回"),
            (r"返回[^，。！]*?不顺滑", "返回不顺滑"),
            (r"返回[^，。！]*?不流畅", "返回不流畅"),
            (r"手势[^，。！]*?操作", "手势操作"),
            (r"手势[^，。！]*?翻页", "手势翻页"),
            (r"分屏", "分屏功能"),
            (r"小窗", "小窗功能"),
            (r"画中画", "画中画"),
            (r"多窗口", "多窗口"),
            (r"全局搜索", "全局搜索"),
            (r"搜索[^，。！]*?动画", "搜索动画"),
            (r"打断[^，。！]*?", "打断动画/操作"),
            (r"触控[^，。！]*?", "触控体验"),
            (r"点击[^，。！]*?响应", "点击响应"),
            (r"响应[^，。！]*?速度", "响应速度"),
            (r"跟手[^，。！]*?", "跟手"),
            (r"不跟手", "不跟手"),
            (r"界面[^，。！]*?流畅", "界面流畅"),
            (r"界面[^，。！]*?丝滑", "界面丝滑"),
        ]
        for pattern, label in expand_patterns:
            if re.search(pattern, text):
                if label not in extracted:
                    extracted.append(label)
                is_mentioned_only = False

        if len(extracted) == 0:
            vague_patterns = [
                r"(?:UI|交互|操作)[^，。！]*?(?:流畅|丝滑|顺滑|卡顿|卡)",
                r"(?:流畅|丝滑|顺滑|卡顿|卡)[^，。！]*?(?:UI|交互|操作)",
            ]
            for vp in vague_patterns:
                if re.search(vp, text):
                    is_mentioned_only = True
                    break

    # ========== 丝滑流畅 | 日常使用 ==========
    elif primary_label == "丝滑流畅" and secondary_label == "日常使用":
        expand_patterns = [
            (r"微信[^，。！]*?延迟", "微信延迟"),
            (r"微信[^，。！]*?没[^，。！]*?延迟", "微信无延迟"),
            (r"微信[^，。！]*?不[^，。！]*?延迟", "微信无延迟"),
            (r"wifi[^，。！]*?自动切换", "WiFi自动切换"),
            (r"wifi[^，。！]*?切换", "WiFi切换"),
            (r"WiFi[^，。！]*?自动切换", "WiFi自动切换"),
            (r"WiFi[^，。！]*?切换", "WiFi切换"),
            (r"打字[^，。！]*?流畅", "打字流畅"),
            (r"打字[^，。！]*?快", "打字快"),
            (r"打字[^，。！]*?不跟手", "打字不跟手"),
            (r"键盘[^，。！]*?打字", "键盘打字"),
            (r"剪视频[^，。！]*?不卡", "剪视频不卡"),
            (r"剪辑[^，。！]*?不卡", "剪辑不卡"),
            (r"剪辑[^，。！]*?4K", "剪辑4K视频"),
            (r"4K[^，。！]*?剪辑", "剪辑4K视频"),
            (r"4K[^，。！]*?不卡", "4K不卡"),
            (r"视频[^，。！]*?流畅", "视频流畅"),
            (r"视频[^，。！]*?卡顿", "视频卡顿"),
            (r"视频[^，。！]*?卡成PPT", "视频卡成PPT"),
            (r"视频[^，。！]*?丝滑", "视频丝滑"),
            (r"拍照[^，。！]*?流畅", "拍照流畅"),
            (r"拍照[^，。！]*?丝滑", "拍照丝滑"),
            (r"拍照[^，。！]*?卡顿", "拍照卡顿"),
            (r"刷视频[^，。！]*?", "刷视频"),
            (r"追剧[^，。！]*?", "追剧"),
            (r"WPS[^，。！]*?", "WPS办公"),
            (r"文件[^，。！]*?解压", "文件解压"),
            (r"文件[^，。！]*?预览", "文件预览"),
            (r"微信[^，。！]*?WPS", "微信WPS联动"),
            (r"办公[^，。！]*?丝滑", "办公丝滑"),
            (r"办公[^，。！]*?流畅", "办公流畅"),
            (r"工作[^，。！]*?丝滑", "工作丝滑"),
            (r"工作[^，。！]*?流畅", "工作流畅"),
            (r"启动[^，。！]*?流畅", "启动流畅"),
            (r"启动[^，。！]*?快", "启动快"),
            (r"打开[^，。！]*?速度", "打开速度"),
            (r"打开[^，。！]*?快", "打开快"),
            (r"后台[^，。！]*?切换", "后台切换"),
            (r"多APP[^，。！]*?切换", "多APP切换"),
            (r"多任务[^，。！]*?", "多任务"),
            (r"信号[^，。！]*?切换", "信号切换"),
            (r"WiFi[^，。！]*?5G", "WiFi切5G"),
            (r"5G[^，。！]*?切换", "5G切换"),
            (r"网络[^，。！]*?切换", "网络切换"),
            (r"充电[^，。！]*?快", "充电快"),
            (r"杀后台", "杀后台"),
            (r"不杀后台", "不杀后台"),
            (r"后台[^，。！]*?留存", "后台留存"),
            (r"APP[^，。！]*?闪退", "APP闪退"),
            (r"闪退", "闪退"),
            (r"日常[^，。！]*?丝滑", "日常丝滑"),
            (r"日常[^，。！]*?流畅", "日常流畅"),
            (r"日常[^，。！]*?不卡", "日常不卡"),
            (r"使用[^，。！]*?丝滑", "使用丝滑"),
            (r"使用[^，。！]*?流畅", "使用流畅"),
            (r"使用[^，。！]*?不卡", "使用不卡"),
        ]
        for pattern, label in expand_patterns:
            if re.search(pattern, text):
                if label not in extracted:
                    extracted.append(label)
                is_mentioned_only = False

        if len(extracted) == 0:
            vague_patterns = [
                r"(?:日常|使用|生活)[^，。！]*?(?:流畅|丝滑|顺滑|不卡|卡顿|卡)",
                r"(?:流畅|丝滑|顺滑|不卡|卡顿|卡)[^，。！]*?(?:日常|使用|生活)",
            ]
            for vp in vague_patterns:
                if re.search(vp, text):
                    is_mentioned_only = True
                    break

    # ========== 丝滑流畅 | 长期使用 ==========
    elif primary_label == "丝滑流畅" and secondary_label == "长期使用":
        expand_patterns = [
            (r"用[^，。！]*?久[^，。！]*?不卡", "用久不卡"),
            (r"用[^，。！]*?久[^，。！]*?流畅", "用久流畅"),
            (r"用[^，。！]*?久[^，。！]*?丝滑", "用久丝滑"),
            (r"长[^，。！]*?时间[^，。！]*?不卡", "长时间不卡"),
            (r"长[^，。！]*?时间[^，。！]*?流畅", "长时间流畅"),
            (r"长[^，。！]*?期[^，。！]*?不卡", "长期不卡"),
            (r"长[^，。！]*?期[^，。！]*?流畅", "长期流畅"),
            (r"几[^，。！]*?年[^，。！]*?不卡", "几年不卡"),
            (r"几[^，。！]*?年[^，。！]*?流畅", "几年流畅"),
            (r"越用越卡", "越用越卡"),
            (r"越用越流畅", "越用越流畅"),
            (r"久[^，。！]*?不卡", "久用不卡"),
            (r"久[^，。！]*?流畅", "久用流畅"),
            (r"老化[^，。！]*?", "老化"),
            (r"衰减[^，。！]*?", "性能衰减"),
            (r"变慢[^，。！]*?", "变慢"),
            (r"变卡[^，。！]*?", "变卡"),
            (r"后期[^，。！]*?卡顿", "后期卡顿"),
            (r"后期[^，。！]*?卡", "后期变卡"),
            (r"半年后[^，。！]*?卡", "半年后变卡"),
            (r"一年后[^，。！]*?卡", "一年后变卡"),
            (r"两年后[^，。！]*?卡", "两年后变卡"),
            (r"时间久了[^，。！]*?卡", "时间久了变卡"),
            (r"时间久了[^，。！]*?流畅", "时间久了流畅"),
            (r"持久[^，。！]*?流畅", "持久流畅"),
            (r"持久[^，。！]*?不卡", "持久不卡"),
            (r"耐用[^，。！]*?", "耐用"),
            (r"耐造[^，。！]*?", "耐造"),
            (r"三四年[^，。！]*?", "三四年使用"),
            (r"两三年[^，。！]*?", "两三年使用"),
            (r"用[^，。！]*?三四年", "用三四年"),
            (r"用[^，。！]*?两三年", "用两三年"),
        ]
        for pattern, label in expand_patterns:
            if re.search(pattern, text):
                if label not in extracted:
                    extracted.append(label)
                is_mentioned_only = False

        if len(extracted) == 0:
            vague_patterns = [
                r"(?:长期|久|长时间|几年|久用)[^，。！]*?(?:流畅|丝滑|顺滑|不卡|卡顿|卡)",
                r"(?:流畅|丝滑|顺滑|不卡|卡顿|卡)[^，。！]*?(?:长期|久|长时间|几年|久用)",
            ]
            for vp in vague_patterns:
                if re.search(vp, text):
                    is_mentioned_only = True
                    break

    # ========== 丝滑流畅 | 打游戏 ==========
    elif primary_label == "丝滑流畅" and secondary_label == "打游戏":
        expand_patterns = [
            (r"游戏[^，。！]*?丝滑", "游戏丝滑"),
            (r"游戏[^，。！]*?流畅", "游戏流畅"),
            (r"游戏[^，。！]*?卡顿", "游戏卡顿"),
            (r"游戏[^，。！]*?掉帧", "游戏掉帧"),
            (r"游戏[^，。！]*?不卡", "游戏不卡"),
            (r"打[^，。！]*?游戏[^，。！]*?丝滑", "打游戏丝滑"),
            (r"打[^，。！]*?游戏[^，。！]*?流畅", "打游戏流畅"),
            (r"打[^，。！]*?游戏[^，。！]*?卡顿", "打游戏卡顿"),
            (r"打[^，。！]*?游戏[^，。！]*?掉帧", "打游戏掉帧"),
            (r"打[^，。！]*?游戏[^，。！]*?不卡", "打游戏不卡"),
            (r"王者[^，。！]*?", "王者荣耀"),
            (r"吃鸡[^，。！]*?", "吃鸡"),
            (r"原神[^，。！]*?", "原神"),
            (r"帧率[^，。！]*?高", "帧率高"),
            (r"帧率[^，。！]*?稳定", "帧率稳定"),
            (r"帧率[^，。！]*?不稳", "帧率不稳"),
            (r"高帧率", "高帧率"),
            (r"120帧", "120帧"),
            (r"60帧", "60帧"),
            (r"锁[^，。！]*?帧", "锁帧"),
            (r"满帧", "满帧"),
            (r"掉帧", "掉帧"),
            (r"发热[^，。！]*?掉帧", "发热掉帧"),
            (r"发热[^，。！]*?卡顿", "发热卡顿"),
            (r"发烫[^，。！]*?掉帧", "发烫掉帧"),
            (r"发烫[^，。！]*?卡顿", "发烫卡顿"),
            (r"画质[^，。！]*?高清", "画质高清"),
            (r"画质[^，。！]*?高", "画质高"),
            (r"分辨率[^，。！]*?高", "分辨率高"),
            (r"3A[^，。！]*?游戏", "3A游戏"),
            (r"大型[^，。！]*?游戏", "大型游戏"),
            (r"重度[^，。！]*?游戏", "重度游戏"),
        ]
        for pattern, label in expand_patterns:
            if re.search(pattern, text):
                if label not in extracted:
                    extracted.append(label)
                is_mentioned_only = False

        if len(extracted) == 0:
            vague_patterns = [
                r"(?:游戏|打)[^，。！]*?(?:流畅|丝滑|顺滑|不卡|卡顿|掉帧)",
                r"(?:流畅|丝滑|顺滑|不卡|卡顿|掉帧)[^，。！]*?(?:游戏|打)",
            ]
            for vp in vague_patterns:
                if re.search(vp, text):
                    is_mentioned_only = True
                    break

    # ========== 丝滑流畅 | 多APP ==========
    elif primary_label == "丝滑流畅" and secondary_label == "多APP":
        expand_patterns = [
            (r"多[^，。！]*?APP[^，。！]*?切换", "多APP切换"),
            (r"多[^，。！]*?应用[^，。！]*?切换", "多应用切换"),
            (r"后台[^，。！]*?切换", "后台切换"),
            (r"后台[^，。！]*?运行", "后台运行"),
            (r"后台[^，。！]*?留存", "后台留存"),
            (r"不杀后台", "不杀后台"),
            (r"杀后台", "杀后台"),
            (r"同时[^，。！]*?运行", "同时运行"),
            (r"同时[^，。！]*?开", "同时开"),
            (r"多任务[^，。！]*?", "多任务"),
            (r"多开[^，。！]*?", "多开"),
            (r"切换[^，。！]*?应用", "切换应用"),
            (r"切换[^，。！]*?APP", "切换APP"),
            (r"应用[^，。！]*?切换", "应用切换"),
            (r"APP[^，。！]*?切换", "APP切换"),
            (r"切出去[^，。！]*?回来", "切出去回来"),
            (r"切出去[^，。！]*?重[^，。！]*?加载", "切出去重加载"),
            (r"重[^，。！]*?加载", "重加载"),
            (r"多设备[^，。！]*?互联", "多设备互联"),
            (r"设备[^，。！]*?互联", "设备互联"),
            (r"无缝[^，。！]*?联动", "无缝联动"),
            (r"接力[^，。！]*?", "接力"),
            (r"隔空投送[^，。！]*?", "隔空投送"),
            (r"通用[^，。！]*?剪贴板", "通用剪贴板"),
        ]
        for pattern, label in expand_patterns:
            if re.search(pattern, text):
                if label not in extracted:
                    extracted.append(label)
                is_mentioned_only = False

        if len(extracted) == 0:
            vague_patterns = [
                r"(?:多APP|多应用|后台|多任务)[^，。！]*?(?:流畅|丝滑|顺滑|不卡|卡顿|卡)",
                r"(?:流畅|丝滑|顺滑|不卡|卡顿|卡)[^，。！]*?(?:多APP|多应用|后台|多任务)",
            ]
            for vp in vague_patterns:
                if re.search(vp, text):
                    is_mentioned_only = True
                    break

    # ========== 卡顿 | 系统动画 ==========
    elif primary_label == "卡顿" and secondary_label == "系统动画":
        expand_patterns = [
            (r"动画[^，。！]*?卡顿", "动画卡顿"),
            (r"动画[^，。！]*?掉帧", "动画掉帧"),
            (r"动画[^，。！]*?不流畅", "动画不流畅"),
            (r"动画[^，。！]*?卡", "动画卡"),
            (r"打断动画[^，。！]*?", "打断动画问题"),
            (r"过渡动画[^，。！]*?", "过渡动画问题"),
            (r"返回动画[^，。！]*?", "返回动画问题"),
            (r"切换动画[^，。！]*?", "切换动画问题"),
            (r"掉帧", "掉帧"),
            (r"卡帧", "卡帧"),
            (r"抽帧", "抽帧"),
            (r"不跟手", "不跟手"),
            (r"延迟[^，。！]*?", "延迟"),
            (r"卡顿[^，。！]*?严重", "卡顿严重"),
            (r"明显[^，。！]*?卡顿", "明显卡顿"),
            (r"偶尔[^，。！]*?卡顿", "偶尔卡顿"),
            (r"小[^，。！]*?卡顿", "小卡顿"),
            (r"轻微[^，。！]*?卡顿", "轻微卡顿"),
            (r"掉帧[^，。！]*?严重", "掉帧严重"),
            (r"掉帧[^，。！]*?明显", "掉帧明显"),
        ]
        for pattern, label in expand_patterns:
            if re.search(pattern, text):
                if label not in extracted:
                    extracted.append(label)
                is_mentioned_only = False

        if len(extracted) == 0:
            vague_patterns = [
                r"(?:动画)[^，。！]*?(?:卡顿|掉帧|卡|不流畅)",
                r"(?:卡顿|掉帧|卡|不流畅)[^，。！]*?(?:动画)",
            ]
            for vp in vague_patterns:
                if re.search(vp, text):
                    is_mentioned_only = True
                    break

    # ========== 卡顿 | 打游戏 ==========
    elif primary_label == "卡顿" and secondary_label == "打游戏":
        expand_patterns = [
            (r"游戏[^，。！]*?卡顿", "游戏卡顿"),
            (r"游戏[^，。！]*?掉帧", "游戏掉帧"),
            (r"游戏[^，。！]*?卡", "游戏卡"),
            (r"游戏[^，。！]*?不流畅", "游戏不流畅"),
            (r"打[^，。！]*?游戏[^，。！]*?卡顿", "打游戏卡顿"),
            (r"打[^，。！]*?游戏[^，。！]*?掉帧", "打游戏掉帧"),
            (r"打[^，。！]*?游戏[^，。！]*?卡", "打游戏卡"),
            (r"王者[^，。！]*?卡顿", "王者荣耀卡顿"),
            (r"王者[^，。！]*?掉帧", "王者荣耀掉帧"),
            (r"吃鸡[^，。！]*?卡顿", "吃鸡卡顿"),
            (r"原神[^，。！]*?卡顿", "原神卡顿"),
            (r"帧率[^，。！]*?不稳", "帧率不稳"),
            (r"帧率[^，。！]*?低", "帧率低"),
            (r"掉帧[^，。！]*?严重", "掉帧严重"),
            (r"掉帧[^，。！]*?明显", "掉帧明显"),
            (r"发热[^，。！]*?掉帧", "发热掉帧"),
            (r"发热[^，。！]*?卡顿", "发热卡顿"),
            (r"发烫[^，。！]*?掉帧", "发烫掉帧"),
            (r"发烫[^，。！]*?卡顿", "发烫卡顿"),
            (r"锁[^，。！]*?60帧", "锁60帧"),
            (r"只能[^，。！]*?60帧", "只能60帧"),
            (r"卡成[^，。！]*?PPT", "卡成PPT"),
            (r"降[^，。！]*?亮度", "降亮度"),
            (r"不降[^，。！]*?亮度", "不降亮度"),
        ]
        for pattern, label in expand_patterns:
            if re.search(pattern, text):
                if label not in extracted:
                    extracted.append(label)
                is_mentioned_only = False

        if len(extracted) == 0:
            vague_patterns = [
                r"(?:游戏|打)[^，。！]*?(?:卡顿|掉帧|卡|不流畅)",
                r"(?:卡顿|掉帧|卡|不流畅)[^，。！]*?(?:游戏|打)",
            ]
            for vp in vague_patterns:
                if re.search(vp, text):
                    is_mentioned_only = True
                    break

    # ========== 稳定性 | 系统 ==========
    elif primary_label == "稳定性" and secondary_label == "系统":
        expand_patterns = [
            (r"系统[^，。！]*?稳定", "系统稳定"),
            (r"系统[^，。！]*?不稳定", "系统不稳定"),
            (r"系统[^，。！]*?崩溃", "系统崩溃"),
            (r"系统[^，。！]*?闪退", "系统闪退"),
            (r"闪退", "闪退"),
            (r"APP[^，。！]*?闪退", "APP闪退"),
            (r"应用[^，。！]*?闪退", "应用闪退"),
            (r"频繁[^，。！]*?闪退", "频繁闪退"),
            (r"崩溃", "崩溃"),
            (r"死机", "死机"),
            (r"重启", "重启"),
            (r"自动[^，。！]*?重启", "自动重启"),
            (r"黑屏", "黑屏"),
            (r"白屏", "白屏"),
            (r"卡死", "卡死"),
            (r"无响应", "无响应"),
            (r"ANR", "ANR无响应"),
            (r"Bug[^，。！]*?", "Bug"),
            (r"bug[^，。！]*?", "Bug"),
            (r"不[^，。！]*?稳定", "不稳定"),
            (r"稳定[^，。！]*?性", "稳定性"),
            (r"可靠[^，。！]*?", "可靠"),
            (r"不可靠[^，。！]*?", "不可靠"),
            (r"莫名[^，。！]*?bug", "莫名bug"),
            (r"莫名[^，。！]*?小[^，。！]*?bug", "莫名小bug"),
        ]
        for pattern, label in expand_patterns:
            if re.search(pattern, text):
                if label not in extracted:
                    extracted.append(label)
                is_mentioned_only = False

        if len(extracted) == 0:
            vague_patterns = [
                r"(?:系统|APP|应用)[^，。！]*?(?:稳定|闪退|崩溃|卡死|Bug|bug)",
                r"(?:稳定|闪退|崩溃|卡死|Bug|bug)[^，。！]*?(?:系统|APP|应用)",
            ]
            for vp in vague_patterns:
                if re.search(vp, text):
                    is_mentioned_only = True
                    break

    # 通用兜底：如果没有任何提取，检查是否有具体展开内容
    if len(extracted) == 0:
        # 检查是否有具体描述词
        detail_words = [
            "很", "非常", "特别", "明显", "有点", "稍微", "轻微", "严重",
            "太", "真", "确实", "的确", "实在", "完全", "根本",
            "比", "不如", "强于", "弱于", "碾压", "吊打", "完胜",
            "感觉", "觉得", "体验", "感受", "发现",
            "有时候", "偶尔", "经常", "总是", "从来",
            "快", "慢", "好", "差", "强", "弱",
        ]
        for word in detail_words:
            if word in text:
                is_mentioned_only = False
                break

        # 检查是否有具体功能/场景名词
        scene_words = [
            "微信", "WPS", "打字", "键盘", "剪视频", "剪辑", "拍照",
            "视频", "游戏", "王者", "吃鸡", "原神", "APP", "应用",
            "WiFi", "5G", "信号", "网络", "充电", "续航",
            "动画", "UI", "交互", "操作", "手势", "分屏", "小窗",
            "后台", "多任务", "切换", "打开", "启动",
        ]
        for word in scene_words:
            if word in text:
                is_mentioned_only = False
                break

    return extracted, is_mentioned_only


def process_batch(input_file, output_file):
    """处理单个batch"""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    output = []
    total_units = 0
    mentioned_only_count = 0
    expanded_count = 0

    for combo_key, units in data.items():
        parts = combo_key.split("|")
        primary_label = parts[0]
        secondary_label = parts[1] if len(parts) > 1 else ""

        combo_output = {
            "primary_label": primary_label,
            "secondary_label": secondary_label,
            "units": [],
            "extracted_summary": []
        }

        all_extracted = []

        for unit in units:
            total_units += 1
            text = unit.get("text", "")

            extracted, is_mentioned_only = extract_third_level(
                text, primary_label, secondary_label
            )

            if is_mentioned_only:
                mentioned_only_count += 1
            else:
                expanded_count += 1

            unit_output = {
                "note_id": unit.get("note_id", ""),
                "text": text,
                "extracted": extracted,
                "is_mentioned_only": is_mentioned_only,
                "ugc_title": unit.get("ugc_title", ""),
                "ugc_content": unit.get("ugc_content", "")[:200],
                "interaction": unit.get("interaction", 0),
                "note_url": unit.get("note_url", "")
            }

            combo_output["units"].append(unit_output)
            all_extracted.extend(extracted)

        # 去重并生成summary
        combo_output["extracted_summary"] = list(dict.fromkeys(all_extracted))
        output.append(combo_output)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"处理完成: {input_file}")
    print(f"  总Units: {total_units}")
    print(f"  仅提及: {mentioned_only_count}")
    print(f"  有展开: {expanded_count}")
    print(f"  输出: {output_file}")
    print()

    return output


if __name__ == "__main__":
    base_dir = "/Users/zhijian/workspace/ai-demand-research-v3/projects/华为苹果性能对比-2026-05-20/05-unit-tagging-v4"

    # 处理 batch 001
    process_batch(
        f"{base_dir}/phase3_v2_batch_001_input.json",
        f"{base_dir}/phase3_v2_batch_001_output.json"
    )

    # 处理 batch 002
    process_batch(
        f"{base_dir}/phase3_v2_batch_002_input.json",
        f"{base_dir}/phase3_v2_batch_002_output.json"
    )

    print("所有batch处理完成！")
