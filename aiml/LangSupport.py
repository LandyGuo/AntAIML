# -*- coding: utf-8 -*-
# from utils.ali_ws import word_seg_original
import jieba
import re
a=u"([\u4e00-\u9fa5]+)( +)" 
b=u"( +)([\u4e00-\u9fa5]+)"

pa = re.compile(a)
pb = re.compile(b)

def isChinese(c):
    # http://www.iteye.com/topic/558050

    r = [
        # 标准CJK文字
        (0x3400, 0x4DB5), (0x4E00, 0x9FA5), (0x9FA6, 0x9FBB), (0xF900, 0xFA2D),
        (0xFA30, 0xFA6A), (0xFA70, 0xFAD9), (0x20000, 0x2A6D6), (0x2F800, 0x2FA1D),
        # 全角ASCII、全角中英文标点、半宽片假名、半宽平假名、半宽韩文字母
        (0xFF00, 0xFFEF),
        # CJK部首补充
        (0x2E80, 0x2EFF),
        # CJK标点符号
        (0x3000, 0x303F),
        # CJK笔划
        (0x31C0, 0x31EF)]
    return any(s <= ord(c) <= e for s, e in r)

def isEnglish(c):
    return (ord('a')<=ord(c)<=ord('z')) or (ord('A')<=ord(c)<=ord('Z'))

def splitUnicode(s):
    assert type(s) == unicode, "string must be a unicode"
    segs = s.split()
    result = []
    for seg in segs:
        if any(map(isChinese, seg)):
            result.extend(splitChinese(seg))
        else:
            result.append(seg)
    return result


def splitChinese(s):
    result = []
    #pure english
    if all([isEnglish(c) for c in s if c!="*" and c!="_" and c!=" "]):
        return s.split()
    s = u"".join(s.strip(u"?？！!,，。.呀啊呢").split())
    #pure chinese
    if all([isChinese(c) for c in s if c!="*" and c!="_" and c!=" "]):
        result = list(s)
    #english and chinese
    else:
        # tmp = word_seg_original(s).split()
        tmp = jieba.cut(s)
        for x in tmp:
            ChineseWord =False
            for c in x:
                if isChinese(c):
                    ChineseWord = True
                    break
            if ChineseWord:
                # print x,"is chinese"
                result.extend(list(x))
            else:
                # print x,"is not chinese"
                result.append(x)
    ret = '|'.join(result)
    return ret.split("|")

def mergeChineseSpace(s):
    assert type(s) == unicode, "string must be a unicode"
    if len(s) == 0 :
        return s
    sa = pa.sub(r"\1",s)
    sb = pb.sub(r"\2",sa)
    return sb
