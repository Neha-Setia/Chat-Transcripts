
import pydot
import numpy as np
import pandas as pd
import json

from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.externals.six import StringIO  
from sklearn.tree import export_graphviz
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import _tree
from collections import OrderedDict
import ibm_boto3
from botocore.client import Config
import io



class DecisionTreeQuestionnaire:

    current_question = ""
    isModelTrained = False
    tags=[]
    des=[]
    paths=[]
    feature_names = []
    temp_qtn_ans = {}
    questions={'Travel Type': 'What type of Travel is it?(Cust/ Non_cust)',
     'Travel Purpose': 'What is the Travel Purpose?(Deal/PMR/Training/Conf)',
     'Travel Restrictions': 'Are there any Travel Restrictions?(Low/High/WW)',
     'Billable': 'Is it Billable?(Y/N)',
     'Estimated cost': 'What is the Estimated cost?(Low/High)',
     'WW Approval': 'Is it WW Approval?(Y/N)',
     'Local Skills Exsit': 'Do Local Skills Exsit?(Y/N)',
     'Customer stratigic': 'How important is Customer stratigic?(High/Low)',
     'PMR Exist': 'Does PMR Exist?(Y/N)',
     'PMR severity': 'What is the PMR severity?(1/2/3)',
     'SalesConnect Exist': 'Does SalesConnect Exist?(Y/N)',
     'Customer sentiments': 'What is the Customer sentiment?(Positive/Negative/Neutral)',
     'How Many people traveling': 'How Many people traveling?(1/2/3)',
     'Role of Person': 'What is the Role of the Person?(Critical/Important)',
     'Visit number': 'Do you have a Visit number?',
     'Revenue Impact': 'What is the Revenue Impact?(High/Low)',
     'Deal Closure Time': 'How long is the Deal Closure Time?(Next Q/Long term/Next 9 months/Next 6 months)',
     'Conference Flag': 'Does Conference Flag exist?(Repute/No)',
     'Speaker': 'Are you a Speaker?(Y/N)',
     'Trainimg': 'Are you Trainimg?(Y/N)',
     'Number of Aud.': 'What is the Number of Aud.?(Large/Small)',
     'Is Aud. decsion maker': 'Are Aud. the decsion makers?(Y/N)'}
    
    searchFeature = 'Local Skills Exsit=Y' #Here we are taking all the paths that has 'Estimated cost' feature.     
    
    @staticmethod
    def encode_onehot(df, cols):
        vec = DictVectorizer()
        
        vec_data = pd.DataFrame(vec.fit_transform(df[cols].to_dict(orient='records')).toarray())
        vec_data.columns = vec.get_feature_names()
        vec_data.index = df.index
        
        df = df.drop(cols, axis=1)
        df = df.join(vec_data)
        return df

    @staticmethod
    def tree_to_code(tree):
        tree_ = tree.tree_
        
        feature_name = [
            DecisionTreeQuestionnaire.feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]
        
        '''class_name = [
            class_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree.classes_
        ]'''
        print ("def tree({}):".format(", ".join(feature_name)))
        '''print ("def tree({}):".format(", ".join(class_name)))'''
        
        def recurse(node, depth):
            indent = "  " * depth
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                print( "{}if {} <= {}:".format(indent, name, threshold))
                recurse(tree_.children_left[node], depth + 1)
                print ("{}else:  # if {} > {}".format(indent, name, threshold))
                recurse(tree_.children_right[node], depth + 1)
            else:
                print( "{}return {}".format(indent, tree_.value[node]))
    
        recurse(0, 1)
        
    @staticmethod
    def tree_to_code2(tree, class_names):
        tree_ = tree.tree_
        
        feature_name = [
            DecisionTreeQuestionnaire.feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]
    #     print(feature_name)
        class_name = [
            class_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree.classes_
        ]
    
        def recurse(node, depth, tag):
            if(not tree_.feature[node]):
                return
            
                
            if tree_.feature[node] == _tree.TREE_UNDEFINED:
                x=np.argmax(max(tree_.value[node]))
                DecisionTreeQuestionnaire.tags.append(tag)
                DecisionTreeQuestionnaire.des.append(class_names[x])
                
                if DecisionTreeQuestionnaire.searchFeature in  DecisionTreeQuestionnaire.des:
                    y = OrderedDict(zip(DecisionTreeQuestionnaire.des, DecisionTreeQuestionnaire.tags))
                    DecisionTreeQuestionnaire.paths.append(y)
                        
                    print(DecisionTreeQuestionnaire.des)
                    
                
            else:
    #             print("hi")
                DecisionTreeQuestionnaire.tags.append(tag)
                #print(tags)
                DecisionTreeQuestionnaire.des.append(feature_name[node])
                #print(des)
                recurse(tree_.children_left[node], depth + 1,'left')
                DecisionTreeQuestionnaire.des.pop(-1)
                DecisionTreeQuestionnaire.tags.pop(-1)
                recurse(tree_.children_right[node], depth + 1,'right')
                DecisionTreeQuestionnaire.des.pop(-1)
                DecisionTreeQuestionnaire.tags.pop(-1)
            
    
        recurse(0, 1, 'NULL')
        
    t_f={}
    


    @staticmethod
    def question_and_answer():
        var = 'null'
        f='true'
        for i in DecisionTreeQuestionnaire.paths:
            if f=='true': 
                var = 'null'
                for k,v in i.items():
                    flag =''
                    if v=='NULL' or v==var or var=='null':
                        flag='true'
                    else:
                        flag='false'
                    if flag=='true':
                        c = k
                        if c in DecisionTreeQuestionnaire.feature_names:
                            n = c.split('=')[0]
                            ans=c.split('=')[1]
                        else:
                            n=c
                        if n in DecisionTreeQuestionnaire.questions:
                            if DecisionTreeQuestionnaire.questions[n] not in DecisionTreeQuestionnaire.temp_qtn_ans:
                                #a = input(questions[n])
                                
                                #current_question = DecisionTreeQuestionnaire.questions[n]
                                current_question = {}
                                current_question["question"] = DecisionTreeQuestionnaire.questions[n]
                                json_response = json.dumps(current_question)
                                return json_response
                                #a = DecisionTreeQuestionnaire.questions_answers(DecisionTreeQuestionnaire.questions[n]) 
                                #DecisionTreeQuestionnaire.t_f[k]=a
                            else:
                                a=DecisionTreeQuestionnaire.temp_qtn_ans.get(DecisionTreeQuestionnaire.questions[n])
                            if a.lower()==ans.lower():
                                var='right'
                            else:
                                var='left'
                        else:
                            print(n)
                            f='false'
                            decision = {}
                            decision["decision"] = n
                            json_response = json.dumps(decision)
                            return json_response
                    else:
                        var='abc'
    
                #print("-----------------------------------")
        if f=='true':
            print('Your inputs are not defined')
                
    @staticmethod
    def get_csv_file_data():
        auth_endpoint = 'https://iam.bluemix.net/oidc/token'
        service_endpoint = 'https://s3-api.us-geo.objectstorage.softlayer.net'
        
        credentials = {
          "apikey": "vFBl_WRKxTI95W68F3-lil3PsOywVtmDRRxyMjZIPh0j",
          "endpoints": "https://cos-service.bluemix.net/endpoints",
          "iam_apikey_description": "Auto generated apikey during resource-key operation for Instance - crn:v1:bluemix:public:cloud-object-storage:global:a/f2043d7defcd090971c66795a834d43c:8e7d0cae-69cd-45ec-8430-f0389e234d95::",
          "iam_apikey_name": "auto-generated-apikey-e87c006c-e6b2-4ba3-853d-9941b41c0db2",
          "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
          "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/f2043d7defcd090971c66795a834d43c::serviceid:ServiceId-26be900e-809f-4c40-90b1-57b422e9691a",
          "resource_instance_id": "crn:v1:bluemix:public:cloud-object-storage:global:a/f2043d7defcd090971c66795a834d43c:8e7d0cae-69cd-45ec-8430-f0389e234d95::"
        }
        
        resource = ibm_boto3.resource('s3',
                              ibm_api_key_id=credentials['apikey'],
                              ibm_service_instance_id=credentials['resource_instance_id'],
                              ibm_auth_endpoint=auth_endpoint,
                              config=Config(signature_version='oauth'),
                              endpoint_url=service_endpoint)
        
        bucket_name = 'cognitivebpm-bucket'
        filename = 'Data.csv'
        obj = resource.Object(bucket_name=bucket_name, key=filename).get()
        obj_bytes = obj['Body'].read() # .read() returns a byte string
        print(obj_bytes)
        obj_bytes_stream = io.BytesIO(obj_bytes) # that we convert to a stream
        return pd.read_csv(obj_bytes_stream, sep=",") # and eventually a pandas dataframe        
    
    @staticmethod
    def train():

        balance_data_excel = DecisionTreeQuestionnaire.get_csv_file_data()
        
                
        ''' Clean the Data and replace with nan
        '''
        balance_data_excel = balance_data_excel.replace(r'^\s*$',str(np.nan),regex=True).replace('',str(np.nan))
        balance_data_excel= balance_data_excel.applymap(str)
        balance_data_excel
        
        
        print ("Dataset Length:: ", len(balance_data_excel))
        print ("Dataset Shape:: ", balance_data_excel.shape)
        
        
        X = balance_data_excel.iloc[:, :-1]
        y = balance_data_excel.iloc[:, 22]
    
        X = DecisionTreeQuestionnaire.encode_onehot(X, X.columns.get_values().tolist())
        X.head()
    
    
        le_y = LabelEncoder()
        y = le_y.fit_transform(y)
    
        
        cols= X.columns
        for c in cols:
            x = c
            if x.split('=')[1] == 'nan':
                 X.drop(c, axis=1, inplace=True)
        
        
        
        X_train, X_test, y_train, y_test = train_test_split( X, y, test_size = 0.1, random_state = 100)
        
        clf_entropy = DecisionTreeClassifier(criterion = "entropy", random_state = 100,
         max_depth=100, min_samples_leaf=5, min_samples_split=8)
        abc = clf_entropy.fit(X_train, y_train)
        
        y_pred = clf_entropy.predict(X_test)
    
    
        print ("Accuracy is ", accuracy_score(y_test,y_pred)*100)
    
    
        
        ''' Convert Target Classes to key-value pairs
        '''
        print("le2")
        class_names = {}
        for i in range(len(le_y.classes_)):
            class_names[i] = le_y.classes_[i]
        print(class_names)
    
    
        
        features = {}
        for i in range(len(list(X.columns[0:56]))):
            features[i] = X.columns[i]
        
        #features
        
        for i in range(len(list(X.columns[0:56]))):
            DecisionTreeQuestionnaire.feature_names.append(X.columns[i])
        #feature_names
        
        
        
        dot_data = StringIO()
        export_graphviz(clf_entropy , out_file=dot_data,  
                        filled=True, rounded=True,
                        special_characters=True, feature_names=features, class_names=class_names)
        
        # graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
        graph = pydot.graph_from_dot_data(dot_data.getvalue())
        # graph_from_dot_file()
        
        graph.write_png('decisiontree.png')
        
        DecisionTreeQuestionnaire.tree_to_code(abc)
    
    
            
        DecisionTreeQuestionnaire.tree_to_code2(abc,class_names)
    
    
        DecisionTreeQuestionnaire.paths
    
        DecisionTreeQuestionnaire.isModelTrained = True
    
        for i in DecisionTreeQuestionnaire.paths:
            for k,v in i.items():
                print (k+' : '+v)
            print("-----------------------------------")    
    
            print('Your inputs are not defined')
            
            #DecisionTreeQuestionnaire.question_and_answer(paths,feature_names,questions)
        
