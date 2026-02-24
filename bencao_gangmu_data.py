import sqlite3

# 连接数据库
conn = sqlite3.connect("chinese_medicine.db")
cursor = conn.cursor()

print("=== 本草纲目中药数据导入 ===")

# 清空现有数据
print("\n1. 清空现有数据...")
try:
    cursor.execute("DELETE FROM medicines")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='medicines'")
    conn.commit()
    print("成功清空现有数据")
except sqlite3.Error as e:
    print(f"清空数据失败: {e}")
    conn.close()
    exit(1)

# 本草纲目中药数据
print("\n2. 导入本草纲目中药数据...")

bencao_sql = """
BEGIN TRANSACTION;

-- 草部
INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('人参', '甘、微苦，温', '脾、肺、心经', '大补元气，复脉固脱，益精，安神', '煎服，3-9g', '五加科植物人参的干燥根和根茎');

INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('甘草', '甘，平', '心、肺、脾、胃经', '补脾益气，清热解毒，祛痰止咳，缓急止痛，调和诸药', '煎服，2-10g', '豆科植物甘草、胀果甘草或光果甘草的干燥根和根茎');

INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('黄芪', '甘，微温', '肺、脾经', '补气升阳，固表止汗，利水消肿，生肌', '煎服，9-30g', '豆科植物蒙古黄芪或膜荚黄芪的干燥根');

INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('白术', '苦、甘，温', '脾、胃经', '健脾益气，燥湿利水，止汗，安胎', '煎服，6-12g', '菊科植物白术的干燥根茎');

INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('黄连', '苦，寒', '心、脾、胃、肝、胆、大肠经', '清热燥湿，泻火解毒', '煎服，2-5g', '毛茛科植物黄连、三角叶黄连或云连的干燥根茎');

INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('黄芩', '苦，寒', '肺、胆、脾、大肠、小肠经', '清热燥湿，泻火解毒，止血，安胎', '煎服，3-10g', '唇形科植物黄芩的干燥根');

INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('黄柏', '苦，寒', '肾、膀胱经', '清热燥湿，泻火除蒸，解毒疗疮', '煎服，3-12g', '芸香科植物黄皮树的干燥树皮');

INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('大黄', '苦，寒', '脾、胃、大肠、肝、心包经', '泻热通便，清热泻火，凉血解毒，逐瘀通经', '煎服，3-15g', '蓼科植物掌叶大黄、唐古特大黄或药用大黄的干燥根和根茎');

-- 木部
INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('肉桂', '辛、甘，大热', '肾、脾、心、肝经', '补火助阳，引火归元，散寒止痛，温通经脉', '煎服，1-5g', '樟科植物肉桂的干燥树皮');

INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('杜仲', '甘，温', '肝、肾经', '补肝肾，强筋骨，安胎', '煎服，6-10g', '杜仲科植物杜仲的干燥树皮');

INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('厚朴', '苦、辛，温', '脾、胃、肺、大肠经', '燥湿消痰，下气除满', '煎服，3-10g', '木兰科植物厚朴或凹叶厚朴的干燥干皮、根皮及枝皮');

-- 果部
INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('枸杞子', '甘，平', '肝、肾经', '滋补肝肾，益精明目', '煎服，6-12g', '茄科植物宁夏枸杞的干燥成熟果实');

INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('五味子', '酸、温', '肺、心、肾经', '收敛固涩，益气生津，补肾宁心', '煎服，3-6g', '木兰科植物五味子的干燥成熟果实');

-- 菜部
INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('生姜', '辛，微温', '肺、脾、胃经', '解表散寒，温中止呕，化痰止咳，解鱼蟹毒', '煎服，3-10g', '姜科植物姜的新鲜根茎');

INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('葱白', '辛，温', '肺、胃经', '发汗解表，散寒通阳', '煎服，3-10g', '百合科植物葱的新鲜鳞茎');

-- 谷部
INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('薏苡仁', '甘、淡，凉', '脾、胃、肺经', '利水渗湿，健脾止泻，除痹，排脓，解毒散结', '煎服，9-30g', '禾本科植物薏苡的干燥成熟种仁');

-- 金石部
INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('石膏', '甘、辛，大寒', '肺、胃经', '清热泻火，除烦止渴', '煎服，15-60g', '硫酸盐类矿物硬石膏族石膏，主含含水硫酸钙');

-- 动物部
INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('麝香', '辛，温', '心、脾经', '开窍醒神，活血通经，消肿止痛', '入丸散，0.03-0.1g', '鹿科动物林麝、马麝或原麝成熟雄体香囊中的干燥分泌物');

INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('牛黄', '苦，凉', '心、肝经', '清心，豁痰，开窍，凉肝，息风，解毒', '入丸散，0.15-0.35g', '牛科动物牛干燥的胆结石');

-- 更多本草纲目中药
INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('当归', '甘、辛，温', '肝、心、脾经', '补血活血，调经止痛，润肠通便', '煎服，6-12g', '伞形科植物当归的干燥根');

INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('白芍', '苦、酸，微寒', '肝、脾经', '养血调经，敛阴止汗，柔肝止痛，平抑肝阳', '煎服，5-10g', '毛茛科植物芍药的干燥根');

INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('熟地黄', '甘，微温', '肝、肾经', '补血滋阴，益精填髓', '煎服，9-15g', '玄参科植物地黄的干燥块根，经炮制加工而成');

INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('川芎', '辛，温', '肝、胆、心包经', '活血行气，祛风止痛', '煎服，3-10g', '伞形科植物川芎的干燥根茎');

INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('白芷', '辛，温', '肺、胃、大肠经', '解表散寒，祛风止痛，宣通鼻窍，燥湿止带，消肿排脓', '煎服，3-10g', '伞形科植物白芷或杭白芷的干燥根');

INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('防风', '辛、甘，微温', '膀胱、肝、脾经', '祛风解表，胜湿止痛，止痉', '煎服，5-10g', '伞形科植物防风的干燥根');

INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('荆芥', '辛，微温', '肺、肝经', '解表散风，透疹，消疮', '煎服，5-10g', '唇形科植物荆芥的干燥地上部分');

INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('薄荷', '辛，凉', '肺、肝经', '疏散风热，清利头目，利咽，透疹，疏肝行气', '煎服，3-6g', '唇形科植物薄荷的干燥地上部分');

INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('柴胡', '辛、苦，微寒', '肝、胆、肺经', '疏散退热，疏肝解郁，升阳举陷', '煎服，3-10g', '伞形科植物柴胡或狭叶柴胡的干燥根');

INSERT INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('升麻', '辛、微甘，微寒', '肺、脾、胃、大肠经', '发表透疹，清热解毒，升举阳气', '煎服，3-10g', '毛茛科植物大三叶升麻、兴安升麻或升麻的干燥根茎');

COMMIT;
"""

try:
    cursor.executescript(bencao_sql)
    conn.commit()
    # 统计导入的数据量
    cursor.execute("SELECT COUNT(*) FROM medicines")
    imported_count = cursor.fetchone()[0]
    print(f"✅ 成功导入 {imported_count} 条本草纲目中药数据")
except sqlite3.Error as e:
    print(f"❌ 导入数据失败: {e}")
    conn.rollback()
    conn.close()
    exit(1)

# 验证导入结果
print("\n3. 验证导入结果...")
try:
    cursor.execute("SELECT COUNT(*) FROM medicines")
    total_count = cursor.fetchone()[0]
    print(f"\n📊 导入完成统计:")
    print(f"- 总导入中药数: {total_count}")
    
    # 查看不同类别中药的分布
    print("\n- 中药类别分布:")
    categories = {
        '草部': ['人参', '甘草', '黄芪', '白术', '黄连', '黄芩', '大黄'],
        '木部': ['肉桂', '杜仲', '厚朴'],
        '果部': ['枸杞子', '五味子'],
        '菜部': ['生姜', '葱白'],
        '谷部': ['薏苡仁'],
        '金石部': ['石膏'],
        '动物部': ['麝香', '牛黄']
    }
    
    for category, medicines in categories.items():
        count = 0
        for med in medicines:
            cursor.execute("SELECT COUNT(*) FROM medicines WHERE name = ?", (med,))
            if cursor.fetchone()[0] > 0:
                count += 1
        print(f"  {category}: {count} 种")
    
    # 查看前5条数据
    print("\n- 前5条导入的中药:")
    cursor.execute("SELECT id, name, property, channel FROM medicines LIMIT 5")
    top_5 = cursor.fetchall()
    for row in top_5:
        print(f"  ID: {row[0]} | 名称: {row[1]} | 性味: {row[2]} | 归经: {row[3]}")
    
    print("\n✅ 验证完成，本草纲目中药数据导入成功！")
    
except sqlite3.Error as e:
    print(f"❌ 验证失败: {e}")

# 关闭连接
conn.close()
print("\n=== 操作完成 ===")
