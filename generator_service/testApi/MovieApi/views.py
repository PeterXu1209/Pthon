from xml.etree.ElementTree import Comment
from django.shortcuts import render
from django.http import HttpResponse
import os
import json
from sklearn.linear_model import ridge_regression
class JsonHandle():
    file_path = ""
    context = None
    __file_handle = None
    def __init__(self,path):
        self.file_path = path
    def open(self):
        self.__file_handle = open(self.file_path,mode='r',encoding='utf-8')
        text = self.__file_handle.read()
        self.context = json.loads(text)
        self.__file_handle.close()
        self.__file_handle = None
    def save(self):
        if self.context:
            self.__file_handle=open(self.file_path,mode='w',encoding='utf-8')
            json.dump(self.context,self.__file_handle,ensure_ascii=False,indent=4)
            self.__file_handle.close()
            self.__file_handle=None
 
    def __del__(self):
        if self.__file_handle:
            self.__file_handle.close()
 
    def __repr__(self):
        if self.context:
            text = json.dumps(self.context,ensure_ascii=False,indent=4)
            return text
        return ""
# Create your views here.
comment_1=[]
k=0
Json_path = '../Json_bank'
file_count = len(os.listdir(Json_path))
def start(request):
    result="no result"
    comment=request.GET['comment']
    comment_1=comment.split(',')

    try:
        print(comment_1)
        for i in range(0,2):
            k=str(i+1)
            json_path = '../Json_bank//'+k+'.json'
            jsonHandle = JsonHandle(json_path)
            jsonHandle.open()
            jsonHandle.context["comment"]=comment_1[i-1]
            jsonHandle.save()
        os.system('python3 /Users/xupeiying/Documents/Code/Big_Projects/Python/generator_service/test.py')
        
        result="success"
    except IOError:
        result = 'Error'
    return HttpResponse(result)