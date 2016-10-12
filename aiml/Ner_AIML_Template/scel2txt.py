#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: minghui.ymh
# @date: 16/7/28
# !/usr/bin/python


import struct
import sys
import codecs
import os
import binascii
import pdb

# 搜狗的scel词库就是保存的文本的unicode编码，每两个字节一个字符（中文汉字或者英文字母）
# 找出其每部分的偏移位置即可
# 主要两部分
# 1.全局拼音表，貌似是所有的拼音组合，字典序
#       格式为(index,len,pinyin)的列表
#       index: 两个字节的整数 代表这个拼音的索引
#       len: 两个字节的整数 拼音的字节长度
#       pinyin: 当前的拼音，每个字符两个字节，总长len
#
# 2.汉语词组表
#       格式为(same,py_table_len,py_table,{word_len,word,ext_len,ext})的一个列表
#       same: 两个字节 整数 同音词数量
#       py_table_len:  两个字节 整数
#       py_table: 整数列表，每个整数两个字节,每个整数代表一个拼音的索引
#
#       word_len:两个字节 整数 代表中文词组字节数长度
#       word: 中文词组,每个中文汉字两个字节，总长度word_len
#       ext_len: 两个字节 整数 代表扩展信息的长度，好像都是10
#       ext: 扩展信息 前两个字节是一个整数(不知道是不是词频) 后八个字节全是0
#
#      {word_len,word,ext_len,ext} 一共重复same次 同音词 相同拼音表

# 拼音表偏移，
startPy = 0x1540;

# 汉语词组表偏移
startChinese = 0x2628;

# 全局拼音表

GPy_Table = {}

# 解析结果
# 元组(词频,拼音,中文词组)的列表
GTable = []


def byte2str(data):
    '''将原始字节码转为字符串'''
    i = 0;
    length = len(data)
    ret = u''
    while i < length:
        x = data[i] + data[i + 1]
        t = unichr(struct.unpack('H', x)[0])
        if t == u'\r':
            ret += u'\n'
        elif t != u' ':
            ret += t
        i += 2
    return ret


# 获取拼音表
def getPyTable(data):
    if data[0:4] != "\x9D\x01\x00\x00":
        return None
    data = data[4:]
    pos = 0
    length = len(data)
    while pos < length:
        index = struct.unpack('H', data[pos] + data[pos + 1])[0]
        # print index,
        pos += 2
        l = struct.unpack('H', data[pos] + data[pos + 1])[0]
        # print l,
        pos += 2
        py = byte2str(data[pos:pos + l])
        # print py
        GPy_Table[index] = py
        pos += l


# 获取一个词组的拼音
def getWordPy(data):
    pos = 0
    length = len(data)
    ret = u''
    while pos < length:
        index = struct.unpack('H', data[pos] + data[pos + 1])[0]
        ret += GPy_Table[index]
        pos += 2
    return ret


# 获取一个词组
def getWord(data):
    pos = 0
    length = len(data)
    ret = u''
    while pos < length:
        index = struct.unpack('H', data[pos] + data[pos + 1])[0]
        ret += GPy_Table[index]
        pos += 2
    return ret


# 读取中文表
def getChinese(data):
    # import pdb
    # pdb.set_trace()

    pos = 0
    length = len(data)
    while pos < length:
        # 同音词数量
        same = struct.unpack('H', data[pos] + data[pos + 1])[0]
        # print '[same]:',same,

        # 拼音索引表长度
        pos += 2
        py_table_len = struct.unpack('H', data[pos] + data[pos + 1])[0]
        # 拼音索引表
        pos += 2
        try:
            py = getWordPy(data[pos: pos + py_table_len])
        except KeyError:
            break
        # 中文词组
        pos += py_table_len

        for i in xrange(same):
            # 中文词组长度
            c_len = struct.unpack('H', data[pos] + data[pos + 1])[0]
            # 中文词组
            pos += 2
            word = byte2str(data[pos: pos + c_len])
            # 扩展数据长度
            pos += c_len
            ext_len = struct.unpack('H', data[pos] + data[pos + 1])[0]
            # 词频
            pos += 2
            count = struct.unpack('H', data[pos] + data[pos + 1])[0]

            # 保存
            GTable.append((count, py, word))

            # 到下个词的偏移位置
            pos += ext_len


def deal(file_name):
    print '-' * 60
    f = open(file_name, 'rb')
    data = f.read()
    f.close()

    if data[0:12] != "\x40\x15\x00\x00\x44\x43\x53\x01\x01\x00\x00\x00":
        print "确认你选择的是搜狗(.scel)词库?"
        sys.exit(0)
    # # pdb.set_trace()
    #
    # print "词库名：", byte2str(data[0x130:0x338])  # .encode('GB18030')
    # print "词库类型：", byte2str(data[0x338:0x540])  # .encode('GB18030')
    # print "描述信息：", byte2str(data[0x540:0xd40])  # .encode('GB18030')
    # print "词库示例：", byte2str(data[0xd40:startPy])  # .encode('GB18030')

    getPyTable(data[startPy:startChinese])
    getChinese(data[startChinese:])


if __name__ == '__main__':

    in_path = "/Users/yangminghui/AliDrive/Work/聊天机器人/语料/搜狗词库"
    out_path = "/Users/yangminghui/AliDrive/Work/聊天机器人/语料/sougou_entity"
    files = os.listdir(in_path)
    for f in files:
        print f
        # GTable = []
        deal(os.path.join(in_path, f))
        # with open(os.path.join(out_path, f + ".txt"), "w") as outf:
        #     for count, py, word in GTable:
        #         outf.write(unicode(word + "\n").encode('utf-8'))
    with open(os.path.join(out_path, "sougou.txt"), "w") as outf:
        for count, py, word in GTable:
            outf.write(unicode(word + "\n").encode('utf-8'))
