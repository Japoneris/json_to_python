
# coding: utf-8

# **To do : find a way to rassemble similar objects**
# 

# In[1]:

import json


# In[3]:




# In[2]:

txt = """{
    "maps": [
        {
            "id": "blabla",
            "iscategorical": "0"
        },
        {
            "id": "blabla",
            "iscategorical": "0"
        }
    ],
    "masks": {
        "id": "valore"
    },
    "om_points": "value",
    "parameters": {
        "id": "valore"
    }
}"""


# In[292]:

txt = """{
    "identity": {
        "local": ":Local",
        "version": 1,
        
    },
    "ciphers": [/*Cipher list to decrypt the share_private_key*/]
}"""


# 

# In[77]:

def object_of_level(serial) :
    """
    Look at an object
    extract basic types
    return uncommon types
    """
    KEYS = serial.keys()
    UNCLASSED = []
    CLASSED = []
    cnt = 0
    
    for idx, i in enumerate(KEYS) :
        ob = serial[i]
        ty = None
        if type(ob) == list :
            #empty list ?
            ob = ob[0]
            ty = check_type(ob)
            print("this is a list of ", ty)
            CLASSED.append([ty])
        else :
            ty = check_type(ob)
            print("this is a ", ty)
            CLASSED.append(ty)
            
        if ty == dict :
            UNCLASSED.append(ob)
            cnt += 1
            
    return CLASSED, UNCLASSED
        

def check_type(item) :
    if type(item) == dict :
        return dict
    try :
        f = float(item)
        if f == round(f) :
            return int
        else :
            return float
    except :
        if item == "true" or item == "false" :
            return bool
        else :
            return str
            
def python_repr_type (ty, level, objname):
    if ty == bool : 
        return True
    elif ty == int :
        return 0
    elif ty == float :
        return 0.1
    elif ty == str :
        return '"string"'
    elif ty == dict :
        return "{}{}".format(objname, level)
    return None


# #### Writable to python

# In[81]:

def item_to_python_text(serial, classname="MyObject_") :
    KEYS = serial.keys()
    cnt = 0
    my_text = "class {}(object) :\n".format(classname)
    UNCLASSED = []
    
    for idx, i in enumerate(KEYS) :
        ob = serial[i]
        if type(ob) == list :
            ob = ob[0]
            ty = check_type(ob)
            tx = python_repr_type(ty, cnt, classname)
            my_text += "    {} = [{}]\n".format(i, tx)

        else :
            ty = check_type(ob)
            tx = python_repr_type(ty, cnt, classname)
            my_text += "    {} = {}\n".format(i, tx)
        
        if type(ob) == dict :
            cnt+=1
            UNCLASSED.append(ob)
        
    for idx, i in enumerate(UNCLASSED) :
        my_text += "\n" + item_to_python_text(i, classname="{}_{}".format(classname, idx))
    
    return my_text

def write_my_object(txti, name="testfile.py") :
    with open(name, "w") as file:  
        file.write(txti)
        


# In[82]:

my_extractable_object= json.loads(txt)

txt_exp = item_to_python_text(my_extractable_object)
      
write_my_object(txt_exp, "create_class_v2.py")

