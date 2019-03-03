from django.http import HttpResponse
from django.contrib import admin
from django.shortcuts import render,render_to_response,HttpResponseRedirect
from . models import Member, FQ, FQ_type, Discuss, Yahoo_new, Transaction_info, Corporate, Track_stock, Information, Category, Yahoo_hot, Yahoo, Yahoo_stock, Yahoo_tec, Yahoo_tra, Cna ,Income_Statement_Q ,Yahoo_Tendency
import random
from django.core.mail import send_mail
import statistics as st


def homepage(request):
    #return HttpResponse('homepage')
    return render(request,'homepage.html')
def about(request):
    #return HttpResponse('about')
    return render(request, 'about.html')

def news(request):
    #return HttpResponse('about')
    return render(request, 'news.html')



def login(request): #登入功能
    status_m = False
    status_p = False
    back = request.GET.get('back', 0)
    article_id = request.GET.get('article_id', 0)
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        check_m = Member.objects.filter(email__exact=username)
        check_p = Member.objects.filter(password__exact=password)

        if check_m is not None:
            status_m = True
        if check_p is not None:
            status_p = True

        user = Member.objects.filter(email=username, password=password)

        if user and status_m is True and status_p is True:
            request.session['userName'] = user[0].email
            request.session['password'] = user[0].password
            request.session['name'] = user[0].member_name
            if back == '0' or back == '':
                return HttpResponseRedirect('/home/')
            elif back == '討論區發文':
                return HttpResponseRedirect('/post/')
            elif back == '討論區回覆':
                return HttpResponseRedirect('/chat_outcome/?id='+article_id)
            elif back == '未來型預測':
                return HttpResponseRedirect('/predict/')
            elif back == '修改基本資料':
                return HttpResponseRedirect('/modify/')
            elif back == '修改密碼':
                return HttpResponseRedirect('/mo_pass/')
            elif back == '新聞首頁':
                return HttpResponseRedirect('/get_news/')
            elif back == '系統首頁':
                return HttpResponseRedirect('/home/')
            elif back == 'My_News':
                return HttpResponseRedirect('/member_news/')
        else:
            return render_to_response('login.html', {'status_m': status_m, 'status_p': status_p})

    return render_to_response('login.html', {'back': back, 'article_id': article_id})


def logout(request): #登出
    try:
        del request.session['userName']
        del request.session['password']
        del request.session['name']
        del request.session['post_page']
    except:
        pass
    return HttpResponseRedirect('/home/')


def index(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    if name != '':
        member_id = Member.objects.get(member_name=name).member_id
        rank2_stock_name, rank_stock_name, rank3_stock_name, rank4_stock_name, info = [], [], [], [], []
        res = Discuss.objects.order_by('-like')
        res_3 = Discuss.objects.order_by('-date', '-time')
        hot = Yahoo_new.objects.order_by('-date')
        rank = Transaction_info.objects.filter(date='20160826').order_by('-change')[:5]
        rank2 = Transaction_info.objects.filter(date='20160826').order_by('-vol')[:5]
        rank3 = Corporate.objects.filter(date='20160826').order_by('-foreign_net')[:5]
        rank4 = Corporate.objects.filter(date='20160826').order_by('-trust_net')[:5]
        list_name = Track_stock.objects.filter(member_id=member_id).order_by('list_name').values('list_name').distinct()
        list2_name = []
        try:
            list2_name = list_name.exclude(list_name=Track_stock.objects.filter(member_id=member_id).order_by('list_name').values('list_name').distinct().first()['list_name'])
        except:
            pass
        track = Track_stock.objects.filter(member_id=member_id)

        for i in rank:
            rank_stock_name.append(Information.objects.get(stock_id=i.stock_id).co_name)
        for i in rank2:
            rank2_stock_name.append(Information.objects.get(stock_id=i.stock_id).co_name)
        for i in rank3:
            rank3_stock_name.append(Information.objects.get(stock_id=i.stock_id).co_name)
        for i in rank4:
            rank4_stock_name.append(Information.objects.get(stock_id=i.stock_id).co_name)
        for i in track:
            s = Share(i.stock_id+'.TW')
            s1,s2, s3, s4 = s.get_price(),s.get_change(),s.get_percent_change(),s.get_volume()
            if s1 is None:
                s1 = 0
            if s2 is None:
                s2 = 0
            if s3 is None:
                s3 = 0
            if s4 is None:
                s4 = 0
            industry_id = Information.objects.get(stock_id=i.stock_id).category
            indusry_name = Category.objects.get(category_id=industry_id).category_name
            capital = Information.objects.get(stock_id=i.stock_id).co_capital
            info.append({'list_name':i.list_name,'stock_id':i.stock_id, 'stock_name':i.stock_name,'price':s1,'change':s2,'change_percent':s3,'vol':s4,'capital':capital,'industry':indusry_name})
        return render_to_response('home.html', {'loginstatus': loginstatus, 'name': name, 'res':res, 'res_3':res_3,'rank':rank,
                                                'rank2':rank2,'hot':hot,'rank3':rank3,'rank4':rank4,'rank_name':rank_stock_name,
                                                'rank2_name':rank2_stock_name,'rank3_name':rank3_stock_name,'rank4_name':rank4_stock_name,
                                                'list_name':list_name,'list2_name': list2_name, 'track':info})
    else:
        rank2_stock_name, rank_stock_name, rank3_stock_name, rank4_stock_name, info = [], [], [], [], []
        res = Discuss.objects.order_by('-like')
        res_3 = Discuss.objects.order_by('-date', '-time')
        hot = Yahoo_new.objects.order_by('-date')
        rank = Transaction_info.objects.filter(date='20160826').order_by('-change')[:5]
        rank2 = Transaction_info.objects.filter(date='20160826').order_by('-vol')[:5]
        rank3 = Corporate.objects.filter(date='20160826').order_by('-foreign_net')[:5]
        rank4 = Corporate.objects.filter(date='20160826').order_by('-trust_net')[:5]
        for i in rank:
            rank_stock_name.append(Information.objects.get(stock_id=i.stock_id).co_name)
        for i in rank2:
            rank2_stock_name.append(Information.objects.get(stock_id=i.stock_id).co_name)
        for i in rank3:
            rank3_stock_name.append(Information.objects.get(stock_id=i.stock_id).co_name)
        for i in rank4:
            rank4_stock_name.append(Information.objects.get(stock_id=i.stock_id).co_name)
        return render_to_response('home.html', {'loginstatus': loginstatus, 'name': name, 'res':res, 'res_3':res_3,'rank':rank,
                                                'rank2':rank2,'hot':hot,'rank3':rank3,'rank4':rank4,'rank_name':rank_stock_name,
                                                'rank2_name':rank2_stock_name,'rank3_name':rank3_stock_name,'rank4_name':rank4_stock_name,
                                                })


def register(request):
    status_m = True
    status_p = True
    status_check_password = True

    if request.method == 'POST':
        check_mail = request.POST.get('mail', '')
        check_password = request.POST.get('password', '')

        check_m = Member.objects.filter(email__exact=check_mail)
        check_p = Member.objects.filter(password__exact=check_password)

        if check_m:#如果回傳陣列是空的
            status_m = False
        if check_p:#如果回傳陣列是空的
            status_p = False

        p1 = request.POST.get('password', '')
        p2 = request.POST.get('password_check', '')

        if p1 == p2:  #!=改成is not
            status_check_password = True
        else:
            status_check_password = False

        name = request.POST.get('name', '')
        email = request.POST.get('mail', '')
        password = request.POST.get('password', '')
        phone = request.POST.get('tel', '')

        if status_m is True and status_p is True and status_check_password is True:

            Member.objects.create(member_name=name, email=email, password=password, phone_num=phone, type='1')
            return HttpResponseRedirect('/index/')
        else:
            return render_to_response('signin.html', {'status_m': status_m, 'status_p': status_p, 'status_check-password': status_check_password, 'name': name, 'mail': email, 'password': password, 'tel': phone} )

    return render_to_response('signin.html', {'status_m': status_m, 'status_p': status_p, 'status_check_password': status_check_password})


def getpassword(request):
    if request.method == 'POST':
        mail = request.POST.get('mail', '')
        check_mail = Member.objects.filter(email=mail)

        if check_mail is not None:
            new_password = random.randint(10000, 100000)
            new_password = str(new_password)
            send_mail('Your New Password', new_password, 'kfjet123@gmail.com', [mail,], fail_silently=False)
            check_mail.update(password=new_password)
            return render_to_response('login.html')
        else:
            status_m = False
            return render_to_response('forgot.html', {'warn': status_m})

    return render_to_response('forgot.html')

def get_news(request): #check
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    #新聞首頁關於最新頭條 國際財經 熱門點閱 台股盤勢 個股動態 科技產業 傳統產業的顯示文章數
    result = []
    result_2 = []
    result_3 = []
    result_4 = []
    result_5 = []
    result_6 = []
    result_7 = []
    last = Yahoo_new.objects.order_by('-date')
    last2 = Cna.objects.order_by('-date')
    last3 = Yahoo_hot.objects.order_by('-date')
    last4 = Yahoo.objects.order_by('-date')
    last5 = Yahoo_stock.objects.order_by('-date')
    last6 = Yahoo_tec.objects.order_by('-date')
    last7 = Yahoo_tra.objects.order_by('-date')

    for n in range(0, 7):
        result.append(last[n])

    for n in range(0, 7):
        result_2.append(last2[n])

    for n in range(0, 7):
        result_3.append(last3[n])

    for n in range(0, 6):
        result_4.append(last4[n])

    for n in range(0, 6):
        result_5.append(last5[n])

    for n in range(0, 6):
        result_6.append(last6[n])

    for n in range(0, 6):
        result_7.append(last7[n])

    return render_to_response('news.html', {'breaking_news': result, 'global': result_2, 'hot': result_3, 't_all':result_4, 'stock':result_5, 'tec':result_6, 'tra':result_7, 'name': name, 'loginstatus': loginstatus})


def search_news(request):#查詢文章關鍵字 check
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    search_status = False#尚未查詢文章前狀態為false
    res_1 = []
    res_2 = []
    res_3 = []
    res_4 = []
    res_5 = []
    res_6 = []
    res_7 = []
    res_8 = []
    res_9 = []
    res_10 = []
    res_11 = []
    res_12 = []
    key2 = '關鍵字'
    if request.method == 'POST':
        search_status = True#開始查詢後狀態為True
        for_member = request.POST.get('search2', '')
        key = request.POST.get('search', '')
        if for_member != '':
            key = for_member[5:]
        else:
            pass

        yahoo_new_res_1 = Yahoo_new.objects.filter(title__contains = key, content__contains=key).order_by('-date')
        yahoo_res_1 = Yahoo.objects.filter(title__contains = key, content__contains=key).order_by('-date')
        yahoo_stock_res_1 = Yahoo_stock.objects.filter(title__contains = key, content__contains=key).order_by('-date')
        yahoo_stock_res_2 = Yahoo_stock.objects.filter(tag__contains = key, content__contains=key).order_by('-date')
        yahoo_tec_res_1 = Yahoo_tec.objects.filter(title__contains = key, content__contains=key).order_by('-date')
        yahoo_tec_res_2 = Yahoo_tec.objects.filter(content__contains=key).order_by('-date')
        yahoo_tra_res_1 = Yahoo_tra.objects.filter(title__contains = key, content__contains=key).order_by('-date')
        yahoo_tra_res_2 = Yahoo_tra.objects.filter(tag__contains = key, content__contains=key).order_by('-date')
        yahoo_hot_res_1 = Yahoo_hot.objects.filter(title__contains = key, content__contains=key).order_by('-date')
        yahoo_hot_res_2 = Yahoo_hot.objects.filter(tag__contains = key, content__contains=key).order_by('-date')
        cna_res_1 = Cna.objects.filter(title__contains = key, content__contains=key).order_by('-date')

        if yahoo_new_res_1:
            res_12 = yahoo_new_res_1
        if yahoo_res_1:
            res_1 = yahoo_res_1
        if yahoo_stock_res_1:
            res_2 = yahoo_stock_res_1
        if yahoo_stock_res_2:
                res_3 = yahoo_stock_res_2
        if yahoo_tec_res_1:
                res_4 = yahoo_tec_res_1
        if yahoo_tec_res_2:
                res_5 = yahoo_tec_res_2
        if yahoo_tra_res_1:
            res_6 = yahoo_tra_res_1
        if yahoo_tra_res_2:
                res_7 = yahoo_tra_res_2
        if yahoo_hot_res_1:
                res_9 = yahoo_hot_res_1
        if yahoo_hot_res_2:
                res_10 = yahoo_hot_res_2
        if cna_res_1:
                res_11 = cna_res_1
        return render_to_response('news_search.html', {'res_1': res_1, 'res_2': res_2, 'res_3': res_3, 'res_4': res_4, 'res_5': res_5, 'res_6': res_6, 'res_7': res_7, 'res_9': res_9, 'res_10': res_10, 'res_11': res_11, 'res_12': res_12, 'status': search_status, 'key_word': key, 'name': name, 'loginstatus': loginstatus, 'key2':key2})

    return render_to_response('news_search.html', {'res_1': res_1, 'res_2': res_2, 'res_3': res_3, 'res_4': res_4, 'res_5': res_5, 'res_6': res_6, 'res_7': res_7, 'res_9': res_9, 'res_10': res_10, 'res_11': res_11, 'res_12': res_12, 'status': search_status, 'name': name, 'loginstatus': loginstatus, 'key2':key2}) #check# #


def income_statement(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    identity = request.GET.get('id', '2330')
    data_2 = Income_Statement_Q.objects.filter(stock_id=identity)
    sets = []
    for i in range(0, 8):
        sets.append(data_2[i])
    share = Share(identity+'.TW')
    price = share.get_price()
    change = share.get_change()
    prev_close = share.get_prev_close()
    change_in_percent = round(float(change)/float(prev_close), ndigits=2)*100
    volume = share.get_volume()
    capital = Information.objects.get(stock_id=identity).co_capital
    category_id = Information.objects.get(stock_id=identity).category
    industry = Category.objects.get(category_id=category_id).category_name
    return render_to_response('inc_sta.html', {'stock_name': Information.objects.get(stock_id=identity).co_name, 'stock': sets, 'price': price, 'change_in_percent': change_in_percent, 'change': change, 'volume': volume, 'capital': capital, 'industry': industry, 'id': identity, 'name': name, 'loginstatus': loginstatus})


def outcome_news(request):#搜尋文章結果 check
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    type = request.GET.get('id', 0)
    status_next = True
    status_prev = True
    if type is '1':
        category = '最新頭條'
        result = request.GET.get('c', 0)
        res = Yahoo_new.objects.filter(title = result)[0]
        last = Yahoo_new.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = Yahoo_new.objects.get(id = res.id+1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = Yahoo_new.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = Yahoo_new.objects.get(id = res.id+1)
            prev_article = Yahoo_new.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})

    if type is '2':
        category = '國際財經'
        result = request.GET.get('c', 0)
        res = Cna.objects.filter(title = result)[0]
        last = Cna.objects.last().id
        if res.id is 520:
            status_prev = False
            next_article = Cna.objects.get(id = res.id+1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = Cna.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = Cna.objects.get(id = res.id+1)
            prev_article = Cna.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})

    if type is '3':
        category = '熱門點閱'
        result = request.GET.get('c', 0)
        res = Yahoo_hot.objects.filter(title = result)[0]
        last = Yahoo_hot.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = Yahoo_hot.objects.get(id = res.id+1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = Yahoo_hot.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = Yahoo_hot.objects.get(id = res.id+1)
            prev_article = Yahoo_hot.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})

    if type is '4':
        category = '台股盤勢'
        result = request.GET.get('c', 0)
        res = Yahoo.objects.filter(title = result)[0]
        last = Yahoo.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = Yahoo.objects.get(id = res.id+1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = Yahoo.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = Yahoo.objects.get(id = res.id+1)
            prev_article = Yahoo.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})

    if type is '5':
        category = '個股動態'
        result = request.GET.get('c', 0)
        res = Yahoo_stock.objects.filter(title = result)[0]
        last = Yahoo_stock.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = Yahoo_stock.objects.get(id = res.id+1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = Yahoo_stock.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = Yahoo_stock.objects.get(id = res.id+1)
            prev_article = Yahoo_stock.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})

    if type is '6':
        category = '科技產業'
        result = request.GET.get('c', 0)
        res = Yahoo_tec.objects.filter(title = result)[0]
        last = Yahoo_tec.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = Yahoo_tec.objects.get(id = res.id+1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = Yahoo_tec.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'satus_prev': status_prev,'prev_article': prev_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = Yahoo_tec.objects.get(id = res.id+1)
            prev_article = Yahoo_tec.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})

    if type is '7':
        category = '傳統產業'
        result = request.GET.get('c', 0)
        res = Yahoo_tra.objects.filter(title = result)[0]
        last = Yahoo_tra.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = Yahoo_tra.objects.get(id = res.id+1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = Yahoo_tra.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = Yahoo_tra.objects.get(id = res.id+1)
            prev_article = Yahoo_tra.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})

    if type is '8':
        category = '國際財經'
        result = request.GET.get('c', 0)
        res = Cna.objects.objects.filter(title = result)[0]
        last = Cna.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = Cna.objects.get(id = res.id+1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = Cna.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = Cna.objects.get(id = res.id+1)
            prev_article = Cna.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})

    if type is '9':
        category = '熱門關鍵字'
        result = request.GET.get('c', 0)
        res = Yahoo_Tendency.objects.filter(title = result)[0]
        last = Yahoo_Tendency.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = Yahoo_Tendency.objects.get(id = res.id+1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:# 目前只有12筆 之後會增加到30多筆
            status_next = False
            prev_article = Yahoo_Tendency.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = Yahoo_Tendency.objects.get(id = res.id+1)
            prev_article = Yahoo_Tendency.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})




def home(request):  #理財小學堂
   name = ''
   loginstatus = False
   try:
        name = request.session['name']
        loginstatus = True
   except:
        pass
   return render_to_response('smallschool.html', {'name': name, 'loginstatus': loginstatus})



def stock_analysis(request):
   name = ''
   loginstatus = False
   try:
        name = request.session['name']
        loginstatus = True
   except:
        pass
   link = request.GET.get('link', 0)
   if link == '1_1':
        return render_to_response('stock_anacon.html', {'loginstatus': loginstatus, 'name': name})
   elif link == '1_10':
        return render_to_response('stock_anacon1.html', {'loginstatus': loginstatus, 'name': name})
   return render_to_response('stock_ana.html', {'loginstatus': loginstatus, 'name': name})





def analysis(request):
    return render(request, 'analysis.html')

def analysis1(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass

    if loginstatus == True:
        type = Member.objects.get(member_name=name).type
        your_type = FQ_type.objects.get(type_id=type).type_name
        return render_to_response('analysis.html', {'type_name': your_type, 'name': name, 'loginstatus': loginstatus})
    else:
        return render_to_response('login.html')
