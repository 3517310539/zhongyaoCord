import sqlite3

# 连接数据库
conn = sqlite3.connect("chinese_medicine.db")
cursor = conn.cursor()

print("=== 中药数据修改工具 ===")

# 示例1：修改单个中药信息
print("\n=== 修改单个中药示例 ===")
update_sql1 = """
UPDATE medicines 
SET property = '辛、甘，温', 
    channel = '肝、肾经', 
    efficacy = '补肾阳，强筋骨，祛风湿', 
    usage = '煎服，6-10g', 
    source = '小檗科植物淫羊藿、箭叶淫羊藿、柔毛淫羊藿或朝鲜淫羊藿的干燥叶'
WHERE name = '淫羊藿'
"""

try:
    cursor.execute(update_sql1)
    conn.commit()
    if cursor.rowcount > 0:
        print("成功修改中药：淫羊藿")
    else:
        print("未找到中药淫羊藿，修改失败")
except sqlite3.Error as e:
    print(f"修改失败: {e}")

# 示例2：批量修改中药信息
print("\n=== 批量修改示例 ===")
batch_update_sql = """
BEGIN TRANSACTION;
UPDATE medicines SET efficacy = '补血活血，调经止痛，润肠通便' WHERE name = '当归';
UPDATE medicines SET efficacy = '养血调经，敛阴止汗，柔肝止痛，平抑肝阳' WHERE name = '白芍';
UPDATE medicines SET efficacy = '补血滋阴，益精填髓' WHERE name = '熟地黄';
COMMIT;
"""

try:
    cursor.executescript(batch_update_sql)
    print("批量修改完成")
except sqlite3.Error as e:
    print(f"批量修改失败: {e}")

# 示例3：根据ID修改中药信息
print("\n=== 根据ID修改示例 ===")
id_update_sql = """
UPDATE medicines 
SET name = '熟地黄', 
    property = '甘，微温', 
    channel = '肝、肾经', 
    efficacy = '补血滋阴，益精填髓', 
    usage = '煎服，9-15g'
WHERE id = 22
"""

try:
    cursor.execute(id_update_sql)
    conn.commit()
    if cursor.rowcount > 0:
        print("成功根据ID修改中药信息")
    else:
        print("未找到指定ID的中药，修改失败")
except sqlite3.Error as e:
    print(f"修改失败: {e}")

# 示例4：修改用法用量
print("\n=== 修改用法用量示例 ===")
usage_update_sql = """
BEGIN TRANSACTION;
UPDATE medicines SET usage = '煎服，3-10g' WHERE name = '人参';
UPDATE medicines SET usage = '煎服，2-10g' WHERE name = '甘草';
UPDATE medicines SET usage = '煎服，9-30g' WHERE name = '黄芪';
COMMIT;
"""

try:
    cursor.executescript(usage_update_sql)
    print("用法用量修改完成")
except sqlite3.Error as e:
    print(f"修改失败: {e}")

# 验证修改结果
print("\n=== 验证修改结果 ===")
cursor.execute("SELECT name, property, efficacy FROM medicines WHERE name IN ('淫羊藿', '当归', '白芍', '熟地黄', '人参')")
updated_medicines = cursor.fetchall()
print("修改后的中药信息：")
for med in updated_medicines:
    print(f"名称: {med[0]} | 性味: {med[1]} | 功效: {med[2]}")

# 查看修改后的熟地黄信息
cursor.execute("SELECT id, name, property, channel, efficacy, usage FROM medicines WHERE id = 22")
熟地_info = cursor.fetchone()
if 熟地_info:
    print(f"\nID为22的中药信息：")
    print(f"ID: {熟地_info[0]} | 名称: {熟地_info[1]} | 性味: {熟地_info[2]} | 归经: {熟地_info[3]} | 功效: {熟地_info[4]} | 用法: {熟地_info[5]}")

# 关闭连接
conn.close()
print("\n操作完成！")
