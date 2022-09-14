import re
import calendar


# 计算以domain1.com为域名的https请求书
def compute_domain_count(log):
    # 获取所有行
    logs = log.split('\n')
    # 匹配所有双引号的内容
    reg1 = re.compile(r'"(.*?)"')
    # 定义计数器
    count = 0
    for s in logs:
        https = re.findall(reg1,s)[1]
        # 获取每一行中域名的内容
        reg2 = re.compile(r'//(.*?)/')
        domain = re.search(reg2,https).group()
        # 若域名为domain1.com则计数器加一
        if domain == 'domain1.com':
            count += 1
    return count


# 给定日期，计算当日请求成功的比例
def compute_success_count(date,log):
    # 获取所有行
    logs = log.split('\n')

    # 匹配所有中括号的内容
    reg1 = re.compile(r'\[(.*?)\]')
    # 匹配状态码
    reg2 = re.compile(r'\s([\d]{3})\s')

    total_count = 0
    success_count = 0
    for s in logs:
        log_date = re.findall(reg1,s)[0]
        day = log_date.split('/')[0]
        mon = list(calendar.month_abbr).index(log_date.split('/')[1])
        year = log_date.split('/')[2][:4]
        log_date_str = str(year)+'/' + str(mon) + '/' +str(day)
        if log_date_str == date:
            total_count += 1
            status_code = int(re.findall(reg2,s)[0])
            if 200 <= status_code < 300:
                success_count += 1
    return success_count/total_count
