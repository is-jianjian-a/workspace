import json

with open('/Users/zhijian/workspace/ai-demand-research-v3/projects/宝爸宝妈-2026-05-19/04-signal-analysis/layer1_input_batch_07.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def classify_signals(item):
    note_id = item.get('note_id', '')

    signals = []

    # 逐条精确判断
    # 条1: 为什么当了妈以后继续做自己要被指责 — 情绪观点表达，无明确需求/产品反馈
    if note_id == '699a7c8d0000000009038b63':
        signals = ['关注讨论信号']

    # 条2: 怀个孕有什么好自豪的 — 孕期体验分享+观点表达
    elif note_id == '68d4e7be0000000013034ccc':
        signals = ['关注讨论信号']

    # 条3: 孕妇照还有必要拍吗 — 询问是否有必要做某事（决策需求）
    elif note_id == '696b5b56000000000a0284d8':
        signals = ['需求信号', '关注讨论信号']

    # 条4: 01年宝妈妊娠油 — 明确分享使用纽乐葆妊娠油的真实体验
    elif note_id == '69cb7784000000002102fc6a':
        signals = ['使用反馈信号', '关注讨论信号']

    # 条5: 妈妈们的巨大孕肚请爆照 — 互动话题，无明确需求
    elif note_id == '699492c7000000001a0347f6':
        signals = ['关注讨论信号']

    # 条6: 怀孕了发现胸有发育 — 身体变化担忧+讨论
    elif note_id == '69cfb941000000002200fac4':
        signals = ['关注讨论信号']

    # 条7: 孕23w新人博主Day1 — 纯自媒体运营内容，与育儿需求无关
    elif note_id == '690b22930000000004029a6a':
        signals = ['噪声']

    # 条8: 孕前vs孕8个月 — 孕期感悟+情感表达
    elif note_id == '69cc9f99000000001a02ad04':
        signals = ['关注讨论信号']

    # 条9: 32w西瓜和肚子一样圆 — 孕晚期身体感受分享
    elif note_id == '68862567000000002203de7a':
        signals = ['关注讨论信号']

    # 条10: 终于有人把怀孕后每周要做什么说清楚了 — 知识分享/攻略类
    elif note_id == '697beefc0000000021033d6d':
        signals = ['关注讨论信号']

    # 条11: 孕26w日渐圆润 — 孕期日常分享
    elif note_id == '6954f9a9000000001f00e5cd':
        signals = ['关注讨论信号']

    # 条12: 39w生娃去了 — 临产记录
    elif note_id == '69d8cd8c000000001d0181bd':
        signals = ['关注讨论信号']

    # 条13: 是不是大家都对孕妇大肚子好奇 — 孕期日常+互动
    elif note_id == '69bd22560000000022029d7e':
        signals = ['关注讨论信号']

    # 条14: 怀孕就猜到奶多 — 详细分享哺乳/吸奶器使用困境和体验
    elif note_id == '695cac14000000002102a361':
        signals = ['使用反馈信号', '关注讨论信号']

    # 条15: 39w+1还在上班 — 孕晚期工作状态+担忧
    elif note_id == '67b3fefb000000000603cb19':
        signals = ['关注讨论信号']

    # 条16: 26岁已生怀孕不会变老变丑 — 详细分享losoki红气铁使用体验
    elif note_id == '69feb84700000000360012b4':
        signals = ['使用反馈信号', '关注讨论信号']

    # 条17: 孕期耻骨分离疼粉色话筒 — 分享用粉色话筒按摩缓解疼痛的方法
    elif note_id == '68c66487000000001d0145fa':
        signals = ['使用反馈信号', '关注讨论信号']

    # 条18: 生育过的女人嘴真严 — 孕期便秘困扰+讨论
    elif note_id == '69f382380000000035027fb5':
        signals = ['关注讨论信号']

    # 条19: 上海孕搭子 — 明确想找上海孕妈妈交流群体（社交需求）
    elif note_id == '69d4b911000000002102eef3':
        signals = ['需求信号', '关注讨论信号']

    # 条20: 27w在家拍孕妇照 — 询问拍摄时间和风格推荐（决策需求）
    elif note_id == '675ffabb000000000b017931':
        signals = ['需求信号', '关注讨论信号']

    # 条21: 怀孕生子是我自愿选择的人生体验卡 — 心态感悟分享
    elif note_id == '66e99b99000000000c019114':
        signals = ['关注讨论信号']

    # 条22: 孕37周居家孕妇照和猫猫 — 孕期记录分享
    elif note_id == '69f7320000000000230150f8':
        signals = ['关注讨论信号']

    # 条23: 孕34+肚子越大穿的越辣 — 孕期穿搭分享
    elif note_id == '69ad3f3c000000002202e510':
        signals = ['关注讨论信号']

    # 条24: 有没有睡不着的小孕妇 — 寻求共鸣+交流（社交需求）
    elif note_id == '693ed627000000001e03abb2':
        signals = ['需求信号', '关注讨论信号']

    # 条25: 分享我的孕妇照 — 纯晒图，无实质内容
    elif note_id == '68beddf4000000001c036b39':
        signals = ['噪声']

    else:
        signals = ['关注讨论信号']

    item['layer1_signals'] = signals
    return item

results = [classify_signals(item) for item in data]

with open('/Users/zhijian/workspace/ai-demand-research-v3/projects/宝爸宝妈-2026-05-19/04-signal-analysis/layer1_output_batch_07.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"已处理 {len(results)} 条UGC，保存至 layer1_output_batch_07.json")
for i, r in enumerate(results):
    print(f"{i+1}. {r['note_id']}: {r['layer1_signals']}")
