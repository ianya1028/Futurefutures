from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    #add in thumbnail later
    #add in author later


    def __str__(self):
        return self.title


    def snippet(self):
        return self.body[:50] + "..."

class FQ(models.Model):
    fq_id = models.CharField(max_length=2)
    fq_question = models.TextField()
    fq_choice1 = models.CharField(max_length=50, default="")
    fq_choice2 = models.CharField(max_length=50, default="")
    fq_choice3 = models.CharField(max_length=50, default="")
    fq_choice4 = models.CharField(max_length=50, default="", null=True)
    fq_choice5 = models.CharField(max_length=50, default="", null=True)

class FQ_type(models.Model):
    type_id = models.CharField(max_length=2, primary_key=True)
    type_name = models.CharField(max_length=20)
    type_score = models.CharField(max_length=20, default="")
    type_describe = models.TextField(default='', null=True)

    def __str__(self):
        return self.type_id


class Member(models.Model):
    member_id = models.AutoField(primary_key=True)  #AutoField
    member_name = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=12)
    type = models.CharField(max_length=3 , null=True)


#討論區
class Discuss(models.Model):
    discuss_id = models.AutoField(primary_key=True)
    theme = models.CharField(max_length=8)
    title = models.CharField(max_length=20)
    content = models.TextField(default='')
    member_id = models.CharField(max_length=50)
    date = models.CharField(max_length=20)
    like = models.IntegerField(null=True)
    reply_times = models.IntegerField(null=True)
    time = models.CharField(max_length=20, default='')
# 討論區回覆  id 文章id 內容 作者id 時間 按讚數

class Yahoo_new(models.Model): # yahoo: 最新財經新聞
    title = models.CharField(max_length=100)
    content = models.TextField(default='')
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=20)
    source = models.CharField(max_length=20)

class Transaction_info(models.Model): #交易資訊
    #日期 股票代碼 開盤價 最高價 最低價 收盤價 漲跌 漲幅(%) 成交量
    date = models.CharField(max_length=10)
    stock_id = models.CharField(db_index=True,max_length=8)
    the_open = models.CharField(max_length=8)
    high_price = models.CharField(max_length=8)
    low_price = models.CharField(max_length=8)
    the_close = models.FloatField()
    change = models.FloatField()
    change_percent = models.CharField(max_length=8)
    vol = models.FloatField()

class Corporate(models.Model): #2.三大法人
    #日期，股票代碼，外資買賣超，外資持股張數，外資持股比率，投信買賣超，投信持股張數，投信持股比率，自營商買賣超，自營商持股張數，自營商持股比率
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    foreign_net = models.FloatField()
    foreign_paper = models.CharField(max_length=12)
    foreign_ratio = models.CharField(max_length=12)
    trust_net = models.FloatField()
    trust_paper = models.CharField(max_length=12)
    trust_ratio = models.CharField(max_length=12)
    dealer_net = models.CharField(max_length=12)
    dealer_paper = models.CharField(max_length=12)
    dealer_ratio = models.CharField(max_length=12)


# 我的追蹤股票
class Track_stock(models.Model):
    member_id = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=10, null=True)
    list_id = models.CharField(max_length=5, default='0', null=True) #0:default 我的自選股
    list_name = models.CharField(max_length=10, default='我的自選股', null=True)
    stock_name = models.CharField(max_length=50, default='', null=True)

class Information(models.Model):
    stock_id = models.CharField(max_length=8, primary_key=True)
    co_name = models.CharField(max_length=12)
    co_market = models.CharField(max_length=5)
    co_tel = models.CharField(max_length=20)
    co_fax = models.CharField(max_length=20)
    co_website = models.CharField(max_length=50)
    co_cheif = models.CharField(max_length=30)
    co_president = models.CharField(max_length=30)
    co_speaker = models.CharField(max_length=30)
    co_capital = models.CharField(max_length=15)
    co_fullname = models.CharField(max_length=30)
    co_add = models.CharField(max_length=60)
    category = models.CharField(max_length=3, default='')
    co_year = models.CharField(max_length=6)
    score = models.CharField(max_length=3, default='', null=True)

    def __str__(self):
        return self.stock_id

class Category(models.Model):
    category_id = models.CharField(max_length=2, primary_key=True)
    category_name = models.CharField(max_length=20)

    def __str__(self):
        return self.category_id

class Yahoo(models.Model): # yahoo: 台股盤勢
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField(default='')
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50, default='')
    source = models.CharField(max_length=20, default='')


class Yahoo_new(models.Model): # yahoo: 最新財經新聞
    title = models.CharField(max_length=100)
    content = models.TextField(default='')
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=20)
    source = models.CharField(max_length=20)

class Yahoo_stock(models.Model): # yahoo: 個股動態
    title = models.CharField(max_length=100)
    content = models.TextField(default='')
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50, default='')
    source = models.CharField(max_length=20, default='')
    tag = models.CharField(max_length=10, null=True)


class Yahoo_tec(models.Model): # yahoo: 科技產業
    title = models.CharField(max_length=100)
    content = models.TextField(default='')
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50, default='')
    source = models.CharField(max_length=20, default='')
    tag = models.CharField(max_length=10, null=True)


class Yahoo_tra(models.Model): # yahoo: 傳統產業
    title = models.CharField(max_length=100)
    content = models.TextField(default='')
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50, default='')
    source = models.CharField(max_length=20, default='')
    tag = models.CharField(max_length=10, null=True)

class Cna(models.Model):  # 中央通訊社: 財經新聞
    title = models.CharField(max_length=100)
    content = models.TextField(default='')
    date = models.CharField(max_length=50, default='')
    time = models.CharField(max_length=50)
    source = models.CharField(max_length=3, default='中央社')

class Yahoo_hot(models.Model): # yahoo: 熱門新聞(最多人閱讀)
    title = models.CharField(max_length=100)
    content = models.TextField(default='')
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    source = models.CharField(max_length=20)
    tag = models.CharField(max_length=10)


class Income_Statement_Q(models.Model): #8.損益表(季)
    #年季 股票代號 營業收入淨額(千) 營業毛利淨額(千) 營業利益(千) 稅前純益(千) 稅後純益(千) 公告基本每股盈餘(元)
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    net_operating_revenues = models.CharField(max_length=15)
    net_gross_profit = models.CharField(max_length=15)
    operating_income = models.CharField(max_length=15)
    income_before_tax = models.CharField(max_length=15)
    net_income = models.CharField(max_length=15)
    eps = models.CharField(max_length=15)
