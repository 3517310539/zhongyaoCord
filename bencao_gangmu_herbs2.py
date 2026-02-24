import sqlite3

# 连接数据库
conn = sqlite3.connect("chinese_medicine.db")
cursor = conn.cursor()

print("=== 本草纲目草部药物添加（第二批次） ===")

print("\n1. 添加草部药物...")

herbs_sql = """
BEGIN TRANSACTION;

-- 草部 - 水草类
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('菖蒲', '辛、苦，温', '心、胃经', '开窍豁痰，醒神益智，化湿开胃', '煎服，3-9g', '天南星科植物石菖蒲的干燥根茎');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('泽泻', '甘、淡，寒', '肾、膀胱经', '利水渗湿，泄热，化浊降脂', '煎服，6-10g', '泽泻科植物泽泻的干燥块茎');

-- 草部 - 石草类
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('石斛', '甘，微寒', '胃、肾经', '益胃生津，滋阴清热', '煎服，6-12g', '兰科植物金钗石斛、霍山石斛、鼓槌石斛或流苏石斛的干燥茎');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('石韦', '甘、苦，微寒', '肺、膀胱经', '利尿通淋，清肺止咳，凉血止血', '煎服，6-12g', '水龙骨科植物庐山石韦、石韦或有柄石韦的干燥叶');

-- 草部 - 苔草类
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('海藻', '苦、咸，寒', '肝、胃、肾经', '消痰软坚散结，利水消肿', '煎服，6-12g', '马尾藻科植物海蒿子或羊栖菜的干燥藻体');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('昆布', '咸，寒', '肝、胃、肾经', '消痰软坚散结，利水消肿', '煎服，6-12g', '海带科植物海带或翅藻科植物昆布的干燥叶状体');

-- 草部 - 杂草类
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('蒲公英', '苦、甘，寒', '肝、胃经', '清热解毒，消肿散结，利尿通淋', '煎服，10-15g', '菊科植物蒲公英、碱地蒲公英或同属数种植物的干燥全草');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('紫花地丁', '苦、辛，寒', '心、肝经', '清热解毒，凉血消肿', '煎服，15-30g', '堇菜科植物紫花地丁的干燥全草');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('败酱草', '辛、苦，微寒', '胃、大肠、肝经', '清热解毒，消痈排脓，祛瘀止痛', '煎服，6-15g', '败酱科植物黄花败酱或白花败酱的干燥全草');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('鱼腥草', '辛，微寒', '肺经', '清热解毒，消痈排脓，利尿通淋', '煎服，15-25g', '三白草科植物蕺菜的干燥地上部分');

-- 草部 - 有名未用类
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('淫羊藿', '辛、甘，温', '肝、肾经', '补肾阳，强筋骨，祛风湿', '煎服，6-10g', '小檗科植物淫羊藿、箭叶淫羊藿、柔毛淫羊藿或朝鲜淫羊藿的干燥叶');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('巴戟天', '甘、辛，微温', '肾、肝经', '补肾阳，强筋骨，祛风湿', '煎服，3-10g', '茜草科植物巴戟天的干燥根');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('肉苁蓉', '甘、咸，温', '肾、大肠经', '补肾阳，益精血，润肠通便', '煎服，6-10g', '列当科植物肉苁蓉或管花肉苁蓉的干燥带鳞叶的肉质茎');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('锁阳', '甘，温', '肝、肾、大肠经', '补肾阳，益精血，润肠通便', '煎服，5-10g', '锁阳科植物锁阳的干燥肉质茎');

-- 草部 - 隰草类
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('麻黄', '辛、微苦，温', '肺、膀胱经', '发汗散寒，宣肺平喘，利水消肿', '煎服，2-9g', '麻黄科植物草麻黄、中麻黄或木贼麻黄的干燥草质茎');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('葛根', '甘、辛，凉', '脾、胃、肺经', '解肌退热，生津止渴，透疹，升阳止泻，通经活络，解酒毒', '煎服，10-15g', '豆科植物野葛的干燥根');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('升麻', '辛、微甘，微寒', '肺、脾、胃、大肠经', '发表透疹，清热解毒，升举阳气', '煎服，3-10g', '毛茛科植物大三叶升麻、兴安升麻或升麻的干燥根茎');

-- 草部 - 毒草类
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('半夏', '辛，温，有毒', '脾、胃、肺经', '燥湿化痰，降逆止呕，消痞散结', '煎服，3-9g，需制用', '天南星科植物半夏的干燥块茎');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('天南星', '苦、辛，温，有毒', '肺、肝、脾经', '燥湿化痰，祛风解痉，散结消肿', '煎服，3-9g，需制用', '天南星科植物天南星、异叶天南星或东北天南星的干燥块茎');

-- 草部 - 蔓草类
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('瓜蒌', '甘、微苦，寒', '肺、胃、大肠经', '清热涤痰，宽胸散结，润燥滑肠', '煎服，9-15g', '葫芦科植物栝楼或双边栝楼的干燥成熟果实');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('天花粉', '甘、微苦，微寒', '肺、胃经', '清热泻火，生津止渴，消肿排脓', '煎服，10-15g', '葫芦科植物栝楼或双边栝楼的干燥根');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('木通', '苦，寒', '心、小肠、膀胱经', '利尿通淋，清心除烦，通经下乳', '煎服，3-6g', '木通科植物木通、三叶木通或白木通的干燥藤茎');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('通草', '甘、淡，微寒', '肺、胃经', '清热利尿，通气下乳', '煎服，3-5g', '五加科植物通脱木的干燥茎髓');

COMMIT;
"""

try:
    cursor.executescript(herbs_sql)
    conn.commit()
    # 统计新增的数据量
    cursor.execute("SELECT COUNT(*) FROM medicines")
    new_count = cursor.fetchone()[0]
    print(f"✅ 成功添加草部药物，当前数据库共有 {new_count} 条中药记录")
except sqlite3.Error as e:
    print(f"❌ 添加失败: {e}")
    conn.rollback()

# 验证添加结果
print("\n2. 验证添加结果...")
try:
    # 查看新添加的药物
    cursor.execute("""
    SELECT name, property, channel, efficacy FROM medicines WHERE name IN (
        '菖蒲', '石韦', '海藻', '昆布', '蒲公英', '紫花地丁', '败酱草', '鱼腥草',
        '淫羊藿', '巴戟天', '肉苁蓉', '锁阳', '葛根', '升麻', '半夏', '天南星',
        '瓜蒌', '天花粉', '木通', '通草'
    )
    """)
    new_herbs = cursor.fetchall()
    print(f"\n成功添加的草部药物（{len(new_herbs)} 种）:")
    for herb in new_herbs:
        print(f"- {herb[0]}: {herb[1]}，{herb[2]}，{herb[3]}")
    
except sqlite3.Error as e:
    print(f"❌ 验证失败: {e}")

# 关闭连接
conn.close()
print("\n=== 操作完成 ===")
