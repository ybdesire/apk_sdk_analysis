import pattern
import pickle

__author__ = 'Bin Yin (ybdesire@gmail.com)'
__date__ = '2016-08-31'
__version_info__ = (0, 0, 0)
__version__ = '.'.join(str(i) for i in __version_info__)




def extract_item(item):
    result = []
    for k in item:
        v = item[k]
        actions = v[0]['actions']
        for a in actions:
            oper = a[0]
            if (oper=='M'):
                methodstr = a[1]
                methodstrList = methodstr.split("->")
                if methodstrList[0].startswith("L") and "/" in methodstrList[0]:
                    className = methodstrList[0]
                else:
                    className = "." + methodstrList[0]
                methodName = methodstrList[-1]
                result.append( (className, methodName) )
    return result




def extract_methods():
    r1 = extract_item(pattern.PERSONAL_INFORMATION)
    r2 = extract_item(pattern.SENSITIVE_DATA_INPUT_DEVICE)
    r3 = extract_item(pattern.COST_SENSITIVE_API)
    r4 = extract_item(pattern.SYSTEM_SENSITIVE_API)
    r5 = extract_item(pattern.OTHER_NEGATIVE_API)
    r6 = extract_item(pattern.NATIVE_SENSITIVE_API)
    pickle.dump(r1+r2+r3+r4+r5+r6, open('api_list.p', 'wb') )








if __name__=='__main__':
    extract_methods()
