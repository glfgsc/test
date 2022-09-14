import pandas as pd
import re


class FileToSql:
    def __init__(self,data,size):
        self.data = data
        self.size = size


    def replacer_factory(self,spelling_dict):
        def replacer(match):
            str = '{0}{1}{0}'.format(match.group(1), spelling_dict.get(match.group(2), match.group(2)))
            str = str[1:len(str)-1]
            return str
        return replacer

    # 转换成列表
    def to_list(self):
        lst = list()

        for i in range(len(self.data)):
            # pattern = re.compile(r'\'(.*?)\'')
            s = str(self.data.loc[i].tolist()).replace('[', '').replace(']', '')
            # s = s[:len(s)-1]
            # find = pattern.findall(s)
            #
            # rep = []
            # for j in find:
            #     rep.append(' cast(\'' + j + '\' as string)')
            #
            # repkeys = {}
            # for  k in range(len(rep)):
            #     repkeys[find[k]] = rep[k]
            #
            # pattern = r'''(['"])([\w\s\d\-、:：\.#￥*!@#$%^&*)(]+)\1'''
            # replacer = self.replacer_factory(repkeys)
            # lst.append(re.sub(pattern, replacer, s))
            lst.append(s)
        return lst

    # 写sql语句
    def write_sql(self,table_name):
        table_name = 'hvdev_dmcp_lab_rw.' + table_name
        lst = self.to_list()
        str1 = 'INSERT INTO ' + str(table_name) + '\n'
        count = 0
        count2 = 0
        for j in range(len(lst)):
            if count > self.size:
                file = open(str(table_name) + '_' + str(count2) + '.txt', 'w',encoding='utf8')
                file.write(str1 + ";\n")
                file.close()
                str1 = 'INSERT INTO ' + str(table_name) + '\n'
                count = 0
            if count <= self.size-1:
                str2 = 'select ' + lst[j] + '\nunion\n '
                str1 = str1 + str2
                count = count + 1
                count2 = count2 + 1
            else:
                str2 = 'select ' + lst[j]
                str1 = str1 + str2
                count = count + 1
            if j == len(lst)-1:
                file = open(str(table_name) + '_' + str(count2) + '.txt', 'w',encoding='utf8')
                file.write(str1 + ";\n")
                file.close()


def main():
    df = pd.read_excel('绿色工厂.xls')
    fts = FileToSql(df,1800)
    fts.write_sql('green_factory')

main()