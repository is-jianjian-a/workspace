import json
import re

def parse_count(val):
    """将点赞/收藏/评论数转换为整数"""
    if val is None:
        return 0
    if isinstance(val, (int, float)):
        return int(val)
    val = str(val).strip()
    if val == '' or val.lower() == 'null':
        return 0
    # 处理 "1.6万" 格式
    if '万' in val:
        num = val.replace('万', '').strip()
        try:
            return int(float(num) * 10000)
        except:
            return 0
    try:
        return int(float(val))
    except:
        return 0

def calc_heat(item):
    """基于互动量判断热度"""
    liked = parse_count(item.get('liked_count', 0))
    collected = parse_count(item.get('collected_count', 0))
    comment = parse_count(item.get('comment_count', 0))
    total = liked + collected + comment
    if total >= 5000:
        return '高'
    elif total >= 500:
        return '中'
    else:
        return '低'

def extract_topic(item):
    """提取关心话题"""
    title = item.get('title', '') or ''
    content = item.get('content', '') or ''
    signal_reason = item.get('signal_reason', '') or ''
    source_keyword = item.get('source_keyword', '') or ''
    full_text = title + ' ' + content + ' ' + signal_reason
    
    # 初始化
    topic = None
    sub_topic = None
    mentioned = None
    focus = None
    emotion = '中性'
    heat = calc_heat(item)
    
    # ===== 根据内容匹配话题 =====
    
    # 1. 体罚/打孩子
    if '打孩子' in full_text or '体罚' in full_text or '挨打' in full_text:
        topic = '打孩子教育方式'
        sub_topic = '体罚的合理性与反思'
        mentioned = None
        focus = '安全性/教育效果'
        emotion = '负向'
    
    # 2. 育儿嫂/月嫂
    elif '育儿嫂' in full_text or '月嫂' in full_text or '阿姨' in full_text:
        if '下药' in full_text or '嗜睡药' in full_text:
            topic = '育儿嫂安全问题'
            sub_topic = '育儿嫂给宝宝下药'
            mentioned = '西替利嗪'
            focus = '安全性'
            emotion = '负向'
        elif '减肥' in full_text:
            topic = '育儿嫂工作状态'
            sub_topic = '育儿嫂节食减肥影响带娃'
            mentioned = None
            focus = '质量/精力'
            emotion = '负向'
        elif '低级错误' in full_text or '错误' in full_text:
            topic = '育儿嫂专业水平'
            sub_topic = '育儿嫂常见操作错误'
            mentioned = None
            focus = '安全性/专业性'
            emotion = '负向'
        elif '价格' in full_text or '薪资' in full_text or '开价' in full_text:
            topic = '育儿嫂市场价格'
            sub_topic = '育儿嫂薪资与能力不匹配'
            mentioned = None
            focus = '价格/性价比'
            emotion = '负向'
        elif '下户' in full_text or '高需求' in full_text:
            topic = '自主带娃vs请育儿嫂'
            sub_topic = '辞退育儿嫂后自主带娃体验'
            mentioned = None
            focus = '效果/独立性'
            emotion = '正向'
        else:
            topic = '育儿嫂雇佣体验'
            sub_topic = '雇主与育儿嫂的矛盾'
            mentioned = None
            focus = '服务质量'
            emotion = '复杂'
    
    # 3. 攀比式育儿
    elif '攀比' in full_text or '别人家的孩子' in full_text:
        topic = '攀比式育儿'
        sub_topic = '拒绝盲目比较'
        mentioned = None
        focus = '教育理念'
        emotion = '正向'
    
    # 4. 养娃成本
    elif '开支' in full_text or '成本' in full_text or '花钱' in full_text or '6w' in full_text:
        topic = '养娃经济成本'
        sub_topic = '上海养两个孩子月开支6万'
        mentioned = None
        focus = '价格/经济压力'
        emotion = '中性'
    
    # 5. 爸爸参与育儿
    elif '爸爸' in full_text and ('带娃' in full_text or '育儿' in full_text or '参与' in full_text):
        if '全职爸爸' in full_text or '全职爸爸' in title:
            topic = '全职爸爸困境'
            sub_topic = '全职爸爸身心疲惫'
            mentioned = None
            focus = '情感/压力'
            emotion = '负向'
        elif '父性松弛' in full_text:
            topic = '父性松弛育儿'
            sub_topic = '爸爸不管娃引发的夫妻矛盾'
            mentioned = None
            focus = '分工/责任'
            emotion = '负向'
        elif '经济越发达' in full_text:
            topic = '奶爸经济现象'
            sub_topic = '经济发达地区爸爸带娃更多'
            mentioned = None
            focus = '社会趋势'
            emotion = '中性'
        else:
            topic = '爸爸参与育儿'
            sub_topic = '倡导爸爸承担育儿责任'
            mentioned = None
            focus = '责任/分工'
            emotion = '正向'
    
    # 6. 凝视式育儿/过度控制
    elif '凝视' in full_text or '过度控制' in full_text or '直升机' in full_text:
        topic = '凝视式育儿'
        sub_topic = '过度监督对孩子自主性的损害'
        mentioned = None
        focus = '自主性/心理健康'
        emotion = '负向'
    
    # 7. 容错率/父母容错
    elif '容错' in full_text or '犯错' in full_text:
        topic = '父母容错率'
        sub_topic = '容错率低的父母易养出焦虑孩子'
        mentioned = None
        focus = '心理健康/成长'
        emotion = '正向'
    
    # 8. 亲子称呼
    elif '儿子' in full_text and ('称呼' in full_text or '叫' in full_text):
        topic = '亲子称呼方式'
        sub_topic = '叫孩子儿子/闺女的权力关系'
        mentioned = None
        focus = '人格独立/尊重'
        emotion = '复杂'
    
    # 9. 教育无力感
    elif '教育' in full_text and ('无力' in full_text or '关系不大' in full_text):
        topic = '教育无力感'
        sub_topic = '孩子成长与教育方式关系不大'
        mentioned = None
        focus = '效果/认知'
        emotion = '负向'
    
    # 10. 打压式教育
    elif '打压' in full_text:
        topic = '打压式教育'
        sub_topic = '终结捆绑打压式教育'
        mentioned = None
        focus = '心理健康/教育效果'
        emotion = '负向'
    
    # 11. 生育决策
    elif '生小孩' in full_text or '生娃' in full_text or '要不要生' in full_text:
        topic = '生育决策'
        sub_topic = '判断是否生孩子的10个问题'
        mentioned = None
        focus = '决策/责任'
        emotion = '中性'
    
    # 12. 鸡娃
    elif '鸡娃' in full_text or 'KPI' in full_text:
        topic = '鸡娃现象批判'
        sub_topic = '过度教育的KPI地狱'
        mentioned = None
        focus = '教育效果/心理健康'
        emotion = '负向'
    
    # 13. 育儿常识误区
    elif '常识' in full_text and ('错' in full_text or '误区' in full_text):
        topic = '育儿常识误区'
        sub_topic = '传统育儿观念的纠正'
        mentioned = '人民日报'
        focus = '科学性/安全性'
        emotion = '中性'
    
    # 14. 带娃日程/精力消耗
    elif '日程' in full_text or '带娃' in full_text and '累' in full_text:
        topic = '带娃精力消耗'
        sub_topic = '完整带娃日程展示'
        mentioned = None
        focus = '精力/负担'
        emotion = '负向'
    
    # 15. 二胎/老大心理
    elif '二胎' in full_text or '老大' in full_text or '弟弟' in full_text or '妹妹' in full_text:
        if '端平' in full_text or '孙俪' in full_text:
            topic = '二胎平衡策略'
            sub_topic = '孙俪二胎育儿经验'
            mentioned = '孙俪'
            focus = '公平/情感'
            emotion = '正向'
        else:
            topic = '二胎老大心理'
            sub_topic = '二胎家庭中老大的心理变化'
            mentioned = None
            focus = '情感/公平'
            emotion = '复杂'
    
    # 16. 宠爱vs溺爱
    elif '宠爱' in full_text or '溺爱' in full_text:
        topic = '宠爱与溺爱界限'
        sub_topic = '有边界的爱vs无边界的纵容'
        mentioned = None
        focus = '教育理念/界限'
        emotion = '正向'
    
    # 17. 西式育儿
    elif '西式' in full_text or '快乐教育' in full_text:
        topic = '西式育儿反思'
        sub_topic = '质疑快乐教育的有效性'
        mentioned = '特朗普家族'
        focus = '教育理念/效果'
        emotion = '复杂'
    
    # 18. 母职外包
    elif '母职' in full_text or '外包' in full_text or '8000' in full_text:
        topic = '母职外包现象'
        sub_topic = '花钱购买育儿服务获得普通男性生活'
        mentioned = None
        focus = '性别分工/阶层'
        emotion = '复杂'
    
    # 19. 城市育儿成本
    elif '城市' in full_text and '养娃' in full_text:
        topic = '城市育儿困境'
        sub_topic = '城市养娃成本高压力大'
        mentioned = None
        focus = '经济压力/劳动力'
        emotion = '负向'
    
    # 20. 母子定律
    elif '母子定律' in full_text or '妈妈越' in full_text:
        topic = '母子互动规律'
        sub_topic = '妈妈行为对孩子的影响'
        mentioned = None
        focus = '教育方法/效果'
        emotion = '正向'
    
    # 21. 育儿博主批判
    elif '育儿博主' in full_text or '清北' in full_text:
        topic = '育儿博主可信度'
        sub_topic = '育儿博主人设与真实效果差距'
        mentioned = None
        focus = '真实性/效果'
        emotion = '复杂'
    
    # 22. 过度商量
    elif '商量' in full_text and ('边界' in full_text or '自由' in full_text):
        topic = '亲子边界设定'
        sub_topic = '给孩子边界里的自由'
        mentioned = None
        focus = '规则/自主性'
        emotion = '正向'
    
    # 23. 企业生育福利
    elif '生育福利' in full_text or '育儿假' in full_text or '45万' in full_text:
        topic = '企业生育福利'
        sub_topic = '韩国游戏公司生娃奖励45万'
        mentioned = 'Krafton'
        focus = '政策/福利'
        emotion = '正向'
    
    # 24. 睡眠安全
    elif '睡眠' in full_text and ('安全' in full_text or '分床' in full_text):
        topic = '宝宝睡眠安全'
        sub_topic = '婴儿睡眠安全要点'
        mentioned = None
        focus = '安全性'
        emotion = '正向'
    
    # 25. 循证妈妈离婚率
    elif '循证' in full_text or '离婚率' in full_text:
        topic = '循证妈妈婚姻危机'
        sub_topic = '育儿认知差异导致夫妻矛盾'
        mentioned = None
        focus = '认知/沟通'
        emotion = '负向'
    
    # 26. 全职带娃决策
    elif '全职' in full_text and ('带娃' in full_text or '太太' in full_text):
        topic = '全职带娃决策'
        sub_topic = '双职工家庭是否全职带娃'
        mentioned = None
        focus = '经济/陪伴'
        emotion = '复杂'
    
    # 27. 郑渊洁/毁孩子
    elif '郑渊洁' in full_text or '毁掉' in full_text:
        topic = '错误育儿方式'
        sub_topic = '摧毁孩子自尊的7条方法'
        mentioned = '郑渊洁'
        focus = '心理健康/教育效果'
        emotion = '负向'
    
    # 28. 宝妈恶意
    elif '宝妈' in full_text and ('恶意' in full_text or '厌蠢' in full_text):
        topic = '宝妈群体社会认知'
        sub_topic = '网络对宝妈的恶意与偏见'
        mentioned = None
        focus = '社会认知/情感'
        emotion = '负向'
    
    # 29. 高敏感孩子
    elif '高敏感' in full_text or '敏娃' in full_text:
        topic = '高敏感孩子养育'
        sub_topic = '过度共情高敏感孩子效果适得其反'
        mentioned = None
        focus = '方法/效果'
        emotion = '复杂'
    
    # 30. 夫妻分工
    elif '分工' in full_text or '值班表' in full_text:
        topic = '夫妻育儿分工'
        sub_topic = '减少争吵的带娃分工方案'
        mentioned = None
        focus = '分工/效率'
        emotion = '正向'
    
    # 31. 小红书育儿焦虑
    elif '小红书' in full_text and '焦虑' in full_text:
        topic = '网络育儿焦虑'
        sub_topic = '少刷小红书减少育儿焦虑'
        mentioned = '小红书'
        focus = '心理健康/信息筛选'
        emotion = '正向'
    
    # 32. 海姆立克急救
    elif '海姆立克' in full_text or '噎到' in full_text or '卡着' in full_text:
        topic = '婴幼儿急救知识'
        sub_topic = '海姆立克急救法救窒息宝宝'
        mentioned = None
        focus = '安全性/知识'
        emotion = '负向'
    
    # 33. 双语教育
    elif '双语' in full_text or '英语启蒙' in full_text:
        if 'SSS' in full_text or '儿歌' in full_text:
            topic = '英语启蒙方法'
            sub_topic = 'SSS儿歌做英语启蒙的有效性'
            mentioned = 'SSS儿歌'
            focus = '效果/方法'
            emotion = '复杂'
        else:
            topic = '双语教育'
            sub_topic = '双语孩子的语言发展'
            mentioned = None
            focus = '效果/发展'
            emotion = '正向'
    
    # 34. A娃/ADHD
    elif 'A娃' in full_text or 'ADHD' in full_text:
        topic = 'ADHD儿童养育'
        sub_topic = 'A娃的日常表现与养育挑战'
        mentioned = None
        focus = '方法/心理'
        emotion = '复杂'
    
    # 35. 育儿内容消费
    elif '育儿博主' in full_text and ('vlog' in full_text or '美女' in full_text):
        topic = '育儿内容消费偏好'
        sub_topic = '宝妈转向看未婚美女vlog'
        mentioned = None
        focus = '心理需求/逃避'
        emotion = '负向'
    
    # ===== 早教类 =====
    # 36. 早教必要性
    elif '早教' in full_text or '早教班' in full_text:
        if '有必要' in full_text or '值不值' in full_text or '有没有用' in full_text:
            topic = '早教必要性讨论'
            sub_topic = '早教班是否值得上'
            mentioned = None
            focus = '效果/性价比'
            emotion = '复杂'
        elif '金宝贝' in full_text or '美吉姆' in full_text:
            topic = '早教机构兴衰'
            sub_topic = '金宝贝美吉姆从兴盛到衰落'
            mentioned = '金宝贝/美吉姆'
            focus = '行业变化/选择'
            emotion = '复杂'
        elif '毒动画' in full_text or '邪典' in full_text:
            topic = '有毒早教内容'
            sub_topic = '警惕儿童邪典视频危害'
            mentioned = None
            focus = '安全性/认知'
            emotion = '负向'
        elif '蒙氏' in full_text:
            topic = '蒙氏早教理念'
            sub_topic = '蒙氏教育解决带娃难题'
            mentioned = '蒙台梭利'
            focus = '方法/效果'
            emotion = '正向'
        elif '托育' in full_text or '托班' in full_text:
            topic = '托育选择'
            sub_topic = '送托育是否可怜/实用'
            mentioned = None
            focus = '实用性/情感'
            emotion = '复杂'
        elif '社区' in full_text or '宝宝屋' in full_text or '免费' in full_text:
            topic = '免费早教资源'
            sub_topic = '上海社区免费早教体验'
            mentioned = '随申办/宝宝屋'
            focus = '性价比/便利性'
            emotion = '正向'
        elif '巧虎' in full_text:
            topic = '早教产品体验'
            sub_topic = '巧虎订阅版本问题'
            mentioned = '巧虎'
            focus = '产品体验/性价比'
            emotion = '负向'
        elif '逻辑思维' in full_text or '骗局' in full_text:
            topic = '早教课程质疑'
            sub_topic = '少儿思维课新骗局的质疑'
            mentioned = None
            focus = '科学性/效果'
            emotion = '负向'
        elif '体验' in full_text or '测评' in full_text:
            topic = '早教课程体验'
            sub_topic = '早教课真实体验分享'
            mentioned = None
            focus = '效果/性价比'
            emotion = '复杂'
        elif '绘本' in full_text or '玩具' in full_text:
            topic = '早教绘本玩具'
            sub_topic = '0-3岁早教绘本玩具推荐'
            mentioned = None
            focus = '产品/效果'
            emotion = '正向'
        elif '英语启蒙' in full_text or '动画片' in full_text:
            topic = '英语启蒙资源'
            sub_topic = '英语启蒙动画推荐'
            mentioned = None
            focus = '方法/资源'
            emotion = '正向'
        elif '胎教' in full_text:
            topic = '胎教方法'
            sub_topic = '4种胎教方式生出高智商宝宝'
            mentioned = None
            focus = '方法/效果'
            emotion = '正向'
        elif '专注力' in full_text:
            topic = '专注力培养'
            sub_topic = '100天专注力游戏打卡'
            mentioned = None
            focus = '方法/效果'
            emotion = '正向'
        elif '公立' in full_text and '私立' in full_text:
            topic = '公立vs私立幼儿园'
            sub_topic = '公立幼儿园2年什么都不会'
            mentioned = None
            focus = '效果/选择'
            emotion = '负向'
        elif '三岁前' in full_text or '能力' in full_text:
            topic = '早期能力培养'
            sub_topic = '三岁前培养6种底层能力'
            mentioned = None
            focus = '方法/发展'
            emotion = '正向'
        elif '崔玉涛' in full_text:
            topic = '语言启蒙方法'
            sub_topic = '崔玉涛语言爆发期建议'
            mentioned = '崔玉涛'
            focus = '方法/效果'
            emotion = '正向'
        elif '桌游' in full_text:
            topic = '桌游教学方法'
            sub_topic = '桌游规则拆分教学'
            mentioned = None
            focus = '方法/效果'
            emotion = '正向'
        elif '国家' in full_text and '资源' in full_text:
            topic = '免费早教资源'
            sub_topic = '国家免费早教音频库'
            mentioned = None
            focus = '资源/性价比'
            emotion = '正向'
        elif '卫健委' in full_text:
            topic = '权威早教指南'
            sub_topic = '卫健委0-6岁早教指南'
            mentioned = '卫健委'
            focus = '科学性/权威性'
            emotion = '正向'
        elif '张雪峰' in full_text:
            topic = '英语启蒙资源'
            sub_topic = '张雪峰推荐9部英语动画'
            mentioned = '张雪峰'
            focus = '资源/方法'
            emotion = '正向'
        elif '感官书' in full_text or '五感' in full_text:
            topic = '感官启蒙绘本'
            sub_topic = '五感启蒙感官绘本推荐'
            mentioned = None
            focus = '产品/效果'
            emotion = '正向'
        elif '上海' in full_text and '早教' in full_text:
            topic = '上海早教选择'
            sub_topic = '上海早教机构体验盘点'
            mentioned = None
            focus = '选择/性价比'
            emotion = '复杂'
        elif '一岁' in full_text and '早教' in full_text:
            topic = '1岁早教决策'
            sub_topic = '1岁宝宝是否有必要上早教'
            mentioned = None
            focus = '必要性/选择'
            emotion = '复杂'
        else:
            topic = '早教相关讨论'
            sub_topic = '早教方法或体验分享'
            mentioned = None
            focus = '方法/效果'
            emotion = '中性'
    
    # ===== 孕期类 =====
    # 37. 孕期身体变化
    elif '孕期' in full_text or '怀孕' in full_text:
        if '耻骨' in full_text or '疼痛' in full_text:
            topic = '孕期身体不适'
            sub_topic = '孕期耻骨分离疼痛'
            mentioned = None
            focus = '身体/缓解'
            emotion = '负向'
        elif '便秘' in full_text or '拉不出' in full_text:
            topic = '孕期便秘困扰'
            sub_topic = '怀孕期间便秘问题'
            mentioned = None
            focus = '身体/健康'
            emotion = '负向'
        elif '妊娠纹' in full_text:
            topic = '妊娠纹接受度'
            sub_topic = '与妊娠纹和解'
            mentioned = None
            focus = '身体/心理'
            emotion = '正向'
        elif '孕照' in full_text or '孕妇照' in full_text:
            topic = '孕妇照拍摄'
            sub_topic = '孕期拍照记录'
            mentioned = None
            focus = '纪念/审美'
            emotion = '正向'
        elif '入盆' in full_text:
            topic = '胎儿入盆'
            sub_topic = '35周入盆体验分享'
            mentioned = None
            focus = '身体/分娩准备'
            emotion = '中性'
        elif '奶多' in full_text or '堵奶' in full_text or '通乳' in full_text:
            topic = '哺乳期堵奶'
            sub_topic = '产后严重堵奶经历'
            mentioned = None
            focus = '身体/痛苦'
            emotion = '负向'
        elif '发动' in full_text or '宫缩' in full_text:
            topic = '临产征兆'
            sub_topic = '39周等待发动'
            mentioned = None
            focus = '身体/焦虑'
            emotion = '复杂'
        elif '孕搭子' in full_text:
            topic = '孕期社交'
            sub_topic = '寻找上海孕搭子'
            mentioned = None
            focus = '社交/支持'
            emotion = '中性'
        elif '孕晚期' in full_text and ('难受' in full_text or '顶' in full_text):
            topic = '孕晚期不适'
            sub_topic = '32周孕晚期身体负担'
            mentioned = None
            focus = '身体/痛苦'
            emotion = '负向'
        elif '穿搭' in full_text or '衣服' in full_text or '裙子' in full_text:
            topic = '孕期穿搭'
            sub_topic = '孕期时尚穿搭分享'
            mentioned = None
            focus = '审美/自信'
            emotion = '正向'
        elif '身材焦虑' in full_text or '孕肚羞耻' in full_text:
            topic = '孕期身材自信'
            sub_topic = '拒绝孕肚羞耻'
            mentioned = None
            focus = '心理/自信'
            emotion = '正向'
        elif '当妈' in full_text and ('指责' in full_text or '束缚' in full_text):
            topic = '妈妈身份认同'
            sub_topic = '当妈后维持自我被指责'
            mentioned = None
            focus = '身份/自我'
            emotion = '负向'
        elif '自豪' in full_text or '神奇' in full_text:
            topic = '孕期身体自豪感'
            sub_topic = '怀孕的身体变化与自豪'
            mentioned = None
            focus = '身体/心理'
            emotion = '正向'
        elif '修行' in full_text or '没人管' in full_text:
            topic = '孕期孤独感'
            sub_topic = '怀孕是一个人的修行'
            mentioned = None
            focus = '情感/孤独'
            emotion = '负向'
        elif '登记' in full_text or '损失' in full_text:
            topic = '孕期福利登记'
            sub_topic = '怀孕登记领取福利'
            mentioned = None
            focus = '福利/信息'
            emotion = '正向'
        elif '每周' in full_text or '任务清单' in full_text:
            topic = '孕期每周指南'
            sub_topic = '怀孕每周任务清单'
            mentioned = None
            focus = '知识/指导'
            emotion = '正向'
        elif '博主' in full_text and '孕期' in full_text:
            topic = '孕期自媒体'
            sub_topic = '新手孕妈做plog博主'
            mentioned = None
            focus = '事业/记录'
            emotion = '正向'
        elif '勇敢' in full_text or '伟大' in full_text:
            topic = '孕育生命的勇气'
            sub_topic = '选择孕育生命的勇敢决定'
            mentioned = None
            focus = '情感/价值'
            emotion = '正向'
        elif '肚子大' in full_text or '好奇' in full_text:
            topic = '孕肚社交'
            sub_topic = '孕妇大肚子引发好奇'
            mentioned = None
            focus = '社交/身体'
            emotion = '正向'
        else:
            topic = '孕期生活分享'
            sub_topic = '孕期日常体验'
            mentioned = None
            focus = '身体/情感'
            emotion = '中性'
    
    # 默认处理
    if topic is None:
        topic = source_keyword + '相关讨论'
        sub_topic = '用户关注和讨论的话题'
        mentioned = None
        focus = '信息/观点'
        emotion = '中性'
    
    return {
        'topic': topic,
        'sub_topic': sub_topic,
        'mentioned': mentioned,
        'focus': focus,
        'emotion': emotion,
        'heat': heat
    }

# 读取输入文件
with open('/Users/zhijian/workspace/ai-demand-research-v3/projects/宝爸宝妈-2026-05-19/04-signal-analysis/layer2_attention_batch_01.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 处理每条数据
output = []
for item in data:
    topic_info = extract_topic(item)
    output_item = dict(item)
    output_item.update(topic_info)
    output.append(output_item)

# 保存输出文件
with open('/Users/zhijian/workspace/ai-demand-research-v3/projects/宝爸宝妈-2026-05-19/04-signal-analysis/layer2_attention_output_batch_01.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"处理完成，共 {len(output)} 条数据")
print(f"输出文件已保存")
