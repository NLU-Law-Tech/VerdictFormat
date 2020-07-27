import json
import re

import requests

def Formal_to_Test(Formal_format_path,output_path):
    # 讀檔
    with open(Formal_format_path,'r',encoding='utf-8') as f:
        Formal_format=json.load(f)

    output_dict={}
    outputs_dict_list=[]
    for index,Formal_dict in enumerate(Formal_format):
        content_id=""
        name=Formal_dict["name"]
        job_location_list,job_title_list=get_job_location_and_title(Formal_dict["positions"])
        laws_list=get_laws_list(Formal_dict["laws"])

        output_dict["content_id"]=content_id
        output_dict["name"]=name
        output_dict["job_location"]=job_location_list
        output_dict["job_title"]=job_title_list
        output_dict["laws"]=laws_list
        outputs_dict_list.append(output_dict.copy())
        output_dict.clear()
    with open(output_path,"w",encoding="utf-8") as file:
        json.dump(outputs_dict_list,file,ensure_ascii=False)

def Test_to_Formal(Test_format_path,output_path):

    with open(Test_format_path,'r',encoding='utf-8') as f:
        Test_format=json.load(f)

    output_dict={}
    outputs_dict_list=[]
    for index,content_dict in enumerate(Test_format):
        # 先讀取測試格式資料
        content_id=content_dict["content_id"]
        name=content_dict["name"]
        job_location_list=content_dict["job_location"]
        job_title_list=content_dict["job_title"]
        laws_list=content_dict["laws"]        
        # 開始建立正式的格式
    
        # 先建立 positions 這個字典
        posistions_dict=get_posistions_dict(job_location_list,job_title_list)
        # print(posistions_dict)
        statuses_dict=get_statuses_dict()
        # print(statuses_dict)
        laws_dict=get_laws_dict(laws_list)
        # print(laws_dict)
        output_dict["name"]=name
        output_dict["statuses"]=statuses_dict
        output_dict["positions"]=posistions_dict
        output_dict["laws"]=laws_dict
        outputs_dict_list.append(output_dict.copy())
        output_dict.clear()

    with open(output_path,"w",encoding="utf-8") as file:
        json.dump(outputs_dict_list,file,ensure_ascii=False)

def Labeled_to_Test(Labeled_data):
    output_dict={}
    output_dict_list=[]
    for index,each_verdict in enumerate(Labeled_data):
        # 讀值
        doc_id=each_verdict["doc_id"]
        identities_list=extract_content_from_dict(json.loads(each_verdict["identities"]))
        laws_list=extract_content_from_dict(json.loads(each_verdict["laws"]))
        name=json.loads(each_verdict["name"])["content"]
        positions_list=extract_content_from_dict(json.loads(each_verdict["positions"]))
        units_list=extract_content_from_dict(json.loads(each_verdict["units"]))


        # 開始轉格式
        output_dict["content_id"]=doc_id
        output_dict["name"]=name
        output_dict["job_location"]=units_list
        output_dict["job_title"]=positions_list
        output_dict["laws"]=laws_list
        
        output_dict_list.append(output_dict.copy())
        output_dict.clear()
    return output_dict_list

def get_posistions_dict(job_location_list,job_title_list):

    posistions_dict={} 
    posistion_dict={}
    posistions_list=[] # 因為posistions 要放list
    # 可能什麼都沒有
    if len(job_location_list)==0 and len(job_title_list)==0:
        posistion_dict["work unit"]=""
        posistion_dict["title"]=""
        posistion_dict["locations"]=[]
        posistions_list.append(posistion_dict)
        posistions_dict["postitions"]=posistions_list.copy()  
    # 其中一個沒有
    elif len(job_location_list)==0 and len(job_title_list)!=0:
        for i in range(len(job_title_list)):
            posistion_dict["work unit"]=""
            posistion_dict["title"]=job_title_list[i]
            posistion_dict["locations"]=[]
            posistions_list.append(posistion_dict.copy())
            posistion_dict.clear()
        posistions_dict["postitions"]=posistions_list.copy()
    elif len(job_location_list)!=0 and len(job_title_list)==0:
        for i in range(len(job_location_list)):
            posistion_dict["work unit"]=job_location_list[i]
            posistion_dict["title"]=""
            posistion_dict["locations"]=[]
            posistions_list.append(posistion_dict.copy())
            posistion_dict.clear()
        posistions_dict["postitions"]=posistions_list.copy()
    # 可能會有多個職稱跟單位，全部配起來~
    else:
        for i in range(len(job_title_list)):
            for j in range(len(job_location_list)):
                posistion_dict["work unit"]=job_location_list[j]
                posistion_dict["title"]=job_title_list[i]
                posistion_dict["locations"]=[]
                posistions_list.append(posistion_dict.copy())
                posistion_dict.clear()
        posistions_dict["postitions"]=posistions_list.copy()

    return posistions_dict

def get_statuses_dict():
    statuses_dict={}
    status_dict={}
    statuses_list=[]
    status_dict["status"]=""
    status_dict["locations"]=[]
    statuses_list.append(status_dict)

    return statuses_list

def get_laws_dict(laws_list):
    # laws_dict裡面小的dict
    law_dict={}
    # 要回傳的dict
    laws_dict={}
    # 存放 law_dict 的list
    laws_dict_list=[]
    if len(laws_list)==0:
        laws_dict["laws"]=[] 
    else:
        for law in laws_list:
            act,article,paragraph,subparagraph=extract_laws_spa(law)
            law_dict["act"]=act
            if article!="":
                law_dict["article"]=article
            if paragraph!="":
                law_dict["paragraph"]=paragraph
            if subparagraph!="":
                law_dict["subparagraph"]=subparagraph
            law_dict["locations"]=[]
            laws_dict_list.append(law_dict.copy())
            law_dict.clear()
        laws_dict["laws"]=laws_dict_list
    return laws_dict

def extract_laws_spa(law):
    # 取出法條的款項條
    regex_article="第\d*條"
    regex_paragraph="第\d*項"
    regex_subparagraph="第\d*款"
    # 假設都沒找到就回傳law
    act=law
    article=""
    paragraph=""
    subparagraph=""
    # 找第幾條，有找到再往下找第幾項
    article_position=re.search(regex_article,law)
    if article_position != None:
        # 取出act(法條名稱，不包含條項款)
        act=law[:article_position.start()]
        article_text=law[article_position.start():article_position.end()]
        # 取出數字
        article=get_laws_number(article_text)
        # 找第幾項，有找到再往下找第幾款
        paragraph_position=re.search(regex_paragraph,law)
        if paragraph_position != None:
            paragraph_text=law[paragraph_position.start():paragraph_position.end()]
            paragraph=get_laws_number(paragraph_text)
            subparagraph_position=re.search(regex_subparagraph,law)
            if subparagraph_position != None:
                subparagraph_text=law[subparagraph_position.start():subparagraph_position.end()]
                subparagraph=get_laws_number(subparagraph_text)

    return act,article,paragraph,subparagraph

def get_laws_number(laws_with_number):
    result=""
    for k in laws_with_number:
        if k.isdigit():
            result+=k
    if result!="":
        return int(result)
    else:
        return result

def get_job_location_and_title(Formal_dict_positions):
    job_location_list=[]
    job_title_list=[]
    for index,positions_dict in enumerate(Formal_dict_positions):
        job_location_list.append(positions_dict["work unit"])
        job_title_list.append(positions_dict["title"])
    return job_location_list,job_title_list

def get_laws_list(laws_dict):
    laws_list=[]
    
    for index,law_dict in enumerate(laws_dict):
        law=law_dict["act"]
        if "article" in law_dict:
            article=str(law_dict["article"])
            law = law+"第"+article+"條"
        if "paragraph" in law_dict:
            paragraph=str(law_dict["paragraph"])
            law = law +"第"+paragraph+"項"
        if "subparagraph" in law_dict:
            subparagraph=str(law_dict["subparagraph"])    
            law = law +"第"+subparagraph+"款"
        laws_list.append(law)
    return laws_list

def extract_content_from_dict(content_dict_list):
    content_list=[]
    for i in content_dict_list:
        content_list.append(clean_string(i["content"]))
    return content_list
def clean_string(dirty_str):
    # 去空白
    clean_str=re.sub(r"\s+","",dirty_str)
    return clean_str
if __name__ == "__main__":
    # Formal_file_path="C:/Yao/ITRI/API (1)/output_v2.json"
    # Test_file_path="C:/Yao/ITRI/API (1)/Test.json"
    # Test_to_Formal_path="C:/Yao/ITRI/API (1)/Test_Formal.json"
    # Formal_to_Test_path="C:/Yao/ITRI/API (1)/Formal_Test.json"
    # with open(Formal_file_path,'r',encoding='utf-8') as f:
    #     Formal_format=json.load(f)
    # with open(Test_file_path,'r',encoding='utf-8') as f:
    #     Test_format=json.load(f)
    # print(Formal_format)
    # print(Test_format)
    # Test_to_Formal(Test_format,Test_to_Formal_path)
    # Formal_to_Test(Formal_format,Formal_to_Test_path)
    response_data = requests.get("http://140.120.13.242:15005/dump_labeled_data")
    labeled_data=response_data.json()
    Labeled_to_Test(labeled_data)
  
        # print(json(i['laws']))
    # print(list_of_dicts)