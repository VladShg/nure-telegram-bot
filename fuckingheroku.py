import os
import psycopg2
import ast
import datetime
from config import StatesGroup

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
c = conn.cursor()

def fix_db():
    aD = list()
    aD.append("(108458898, 'Vled', 1, 1, 'КН', 'ПЗПІ-17-4', 6496579, '2018-09-13 18:04:30.268519', 44, 1)")
    aD.append("(254017485, 'Drew', 1, 1, 'КН', 'ПЗПІ-16-3', 5721681, '2018-09-13 16:44:16.643912', 4, 1)")
    aD.append("(303549253, 'ᴇʟɪᴊᴀʜ sᴏʟᴏᴠᴇʏ', 0, 1, 'КН', 'ПЗПІ-17-4', 6496579, '2018-09-14 12:58:42.018436', 4, 1)")
    aD.append("(347414945, 'Anton Zelenkov', 1, 1, 'КН', 'ПЗПІ-17-2', 6283375, '2018-09-13 19:01:18.406412', 10, 1)")
    aD.append("(308343822, 'Yulia', 1, 1, 'КН', 'ПЗПІ-17-7', 6283409, '2018-09-13 16:45:08.764395', 4, 1)")
    aD.append("(360374594, 'Pavel', 1, 1, 'КН', 'ІСТ-17-1', 6497191, '2018-09-13 16:47:13.684763', 3, 1)")
    aD.append("(393529567, 'Дмитрий Мортал', 1, 1, 'КН', 'ПЗПІ-17-1', 6283365, '2018-09-13 16:48:48.783008', 2, 1)")
    aD.append("(402226256, 'Саша Саня Александр', 0, 0, 'КН', 'ПЗПІ-17-3', 6496576, '2018-09-13 16:52:29.514895', 7, 1)")
    aD.append("(324549432, 'Den Vys', 1, 1, 'КН', 'ПЗПІ-17-2', 6283375, '2018-09-13 17:16:51.280244', 7, 1)")
    aD.append("(283915888, 'Димитрий Руденко', 1, 1, 'КН', 'ПЗПІ-17-7', 6283409, '2018-09-13 16:49:58.284629', 2, 1)")
    aD.append("(392436508, 'Maryna Zhernova', 1, 1, 'КН', 'ПЗПІ-17-2', 6283375, '2018-09-13 16:52:52.964494', 2, 1)")
    aD.append("(344807839, 'Эльдар Мамишев', 1, 1, 'КН', 'ПЗПІ-17-5', 6283463, '2018-09-13 16:53:48.310781', 3, 1)")
    aD.append("(244455099, 'Saveliy Kolesnikov', 1, 1, 'КН', 'ПЗПІ-17-4', 6496579, '2018-09-13 16:54:12.623400', 3, 1)")
    aD.append("(232142636, 'Lazarus Havron', 0, 0, 'КН', 'ПЗПІ-17-7', 6283409, '2018-09-13 16:54:20.997545', 2, 1)")
    aD.append("(247334343, 'Victoria Sokolova', 1, 1, 'КН', 'ПЗПІ-17-4', 6496579, '2018-09-13 16:54:31.335269', 2, 1)")
    aD.append("(372675274, 'Stepan Titarenko', 1, 1, '', '', -1, '2018-09-13 16:56:23.408136', 1, 1)")
    aD.append("(381838415, 'Дарья Парахина', 1, 1, 'КН', 'ПЗПІ-17-6', 6283489, '2018-09-13 16:59:32.246589', 4, 1)")
    aD.append("(421189580, 'Катя Саламатина', 0, 0, 'КН', 'ПЗПІ-17-5', 6283463, '2018-09-13 17:02:44.299490', 7, 1)")
    aD.append("(409446501, 'Назар Хазратов', 1, 1, 'КН', 'ПЗПІ-17-3', 6496576, '2018-09-13 17:03:44.125339', 3, 1)")
    aD.append("(350408046, 'д и м а', 1, 0, '', '', -1, '2018-09-13 17:03:47.719869', 2, 1)")
    aD.append("(407369924, 'Макс Довжий', 1, 1, '', '', -1, '2018-09-13 17:09:33.719866', 1, 1)")
    aD.append("(281244393, 'Alex Green', 1, 0, 'КН', 'ПЗПІ-16-3', 5721681, '2018-09-13 17:12:04.836528', 2, 1)")
    aD.append("(430957817, 'Elias', 1, 1, 'КН', 'ПЗПІ-17-4', 6496579, '2018-09-13 17:13:37.088735', 4, 1)")
    aD.append("(655438774, 'Danya Prokopenko', 1, 1, 'КН', 'ПЗПІ-17-9', 6496598, '2018-09-13 17:28:16.396716', 3, 4)")
    aD.append("(430758122, 'DANIL', 1, 1, 'КН', 'ПЗПІ-17-4', 6496579, '2018-09-13 17:28:10.443636', 3, 1)")
    aD.append("(607075603, 'Алексей Семенов', 1, 1, '', '', -1, '2018-09-14 05:51:17.429230', 1, 1)")
    aD.append("(415688989, 'Mykhailo Pashchenko', 1, 1, 'КН', 'ПЗПІ-17-2', 6283375, '2018-09-13 19:04:09.880612', 2, 1)")
    aD.append("(380296935, 'Vadim', 1, 1, '', '', -1, '2018-09-14 09:05:48.650005', 2, 1)")
    aD.append("(365904688, 'Влад Безродный', 1, 1, 'КН', 'ПЗПІ-17-7', 6283409, '2018-09-14 11:19:27.302334', 2, 1)")
    aD.append("(384392276, 'Danil Kutovoy', 1, 1, 'КН', 'ІТКН-17-9', 6496526, '2018-09-14 11:42:00.994678', 4, 1)")
    aD.append("(385332290, 'Дмитрий Лутфулин', 0, 1, 'КН', 'ІТКН-17-9', 6496526, '2018-09-14 11:41:27.566619', 2, 1)")
    aD.append("(438572516, 'Максим', 1, 1, 'КН', 'ПЗПІ-17-8', 6496585, '2018-09-14 15:01:35.820841', 2, 1)")

    with conn:
        for item in aD:
            item = ast.literal_eval(item)
            c.execute("SELECT * FROM users WHERE id={}".format(item[0]))
            if len(list(c.fetchall())) == 0:
                c.execute("INSERT INTO users(id, name, short_subj, short_teacher, faculty_name, group_name, group_id, last_update, updates, grp_state, notify, time_state, pair_state) VALUES ({}, {}, 1, 1, '{}', '{}', {}, CURRENT_TIMESTAMP , 1, {}, 1, 0, 0);".format(item[0], \
                 "'" + item[1] + "'", item[4], item[5], item[6], StatesGroup.S_NONE.value))


a = 1



with conn:
    c.execute("SELECT * FROM users")
    s = ""
    lst = c.fetchall()
    for n in range(len(lst)):
        print(lst[n])