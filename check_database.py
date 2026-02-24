import sqlite3

# 连接数据库
conn = sqlite3.connect("chinese_medicine.db")
cursor = conn.cursor()

print("=== 数据库结构 ===")
# 查看表结构
cursor.execute("PRAGMA table_info(medicines)")
table_info = cursor.fetchall()
print("表结构:")
for column in table_info:
    print(f"ID: {column[0]} | 名称: {column[1]} | 类型: {column[2]} | 非空: {column[3]} | 默认值: {column[4]} | 主键: {column[5]}")

print("\n=== 现有数据 ===")
# 查看数据总量
cursor.execute("SELECT COUNT(*) FROM medicines")
total_count = cursor.fetchone()[0]
print(f"数据库中共有 {total_count} 条中药记录")

# 查看所有数据
print("\n所有中药数据:")
cursor.execute("SELECT id, name, property, channel, efficacy FROM medicines ORDER BY id")
all_data = cursor.fetchall()
for row in all_data:
    print(f"ID: {row[0]} | 名称: {row[1]} | 性味: {row[2]} | 归经: {row[3]} | 功效: {row[4]}")

# 关闭连接
conn.close()
print("\n检查完成！")