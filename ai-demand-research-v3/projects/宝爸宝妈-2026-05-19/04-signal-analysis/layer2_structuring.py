import json

# 读取输入文件
with open("/Users/zhijian/workspace/ai-demand-research-v3/projects/宝爸宝妈-2026-05-19/04-signal-analysis/layer2_input_batch_01.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 结构化处理函数
def structure_signal(item):
    signal_types = item.get("signal_types", [])
    title = item.get("title", "")
    content = item.get("content", "")
    text = f"{title}\n{content}"
    
    structured = {
        "scene": None,
        "pain_point": None,
        "need": None,
        "topic": None,
        "mentioned": None,
        "focus": None,
        "emotion": None,
        "emotion_intensity": None
    }
    
    # === 需求信号结构化 ===
    if "需求信号" in signal_types:
        # note_id: 6986ccde000000000a029ab4 - 上海育儿嫂避雷
        if item["note_id"] == "6986ccde000000000a029ab4":
            structured["scene"] = "雇佣育儿嫂照顾婴儿，夜间通过监控发现育儿嫂暴力对待宝宝"
            structured["pain_point"] = "育儿嫂在夜间多次粗暴对待宝宝，用力摔头部、扇巴掌，家政服务存在严重安全隐患"
            structured["need"] = "需要可靠的育儿嫂筛选机制、家政服务安全保障、暴力育儿嫂黑名单/避雷信息"
            structured["emotion"] = "愤怒/担忧/恐惧"
            structured["emotion_intensity"] = "高"
        # note_id: 684af466000000002301d260 - 找育儿嫂踩坑
        elif item["note_id"] == "684af466000000002301d260":
            structured["scene"] = "宝宝四个月大开始找育儿嫂，连续遇到三位不靠谱阿姨"
            structured["pain_point"] = "育儿嫂身份造假、频繁预支工资、隐瞒健康问题、缺乏职业道德、突然离职，找阿姨过程真心错付"
            structured["need"] = "需要可靠的家政中介筛选机制、育儿嫂背景核查、职业道德保障、替代方案"
            structured["emotion"] = "无奈/失望/焦虑"
            structured["emotion_intensity"] = "高"
        # note_id: 69fc504900000000230151d6 - 育儿补贴被侵占
        elif item["note_id"] == "69fc504900000000230151d6":
            structured["scene"] = "单亲妈妈申请育儿补贴，被孩子父亲偷偷申领并被村委驳回申请"
            structured["pain_point"] = "育儿补贴被孩子父亲侵占，村委偏袒对方，家庭支出AA不公，对方拖欠房租和生活费"
            structured["need"] = "需要法律途径维权、育儿补贴的公平分配机制、单亲妈妈的权益保障"
            structured["emotion"] = "愤怒/无助/焦虑"
            structured["emotion_intensity"] = "高"
    
    # === 使用反馈信号结构化 ===
    if "使用反馈信号" in signal_types:
        # note_id: 6778f90f00000000130188b1 - 育儿嫂吐槽雇主
        if item["note_id"] == "6778f90f00000000130188b1":
            structured["scene"] = "育儿嫂在雇主家工作，吐槽雇主各种要求和行为"
            structured["pain_point"] = "雇主反驳喂养顺序、要求新鲜早餐、不让吃饱、宝爸不搭手、宝妈总盯着，感到不被尊重"
            structured["emotion"] = "不满/委屈"
            structured["emotion_intensity"] = "中"
        # note_id: 65ff96c6000000001203c535 - 画画和勇敢是妈妈后天给予的天赋
        elif item["note_id"] == "65ff96c6000000001203c535":
            structured["scene"] = "分享个人成长经历，回忆父母高容错率对自己性格和能力的影响"
            structured["pain_point"] = "看到很多家长因小事胖揍孩子，担心低容错率教育会扼杀孩子的探索欲和创造力"
            structured["emotion"] = "正向/感恩"
            structured["emotion_intensity"] = "中"
        # note_id: 6986ccde000000000a029ab4 - 上海育儿嫂避雷
        elif item["note_id"] == "6986ccde000000000a029ab4":
            structured["scene"] = "发现雇佣的育儿嫂在夜间多次粗暴对待宝宝"
            structured["pain_point"] = "育儿嫂表面和善，背地里暴力对待婴儿，家政服务信任崩塌"
            structured["emotion"] = "愤怒/恐惧"
            structured["emotion_intensity"] = "高"
        # note_id: 685d0963000000001203e32d - 崔玉涛育儿知识发给爸爸
        elif item["note_id"] == "685d0963000000001203e32d":
            structured["scene"] = "把崔玉涛育儿知识发给爸爸，爸爸却认为冻到孩子"
            structured["pain_point"] = "长辈育儿观念与现代科学育儿知识冲突，代际育儿分歧难以沟通"
            structured["emotion"] = "无奈/不满"
            structured["emotion_intensity"] = "中"
        # note_id: 6868cf1d0000000013012b8e - 全职爸爸疲惫
        elif item["note_id"] == "6868cf1d0000000013012b8e":
            structured["scene"] = "全职爸爸独自带娃三年，日常被孩子严格看守"
            structured["pain_point"] = "24小时待命、睡眠困难、性格暴躁、与社会脱节、没有工资没有倾诉渠道，带娃极度折磨"
            structured["emotion"] = "疲惫/无奈"
            structured["emotion_intensity"] = "高"
        # note_id: 6937b071000000000d036140 - 教育无力感
        elif item["note_id"] == "6937b071000000000d036140":
            structured["scene"] = "孩子逐渐长大，发现教育效果不如预期"
            structured["pain_point"] = "娃越大越发现成长跟自己想怎么教育关系不大，产生教育无力感"
            structured["emotion"] = "无奈/困惑"
            structured["emotion_intensity"] = "中"
        # note_id: 674daec6000000000702ba90 - 一年级逆子
        elif item["note_id"] == "674daec6000000000702ba90":
            structured["scene"] = "看到孩子一年级的学业表现"
            structured["pain_point"] = "孩子学业表现极差，感到震惊和失望"
            structured["emotion"] = "震惊/无奈"
            structured["emotion_intensity"] = "高"
        # note_id: 68cb653d000000000e00fa48 - 三胎育儿感悟
        elif item["note_id"] == "68cb653d000000000e00fa48":
            structured["scene"] = "养育三个孩子后观察孩子性格差异"
            structured["pain_point"] = "无明确痛点，主要是观察发现孩子性格与生俱来"
            structured["emotion"] = "正向/幸福"
            structured["emotion_intensity"] = "中"
        # note_id: 69f0a0c5000000001a02d8b5 - 带娃日程
        elif item["note_id"] == "69f0a0c5000000001a02d8b5":
            structured["scene"] = "周末完整跟了一天带娃日程，整理出时间表"
            structured["pain_point"] = "带娃日程极其繁忙，精力消耗巨大，还要面对传统观念压力"
            structured["emotion"] = "疲惫/无奈"
            structured["emotion_intensity"] = "中"
        # note_id: 67b8ae71000000002902c210 - 二胎老大心理变化
        elif item["note_id"] == "67b8ae71000000002902c210":
            structured["scene"] = "二胎后观察到大女儿的心理变化和行为变化"
            structured["pain_point"] = "女儿从喜欢弟弟到排斥弟弟，老人言语伤害老大，自己努力平衡但仍有愧疚"
            structured["emotion"] = "愧疚/心疼"
            structured["emotion_intensity"] = "高"
        # note_id: 67c519e1000000000e005d29 - 育儿嫂没边界感
        elif item["note_id"] == "67c519e1000000000e005d29":
            structured["scene"] = "雇佣的育儿嫂缺乏边界感，做出让雇主不适的行为"
            structured["pain_point"] = "育儿嫂躺到雇主床上、发出逗猫逗狗声音、威胁孩子，缺乏职业边界"
            structured["emotion"] = "不满/困扰"
            structured["emotion_intensity"] = "中"
        # note_id: 684af466000000002301d260 - 找育儿嫂踩坑
        elif item["note_id"] == "684af466000000002301d260":
            structured["scene"] = "连续找三位育儿嫂都遇到各种问题"
            structured["pain_point"] = "阿姨身份造假、健康隐患、缺乏职业道德，家政服务体验极差"
            structured["emotion"] = "失望/无奈"
            structured["emotion_intensity"] = "高"
    
    # === 关注讨论信号结构化 ===
    if "关注讨论信号" in signal_types:
        # note_id: 68602d19000000000b02ce4d - 打孩子育儿话题
        if item["note_id"] == "68602d19000000000b02ce4d":
            structured["topic"] = "打孩子是否合理以及科学育儿方式"
            structured["mentioned"] = "体罚、家暴、蒙台梭利、育儿资料"
            structured["focus"] = "育儿方式的科学性、儿童心理发展、父母责任边界"
            structured["emotion"] = "负向/批判"
            structured["emotion_intensity"] = "高"
        # note_id: 6778f90f00000000130188b1 - 育儿嫂吐槽雇主
        elif item["note_id"] == "6778f90f00000000130188b1":
            structured["topic"] = "育儿嫂与雇主之间的矛盾和家政服务供需关系"
            structured["mentioned"] = "育儿嫂、雇主、中介、家务设备"
            structured["focus"] = "家政服务体验、雇主与育儿嫂的期望差异"
            structured["emotion"] = "负向/抱怨"
            structured["emotion_intensity"] = "中"
        # note_id: 66a8d5d3000000002701f0a9 - 攀比式育儿
        elif item["note_id"] == "66a8d5d3000000002701f0a9":
            structured["topic"] = "攀比式育儿现象和理性教育理念"
            structured["mentioned"] = "学业成绩、家教、夏令营"
            structured["focus"] = "教育公平、个体差异、陪伴与关爱"
            structured["emotion"] = "负向/批判"
            structured["emotion_intensity"] = "中"
        # note_id: 693a3106000000001e020f70 - 单亲爸爸养娃成本
        elif item["note_id"] == "693a3106000000001e020f70":
            structured["topic"] = "上海养两个孩子的每月开支和生育成本"
            structured["mentioned"] = "公立学校、私立小学、兴趣班、家教、保险、医美、旅游"
            structured["focus"] = "养娃经济成本、生活质量、生育意愿"
            structured["emotion"] = "中性/惊讶"
            structured["emotion_intensity"] = "中"
        # note_id: 683bb2f5000000002301c1bf - 父子定律
        elif item["note_id"] == "683bb2f5000000002301c1bf":
            structured["topic"] = "父亲参与育儿的重要性和爸爸带娃观念"
            structured["mentioned"] = "爸爸带娃、工作与家庭平衡"
            structured["focus"] = "父职参与、性别角色、育儿责任分担"
            structured["emotion"] = "正向/倡导"
            structured["emotion_intensity"] = "中"
        # note_id: 69247e2e000000001d03a17f - 凝视式育儿
        elif item["note_id"] == "69247e2e000000001d03a17f":
            structured["topic"] = "凝视式育儿/过度控制式育儿对孩子的影响"
            structured["mentioned"] = "直升机式育儿、蒙台梭利、自主感、内在动机"
            structured["focus"] = "儿童心理发展、自主性培养、父母边界"
            structured["emotion"] = "负向/批判"
            structured["emotion_intensity"] = "高"
        # note_id: 65ff96c6000000001203c535 - 画画和勇敢
        elif item["note_id"] == "65ff96c6000000001203c535":
            structured["topic"] = "父母容错率对孩子成长和性格的影响"
            structured["mentioned"] = "画画、容错率、体制内裸辞"
            structured["focus"] = "教育方式、儿童创造力、心理健康、亲子支持"
            structured["emotion"] = "正向/感恩"
            structured["emotion_intensity"] = "中"
        # note_id: 69f977480000000035029127 - 别叫儿子闺女
        elif item["note_id"] == "69f977480000000035029127":
            structured["topic"] = "亲子称呼背后的权力关系和独立人格"
            structured["mentioned"] = "儿子、闺女、独立人格、权力感"
            structured["focus"] = "亲子关系、人格独立、语言塑造"
            structured["emotion"] = "负向/批判"
            structured["emotion_intensity"] = "中"
        # note_id: 6986ccde000000000a029ab4 - 上海育儿嫂避雷
        elif item["note_id"] == "6986ccde000000000a029ab4":
            structured["topic"] = "育儿嫂暴力行为和家政服务安全"
            structured["mentioned"] = "育儿嫂、监控、上海宝妈"
            structured["focus"] = "儿童安全、家政服务信任、避雷提醒"
            structured["emotion"] = "负向/愤怒"
            structured["emotion_intensity"] = "高"
        # note_id: 684fdacd000000002001d9c8 - 男孩每个阶段喜欢的爸爸
        elif item["note_id"] == "684fdacd000000002001d9c8":
            structured["topic"] = "男孩成长过程中父亲角色的变化"
            structured["mentioned"] = "爸爸陪伴、游戏、讲故事、青春期"
            structured["focus"] = "父职教育、成长阶段、陪伴方式"
            structured["emotion"] = "正向/倡导"
            structured["emotion_intensity"] = "中"
        # note_id: 6868cf1d0000000013012b8e - 全职爸爸疲惫
        elif item["note_id"] == "6868cf1d0000000013012b8e":
            structured["topic"] = "全职爸爸的身心压力和父职困境"
            structured["mentioned"] = "全职爸爸、睡眠困难、社交脱节"
            structured["focus"] = "父职压力、心理健康、社会支持"
            structured["emotion"] = "负向/疲惫"
            structured["emotion_intensity"] = "高"
        # note_id: 6937b071000000000d036140 - 教育无力感
        elif item["note_id"] == "6937b071000000000d036140":
            structured["topic"] = "教育效果与父母努力之间的关系"
            structured["mentioned"] = "教育、成长"
            structured["focus"] = "教育观念、成长规律、父母焦虑"
            structured["emotion"] = "负向/无力"
            structured["emotion_intensity"] = "中"
        # note_id: 68de38db0000000003037e27 - 终结打压式教育
        elif item["note_id"] == "68de38db0000000003037e27":
            structured["topic"] = "打压式教育的危害和终结呼吁"
            structured["mentioned"] = "打压式教育、糟粕"
            structured["focus"] = "教育方式改革、心理健康、代际传承"
            structured["emotion"] = "负向/批判"
            structured["emotion_intensity"] = "高"
        # note_id: 695be531000000001a035371 - 要不要生小孩
        elif item["note_id"] == "695be531000000001a035371":
            structured["topic"] = "生育决策的思考框架和是否要生小孩"
            structured["mentioned"] = "新手奶爸、人生节点"
            structured["focus"] = "生育决策、人生规划、责任准备"
            structured["emotion"] = "中性/理性"
            structured["emotion_intensity"] = "低"
        # note_id: 691dacc1000000001f0047ad - 鸡娃KPI地狱
        elif item["note_id"] == "691dacc1000000001f0047ad":
            structured["topic"] = "鸡娃现象和过度教育的批判"
            structured["mentioned"] = "鸡娃、名校、年薪、投资"
            structured["focus"] = "教育焦虑、过度教育、亲子压力"
            structured["emotion"] = "负向/批判"
            structured["emotion_intensity"] = "高"
        # note_id: 68c13f3d000000001d02e51a - 育儿常识错误
        elif item["note_id"] == "68c13f3d000000001d02e51a":
            structured["topic"] = "传统育儿常识的错误和科学育儿知识"
            structured["mentioned"] = "剃胎毛、剪睫毛、捏鼻子、小偏方、人民日报"
            structured["focus"] = "科学育儿、传统误区、权威知识"
            structured["emotion"] = "负向/纠正"
            structured["emotion_intensity"] = "中"
        # note_id: 69f0a0c5000000001a02d8b5 - 带娃日程
        elif item["note_id"] == "69f0a0c5000000001a02d8b5":
            structured["topic"] = "带娃日程的繁忙程度和生育率话题"
            structured["mentioned"] = "带娃日程、生育率"
            structured["focus"] = "育儿负担、生育意愿、社会支持"
            structured["emotion"] = "负向/讽刺"
            structured["emotion_intensity"] = "中"
        # note_id: 67b8ae71000000002902c210 - 二胎老大心理
        elif item["note_id"] == "67b8ae71000000002902c210":
            structured["topic"] = "二胎家庭中老大的心理变化和平衡问题"
            structured["mentioned"] = "二胎、姐弟关系、老人育儿观念"
            structured["focus"] = "多孩家庭、心理平衡、公平对待"
            structured["emotion"] = "负向/愧疚"
            structured["emotion_intensity"] = "高"
        # note_id: 68987b7f0000000023031dd9 - 宠爱和溺爱
        elif item["note_id"] == "68987b7f0000000023031dd9":
            structured["topic"] = "宠爱与溺爱的区别和边界把握"
            structured["mentioned"] = "宠爱、溺爱、边界、哭闹"
            structured["focus"] = "教育方式、边界设定、情绪管理"
            structured["emotion"] = "中性/理性"
            structured["emotion_intensity"] = "中"
    
    item["structured"] = structured
    return item

# 逐条处理
output = [structure_signal(item) for item in data]

# 保存输出
with open("/Users/zhijian/workspace/ai-demand-research-v3/projects/宝爸宝妈-2026-05-19/04-signal-analysis/layer2_output_batch_01.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"处理完成，共 {len(output)} 条UGC")
