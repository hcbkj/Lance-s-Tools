import re
import docx


def patch_list(xml):
    # 文本循环
    result = re.findall(r'\[%L(\d?)(.*?)%\]', xml)
    for number, context in result:
        raw = context
        v = re.findall(r'\{\{(.*?)\}\}', context)
        for i in v:
            print(i)
            if i.startswith("案件."): continue
            if "|" in i:
                f = i.replace("|", '\|')
            else:
                f = i
            context = re.sub(r'\{\{%s\}\}' % f, string=context, repl='{{案件.%s}}' % (i))
        if number:
            n = int(number)
        else:
            n = -1
        if n == -1:
            xml = xml.replace('[%L' + raw + '%]', "{%- for 案件 in _LIST_ -%}" + context + "{%- endfor -%}")
        else:
            xml = xml.replace('[%L' + number + raw + '%]',
                              "{%- for 案件 in _LIST_[:" + str(n) + "] -%}" + context + "{%- endfor -%}")
    return xml

