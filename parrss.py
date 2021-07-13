import copy
import codecs
import re

def clear_file(name):
    input_file = codecs.open(name, 'r')
    output_file = open('temp.htm', 'w')
    for i in range(1, 119):
        next(input_file)
    while True:
        try:
            words = input_file.readline()
        except Exception:
            next(input_file)
            words = input_file.readline()
        output_file.write(words)
        if not words:
            break
    input_file.close()
    output_file.close()


def parse_programm():
    f = open('temp.htm', 'r')
    html = f.read()
    lst = html.split('\n')
    out_text = []
    checked_element = """Установленные программы"""
    checked_end_element = """</TABLE><BR><BR>"""
    checked_header = """<TR><TD><TD><TD><B>Программа</B>&nbsp;&nbsp;<TD CLASS=cr><B>Версия</B>&nbsp;&nbsp;<TD 
    CLASS=cr><B>Размер</B>&nbsp;&nbsp;<TD><B>GUID</B>&nbsp;&nbsp;<TD><B>Издатель</B>&nbsp;&nbsp;<TD 
    CLASS=cr><B>Дата</B> """
    t = -1
    for element in lst:
        if element.find(checked_header) != -1:
            continue
        if t == -1:
            t = element.find(checked_element)
            continue
        if t > 0 and element.find(checked_end_element) != -1:
            t = -1
        if t > 0:
            out = element.replace('<TR><TD><TD><TD>', '')
            out1 = out.replace('&nbsp;&nbsp;<TD CLASS=cr>', '$$').split('$$')[0]
            out_text.append(out1)
    return out_text


def parse_licence():
    f = open('temp.htm', 'r')
    html = f.read()
    lst = html.split('\n')
    out_text = {}
    checked_element = """<A NAME="licenses">Лицензии</A>"""
    checked_end_element = """</TABLE><BR><BR>"""
    checked_header = """<TR><TD><TD><TD><B>Программы</B>&nbsp;&nbsp;<TD><B>Ключ продукта</B>"""
    t = -1
    for element in lst:
        if element.find(checked_header) != -1:
            continue
        if t == -1:
            t = element.find(checked_element)
            continue
        if t > 0 and element.find(checked_end_element) != -1:
            t = -1
        if t > 0:
            out = element.replace('<TR><TD><TD><TD>', '')
            out1 = out.replace('&nbsp;&nbsp;<TD>', '$$').split('$$')[0]
            out_l = out.replace('&nbsp;&nbsp;<TD>', '$$').split('$$')[1]
            out_text[out1] = out_l
    return out_text


def parse_fix():
    f = open('Report_New_0.html', 'r')
    file_element = []
    file_params = []
    check = -1
    while True:
        str = f.readline()
        if not str:
            break
        if re.match(
                r"""<td class="ktlg" COLSPAN=6 ALIGN=CENTER>Каталог C:\\Program\sFiles(\s\(x86\))?\\Secret\sNet\sStudio\\Client\\</td>""",
                str):
            check = 0
            continue
        if check == 0:
            if str.find('<td class="ks" >') != -1:
                name_file = str.replace("<", ">").split(">")[2]
                file_params.append(name_file)
                check = 1
                continue
        if check == 1:
            data_file = str.replace("<", ">").split(">")[2]
            file_params.append(data_file)
            check = 2
            continue
        if check == 2:
            len_file = str.replace("<", ">").split(">")[2]
            file_params.append(len_file)
            check = 3
            continue
        if check == 3:
            if str.find('<td class="ks" ALIGN=CENTER>') != -1:
                ks = str.replace("<", ">").split(">")[2]
                file_params.append(ks)
                check = 0
            else:
                continue
        if str.find("итого:") != -1:
            break
        if not file_params:
            continue
        file_element.append(copy.deepcopy(file_params))
        file_params.clear()
    return file_element


if __name__ == '__main__':
    clear_file('Report.htm')
    # print(parse_programm())
    # print(parse_licence())
    #parse_fix()
    print(len(parse_fix()))
