import sqlite3

# 连接数据库
conn = sqlite3.connect("chinese_medicine.db")
cursor = conn.cursor()

print("=== 本草纲目草部药物添加（第一批次） ===")

print("\n1. 添加草部药物...")

herbs_sql = """
BEGIN TRANSACTION;

-- 草部 - 山草类
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('知母', '苦、甘，寒', '肺、胃、肾经', '清热泻火，滋阴润燥', '煎服，6-12g', '百合科植物知母的干燥根茎');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('贝母', '苦、甘，微寒', '肺、心经', '清热润肺，化痰止咳，散结消肿', '煎服，3-10g', '百合科植物川贝母、暗紫贝母、甘肃贝母或梭砂贝母的干燥鳞茎');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('天门冬', '甘、苦，寒', '肺、肾经', '养阴润燥，清肺生津', '煎服，6-12g', '百合科植物天冬的干燥块根');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('麦门冬', '甘、微苦，微寒', '肺、胃、心经', '养阴润肺，益胃生津，清心除烦', '煎服，6-12g', '百合科植物麦冬的干燥块根');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('玉竹', '甘，微寒', '肺、胃经', '养阴润燥，生津止渴', '煎服，6-12g', '百合科植物玉竹的干燥根茎');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('黄精', '甘，平', '脾、肺、肾经', '补气养阴，健脾，润肺，益肾', '煎服，9-15g', '百合科植物滇黄精、黄精或多花黄精的干燥根茎');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('石斛', '甘，微寒', '胃、肾经', '益胃生津，滋阴清热', '煎服，6-12g', '兰科植物金钗石斛、霍山石斛、鼓槌石斛或流苏石斛的干燥茎');

-- 草部 - 芳草类
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('藿香', '辛，微温', '脾、胃、肺经', '芳香化浊，和中止呕，发表解暑', '煎服，3-10g', '唇形科植物广藿香的干燥地上部分');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('佩兰', '辛，平', '脾、胃、肺经', '芳香化湿，醒脾开胃，发表解暑', '煎服，3-10g', '菊科植物佩兰的干燥地上部分');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('苍术', '辛、苦，温', '脾、胃、肝经', '燥湿健脾，祛风散寒，明目', '煎服，3-9g', '菊科植物茅苍术或北苍术的干燥根茎');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('砂仁', '辛，温', '脾、胃、肾经', '化湿开胃，温脾止泻，理气安胎', '煎服，3-6g', '姜科植物阳春砂、绿壳砂或海南砂的干燥成熟果实');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('白豆蔻', '辛，温', '肺、脾、胃经', '化湿行气，温中止呕', '煎服，3-6g', '姜科植物白豆蔻或爪哇白豆蔻的干燥成熟果实');

-- 草部 - 湿草类
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('茯苓', '甘、淡，平', '心、肺、脾、肾经', '利水渗湿，健脾，宁心', '煎服，10-15g', '多孔菌科真菌茯苓的干燥菌核');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('猪苓', '甘、淡，平', '肾、膀胱经', '利水渗湿', '煎服，6-12g', '多孔菌科真菌猪苓的干燥菌核');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('泽泻', '甘、淡，寒', '肾、膀胱经', '利水渗湿，泄热，化浊降脂', '煎服，6-10g', '泽泻科植物泽泻的干燥块茎');

-- 草部 - 毒草类
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('附子', '辛、甘，大热，有毒', '心、肾、脾经', '回阳救逆，补火助阳，散寒止痛', '煎服，3-15g，需先煎、久煎', '毛茛科植物乌头的子根的加工品');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('川乌', '辛、苦，热，有毒', '心、肝、肾、脾经', '祛风除湿，温经止痛', '煎服，1.5-3g，需先煎、久煎', '毛茛科植物乌头的干燥母根');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('草乌', '辛、苦，热，有毒', '心、肝、肾、脾经', '祛风除湿，温经止痛', '煎服，1.5-3g，需先煎、久煎', '毛茛科植物北乌头的干燥块根');

-- 草部 - 蔓草类
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('何首乌', '苦、甘、涩，微温', '肝、心、肾经', '解毒，消痈，截疟，润肠通便', '煎服，3-6g', '蓼科植物何首乌的干燥块根');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('牛膝', '苦、甘、酸，平', '肝、肾经', '逐瘀通经，补肝肾，强筋骨，利尿通淋，引血下行', '煎服，5-12g', '苋科植物牛膝的干燥根');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('忍冬', '甘，寒', '肺、心、胃经', '清热解毒，疏散风热', '煎服，6-15g', '忍冬科植物忍冬的干燥花蕾或带初开的花');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('菟丝子', '辛、甘，平', '肝、肾、脾经', '补益肝肾，固精缩尿，安胎，明目，止泻', '煎服，6-12g', '旋花科植物南方菟丝子或菟丝子的干燥成熟种子');

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
        '知母', '贝母', '天门冬', '麦门冬', '玉竹', '黄精', '石斛',
        '藿香', '佩兰', '苍术', '砂仁', '白豆蔻',
        '茯苓', '猪苓', '泽泻',
        '附子', '川乌', '草乌',
        '何首乌', '牛膝', '忍冬', '菟丝子'
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
