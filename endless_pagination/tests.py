__test__ = {"doctest": """

>>> import string
>>> from django.template import Template, Context
>>> from django.core.handlers.wsgi import WSGIRequest
>>> from endless_pagination import settings
>>> from endless_pagination import models
>>> from endless_pagination import paginator
>>> from endless_pagination import decorators
>>> from endless_pagination import utils


LOW LEVEL TESTS: PAGINATORS

>>> p = paginator.DefaultPaginator(range(30), 7, orphans=2)
>>> p.page(2).object_list
[7, 8, 9, 10, 11, 12, 13]
>>> p.page_range
[1, 2, 3, 4]
>>> p.num_pages
4
>>> p.count
30
>>> p.page(5).object_list
Traceback (most recent call last):
EmptyPage: That page contains no results
>>> p.page(2).start_index()
8
>>> p.page(2).end_index()
14

>>> p = paginator.DefaultPaginator(range(9), 7, orphans=2)
>>> p.num_pages
1
>>> p.page(2)
Traceback (most recent call last):
EmptyPage: That page contains no results
>>> p.page(1).start_index()
1
>>> p.page(1).end_index()
9

>>> p = paginator.LazyPaginator(range(30), 7, orphans=2)
>>> p.page(2).object_list
[7, 8, 9, 10, 11, 12, 13]
>>> p.num_pages
3
>>> p.count
Traceback (most recent call last):
NotImplementedError
>>> p.page(4).object_list
[21, 22, 23, 24, 25, 26, 27, 28, 29]
>>> p.page_range
Traceback (most recent call last):
NotImplementedError
>>> p.page(5).object_list
Traceback (most recent call last):
EmptyPage: That page contains no results
>>> p.page(0)
Traceback (most recent call last):
EmptyPage: That page number is less than 1

>>> p = paginator.LazyPaginator(range(11), 8, orphans=2)
>>> p.num_pages
>>> p.page(1).object_list
[0, 1, 2, 3, 4, 5, 6, 7]
>>> p.page(2).object_list
[8, 9, 10]

>>> p = paginator.LazyPaginator(range(10), 8, orphans=3)
>>> p.page(2)
Traceback (most recent call last):
EmptyPage: That page contains no results
>>> p.page(1).object_list
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


LOW LEVEL TESTS: PAGINATORS WITH DIFFERENT NUMBER OF ITEMS ON THE FIRST PAGE

>>> p = paginator.DefaultPaginator(range(30), 7, first_page=3, orphans=2)
>>> p.page(1).object_list
[0, 1, 2]
>>> p.page(2).object_list
[3, 4, 5, 6, 7, 8, 9]
>>> p.page(5).object_list
[24, 25, 26, 27, 28, 29]
>>> p.num_pages
5
>>> p.page(6).object_list
Traceback (most recent call last):
EmptyPage: That page contains no results

>>> p = paginator.DefaultPaginator(range(30), 7, first_page=15, orphans=2)
>>> p.page_range
[1, 2, 3]
>>> p.page(1).object_list
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
>>> p.page(2).object_list
[15, 16, 17, 18, 19, 20, 21]
>>> p.page(3).object_list
[22, 23, 24, 25, 26, 27, 28, 29]
>>> p.page(4)
Traceback (most recent call last):
EmptyPage: That page contains no results
>>> p.page(-2)
Traceback (most recent call last):
EmptyPage: That page number is less than 1

>>> p = paginator.DefaultPaginator(range(6), 7, first_page=3, orphans=3)
>>> p.num_pages
1
>>> p.page(2).object_list
Traceback (most recent call last):
EmptyPage: That page contains no results
>>> p.page(1).object_list
[0, 1, 2, 3, 4, 5]
>>> p.page(1).start_index()
1
>>> p.page(1).end_index()
6

>>> p = paginator.LazyPaginator(range(30), 7, first_page=3, orphans=2)
>>> p.num_pages
>>> p.page(1).object_list
[0, 1, 2]
>>> p.num_pages
2
>>> p.page(5).object_list
[24, 25, 26, 27, 28, 29]
>>> p.page(6).object_list
Traceback (most recent call last):
EmptyPage: That page contains no results

>>> p = paginator.LazyPaginator(range(30), 7, first_page=15, orphans=2)
>>> p.page(1).object_list
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
>>> p.page(2).object_list
[15, 16, 17, 18, 19, 20, 21]
>>> p.num_pages
3
>>> p.page(3).object_list
[22, 23, 24, 25, 26, 27, 28, 29]
>>> p.num_pages
3
>>> p.page(4)
Traceback (most recent call last):
EmptyPage: That page contains no results

>>> p = paginator.LazyPaginator(range(10), 1, first_page=8, orphans=2)
>>> p.page(2)
Traceback (most recent call last):
EmptyPage: That page contains no results
>>> p.page(1).object_list
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> p.num_pages
1


LOW LEVEL TESTS: PAGE LIST

>>> p = paginator.Paginator(range(30), 7, orphans=2)
>>> request = WSGIRequest({'REQUEST_METHOD': "get", 'QUERY_STRING': "page=2"})
>>> pages = models.PageList(request, p.page(2), 'page')
>>> len(pages)
4
>>> pages.last().path
u'/?page=4'
>>> pages.current().url
'?page=2'
>>> pages.previous().number == pages.first().number
True
>>> [unicode(i) for i in pages]
[u'<a class="endless_page_link" href="/" rel="page">1</a>', u'<span class="endless_page_current"><strong>2</strong></span>', u'<a class="endless_page_link" href="/?page=3" rel="page">3</a>', u'<a class="endless_page_link" href="/?page=4" rel="page">4</a>']


LOW LEVEL TESTS: DECORATORS

>>> def view(request, extra_context=None, template="default.html"):
...     context = {}
...     if extra_context is not None:
...         context.update(extra_context)
...     return template, context
... 
>>> request = WSGIRequest({'REQUEST_METHOD': "get"})
>>> request_querystring = WSGIRequest({'REQUEST_METHOD': "get", 'QUERY_STRING': "page=2&mypage=10&querystring_key=page"})
>>> ajax_request = WSGIRequest({'REQUEST_METHOD': "get", 'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
>>> ajax_request_querystring = WSGIRequest({'REQUEST_METHOD': "get", 'QUERY_STRING': "page=2&mypage=10&querystring_key=page", 'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
>>> ajax_request_querystring_mypage = WSGIRequest({'REQUEST_METHOD': "get", 'QUERY_STRING': "page=2&mypage=10&querystring_key=mypage", 'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
>>> decorated = decorators.page_template("page.html")(view)
>>> decorated_mypage = decorators.page_template("mypage.html", key="mypage")(view)
>>> decorated_multiple = decorators.page_templates({"page.html": None, "mypage.html": "mypage"})(view)

>>> decorated(request)
('default.html', {'page_template': 'page.html'})
>>> decorated(request_querystring)
('default.html', {'page_template': 'page.html'})
>>> decorated(ajax_request)
('page.html', {'page_template': 'page.html'})
>>> decorated(ajax_request_querystring)
('page.html', {'page_template': 'page.html'})
>>> decorated(ajax_request_querystring_mypage)
('default.html', {'page_template': 'page.html'})

>>> decorated_mypage(request)
('default.html', {'page_template': 'mypage.html'})
>>> decorated_mypage(request_querystring)
('default.html', {'page_template': 'mypage.html'})
>>> decorated_mypage(ajax_request)
('default.html', {'page_template': 'mypage.html'})
>>> decorated_mypage(ajax_request_querystring)
('default.html', {'page_template': 'mypage.html'})
>>> decorated_mypage(ajax_request_querystring_mypage)
('mypage.html', {'page_template': 'mypage.html'})

>>> decorated_multiple(request)
('default.html', {'page_template': 'page.html'})
>>> decorated_multiple(request_querystring)
('default.html', {'page_template': 'page.html'})
>>> decorated_multiple(ajax_request)
('page.html', {'page_template': 'page.html'})
>>> decorated_multiple(ajax_request)
('page.html', {'page_template': 'page.html'})
>>> decorated_multiple(ajax_request_querystring)
('page.html', {'page_template': 'page.html'})
>>> decorated_multiple(ajax_request_querystring_mypage)
('mypage.html', {'page_template': 'mypage.html'})


LOW LEVEL TESTS: UTILS

>>> utils.get_page_number_from_request(request, "page")
1
>>> utils.get_page_number_from_request(request_querystring, "page")
2
>>> utils.get_page_number_from_request(request_querystring, "mypage")
10

>>> utils.get_page_numbers(1, 20)
['previous', 1, 2, 3, None, 18, 19, 20, 'next']
>>> utils.get_page_numbers(4, 20)
['previous', 1, 2, 3, 4, 5, 6, None, 18, 19, 20, 'next']
>>> utils.get_page_numbers(7, 20)
['previous', 1, 2, 3, None, 5, 6, 7, 8, 9, None, 18, 19, 20, 'next']
>>> utils.get_page_numbers(18, 20)
['previous', 1, 2, 3, None, 16, 17, 18, 19, 20, 'next']
>>> utils.get_page_numbers(5, 20, extremes=1, arounds=4)
['previous', 1, 2, 3, 4, 5, 6, 7, 8, 9, None, 20, 'next']
>>> utils.get_page_numbers(5, 20, extremes=1, arounds=0)
['previous', 1, None, 5, None, 20, 'next']
>>> utils.get_page_numbers(10, 20, extremes=2, arounds=3)
['previous', 1, 2, None, 7, 8, 9, 10, 11, 12, 13, None, 19, 20, 'next']
>>> utils.get_page_numbers(4, 20, extremes=1, arounds=2)
['previous', 1, 2, 3, 4, 5, 6, None, 20, 'next']
>>> utils.get_page_numbers(5, 20, extremes=1, arounds=2)
['previous', 1, None, 3, 4, 5, 6, 7, None, 20, 'next']
>>> utils.get_page_numbers(5, 20, extremes=0, arounds=2)
['previous', 3, 4, 5, 6, 7, 'next']
>>> utils.get_page_numbers(5, 20, extremes=0, arounds=0)
['previous', 5, 'next']
>>> utils.get_page_numbers(5, 20, extremes=0, arounds=10)
['previous', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 'next']


TEMPLATETAG TESTS: SIMPLE USAGE

>>> t = Template("{% load endless %}{% paginate objects %}{{ objects }}{% show_pages %}")
>>> request = WSGIRequest({'REQUEST_METHOD': "get"})
>>> context = Context({'objects': range(30), 'request': request})
>>> html = t.render(context)

>>> context["endless_default_number"]
1
>>> context["objects"]
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> page = context["endless_page"]

>>> page.number
1
>>> page.has_next()
True
>>> page.has_previous()
False
>>> page.next_page_number()
2

>>> [i.strip() for i in html.split('\\n') if i.strip()]
[u'[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]', u'<span class="endless_page_current"><strong>1</strong></span>', u'<a class="endless_page_link" href="/?page=2" rel="page">2</a>', u'<a class="endless_page_link" href="/?page=3" rel="page">3</a>', u'<a class="endless_page_link" href="/?page=2" rel="page">&gt;&gt;</a>']


TEMPLATETAG TESTS: USING ALL ARGUMENTS

>>> t = Template("{% load endless %}{% paginate 5 objects starting from page 3 using key with url as paginated_objects %}{{ objects }}{% get_pages %}")
>>> request = WSGIRequest({'REQUEST_METHOD': "get"})
>>> context = Context({'objects': range(30), 'request': request, 'url':"/myurl/", 'key': 'mykey'})
>>> html = t.render(context)

>>> context["paginated_objects"]
[10, 11, 12, 13, 14]
>>> context["endless_default_number"]
3

>>> page = context["endless_page"]
>>> page.number
3
>>> page.has_next()
True
>>> page.has_previous()
True
>>> page.next_page_number()
4

>>> pages = context["pages"]
>>> pages.last().number
6
>>> pages.last().is_last
True
>>> pages.last().path
'/myurl/?mykey=6'
>>> pages.current().number
3
>>> pages.current().querystring_key
'mykey'
>>> pages.previous().url
'?mykey=2'
>>> pages.next().is_current
False
>>> pages.next().path
'/myurl/?mykey=4'
>>> [(i.number, i.path) for i in pages]
[(1, '/myurl/?mykey=1'), (2, '/myurl/?mykey=2'), (3, '/myurl/'), (4, '/myurl/?mykey=4'), (5, '/myurl/?mykey=5'), (6, '/myurl/?mykey=6')]


TEMPLATETAG TESTS: GETTING A DIFFERENT PAGE

>>> t = Template("{% load endless %}{% paginate 7 objects %}{{ objects }}{% get_pages as mypages %}")
>>> request = WSGIRequest({'REQUEST_METHOD': "get", 'QUERY_STRING': "page=2"})
>>> context = Context({'objects': range(30), 'request': request})
>>> html = t.render(context)

>>> context["objects"]
[7, 8, 9, 10, 11, 12, 13]
>>> pages = context["mypages"]
>>> pages.current().number
2


TEMPLATETAG TESTS: GETTING AN INVALID PAGE

>>> t = Template("{% load endless %}{% paginate 7 objects %}{{ objects }}{% get_pages as mypages %}")
>>> request = WSGIRequest({'REQUEST_METHOD': "get", 'QUERY_STRING': "page=6"})
>>> context = Context({'objects': range(30), 'request': request})
>>> html = t.render(context)

>>> context["objects"]
[0, 1, 2, 3, 4, 5, 6]
>>> context["endless_page"].number
1


TEMPLATETAG TESTS: ORPHANS

>>> settings.ORPHANS = 3
>>> t = Template("{% load endless %}{% paginate 7 objects %}{{ objects }}{% get_pages %}")
>>> request = WSGIRequest({'REQUEST_METHOD': "get", 'QUERY_STRING': "page=4"})
>>> context = Context({'objects': range(30), 'request': request})
>>> html = t.render(context)

>>> context["objects"]
[21, 22, 23, 24, 25, 26, 27, 28, 29]
>>> context["endless_page"].number
4
>>> context["pages"].current().is_last
True


TEMPLATETAG TESTS: LAZY PAGINATION

>>> t = Template("{% load endless %}{% lazy_paginate 6 objects %}{{ objects }}{% get_pages %}")
>>> request = WSGIRequest({'REQUEST_METHOD': "get", 'QUERY_STRING': "page=2"})
>>> context = Context({'objects': range(30), 'request': request})
>>> html = t.render(context)

>>> isinstance(context["endless_page"].paginator, paginator.LazyPaginator)
True
>>> context["endless_page"].paginator.num_pages
3
>>> context["objects"]
[6, 7, 8, 9, 10, 11]


TEMPLATETAG TESTS: MULTIPLE PAGINATION

>>> t = Template("{% load endless %}{% lazy_paginate 6 objects as myobjects %}{{ myobjects }}{% get_pages as mypages %}{% show_more %}{% paginate other_objects using 'mypage' %}{{ other_objects }}{% get_pages %}{{ pages }}")
>>> request = WSGIRequest({'REQUEST_METHOD': "get", 'QUERY_STRING': "page=2&mypage=3"})
>>> context = Context({'objects': range(30), 'other_objects': list(string.lowercase), 'request': request})
>>> html = t.render(context)

>>> context["myobjects"]
[6, 7, 8, 9, 10, 11]
>>> context["other_objects"]
['u', 'v', 'w', 'x', 'y', 'z']
>>> context["mypages"].current().number
2
>>> context["pages"].current().number
3
>>> [i.strip() for i in html.split('\\n') if i.strip()]
[u'[6, 7, 8, 9, 10, 11]', u'<div class="endless_container">', u'<a class="endless_more" href="/?page=3&amp;mypage=3" rel="page">more</a>', u'<div class="endless_loading" style="display: none;">loading</div>', u'</div>', u'[&#39;u&#39;, &#39;v&#39;, &#39;w&#39;, &#39;x&#39;, &#39;y&#39;, &#39;z&#39;]', u'<a class="endless_page_link" href="/?page=2&amp;mypage=2" rel="mypage">&lt;&lt;</a>', u'<a class="endless_page_link" href="/?page=2" rel="mypage">1</a>', u'<a class="endless_page_link" href="/?page=2&amp;mypage=2" rel="mypage">2</a>', u'<span class="endless_page_current"><strong>3</strong></span>']


TEMPLATETAG TESTS: DIFFERENT NUMBER OF ITEMS IN THE FIRST PAGE

>>> t = Template("{% load endless %}{% lazy_paginate 2,6 objects %}{{ objects }}{% get_pages %}")
>>> request = WSGIRequest({'REQUEST_METHOD': "get", 'QUERY_STRING': "page=1"})
>>> context = Context({'objects': range(30), 'request': request})
>>> html = t.render(context)
>>> context["objects"]
[0, 1]
>>> len(context["pages"])
2

>>> t = Template("{% load endless %}{% paginate 2,6 objects %}{{ objects }}{% get_pages %}")
>>> request = WSGIRequest({'REQUEST_METHOD': "get", 'QUERY_STRING': "page=3"})
>>> context = Context({'objects': range(30), 'request': request})
>>> html = t.render(context)
>>> context["objects"]
[8, 9, 10, 11, 12, 13]
>>> len(context["pages"])
6
>>> context["pages"].previous().number
2

>>> t = Template("{% load endless %}{% paginate 15,6 objects starting from page 2 %}{{ objects }}{% get_pages %}")
>>> request = WSGIRequest({'REQUEST_METHOD': "get", 'QUERY_STRING': "page=1"})
>>> context = Context({'objects': range(30), 'request': request})
>>> html = t.render(context)
>>> context["objects"]
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
>>> context["pages"].current().url
'?page=1'

>>> t = Template("{% load endless %}{% paginate 15,6 objects starting from page 2 using 'mypage' %}{{ objects }}{% get_pages %}")
>>> request = WSGIRequest({'REQUEST_METHOD': "get"})
>>> context = Context({'objects': range(30), 'request': request})
>>> html = t.render(context)
>>> context["objects"]
[15, 16, 17, 18, 19, 20]
>>> context["pages"].previous().path
u'/?mypage=1'
>>> context["pages"].current().url
''
>>> context["pages"].last().number
3


TEMPLATETAG TESTS: CURRENT PAGE NUMBER

>>> t = Template("{% load endless %}{% show_current_number %}")
>>> request = WSGIRequest({'REQUEST_METHOD': "get", 'QUERY_STRING': "page=2001"})
>>> context = Context({'request': request})
>>> t.render(context)
u'2001'

>>> t = Template("{% load endless %}{% show_current_number using mykey %}")
>>> request = WSGIRequest({'REQUEST_METHOD': "get", 'QUERY_STRING': "page=2001&mypage=5"})
>>> context = Context({'request': request, 'mykey': "mypage"})
>>> t.render(context)
u'5'

>>> t = Template("{% load endless %}{% show_current_number starting from page mypage %}")
>>> request = WSGIRequest({'REQUEST_METHOD': "get"})
>>> context = Context({'request': request, 'mypage': 12})
>>> t.render(context)
u'12'

>>> t = Template("{% load endless %}{% show_current_number as page_number %}")
>>> request = WSGIRequest({'REQUEST_METHOD': "get", 'QUERY_STRING': "page=2001"})
>>> context = Context({'request': request})
>>> t.render(context)
u''

>>> t = Template("{% load endless %}{% show_current_number as page_number %}{{ page_number }}")
>>> request = WSGIRequest({'REQUEST_METHOD': "get", 'QUERY_STRING': "page=2001"})
>>> context = Context({'request': request})
>>> t.render(context)
u'2001'

>>> t = Template("{% load endless %}{% show_current_number starting from page mypage as page_number %}")
>>> request = WSGIRequest({'REQUEST_METHOD': "get"})
>>> context = Context({'request': request, 'mypage': 12})
>>> t.render(context)
u''

>>> t = Template("{% load endless %}{% show_current_number starting from page mypage as page_number %}{{ page_number }}")
>>> request = WSGIRequest({'REQUEST_METHOD': "get"})
>>> context = Context({'request': request, 'mypage': 12})
>>> t.render(context)
u'12'

>>> t = Template("{% load endless %}{% show_current_number using mykey %}{{ page_number }}")
>>> request = WSGIRequest({'REQUEST_METHOD': "get", 'QUERY_STRING': "page=2001&mypage=9"})
>>> context = Context({'request': request, 'mykey': "mypage"})
>>> t.render(context)
u'9'

>>> t = Template("{% load endless %}{% show_current_number using 'another_key' %}{{ page_number }}")
>>> request = WSGIRequest({'REQUEST_METHOD': "get", 'QUERY_STRING': "page=2001&mypage=9"})
>>> context = Context({'request': request, 'mykey': "mypage"})
>>> t.render(context)
u'1'

"""}
