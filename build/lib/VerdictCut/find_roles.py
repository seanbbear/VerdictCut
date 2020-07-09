import json
import re

def find_roles(cj_doc, target_roles = ['上訴人','被告','選任辯護人'],\
    break_line='\r\n', name_length_limit = 25 ,search_rows_limit = 100):
    """
    找判決書的人跟此人在判決書中之角色
    cj_doc:str 整篇判決書或部分內容 
    target_roles:list->str 要找的腳色名稱, e.g. 上訴人、被告
    name_length_limit:int 限制找到的名稱長度
    search_rows_limit:int 要搜尋cj_doc的前x列
    """
    role_clean_patterns=["^即　"," ","律師$","（.*）","\(.*\)"]
    cj_doc_rows = cj_doc.split(break_line)[:search_rows_limit]
    
    people = []
    encode_reg_role_clean_chars = "|".join(role_clean_patterns)
    last_role_flag = 'undefine'
    # last_index = 1
    for index,cj_doc_row in enumerate(cj_doc_rows):
        cj_doc_row = re.sub(encode_reg_role_clean_chars,"",cj_doc_row)
        cj_doc_row_keep_full_space = cj_doc_row
        cj_doc_row = cj_doc_row.replace("　","")
        for role in target_roles:
            encode_reg_roles = r"^"+role
            if(re.match(encode_reg_roles,cj_doc_row)):
                target_name = cj_doc_row.replace(role,"")
                if len(target_name) > name_length_limit or len(target_name) == 0:
                    continue
                
                # print(role,target_name)
                people.append({"name":target_name, "role":role})
                last_role_flag = role

                last_index = index + 1
                break
            elif(re.match(r"^　+.+$",cj_doc_row_keep_full_space)):
                role = last_role_flag
                target_name = cj_doc_row_keep_full_space.replace("　","")
                if(last_role_flag != 'undefine'):
                    # print(role,target_name)
                    people.append({"name":target_name, "role":role})
                
                last_index = index + 1
                break
    return people

# 讀取裁判(judgement)全文
def loadData():
    judgement = []
    with open('./law.json','r',encoding='utf-8') as f:
        for line in f.readlines():
            doc = json.loads(line)
            jud = doc['judgement']
            judgement.append(jud)
    return judgement

if __name__ == "__main__":
    data = loadData()    
    people = find_roles(data[7])
    print(people)