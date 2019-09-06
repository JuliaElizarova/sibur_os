from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from .forms import DummyForm

import pickle
import json

from keras.models import load_model
from keras import backend as K
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class FormDummyView(View):

    def get(self, request):
        #form = DummyForm()
        return render(request, 'form.html', {})

    def post(self, request):
        if 'okof_first' in request.POST:
            text = request.POST.get('text')
            context = self.FirstLevelOKOF(text)

        elif 'okof_second' in request.POST:
            okof_first_level = request.POST.get('okof-first-level')
            text = request.POST.get('text')
            context = {}
            context['text_0'] = request.POST.get('ag')
            context = self.SecondLevelOKOF(text, okof_first_level, context)

        elif 'okof_third' in request.POST:
            okof_second_level = request.POST.get('okof-second-level')
            text = request.POST.get('text')
            context = {}
            context['text_0'] = request.POST.get('ag')
            context = self.ThirdLevelOKOF(text, okof_second_level, context)

        elif 'okof_all' in request.POST:
            okof_third_level = request.POST.get('okof-third-level')
            text = request.POST.get('text')
            context = {}
            context['text_0'] = request.POST.get('ag')
            context = self.AllLevelOKOF(text, okof_third_level, context)

        return render(request, 'form.html', context)
        #return JsonResponse(context)

    
    def FirstLevelOKOF(self, text):
        text_list = []
        text_list.append(str(text))

        main_path = 'C:\\Users\\Julia\\sibur_os'
        #амортизационная группа
        #f_2 = open(r''+main_path +'\\Data_new\\Models\\vect_ag_5.txt', 'rb')
        f_2 = open(r'Data_new/Models/vect_ag_5.txt', 'rb')
        vectorizer = pickle.load(f_2)
        x_test = vectorizer.transform(text_list)
        new_model = load_model(r'Data_new/Models/nn_model_ag_5.h5')
        prediction_ag = new_model.predict([x_test])
        K.clear_session() 
        predicted_ag = np.round(prediction_ag)
        predicted_ag = int((str((predicted_ag[0][0])+1))[:-2])
        list_ag_new = []
        list_ag_new.append(predicted_ag)
        for i in range(1, 11):
            if not i in list_ag_new:
                list_ag_new.append(i)
        #заполнение словаря context по амортизационной группе
        context = {'text_' + str(num): list_ag_new[num] for num in range(0, 10)}
        context['text'] = text

        #спи - из словаря
        with open(main_path+'\\Data_new\\dict_ag.json', 'r') as f: 
            dict_okof = json.loads(str(f.read()))
        for code in dict_okof.keys():
            if str(code) == str(predicted_ag):
                context['ag_spi'] = dict_okof[code][0]
                break


        #вид основного фонда
        f_2 = open(r''+main_path+'\\Data_new\\Models\\first.txt', 'rb')        
        vectorizer = pickle.load(f_2)
        x_test = vectorizer.transform(text_list)
        new_model = load_model(main_path+'\\Data_new\\Models\\nn_model_first.h5') 
        prediction_1 = new_model.predict([x_test]) 
        K.clear_session()
        with open(main_path+'\\Data_new\\dict_y_one.json', 'r') as f:
            dict_y = json.loads(str(f.read()))          
        prediction_2 = list(np.array(prediction_1)[0])      
        dict_test = {key: value for value, key in enumerate(prediction_2)}
        dict_sort = sorted(dict_test.items())        
        list_5 = dict_sort[len(dict_sort):len(dict_sort)-6:-1] #словарь отсортированный по вероятностям - первые 5 наиболее вероятных значений
        #list_5_classes = [i[0] for i in list_5] #5 наиболее вероятных исхода
        result = []
        for i in list_5: #подтягваем номера ОКОФ по номерам в модели
            for j in dict_y.keys():
                if i[1] == dict_y[j]:
                    result.append(j)
        
        context['okof_0'] = result[0] #самая вероятная категория
        context['okof_1'] = result[1]
        context['okof_2'] = result[2]
        context['okof_3'] = result[3]
        context['okof_4'] = result[4]  
        context['prob_okof_0'] = str(dict_sort[-1][0])
        #context['prob_okof_1'] = dict_sort[-2][0]
        #context['prob_okof_2'] = dict_sort[-3][0]
        #context['prob_okof_3'] = dict_sort[-4][0]
        #context['prob_okof_4'] = dict_sort[-5][0]


        #---------------------добавляем все возможные варианты по всем 5 категориям---------------------------
        first_model_result = result #список 5 наиболее вероятных исходов по первой цифре кода
        #prediction fo each model (5)
        result_second = []
        for model_num in first_model_result:
            with open(main_path+'\\Data_new\\dict_okof_current_data_new.json', 'r') as f:
                dict_all = json.loads(str(f.read()))
            h = ''
            for number in dict_all.keys():
                if model_num == number:
                    if len(dict_all[number]) == 1: #если у нас только одна возможная категория у выбранной первой цифры окоф
                        context['okof_2_'  + model_num + '_0'] = next(iter(dict_all[number])) #Возвращает следующий элемент итератора
                    else:
                        h = number
                    break

            if h != '':
                f_2 = open(r''+main_path+'\\Data_new\\Models\\second_'+model_num+'.txt', 'rb')        
                vectorizer = pickle.load(f_2)
                x_test = vectorizer.transform(text_list)
                new_model = load_model(main_path+'\\Data_new\\Models\\nn_model_second_'+model_num+'.h5') 
                prediction_2_1 = new_model.predict([x_test]) 
                K.clear_session()      
                with open(main_path+'\\Data_new\\dict_y_'+model_num+'.json', 'r') as f:
                    dict_y = json.loads(str(f.read()))   
                prediction_2_2 = list(np.array(prediction_2_1)[0])       
                dict_test = {key: value for value, key in enumerate(prediction_2_2)}
                dict_sort = sorted(dict_test.items())
                if (len(dict_sort)) <= 5:
                    list_5 = dict_sort[::-1]
                else:
                    list_5 = dict_sort[len(dict_sort):len(dict_sort)-6:-1]
                result = []
                for i in list_5: #подтягваем номера ОКОФ по номерам в модели
                    for j in dict_y.keys():
                        if i[1] == dict_y[j]:
                            result.append(j)
                            result_second.append(j)

                for i in range(0, len(list_5)):
                        context['okof_2_' + model_num + '_' + str(i)] = result[i]

                # если самая вероятная цифра, то записываем к ней коды
                if model_num == context['okof_0']:
                    for i in range(0, len(list_5)):
                        if i == 0:
                            context['okof_2_0'] = result[i] #находим наиболее вероятное значение для втрой цифры                       
                        context['okof_2_' + str(i)] = result[i]



        #добавляем определение третьей категории окоф
        second_model_result = result_second
        result_third = []
        for model_num in second_model_result:
            with open(main_path+'\\Data_new\\dict_okof_current_data_new.json', 'r') as f:
                dict_all = json.loads(str(f.read()))
            p = ''
            for number in dict_all.keys():
                for number2 in dict_all[number].keys():
                    if model_num == number2:
                        if len(dict_all[number][number2]) == 1:
                            context['okof_3_'  + model_num + '_0'] = next(iter(dict_all[number][number2][0]))
                        else:
                            p = number2
                        break

            if p != '':
                f_2 = open(r''+main_path+'\\Data_new\\Models\\third_'+p+'.txt', 'rb')        
                vectorizer = pickle.load(f_2)
                x_test = vectorizer.transform(text_list)
                new_model = load_model(main_path+'\\Data_new\\Models\\nn_model_third_'+p+'.h5')
                prediction_1 = new_model.predict([x_test])     
                K.clear_session()     
                with open(main_path+'\\Data_new\\dict_y_'+p+'.json', 'r') as f:
                    dict_y = json.loads(str(f.read()))   
                prediction_2 = list(np.array(prediction_1)[0])        
                dict_test = {key: value for value, key in enumerate(prediction_2)}
                dict_sort = sorted(dict_test.items())        
                if (len(dict_sort)) <= 5:
                    list_5 = dict_sort[::-1]
                else:
                    list_5 = dict_sort[len(dict_sort):len(dict_sort)-6:-1]

                result = []
                for i in list_5:
                    for j in dict_y.keys():
                        if i[1] == dict_y[j]:
                            result.append(j)
                            result_third.append(j) 

                for i in range(0, len(list_5)):
                    context['okof_3_' + model_num + '_' + str(i)] = result[i]  

                # если самая вероятная цифра, то записываем к ней коды
                if model_num == context['okof_2_0']:
                    for i in range(0, len(list_5)):
                        if i == 0:
                            context['okof_3_0'] = result[i] #находим наиболее вероятное значение для втрой цифры  
                        context['okof_3_' + str(i)] = result[i]


        #находим основные коды по самому вероятному
        with open(main_path+'\\Data_new\\data_okof.json', 'r', encoding='utf-8') as f: #вести словарь кодов 
            dict_okof = json.loads(str(f.read()))
        result = []
        json_all = []
        for code in dict_okof.keys():
            if str(code[:9]) == context['okof_3_0'] and len(str(code)) == 11:
                result.append(code)
            json_all.append(code)
            #context['discription_' + str(code)] = dict_okof[code]

        for i in range(0, len(result)):
                context['okof_4_' + str(i)] = result[i]

        context['all_count'] = len(result)
        context['context_json_for_js'] = json_all
        #context['text_codes'] = dict_okof

        #content.append(9)
        context = {'context_json': json.dumps(context), 'context': context}
        #-----------------------------------------------------------------------------------------------------

        return context


    def SecondLevelOKOF(self, text, okof_first_level, context):
        main_path = 'C:\\Users\\Julia\\sibur_os'
        text_list = []
        text_list.append(str(text))
        context['text'] = text

        #boxtext = str(self.comboBox.currentText())
        with open(main_path+'\\Data_new\\dict_okof_current_data_new.json', 'r') as f:
            dict_all = json.loads(str(f.read()))
        h = ''
        for number in dict_all.keys():
            if okof_first_level == number:
                if len(dict_all[number]) == 1: #если у нас только одна возможная категория у выбранной первой цифры окоф
                    context['okof_2_0'] = next(iter(dict_all[number])) #Возвращает следующий элемент итератора
                    #context['okof_2_1'], context['okof_2_2'], context['okof_2_3'], context['okof_2_4'] = '', '', '', ''
                else:
                    h = number
                break

        if h != '':
            f_2 = open(r''+main_path+'\\Data_new\\Models\\second_'+h+'.txt', 'rb')        
            vectorizer = pickle.load(f_2)
            x_test = vectorizer.transform(text_list)
            new_model = load_model(main_path+'\\Data_new\\Models\\nn_model_second_'+h+'.h5') 
            prediction_2_1 = new_model.predict([x_test]) 
            K.clear_session()      
            with open(main_path+'\\Data_new\\dict_y_'+h+'.json', 'r') as f:
                dict_y = json.loads(str(f.read()))   
            prediction_2_2 = list(np.array(prediction_2_1)[0])       
            dict_test = {key: value for value, key in enumerate(prediction_2_2)}
            dict_sort = sorted(dict_test.items())

            if (len(dict_sort)) <= 5:
                list_5 = dict_sort[::-1]
            else:
                list_5 = dict_sort[len(dict_sort):len(dict_sort)-6:-1]
            result = []
            for i in list_5: #подтягваем номера ОКОФ по номерам в модели
                for j in dict_y.keys():
                    if i[1] == dict_y[j]:
                        result.append(j)

            for i in range(0, len(list_5)):
                context['okof_2_' + str(i)] = result[i]

        return context


    def ThirdLevelOKOF(self, text, okof_second_level, context):
        main_path = 'C:\\Users\\Julia\\sibur_os'
        text_list = []
        text_list.append(str(text))
        context['text'] = text

        with open(main_path+'\\Data_new\\dict_okof_current_data_new.json', 'r') as f:
            dict_all = json.loads(str(f.read()))
        p = ''
        for number in dict_all.keys():
            for number2 in dict_all[number].keys():
                if okof_second_level == number2:
                    if len(dict_all[number][number2]) == 1:
                        context['okof_3_0'] = next(iter(dict_all[number][number2][0]))
                    else:
                        p = number2
                    break

        if p != '':
            f_2 = open(r''+main_path+'\\Data_new\\Models\\third_'+p+'.txt', 'rb')        
            vectorizer = pickle.load(f_2)
            x_test = vectorizer.transform(text_list)
            new_model = load_model(main_path+'\\Data_new\\Models\\nn_model_third_'+p+'.h5')
            prediction_1 = new_model.predict([x_test])     
            K.clear_session()     
            with open(main_path+'\\Data_new\\dict_y_'+p+'.json', 'r') as f:
                dict_y = json.loads(str(f.read()))   
            prediction_2 = list(np.array(prediction_1)[0])        
            dict_test = {key: value for value, key in enumerate(prediction_2)}
            dict_sort = sorted(dict_test.items())        
            if (len(dict_sort)) <= 5:
                list_5 = dict_sort[::-1]
            else:
                list_5 = dict_sort[len(dict_sort):len(dict_sort)-6:-1]

            result = []
            for i in list_5:
                for j in dict_y.keys():
                    if i[1] == dict_y[j]:
                        result.append(j) 

            for i in range(0, len(list_5)):
                context['okof_3_' + str(i)] = result[i]                     
   
        return context

    
    def AllLevelOKOF(self, text, okof_third_level, context):
        main_path = 'C:\\Users\\Julia\\sibur_os'
        text_list = []
        text_list.append(str(text))
        context['text'] = text

        with open(main_path+'\\Data_new\\data_okof.json', 'r') as f: #вести словарь кодов 
            dict_okof = json.loads(str(f.read()))
        result = []
        for code in dict_okof.keys():
            if str(code[:9]) == okof_third_level and len(str(code)) == 11:
                result.append(code)

        for i in range(0, len(result)):
                context['okof_4_' + str(i)] = result[i]

        return context


