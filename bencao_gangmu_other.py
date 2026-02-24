import sqlite3

# 连接数据库
conn = sqlite3.connect("chinese_medicine.db")
cursor = conn.cursor()

print("=== 本草纲目其他部类药物添加 ===")

print("\n1. 添加其他部类药物...")

other_sql = """
BEGIN TRANSACTION;

-- 木部
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('黄柏', '苦，寒', '肾、膀胱经', '清热燥湿，泻火除蒸，解毒疗疮', '煎服，3-12g', '芸香科植物黄皮树的干燥树皮');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('苦参', '苦，寒', '心、肝、胃、大肠、膀胱经', '清热燥湿，杀虫，利尿', '煎服，4.5-9g', '豆科植物苦参的干燥根');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('秦皮', '苦、涩，寒', '肝、胆、大肠经', '清热燥湿，收涩止痢，止带，明目', '煎服，6-12g', '木犀科植物苦枥白蜡树、白蜡树、尖叶白蜡树或宿柱白蜡树的干燥枝皮或干皮');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('桑白皮', '甘，寒', '肺经', '泻肺平喘，利水消肿', '煎服，6-12g', '桑科植物桑的干燥根皮');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('地骨皮', '甘，寒', '肺、肝、肾经', '凉血除蒸，清肺降火', '煎服，9-15g', '茄科植物枸杞或宁夏枸杞的干燥根皮');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('肉桂', '辛、甘，大热', '肾、脾、心、肝经', '补火助阳，引火归元，散寒止痛，温通经脉', '煎服，1-5g', '樟科植物肉桂的干燥树皮');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('杜仲', '甘，温', '肝、肾经', '补肝肾，强筋骨，安胎', '煎服，6-10g', '杜仲科植物杜仲的干燥树皮');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('厚朴', '苦、辛，温', '脾、胃、肺、大肠经', '燥湿消痰，下气除满', '煎服，3-10g', '木兰科植物厚朴或凹叶厚朴的干燥干皮、根皮及枝皮');

-- 果部
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('枸杞子', '甘，平', '肝、肾经', '滋补肝肾，益精明目', '煎服，6-12g', '茄科植物宁夏枸杞的干燥成熟果实');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('五味子', '酸、温', '肺、心、肾经', '收敛固涩，益气生津，补肾宁心', '煎服，3-6g', '木兰科植物五味子或华中五味子的干燥成熟果实');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('乌梅', '酸、涩，平', '肝、脾、肺、大肠经', '敛肺，涩肠，生津，安蛔', '煎服，6-12g', '蔷薇科植物梅的干燥近成熟果实');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('山茱萸', '酸、涩，微温', '肝、肾经', '补益肝肾，收涩固脱', '煎服，6-12g', '山茱萸科植物山茱萸的干燥成熟果肉');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('金樱子', '酸、涩，平', '肾、膀胱、大肠经', '固精缩尿，固崩止带，涩肠止泻', '煎服，6-12g', '蔷薇科植物金樱子的干燥成熟果实');

-- 菜部
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('生姜', '辛，微温', '肺、脾、胃经', '解表散寒，温中止呕，化痰止咳，解鱼蟹毒', '煎服，3-10g', '姜科植物姜的新鲜根茎');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('葱白', '辛，温', '肺、胃经', '发汗解表，散寒通阳', '煎服，3-10g', '百合科植物葱近根部的鳞茎');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('大蒜', '辛，温', '脾、胃、肺经', '解毒消肿，杀虫，止痢', '煎服，3-9g', '百合科植物大蒜的鳞茎');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('韭菜', '辛，温', '肝、肾、胃经', '补肾，温中，散瘀，解毒', '煎服，30-60g', '百合科植物韭的叶');

-- 谷部
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('薏苡仁', '甘、淡，凉', '脾、胃、肺经', '利水渗湿，健脾止泻，除痹，排脓，解毒散结', '煎服，9-30g', '禾本科植物薏苡的干燥成熟种仁');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('小麦', '甘，微寒', '心、脾、肾经', '养心安神，除烦', '煎服，30-60g', '禾本科植物小麦的干燥成熟果实');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('粳米', '甘，平', '脾、胃、肺经', '补中益气，健脾和胃，除烦渴，止泻痢', '煎服，30-60g', '禾本科植物稻的种仁');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('糯米', '甘，温', '脾、胃、肺经', '补中益气，健脾止泻，缩尿，敛汗，解毒', '煎服，30-60g', '禾本科植物糯稻的种仁');

-- 金石部
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('石膏', '甘、辛，大寒', '肺、胃经', '清热泻火，除烦止渴', '煎服，15-60g，先煎', '硫酸盐类矿物硬石膏族石膏，主要含含水硫酸钙');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('知母', '苦、甘，寒', '肺、胃、肾经', '清热泻火，滋阴润燥', '煎服，6-12g', '百合科植物知母的干燥根茎');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('芒硝', '咸、苦，寒', '胃、大肠经', '泻下通便，润燥软坚，清火消肿', '6-12g，冲入药汁内或开水溶化后服', '硫酸盐类矿物芒硝族芒硝，经加工精制而成的结晶体');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('磁石', '咸，寒', '肝、心、肾经', '镇惊安神，平肝潜阳，聪耳明目，纳气平喘', '煎服，9-30g，先煎', '氧化物类矿物尖晶石族磁铁矿，主要含四氧化三铁');

-- 动物部
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('麝香', '辛，温', '心、脾经', '开窍醒神，活血通经，消肿止痛', '入丸散，0.03-0.1g', '鹿科动物林麝、马麝或原麝成熟雄体香囊中的干燥分泌物');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('牛黄', '苦，凉', '心、肝经', '凉肝息风，清心豁痰，开窍醒神，清热解毒', '入丸散，0.15-0.35g', '牛科动物牛的干燥胆结石');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('羚羊角', '咸，寒', '肝、心经', '平肝息风，清肝明目，散血解毒', '煎服，1-3g，宜单煎2小时以上', '牛科动物赛加羚羊的角');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('鹿茸', '甘、咸，温', '肾、肝经', '壮肾阳，益精血，强筋骨，调冲任，托疮毒', '1-2g，研末冲服', '鹿科动物梅花鹿或马鹿的雄鹿未骨化密生茸毛的幼角');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('龟甲', '咸、甘，微寒', '肝、肾、心经', '滋阴潜阳，益肾强骨，养血补心，固经止崩', '煎服，9-24g，先煎', '龟科动物乌龟的背甲及腹甲');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('鳖甲', '咸，微寒', '肝、肾经', '滋阴潜阳，退热除蒸，软坚散结', '煎服，9-24g，先煎', '鳖科动物鳖的背甲');

-- 虫部
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('地龙', '咸，寒', '肝、脾、膀胱经', '清热定惊，通络，平喘，利尿', '煎服，5-10g', '钜蚓科动物参环毛蚓或通俗环毛蚓的干燥体');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('全蝎', '辛，平，有毒', '肝经', '息风镇痉，通络止痛，攻毒散结', '煎服，3-6g', '钳蝎科动物东亚钳蝎的干燥体');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('蜈蚣', '辛，温，有毒', '肝经', '息风镇痉，通络止痛，攻毒散结', '煎服，3-5g', '蜈蚣科动物少棘巨蜈蚣的干燥体');

INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('蝉蜕', '甘，寒', '肺、肝经', '疏散风热，利咽开音，透疹，明目退翳，息风止痉', '煎服，3-6g', '蝉科昆虫黑蚱的若虫羽化时脱落的皮壳');

COMMIT;
"""

try:
    cursor.executescript(other_sql)
    conn.commit()
    # 统计新增的数据量
    cursor.execute("SELECT COUNT(*) FROM medicines")
    new_count = cursor.fetchone()[0]
    print(f"✅ 成功添加其他部类药物，当前数据库共有 {new_count} 条中药记录")
except sqlite3.Error as e:
    print(f"❌ 添加失败: {e}")
    conn.rollback()

# 验证添加结果
print("\n2. 验证添加结果...")
try:
    # 查看新添加的药物
    cursor.execute("""
    SELECT name, property, channel, efficacy FROM medicines WHERE name IN (
        '黄柏', '苦参', '秦皮', '桑白皮', '地骨皮',
        '乌梅', '山茱萸', '金樱子',
        '大蒜', '韭菜',
        '小麦', '粳米', '糯米',
        '芒硝', '磁石',
        '羚羊角', '鹿茸', '龟甲', '鳖甲',
        '地龙', '全蝎', '蜈蚣', '蝉蜕'
    )
    """)
    new_medicines = cursor.fetchall()
    print(f"\n成功添加的其他部类药物（{len(new_medicines)} 种）:")
    for medicine in new_medicines:
        print(f"- {medicine[0]}: {medicine[1]}，{medicine[2]}，{medicine[3]}")
    
except sqlite3.Error as e:
    print(f"❌ 验证失败: {e}")

# 关闭连接
conn.close()
print("\n=== 操作完成 ===")
