function agChoice(event) {
    let num = document.getElementsByTagName('select')[0].value;
    if (num === '1') {
        document.getElementById('feedback-text1').value = 'От 1 года до 2 лет включительно'
    } else if (num === '2') {
        document.getElementById('feedback-text1').value = 'Свыше 2 лет до 3 лет включительно'
    } else if (num === '3') {
        document.getElementById('feedback-text1').value = 'Свыше 3 лет до 5 лет включительно'
    } else if (num === '4') {
        document.getElementById('feedback-text1').value = 'Свыше 5 лет до 7 лет включительно'
    } else if (num === '5') {
        document.getElementById('feedback-text1').value = 'Свыше 7 лет до 10 лет включительно'
    } else if (num === '6') {
        document.getElementById('feedback-text1').value = 'Свыше 10 лет до 15 лет включительно'
    } else if (num === '7') {
        document.getElementById('feedback-text1').value = 'Свыше 15 лет до 20 лет включительно'
    } else if (num === '8') {
        document.getElementById('feedback-text1').value = 'Свыше 20 лет до 25 лет включительно'
    } else if (num === '9') {
        document.getElementById('feedback-text1').value = 'Свыше 25 лет до 30 лет включительно'
    } else if (num === '10') {
        document.getElementById('feedback-text1').value = 'Свыше 30 лет'
    };
}




function firstOKOF(event){
    var context = JSON.parse("{{ context_json|escapejs }}");
    //alert(context.text);
    
    let num = document.getElementsByTagName('select')[1].value; //зачение основного селекта первого уровня
    let option_first_0 = document.getElementById('option-first-0').value;
    let option_first_1 = document.getElementById('option-first-1').value;
    let option_first_2 = document.getElementById('option-first-2').value;
    let option_first_3 = document.getElementById('option-first-3').value;
    let option_first_4 = document.getElementById('option-first-4').value;

    let arr_options_first = [option_first_0, option_first_1, option_first_2, option_first_3, option_first_4]; //массив первых 5 наиболее вероятных значений для первой цифры [300, 210, 310]
    
    for (let i = 0; i < arr_options_first.length; i++){
        if (arr_options_first[i] === num){
            for (let key in context){
                if (('okof_2_' + arr_options_first[i] + '_0' === key) || ('okof_2_' + arr_options_first[i] + '_1' === key) || ('okof_2_' + arr_options_first[i] + '_2' === key) || ('okof_2_' + arr_options_first[i] + '_3' === context.key) || ('okof_2_' + arr_options_first[i] + '_4' === key)) {
                    if (typeof context['okof_2_' + arr_options_first[i] + '_0'] == "undefined") {
                        document.getElementById('option-second-0').innerHTML = ''
                    } else {
                        document.getElementById('option-second-0').innerHTML = context['okof_2_' + arr_options_first[i] + '_0']
                    }
                    if (typeof context['okof_2_' + arr_options_first[i] + '_1'] == "undefined") {
                        document.getElementById('option-second-1').innerHTML = ''
                    } else {
                        document.getElementById('option-second-1').innerHTML = context['okof_2_' + arr_options_first[i] + '_1']
                    }
                    if (typeof context['okof_2_' + arr_options_first[i] + '_2'] == "undefined") {
                        document.getElementById('option-second-2').innerHTML = ''
                    } else {
                        document.getElementById('option-second-2').innerHTML = context['okof_2_' + arr_options_first[i] + '_2']
                    }
                    if (typeof context['okof_2_' + arr_options_first[i] + '_3'] == "undefined") {
                        document.getElementById('option-second-3').innerHTML = ''
                    } else {
                        document.getElementById('option-second-3').innerHTML = context['okof_2_' + arr_options_first[i] + '_3']
                    }
                    if (typeof context['okof_2_' + arr_options_first[i] + '_4'] == "undefined") {
                        document.getElementById('option-second-4').innerHTML = ''
                    } else {
                        document.getElementById('option-second-4').innerHTML = context['okof_2_' + arr_options_first[i] + '_4']
                    }
                    break
                };
            }
        };
    }


    let num2 = document.getElementsByTagName('select')[2].value; //значение основного селекта второго уровня

    let option_second_0 = document.getElementById('option-second-0').value;
    let option_second_1 = document.getElementById('option-second-1').value;
    let option_second_2 = document.getElementById('option-second-2').value;
    let option_second_3 = document.getElementById('option-second-3').value;
    let option_second_4 = document.getElementById('option-second-4').value;

    let arr_options_second = [option_second_0, option_second_1, option_second_2, option_second_3, option_second_4]; //массив первых 5 наиболее вероятных значений для второй цифры
    
    let keys = Object.keys(context);

    for (let i = 0; i < arr_options_second.length; i++){
        if (arr_options_second[i] === num2){
            for (let key in context){
                if (('okof_3_' + arr_options_second[i] + '_0' === key) || ('okof_3_' + arr_options_second[i] + '_1' === key) || ('okof_3_' + arr_options_second[i] + '_2' === key) || ('okof_3_' + arr_options_second[i] + '_3' === context.key) || ('okof_3_' + arr_options_second[i] + '_4' === key)) {

                    if (typeof context['okof_3_' + arr_options_second[i] + '_0'] == "undefined") {
                        document.getElementById('option-third-0').innerHTML = ''
                    } else {
                        document.getElementById('option-third-0').innerHTML = context['okof_3_' + arr_options_second[i] + '_0']
                    }
                    if (typeof context['okof_3_' + arr_options_second[i] + '_1'] == "undefined") {
                        document.getElementById('option-third-1').innerHTML = ''
                    } else {
                        document.getElementById('option-third-1').innerHTML = context['okof_3_' + arr_options_second[i] + '_1']
                    }
                    if (typeof context['okof_3_' + arr_options_second[i] + '_2'] == "undefined") {
                        document.getElementById('option-third-2').innerHTML = ''
                    } else {
                        document.getElementById('option-third-2').innerHTML = context['okof_3_' + arr_options_second[i] + '_2']
                    }
                    if (typeof context['okof_3_' + arr_options_second[i] + '_3'] == "undefined") {
                        document.getElementById('option-third-3').innerHTML = ''
                    } else {
                        document.getElementById('option-third-3').innerHTML = context['okof_3_' + arr_options_second[i] + '_3']
                    }
                    if (typeof context['okof_3_' + arr_options_second[i] + '_4'] == "undefined") {
                        document.getElementById('option-third-4').innerHTML = ''
                    } else {
                        document.getElementById('option-third-4').innerHTML = context['okof_3_' + arr_options_second[i] + '_4']
                    }
                    break

                } else if ((keys[keys.length - 1] === key) && ('okof_3_' + arr_options_second[i] + '_0' !== key) && ('okof_3_' + arr_options_second[i] + '_1' !== key) && ('okof_3_' + arr_options_second[i] + '_2' !== key) && ('okof_3_' + arr_options_second[i] + '_3' !== context.key) && ('okof_3_' + arr_options_second[i] + '_4' !== key)){
                    document.getElementById('option-third-0').innerHTML = arr_options_second[i] + '.00'
                    document.getElementById('option-third-1').innerHTML = ''
                    document.getElementById('option-third-2').innerHTML = ''
                    document.getElementById('option-third-3').innerHTML = ''
                    document.getElementById('option-third-4').innerHTML = ''
                };
            }
        };
    }
}