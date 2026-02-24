import sqlite3

# 连接数据库
conn = sqlite3.connect("chinese_medicine.db")
cursor = conn.cursor()

# 示例1：单个添加
print("=== 单个添加示例 ===")
sql1 = """
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('白芍', '苦、酸，微寒', '肝、脾经', '养血调经，敛阴止汗，柔肝止痛，平抑肝阳', '煎服，5-10g', '毛茛科植物芍药的干燥根')
"""

try:
    cursor.execute(sql1)
    conn.commit()
    if cursor.rowcount > 0:
        print("✅ 成功添加中药：白芍")
    else:
        print("⚠️  中药白芍已存在，跳过添加")
except sqlite3.Error as e:
    print(f"❌ 添加失败: {e}")

# 示例2：批量添加
print("\n=== 批量添加示例 ===")
batch_sql = """
BEGIN TRANSACTION;
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('川芎', '辛，温', '肝、胆、心包经', '活血行气，祛风止痛', '煎服，3-10g', '伞形科植物川芎的干燥根茎');
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('熟地', '甘，微温', '肝、肾经', '补血滋阴，益精填髓', '煎服，9-15g', '玄参科植物地黄的干燥块根（炮制后）');
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('当归', '甘、辛，温', '肝、心、脾经', '补血活血，调经止痛，润肠通便', '煎服，6-12g', '伞形科植物当归的干燥根');
COMMIT;
"""

# 示例3：添加非补气类中药
print("\n=== 添加非补气类中药 ===")
non_qi_sql = """
BEGIN TRANSACTION;
-- 清热类
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('黄芩', '苦，寒', '肺、胆、脾、大肠、小肠经', '清热燥湿，泻火解毒，止血，安胎', '煎服，3-10g', '唇形科植物黄芩的干燥根');
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('黄连', '苦，寒', '心、脾、胃、肝、胆、大肠经', '清热燥湿，泻火解毒', '煎服，2-5g', '毛茛科植物黄连、三角叶黄连或云连的干燥根茎');
-- 活血化瘀类
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('丹参', '苦，微寒', '心、肝经', '活血祛瘀，通经止痛，清心除烦，凉血消痈', '煎服，10-15g', '唇形科植物丹参的干燥根和根茎');
-- 解表类
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('麻黄', '辛、微苦，温', '肺、膀胱经', '发汗散寒，宣肺平喘，利水消肿', '煎服，2-9g', '麻黄科植物草麻黄、中麻黄或木贼麻黄的干燥草质茎');
-- 利水渗湿类
INSERT OR IGNORE INTO medicines (name, property, channel, efficacy, usage, source)
VALUES ('泽泻', '甘、淡，寒', '肾、膀胱经', '利水渗湿，泄热，化浊降脂', '煎服，6-10g', '泽泻科植物泽泻的干燥块茎');
COMMIT;
"""

try:
    cursor.executescript(batch_sql)
    print("✅ 批量添加完成")
except sqlite3.Error as e:
    print(f"❌ 批量添加失败: {e}")

# 执行非补气类中药添加
try:
    cursor.executescript(non_qi_sql)
    print("✅ 非补气类中药添加完成")
except sqlite3.Error as e:
    print(f"❌ 非补气类中药添加失败: {e}")

# 验证添加结果
print("\n=== 验证添加结果 ===")
cursor.execute("SELECT COUNT(*) FROM medicines")
total_count = cursor.fetchone()[0]
print(f"数据库中共有 {total_count} 条中药记录")

# 查看新添加的中药
cursor.execute("SELECT name, property FROM medicines WHERE name IN ('白芍', '川芎', '熟地', '黄芩', '黄连', '丹参', '麻黄', '泽泻')")
new_medicines = cursor.fetchall()
print("\n新添加的中药：")
for med in new_medicines:
    print(f"名称: {med[0]} | 性味: {med[1]}")

# 查看非补气类中药
print("\n=== 非补气类中药列表 ===")
cursor.execute("SELECT name, property, efficacy FROM medicines WHERE name IN ('黄芩', '黄连', '丹参', '麻黄', '泽泻')")
non_qi_medicines = cursor.fetchall()
for med in non_qi_medicines:
    print(f"名称: {med[0]} | 性味: {med[1]} | 功效: {med[2]}")

# 关闭连接
conn.close()
print("\n数据库操作完成！")