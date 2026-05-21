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
    """提取关心话题 - 基于规则匹配"""
    title = item.get('title', '') or ''
    content = item.get('content', '') or ''
    signal_reason = item.get('signal_reason', '') or ''
    source_keyword = item.get('source_keyword', '') or ''
    full_text = title + ' ' + content + ' ' + signal_reason
    
    topic = None
    sub_topic = None
    mentioned = None
    focus = None
    emotion = '中性'
    heat = calc_heat(item)
    
    # ===== 精确匹配规则（按优先级排序）=====
    
    # 1. 体罚/打孩子教育方式
    if any(k in full_text for k in ['打孩子', '体罚', '挨打', '该不该打']):
        topic = '打孩子教育方式'
        sub_topic = '体罚合理性与替代方案'
        mentioned = None
        focus = '安全性/教育效果'
        emotion = '负向'
    
    # 2. 育儿嫂安全问题（下药）
    elif '下药' in full_text or ('嗜睡药' in full_text and '育儿嫂' in full_text):
        topic = '育儿嫂安全问题'
        sub_topic = '育儿嫂给宝宝下药的隐患'
        mentioned = '西替利嗪'
        focus = '安全性'
        emotion = '负向'
    
    # 3. 育儿嫂专业水平/错误操作
    elif '育儿嫂' in full_text and any(k in full_text for k in ['低级错误', '错误处理', '错误操作', '经验主义']):
        topic = '育儿嫂专业水平'
        sub_topic = '育儿嫂常见操作错误与隐患'
        mentioned = None
        focus = '安全性/专业性'
        emotion = '负向'
    
    # 4. 育儿嫂节食减肥
    elif '育儿嫂' in full_text and '减肥' in full_text:
        topic = '育儿嫂工作状态'
        sub_topic = '育儿嫂节食减肥影响带娃质量'
        mentioned = None
        focus = '精力/质量'
        emotion = '负向'
    
    # 5. 育儿嫂市场价格
    elif '育儿嫂' in full_text and any(k in full_text for k in ['价格', '薪资', '开价', '赶上上海']):
        topic = '育儿嫂市场价格'
        sub_topic = '育儿嫂薪资与技能不匹配'
        mentioned = None
        focus = '价格/性价比'
        emotion = '负向'
    
    # 6. 自主带娃vs请育儿嫂
    elif '育儿嫂' in full_text and '下户' in full_text:
        topic = '自主带娃vs请育儿嫂'
        sub_topic = '辞退育儿嫂后自主带娃的真实体验'
        mentioned = None
        focus = '独立性/效果'
        emotion = '正向'
    
    # 7. 育儿嫂雇佣体验
    elif '育儿嫂' in full_text or ('月嫂' in full_text and '不好当' in full_text):
        topic = '育儿嫂雇佣体验'
        sub_topic = '雇主与育儿嫂的矛盾与体验'
        mentioned = None
        focus = '服务质量'
        emotion = '复杂'
    
    # 8. 月嫂管理
    elif '月嫂' in full_text and ('立规矩' in full_text or '纸条' in full_text):
        topic = '月嫂管理'
        sub_topic = '给月嫂立规矩的沟通方式'
        mentioned = None
        focus = '沟通/管理'
        emotion = '复杂'
    
    # 9. 育儿嫂依赖
    elif '阿姨不捡' in full_text or ('阿姨' in full_text and '没人敢动' in full_text):
        topic = '育儿嫂依赖现象'
        sub_topic = '有育儿嫂后夫妻变懒'
        mentioned = None
        focus = '依赖性/生活习惯'
        emotion = '复杂'
    
    # 10. 攀比式育儿
    elif '攀比' in full_text or '别人家的孩子' in full_text:
        topic = '攀比式育儿'
        sub_topic = '拒绝盲目比较，专注孩子自身'
        mentioned = None
        focus = '教育理念'
        emotion = '正向'
    
    # 11. 养娃经济成本
    elif any(k in full_text for k in ['每月6W', '养娃成本', '吞金兽', '年薪50W']):
        topic = '养娃经济成本'
        sub_topic = '一线城市养娃开支明细'
        mentioned = None
        focus = '价格/经济压力'
        emotion = '中性'
    
    # 12. 全职爸爸困境
    elif '全职爸爸' in full_text or ('爸爸' in full_text and '再不休息就要死去' in full_text):
        topic = '全职爸爸困境'
        sub_topic = '全职爸爸身心疲惫与压力'
        mentioned = None
        focus = '情感/压力'
        emotion = '负向'
    
    # 13. 父性松弛
    elif '父性松弛' in full_text or ('老公' in full_text and '不管娃' in full_text):
        topic = '父性松弛育儿'
        sub_topic = '爸爸不管娃引发的夫妻矛盾'
        mentioned = None
        focus = '分工/责任'
        emotion = '负向'
    
    # 14. 爸爸参与育儿
    elif '爸爸' in full_text and any(k in full_text for k in ['带娃', '育儿', '参与', '不只是妈妈']):
        topic = '爸爸参与育儿'
        sub_topic = '倡导爸爸承担育儿责任'
        mentioned = None
        focus = '责任/分工'
        emotion = '正向'
    
    # 15. 奶爸经济
    elif '奶爸经济' in full_text or ('经济越发达' in full_text and '奶爸' in full_text):
        topic = '奶爸经济现象'
        sub_topic = '经济发达地区爸爸带娃趋势'
        mentioned = None
        focus = '社会趋势'
        emotion = '中性'
    
    # 16. 凝视式育儿
    elif '凝视式育儿' in full_text or ('过度控制' in full_text and '直升机' in full_text):
        topic = '凝视式育儿'
        sub_topic = '过度监督对孩子自主性的损害'
        mentioned = None
        focus = '自主性/心理健康'
        emotion = '负向'
    
    # 17. 父母容错率
    elif '容错' in full_text or ('容错率低的父母' in full_text):
        topic = '父母容错率'
        sub_topic = '容错率影响孩子焦虑程度'
        mentioned = None
        focus = '心理健康/成长'
        emotion = '正向'
    
    # 18. 亲子称呼
    elif ('儿子' in full_text or '闺女' in full_text) and ('称呼' in full_text or '权力' in full_text or '附属品' in full_text):
        topic = '亲子称呼方式'
        sub_topic = '叫孩子儿子/闺女暗含权力关系'
        mentioned = None
        focus = '人格独立/尊重'
        emotion = '复杂'
    
    # 19. 教育无力感
    elif '教育' in full_text and ('关系不大' in full_text or '无力' in full_text):
        topic = '教育无力感'
        sub_topic = '孩子成长与教育方式关系不大'
        mentioned = None
        focus = '效果/认知'
        emotion = '负向'
    
    # 20. 打压式教育
    elif '打压式教育' in full_text or '捆绑打压' in full_text:
        topic = '打压式教育'
        sub_topic = '终结捆绑打压式教育'
        mentioned = None
        focus = '心理健康/教育效果'
        emotion = '负向'
    
    # 21. 生育决策
    elif any(k in full_text for k in ['要不要生小孩', '生小孩', '生育决策', '奢侈品']):
        topic = '生育决策'
        sub_topic = '判断是否生孩子的思考框架'
        mentioned = None
        focus = '决策/责任'
        emotion = '中性'
    
    # 22. 鸡娃现象
    elif '鸡娃' in full_text or ('KPI' in full_text and '便签' in full_text):
        topic = '鸡娃现象批判'
        sub_topic = '过度教育的KPI地狱'
        mentioned = None
        focus = '教育效果/心理健康'
        emotion = '负向'
    
    # 23. 育儿常识误区
    elif '常识' in full_text and any(k in full_text for k in ['错', '误区', '人民日报']):
        topic = '育儿常识误区'
        sub_topic = '传统育儿观念的纠正'
        mentioned = '人民日报'
        focus = '科学性/安全性'
        emotion = '中性'
    
    # 24. 带娃精力消耗
    elif '日程' in full_text and ('生育率杀手' in full_text or '带娃' in full_text):
        topic = '带娃精力消耗'
        sub_topic = '完整带娃日程展示'
        mentioned = None
        focus = '精力/负担'
        emotion = '负向'
    
    # 25. 二胎平衡
    elif '二胎' in full_text and ('端平' in full_text or '孙俪' in full_text):
        topic = '二胎平衡策略'
        sub_topic = '孙俪二胎育儿经验'
        mentioned = '孙俪'
        focus = '公平/情感'
        emotion = '正向'
    
    # 26. 二胎老大心理
    elif '二胎' in full_text or ('老大' in full_text and ('弟弟' in full_text or '妹妹' in full_text)):
        topic = '二胎老大心理'
        sub_topic = '二胎家庭中老大的心理变化'
        mentioned = None
        focus = '情感/公平'
        emotion = '复杂'
    
    # 27. 宠爱vs溺爱
    elif '宠爱' in full_text or '溺爱' in full_text:
        topic = '宠爱与溺爱界限'
        sub_topic = '有边界的爱vs无边界的纵容'
        mentioned = None
        focus = '教育理念/界限'
        emotion = '正向'
    
    # 28. 西式育儿反思
    elif '西式' in full_text or '快乐教育' in full_text:
        topic = '西式育儿反思'
        sub_topic = '质疑快乐教育的有效性'
        mentioned = '特朗普家族'
        focus = '教育理念/效果'
        emotion = '复杂'
    
    # 29. 母职外包
    elif '母职' in full_text or ('8000' in full_text and '普通男人' in full_text):
        topic = '母职外包现象'
        sub_topic = '花钱购买育儿服务获得普通男性生活'
        mentioned = None
        focus = '性别分工/阶层'
        emotion = '复杂'
    
    # 30. 城市育儿困境
    elif '城市' in full_text and '养娃' in full_text:
        topic = '城市育儿困境'
        sub_topic = '城市养娃成本高压力大'
        mentioned = None
        focus = '经济压力/劳动力'
        emotion = '负向'
    
    # 31. 母子定律
    elif '母子定律' in full_text or '妈妈越' in full_text:
        topic = '母子互动规律'
        sub_topic = '妈妈行为对孩子的影响'
        mentioned = None
        focus = '教育方法/效果'
        emotion = '正向'
    
    # 32. 育儿博主可信度
    elif '育儿博主' in full_text and ('清北' in full_text or '人设' in full_text):
        topic = '育儿博主可信度'
        sub_topic = '育儿博主人设与真实效果差距'
        mentioned = None
        focus = '真实性/效果'
        emotion = '复杂'
    
    # 33. 亲子边界
    elif '商量' in full_text and ('边界' in full_text or '自由' in full_text):
        topic = '亲子边界设定'
        sub_topic = '给孩子边界里的自由'
        mentioned = None
        focus = '规则/自主性'
        emotion = '正向'
    
    # 34. 企业生育福利
    elif any(k in full_text for k in ['45万', '育儿假', '生育福利', 'Krafton']):
        topic = '企业生育福利'
        sub_topic = '韩国企业生娃奖励45万'
        mentioned = 'Krafton'
        focus = '政策/福利'
        emotion = '正向'
    
    # 35. 宝宝睡眠安全
    elif '睡眠' in full_text and any(k in full_text for k in ['安全', '分床', '窒息']):
        topic = '宝宝睡眠安全'
        sub_topic = '婴儿睡眠安全要点'
        mentioned = None
        focus = '安全性'
        emotion = '正向'
    
    # 36. 循证妈妈离婚率
    elif '循证' in full_text or ('离婚率' in full_text and '妈妈' in full_text):
        topic = '循证妈妈婚姻危机'
        sub_topic = '育儿认知差异导致夫妻矛盾'
        mentioned = None
        focus = '认知/沟通'
        emotion = '负向'
    
    # 37. 全职带娃决策
    elif '全职' in full_text and ('带娃' in full_text or '太太' in full_text or '建议' in full_text):
        topic = '全职带娃决策'
        sub_topic = '双职工家庭是否全职带娃'
        mentioned = None
        focus = '经济/陪伴'
        emotion = '复杂'
    
    # 38. 郑渊洁毁孩子
    elif '郑渊洁' in full_text or '毁掉孩子' in full_text:
        topic = '错误育儿方式'
        sub_topic = '摧毁孩子自尊的7条方法'
        mentioned = '郑渊洁'
        focus = '心理健康/教育效果'
        emotion = '负向'
    
    # 39. 宝妈社会认知
    elif '宝妈' in full_text and any(k in full_text for k in ['恶意', '厌蠢', '神奇的人群']):
        topic = '宝妈群体社会认知'
        sub_topic = '网络对宝妈的恶意与偏见'
        mentioned = None
        focus = '社会认知/情感'
        emotion = '负向'
    
    # 40. 高敏感孩子
    elif '高敏感' in full_text or '敏娃' in full_text:
        topic = '高敏感孩子养育'
        sub_topic = '过度共情高敏感孩子效果适得其反'
        mentioned = None
        focus = '方法/效果'
        emotion = '复杂'
    
    # 41. 夫妻育儿分工
    elif '分工' in full_text and ('带娃' in full_text or '减少争吵' in full_text):
        topic = '夫妻育儿分工'
        sub_topic = '减少争吵的带娃分工方案'
        mentioned = None
        focus = '分工/效率'
        emotion = '正向'
    
    # 42. 网络育儿焦虑
    elif '小红书' in full_text and '焦虑' in full_text:
        topic = '网络育儿焦虑'
        sub_topic = '少刷小红书减少育儿焦虑'
        mentioned = '小红书'
        focus = '心理健康/信息筛选'
        emotion = '正向'
    
    # 43. 海姆立克急救
    elif '海姆立克' in full_text or ('噎到' in full_text and '急救' in full_text):
        topic = '婴幼儿急救知识'
        sub_topic = '海姆立克急救法救窒息宝宝'
        mentioned = None
        focus = '安全性/知识'
        emotion = '负向'
    
    # 44. 英语启蒙SSS
    elif 'SSS' in full_text and ('英语启蒙' in full_text or '有效性' in full_text):
        topic = '英语启蒙方法'
        sub_topic = 'SSS儿歌做英语启蒙的有效性讨论'
        mentioned = 'SSS儿歌'
        focus = '效果/方法'
        emotion = '复杂'
    
    # 45. 双语教育
    elif '双语' in full_text and ('弊端' in full_text or '误会' in full_text):
        topic = '双语教育'
        sub_topic = '双语孩子的语言发展趣事'
        mentioned = None
        focus = '效果/发展'
        emotion = '正向'
    
    # 46. ADHD儿童
    elif 'A娃' in full_text or 'ADHD' in full_text:
        topic = 'ADHD儿童养育'
        sub_topic = 'A娃的日常表现与养育挑战'
        mentioned = None
        focus = '方法/心理'
        emotion = '复杂'
    
    # 47. 育儿内容消费
    elif '育儿博主' in full_text and ('vlog' in full_text or '未婚美女' in full_text):
        topic = '育儿内容消费偏好'
        sub_topic = '宝妈转向看未婚美女vlog'
        mentioned = None
        focus = '心理需求/逃避'
        emotion = '负向'
    
    # 48. 独立带娃挑战
    elif '独立带娃' in full_text or ('没有父母托举' in full_text and '带娃' in full_text):
        topic = '独立带娃挑战'
        sub_topic = '一线城市无老人支持带娃失败'
        mentioned = None
        focus = '压力/支持'
        emotion = '负向'
    
    # 49. 多支点托举
    elif '多支点' in full_text or ('托举的顺序' in full_text):
        topic = '多支点家庭教育'
        sub_topic = '生活情感兴趣学习多支点托举'
        mentioned = None
        focus = '方法/效果'
        emotion = '正向'
    
    # 50. 一年级习惯培养
    elif '一年级' in full_text and ('习惯' in full_text or '放飞' in full_text):
        topic = '一年级习惯培养'
        sub_topic = '一年级学习习惯黄金期'
        mentioned = None
        focus = '方法/时机'
        emotion = '正向'
    
    # ===== 早教类 =====
    # 51. 早教必要性
    elif '早教' in full_text and any(k in full_text for k in ['有必要', '值不值', '有没有用', '有没有区别']):
        topic = '早教必要性讨论'
        sub_topic = '早教班是否值得上'
        mentioned = None
        focus = '效果/性价比'
        emotion = '复杂'
    
    # 52. 早教机构兴衰
    elif any(k in full_text for k in ['金宝贝', '美吉姆', '早教机构', '跑路']):
        topic = '早教机构兴衰'
        sub_topic = '金宝贝美吉姆从兴盛到衰落'
        mentioned = '金宝贝/美吉姆'
        focus = '行业变化/选择'
        emotion = '复杂'
    
    # 53. 有毒早教内容
    elif any(k in full_text for k in ['毒动画', '邪典', '有毒早教']):
        topic = '有毒早教内容'
        sub_topic = '警惕儿童邪典视频危害'
        mentioned = None
        focus = '安全性/认知'
        emotion = '负向'
    
    # 54. 蒙氏早教
    elif '蒙氏' in full_text and ('带娃难题' in full_text or '蒙台梭利' in full_text):
        topic = '蒙氏早教理念'
        sub_topic = '蒙氏教育解决带娃难题'
        mentioned = '蒙台梭利'
        focus = '方法/效果'
        emotion = '正向'
    
    # 55. 蒙氏早教祛魅
    elif '蒙氏' in full_text and ('祛魅' in full_text or '费解' in full_text):
        topic = '蒙氏早教理解'
        sub_topic = '什么是真正的蒙氏早教'
        mentioned = None
        focus = '认知/方法'
        emotion = '复杂'
    
    # 56. 托育选择
    elif '托育' in full_text or ('托班' in full_text and ('可怜' in full_text or '解放' in full_text)):
        topic = '托育选择'
        sub_topic = '送托育是否可怜/实用'
        mentioned = None
        focus = '实用性/情感'
        emotion = '复杂'
    
    # 57. 国内托育不流行
    elif '托育' in full_text and ('不太流行' in full_text or 'daycare' in full_text):
        topic = '国内托育现状'
        sub_topic = '国内托育为什么不流行'
        mentioned = None
        focus = '社会现状/选择'
        emotion = '中性'
    
    # 58. 免费早教资源
    elif ('社区' in full_text or '宝宝屋' in full_text) and ('免费' in full_text or '随申办' in full_text):
        topic = '免费早教资源'
        sub_topic = '上海社区免费早教体验'
        mentioned = '随申办/宝宝屋'
        focus = '性价比/便利性'
        emotion = '正向'
    
    # 59. 巧虎产品问题
    elif '巧虎' in full_text:
        topic = '早教产品体验'
        sub_topic = '巧虎订阅版本问题'
        mentioned = '巧虎'
        focus = '产品体验/性价比'
        emotion = '负向'
    
    # 60. 逻辑思维课质疑
    elif '逻辑思维' in full_text and ('骗局' in full_text or 'ADHD' in full_text):
        topic = '早教课程质疑'
        sub_topic = '少儿思维课新骗局的质疑'
        mentioned = None
        focus = '科学性/效果'
        emotion = '负向'
    
    # 61. 早教体验分享
    elif '早教' in full_text and any(k in full_text for k in ['体验', '测评', '真实感受', '盘点']):
        topic = '早教课程体验'
        sub_topic = '早教课真实体验分享'
        mentioned = None
        focus = '效果/性价比'
        emotion = '复杂'
    
    # 62. 早教绘本玩具
    elif '早教' in full_text and any(k in full_text for k in ['绘本', '玩具', '洞洞书', '布书']):
        topic = '早教绘本玩具'
        sub_topic = '0-3岁早教绘本玩具推荐'
        mentioned = None
        focus = '产品/效果'
        emotion = '正向'
    
    # 63. 英语启蒙动画
    elif '英语启蒙' in full_text and ('动画' in full_text or '动画片' in full_text):
        topic = '英语启蒙资源'
        sub_topic = '英语启蒙动画推荐'
        mentioned = None
        focus = '方法/资源'
        emotion = '正向'
    
    # 64. 胎教方法
    elif '胎教' in full_text:
        topic = '胎教方法'
        sub_topic = '4种胎教方式生出高智商宝宝'
        mentioned = None
        focus = '方法/效果'
        emotion = '正向'
    
    # 65. 专注力培养
    elif '专注力' in full_text and ('游戏' in full_text or '打卡' in full_text):
        topic = '专注力培养'
        sub_topic = '100天专注力游戏打卡'
        mentioned = None
        focus = '方法/效果'
        emotion = '正向'
    
    # 66. 公立vs私立幼儿园
    elif '公立' in full_text and '私立' in full_text and '幼儿园' in full_text:
        topic = '公立vs私立幼儿园'
        sub_topic = '公立幼儿园2年什么都不会'
        mentioned = None
        focus = '效果/选择'
        emotion = '负向'
    
    # 67. 三岁前能力培养
    elif '三岁前' in full_text and ('能力' in full_text or '知识' in full_text):
        topic = '早期能力培养'
        sub_topic = '三岁前培养6种底层能力'
        mentioned = None
        focus = '方法/发展'
        emotion = '正向'
    
    # 68. 崔玉涛语言启蒙
    elif '崔玉涛' in full_text:
        topic = '语言启蒙方法'
        sub_topic = '崔玉涛语言爆发期建议'
        mentioned = '崔玉涛'
        focus = '方法/效果'
        emotion = '正向'
    
    # 69. 桌游教学
    elif '桌游' in full_text:
        topic = '桌游教学方法'
        sub_topic = '桌游规则拆分教学'
        mentioned = None
        focus = '方法/效果'
        emotion = '正向'
    
    # 70. 国家免费资源
    elif '国家' in full_text and ('资源' in full_text or '免费' in full_text) and '早教' in full_text:
        topic = '免费早教资源'
        sub_topic = '国家免费早教音频库'
        mentioned = None
        focus = '资源/性价比'
        emotion = '正向'
    
    # 71. 卫健委早教指南
    elif '卫健委' in full_text:
        topic = '权威早教指南'
        sub_topic = '卫健委0-6岁早教指南'
        mentioned = '卫健委'
        focus = '科学性/权威性'
        emotion = '正向'
    
    # 72. 张雪峰英语启蒙
    elif '张雪峰' in full_text:
        topic = '英语启蒙资源'
        sub_topic = '张雪峰推荐9部英语动画'
        mentioned = '张雪峰'
        focus = '资源/方法'
        emotion = '正向'
    
    # 73. 感官启蒙绘本
    elif '感官' in full_text or ('五感' in full_text and '绘本' in full_text):
        topic = '感官启蒙绘本'
        sub_topic = '五感启蒙感官绘本推荐'
        mentioned = None
        focus = '产品/效果'
        emotion = '正向'
    
    # 74. 上海早教选择
    elif '上海' in full_text and '早教' in full_text and ('体验' in full_text or '盘点' in full_text):
        topic = '上海早教选择'
        sub_topic = '上海早教机构体验盘点'
        mentioned = None
        focus = '选择/性价比'
        emotion = '复杂'
    
    # 75. 1岁早教决策
    elif '1岁' in full_text and '早教' in full_text and ('必要' in full_text or '有没有' in full_text):
        topic = '1岁早教决策'
        sub_topic = '1岁宝宝是否有必要上早教'
        mentioned = None
        focus = '必要性/选择'
        emotion = '复杂'
    
    # 76. 早教制造焦虑
    elif '早教' in full_text and ('焦虑' in full_text or '制造焦虑' in full_text):
        topic = '早教焦虑'
        sub_topic = '早教机构制造焦虑'
        mentioned = None
        focus = '心理/选择'
        emotion = '负向'
    
    # 77. 早教费用
    elif '早教' in full_text and ('10个W' in full_text or '花费' in full_text or '钱' in full_text):
        topic = '早教费用'
        sub_topic = '2岁早教花费10万值不值'
        mentioned = None
        focus = '价格/性价比'
        emotion = '复杂'
    
    # 78. 放弃早教
    elif '停掉' in full_text and '早教' in full_text:
        topic = '放弃早教课'
        sub_topic = '决定停掉女儿的早教课'
        mentioned = None
        focus = '选择/效果'
        emotion = '复杂'
    
    # 79. 早教 vs 自己教
    elif '早教' in full_text and ('自己' in full_text or '在家' in full_text):
        topic = '早教vs家庭早教'
        sub_topic = '早教课与在家早教的对比'
        mentioned = None
        focus = '方法/选择'
        emotion = '复杂'
    
    # 80. 早教行业冷清
    elif '早教' in full_text and ('冷清' in full_text or '关门' in full_text):
        topic = '早教行业现状'
        sub_topic = '早教机构从热闹到冷清'
        mentioned = None
        focus = '行业/选择'
        emotion = '复杂'
    
    # 81. 中福会托班
    elif '中福会' in full_text:
        topic = '中福会托班'
        sub_topic = '中福会托班入园考试体验'
        mentioned = '中福会'
        focus = '体验/选择'
        emotion = '复杂'
    
    # 82. 5个月送托
    elif '五个月' in full_text and '托' in full_text:
        topic = '小月龄送托'
        sub_topic = '五个月宝宝送托真实感受'
        mentioned = None
        focus = '体验/选择'
        emotion = '复杂'
    
    # 83. 魔都英语启蒙
    elif '魔都' in full_text and '英语启蒙' in full_text:
        topic = '魔都英语启蒙'
        sub_topic = '上海幼儿英语启蒙有多卷'
        mentioned = None
        focus = '竞争/方法'
        emotion = '复杂'
    
    # 84. 孩子不在乎去哪玩
    elif '不在乎去哪里玩' in full_text or ('孩子其实并不在乎' in full_text):
        topic = '亲子陪伴质量'
        sub_topic = '孩子更在乎父母陪伴而非地点'
        mentioned = None
        focus = '情感/陪伴'
        emotion = '正向'
    
    # 85. 生命教育绘本
    elif '生命教育' in full_text and '绘本' in full_text:
        topic = '生命教育绘本'
        sub_topic = '生命教育绘本推荐'
        mentioned = None
        focus = '产品/情感'
        emotion = '正向'
    
    # 86. 宝宝语言发展
    elif '语言爆发期' in full_text or ('宝宝学说话' in full_text):
        topic = '宝宝语言发展'
        sub_topic = '促进宝宝语言爆发期的方法'
        mentioned = None
        focus = '方法/发展'
        emotion = '正向'
    
    # 87. 早教儿歌
    elif '儿歌' in full_text and ('早教' in full_text or '启蒙' in full_text):
        topic = '早教儿歌'
        sub_topic = '儿歌在早教中的作用'
        mentioned = None
        focus = '方法/效果'
        emotion = '正向'
    
    # 88. 绘本避雷
    elif '绘本' in full_text and ('避雷' in full_text or '恶心' in full_text):
        topic = '绘本避雷'
        sub_topic = '问题绘本内容避雷'
        mentioned = None
        focus = '安全性/内容'
        emotion = '负向'
    
    # 89. 早教玩具清单
    elif '玩具' in full_text and ('0-12月' in full_text or '每月' in full_text):
        topic = '早教玩具清单'
        sub_topic = '0-12月每月一个玩具推荐'
        mentioned = None
        focus = '产品/选择'
        emotion = '正向'
    
    # 90. 早教打卡
    elif '打卡' in full_text and ('早教' in full_text or 'SSS' in full_text):
        topic = '早教打卡计划'
        sub_topic = 'SSS儿歌打卡计划'
        mentioned = 'SSS儿歌'
        focus = '方法/计划'
        emotion = '正向'
    
    # 91. 早教通用
    elif '早教' in full_text:
        topic = '早教相关讨论'
        sub_topic = '早教方法或体验分享'
        mentioned = None
        focus = '方法/效果'
        emotion = '中性'
    
    # ===== 孕期类 =====
    # 92. 孕期耻骨疼痛
    elif '耻骨' in full_text or ('耻骨分离' in full_text):
        topic = '孕期身体不适'
        sub_topic = '孕期耻骨分离疼痛'
        mentioned = None
        focus = '身体/缓解'
        emotion = '负向'
    
    # 93. 孕期便秘
    elif '便秘' in full_text or ('拉不出屎' in full_text):
        topic = '孕期便秘困扰'
        sub_topic = '怀孕期间便秘问题'
        mentioned = None
        focus = '身体/健康'
        emotion = '负向'
    
    # 94. 妊娠纹和解
    elif '妊娠纹' in full_text:
        topic = '妊娠纹接受度'
        sub_topic = '与妊娠纹和解'
        mentioned = None
        focus = '身体/心理'
        emotion = '正向'
    
    # 95. 孕妇照
    elif '孕妇照' in full_text or ('孕照' in full_text):
        topic = '孕妇照拍摄'
        sub_topic = '孕期拍照记录'
        mentioned = None
        focus = '纪念/审美'
        emotion = '正向'
    
    # 96. 胎儿入盆
    elif '入盆' in full_text:
        topic = '胎儿入盆'
        sub_topic = '35周入盆体验分享'
        mentioned = None
        focus = '身体/分娩准备'
        emotion = '中性'
    
    # 97. 哺乳期堵奶
    elif '堵奶' in full_text or ('通乳' in full_text) or ('奶多' in full_text and '痛苦' in full_text):
        topic = '哺乳期堵奶'
        sub_topic = '产后严重堵奶经历'
        mentioned = None
        focus = '身体/痛苦'
        emotion = '负向'
    
    # 98. 临产征兆
    elif '发动' in full_text or ('宫缩' in full_text and '规律' in full_text):
        topic = '临产征兆'
        sub_topic = '39周等待发动'
        mentioned = None
        focus = '身体/焦虑'
        emotion = '复杂'
    
    # 99. 孕期社交
    elif '孕搭子' in full_text:
        topic = '孕期社交'
        sub_topic = '寻找上海孕搭子'
        mentioned = None
        focus = '社交/支持'
        emotion = '中性'
    
    # 100. 孕晚期不适
    elif '孕晚期' in full_text and any(k in full_text for k in ['难受', '顶', '踹', '紧绷']):
        topic = '孕晚期不适'
        sub_topic = '32周孕晚期身体负担'
        mentioned = None
        focus = '身体/痛苦'
        emotion = '负向'
    
    # 101. 孕期穿搭
    elif '孕期' in full_text and any(k in full_text for k in ['穿搭', '衣服', '裙子', 'ootd']):
        topic = '孕期穿搭'
        sub_topic = '孕期时尚穿搭分享'
        mentioned = None
        focus = '审美/自信'
        emotion = '正向'
    
    # 102. 孕肚羞耻
    elif '孕肚' in full_text and ('羞耻' in full_text or '焦虑' in full_text):
        topic = '孕期身材自信'
        sub_topic = '拒绝孕肚羞耻'
        mentioned = None
        focus = '心理/自信'
        emotion = '正向'
    
    # 103. 妈妈身份认同
    elif '当妈' in full_text and ('指责' in full_text or '束缚' in full_text or '封印' in full_text):
        topic = '妈妈身份认同'
        sub_topic = '当妈后维持自我被指责'
        mentioned = None
        focus = '身份/自我'
        emotion = '负向'
    
    # 104. 孕期自豪感
    elif '怀孕' in full_text and ('自豪' in full_text or '神奇' in full_text or '超人' in full_text):
        topic = '孕期身体自豪感'
        sub_topic = '怀孕的身体变化与自豪'
        mentioned = None
        focus = '身体/心理'
        emotion = '正向'
    
    # 105. 孕期孤独感
    elif '怀孕' in full_text and ('修行' in full_text or '没人管' in full_text or '无助' in full_text):
        topic = '孕期孤独感'
        sub_topic = '怀孕是一个人的修行'
        mentioned = None
        focus = '情感/孤独'
        emotion = '负向'
    
    # 106. 孕期福利登记
    elif '怀孕' in full_text and ('登记' in full_text or '损失' in full_text or '几万' in full_text):
        topic = '孕期福利登记'
        sub_topic = '怀孕登记领取福利'
        mentioned = None
        focus = '福利/信息'
        emotion = '正向'
    
    # 107. 孕期每周指南
    elif '怀孕' in full_text and ('每周' in full_text or '任务清单' in full_text or '每周要做什么' in full_text):
        topic = '孕期每周指南'
        sub_topic = '怀孕每周任务清单'
        mentioned = None
        focus = '知识/指导'
        emotion = '正向'
    
    # 108. 孕期自媒体
    elif '孕期' in full_text and ('博主' in full_text or 'plog' in full_text or '自媒体' in full_text):
        topic = '孕期自媒体'
        sub_topic = '新手孕妈做plog博主'
        mentioned = None
        focus = '事业/记录'
        emotion = '正向'
    
    # 109. 孕育勇气
    elif '孕育' in full_text and ('勇敢' in full_text or '伟大' in full_text):
        topic = '孕育生命的勇气'
        sub_topic = '选择孕育生命的勇敢决定'
        mentioned = None
        focus = '情感/价值'
        emotion = '正向'
    
    # 110. 孕肚社交
    elif '肚子大' in full_text or ('孕妇' in full_text and '好奇' in full_text):
        topic = '孕肚社交'
        sub_topic = '孕妇大肚子引发好奇'
        mentioned = None
        focus = '社交/身体'
        emotion = '正向'
    
    # 111. 孕期工作
    elif '孕' in full_text and ('上班' in full_text or '工作' in full_text or '开会' in full_text):
        topic = '孕期工作'
        sub_topic = '孕晚期坚持工作'
        mentioned = None
        focus = '工作/身体'
        emotion = '中性'
    
    # 112. 孕期身体变化
    elif '怀孕' in full_text and ('胸' in full_text or '变大' in full_text or '下垂' in full_text):
        topic = '孕期身体变化'
        sub_topic = '怀孕后胸部变化'
        mentioned = None
        focus = '身体/担忧'
        emotion = '复杂'
    
    # 113. 孕期肚子变化
    elif '怀孕' in full_text and ('肚子' in full_text and ('突然大' in full_text or '神奇' in full_text)):
        topic = '孕期肚子变化'
        sub_topic = '怀孕后肚子突然变大'
        mentioned = None
        focus = '身体/好奇'
        emotion = '正向'
    
    # 114. 孕期通用
    elif '孕期' in full_text or '怀孕' in full_text:
        topic = '孕期生活分享'
        sub_topic = '孕期日常体验'
        mentioned = None
        focus = '身体/情感'
        emotion = '中性'
    
    # 115. 男孩成长阶段
    elif '男孩' in full_text and ('阶段' in full_text or '爸爸' in full_text):
        topic = '男孩成长阶段'
        sub_topic = '男孩各阶段爸爸角色'
        mentioned = None
        focus = '成长/陪伴'
        emotion = '正向'
    
    # 116. 生长发育对照
    elif '生长发育' in full_text or ('对照表' in full_text):
        topic = '宝宝生长发育'
        sub_topic = '1岁内宝宝生长发育对照'
        mentioned = None
        focus = '发展/焦虑缓解'
        emotion = '正向'
    
    # 117. 幼儿园公立私立
    elif '幼儿园' in full_text and ('公立' in full_text or '私立' in full_text):
        topic = '公立vs私立幼儿园'
        sub_topic = '公立幼儿园学习效果讨论'
        mentioned = None
        focus = '效果/选择'
        emotion = '负向'
    
    # 118. 宝宝睡眠
    elif '哄睡' in full_text or ('睡眠' in full_text and '费妈' in full_text):
        topic = '宝宝哄睡困难'
        sub_topic = '哄睡太费妈'
        mentioned = None
        focus = '精力/方法'
        emotion = '负向'
    
    # 119. 生孩子好处
    elif '生娃' in full_text and ('举大旗' in full_text or '好处' in full_text):
        topic = '生孩子好处'
        sub_topic = '生娃后的积极体验'
        mentioned = None
        focus = '情感/价值'
        emotion = '正向'
    
    # 120. 秦昊生育观
    elif '秦昊' in full_text or ('奢侈品' in full_text and '孩子' in full_text):
        topic = '生育观讨论'
        sub_topic = '秦昊孩子是人生最大奢侈品'
        mentioned = '秦昊'
        focus = '价值/责任'
        emotion = '中性'
    
    # 121. 国外vs国内带娃
    elif '外国人' in full_text and ('带娃' in full_text or '轻松' in full_text):
        topic = '中外育儿差异'
        sub_topic = '为什么外国人带娃更轻松'
        mentioned = None
        focus = '文化/方法'
        emotion = '复杂'
    
    # 122. 宝妈工作选择
    elif '宝妈' in full_text and ('工作' in full_text or '工资' in full_text) and '育儿嫂' in full_text:
        topic = '宝妈工作选择'
        sub_topic = '宝妈宁愿低工资也要工作'
        mentioned = None
        focus = '价值/独立'
        emotion = '复杂'
    
    # 123. 宝宝急救
    elif '噎到' in full_text or ('急救' in full_text and '宝宝' in full_text):
        topic = '婴幼儿急救'
        sub_topic = '宝宝异物卡喉急救'
        mentioned = None
        focus = '安全性/知识'
        emotion = '负向'
    
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

# 统计话题分布
from collections import Counter
topic_counts = Counter([item['topic'] for item in output])
print("\n话题分布Top20:")
for topic, count in topic_counts.most_common(20):
    print(f"  {topic}: {count}条")
