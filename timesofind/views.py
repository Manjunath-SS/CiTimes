from django.http import HttpResponse
from django.template import Context, loader
import urllib.request
from .models import Toi
import ast, re, datetime, requests

def timesofind(request):
    try:
        #page=urllib.request.urlopen('https://newsapi.org/v1/articles?source=the-hindu&sortBy=top&apiKey=0ca6ea2df18e4d128f1490601cfa5785')
        #extracted_data=page.read()
        #string_data=str(extracted_data,'utf-8')
        response=requests.get(' https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=0ca6ea2df18e4d128f1490601cfa5785', verify=False)
        extracted_data=response.content
        string_data=str(extracted_data,'utf-8')
        regex = r"\[.*\]"
        lists=re.findall(regex,string_data)
        li=''.join(lists)
        regex2 = r"\{.*\}"
        list2=re.findall(regex2,li)
        strng=''.join(list2)
        mydict=ast.literal_eval(strng)
        for tup in mydict:
            if not Toi.objects.filter(title=tup['title']):
                if not tup['author']:
                    tup['author']="Anonymous"
                Toi.objects.create(author=tup['author'],title=tup['title'],description=tup['description'],url=tup['url'],imgurl=tup['urlToImage'],pubat=tup['publishedAt'])

    finally:
        today = datetime.datetime.today()
        rec=Toi.objects.all().order_by('-pubat')
        tmpl = loader.get_template("TimesOfIndia.html")
        cont = Context({'Toi': rec, 'Daa': today})
        return HttpResponse(tmpl.render(cont))
