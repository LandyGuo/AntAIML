#coding=utf-8
"""This file contains the default (English) substitutions for the
PyAIML kernel.  These substitutions may be overridden by using the
Kernel.loadSubs(filename) method.  The filename specified should refer
to a Windows-style INI file with the following format:

    # lines that start with '#' are comments

    # The 'gender' section contains the substitutions performed by the
    # <gender> AIML tag, which swaps masculine and feminine pronouns.
    [gender]
    he = she
    she = he
    # and so on...

    # The 'person' section contains the substitutions performed by the
    # <person> AIML tag, which swaps 1st and 2nd person pronouns.
    [person]
    I = you
    you = I
    # and so on...

    # The 'person2' section contains the substitutions performed by
    # the <person2> AIML tag, which swaps 1st and 3nd person pronouns.
    [person2]
    I = he
    he = I
    # and so on...

    # the 'normal' section contains subtitutions run on every input
    # string passed into Kernel.respond().  It's mainly used to
    # correct common misspellings, and to convert contractions
    # ("WHAT'S") into a format that will match an AIML pattern ("WHAT
    # IS").
    [normal]
    what's = what is
"""

defaultGender = {
    # masculine -> feminine
    "he": "she",
    "him": "her",
    "his": "her",
    "himself": "herself",

    # feminine -> masculine    
    "she": "he",
    "her": "him",
    "hers": "his",
    "herself": "himself",
}

defaultPerson = {
    # 1st->3rd (masculine)
    "I": "he",
    "me": "him",
    "my": "his",
    "mine": "his",
    "myself": "himself",
    u"我": u"你 ",

    # 3rd->1st (masculine)
    "he":"I",
    "him":"me",
    "his":"my",
    "himself":"myself",
    
    # 3rd->1st (feminine)
    "she":"I",
    "her":"me",
    "hers":"mine",
    "herself":"myself",
}

defaultPerson2 = {
    # 1st -> 2nd
    "I": "you",
    "me": "you",
    "my": "your",
    "mine": "yours",
    "myself": "yourself",
    # u"我": u"你 ",

    # 2nd -> 1st
    "you": "me",
    u"你": u"我 ",
    "your": "my",
    "yours": "mine",
    "yourself": "myself",
}





# TODO: this list is far from complete
defaultNormal = {


    u"咋":u"怎 么 ",
    u"啥":u"什 么 ",
    u"能":u"可 以 ",

    u"股 票":u"基 金 ",

    u"哪 些":u"什 么 ",
    u"玩 儿":u"玩 ",
    u"什 么 地 方":u"哪 里 ",
    u"哪 儿":u"哪 里 ",

    u"啥 时 候":u"什 么 时 间 ",
    u"啥 时 间":u"什 么 时 间 ",
    u"有 多 远":u"多 远 ",
    u"要 多 久":u"多 久 ",
    u"有 多 久":u"多 久 ",
    u"多 长 时 间":u"多 久 ",
    u"有 多 大":u"多 大 ",

    u"听 过":u"知 道 ",
    u"认 识":u"知 道 ",
    u"了 解":u"知 道 ",
    u"时 候":u"时 间 ",
    u"是 什 么 样 的":u"怎 么 样 ",

    u"如 何":u"怎 么 样 ",
    u"啥 样":u"怎 么 样 ",
    u"怎 样":u"怎 么 样 ",

    u"买 啥":u"买 什 么 ",
    u"卖 啥":u"卖 什 么 ",
    u"你 喜 欢":u"喜 欢",
    u"你 知 道":u"知 道",
    u"多 少 岁":u"几 岁",
    # u"啥 时 候":u"什 么 时 间",
    u"瘦 身":u"减 肥 ",
    u"塑 身":u"减 肥 ",
    u"年 龄":u"岁 数 ",
    u"芳 龄":u"岁 数 ",
    u"贵 庚":u"岁 数 ",
    u"年 纪":u"岁 数 ",
    u"最 爱":u"喜 欢 ",
    u"愿 望":u"梦 想 ",
    u"记 忆 最 深":u"难 忘 ",
    u"印 象 最 深":u"难 忘 ",
    # u"么":u"吗",怎么
    u"没 意 思":u"无 聊 ",
    u"帅 气":u"帅 ",
    u"漂 亮":u"美 ",
    u"美 丽":u"美 ",
    u"大 学":u"学 校 ",
    u"小 学":u"学 校 ",
    u"中 学":u"学 校 ",
    u"好 看 的 书":u"好 书 ",
    u"姓 名":u"名 字 ",
    u"明 星":u"演 员 ",
    u"愿 望":u"梦 想 ",

    u"体 育 项 目":u"运 动 ",
    # u"你":u"我 ",
    u"男 人":u"男 生",
    u"女 人":u"女 生",
    u"兴 趣 爱 好":u"爱 好",
    u"不 明 白":u"不 懂",
    u"阿 里":u"阿 里 巴 巴",



    # "wanna": "want to",
    # "gonna": "going to",

    # "I'm": "I am",
    # "I'd": "I would",
    # "I'll": "I will",
    # "I've": "I have",
    # "you'd": "you would",
    # "you're": "you are",
    # "you've": "you have",
    # "you'll": "you will",
    # "he's": "he is",
    # "he'd": "he would",
    # "he'll": "he will",
    # "she's": "she is",
    # "she'd": "she would",
    # "she'll": "she will",
    # "we're": "we are",
    # "we'd": "we would",
    # "we'll": "we will",
    # "we've": "we have",
    # "they're": "they are",
    # "they'd": "they would",
    # "they'll": "they will",
    # "they've": "they have",

    "y'all": "you all",    

    "can't": "can not",
    "cannot": "can not",
    "couldn't": "could not",
    "wouldn't": "would not",
    "shouldn't": "should not",
    
    "isn't": "is not",
    "ain't": "is not",
    "don't": "do not",
    "aren't": "are not",
    "won't": "will not",
    "weren't": "were not",
    "wasn't": "was not",
    "didn't": "did not",
    "hasn't": "has not",
    "hadn't": "had not",
    "haven't": "have not",

    "where's": "where is",
    "where'd": "where did",
    "where'll": "where will",
    "who's": "who is",
    "who'd": "who did",
    "who'll": "who will",
    "what's": "what is",
    "what'd": "what did",
    "what'll": "what will",
    "when's": "when is",
    "when'd": "when did",
    "when'll": "when will",
    "why's": "why is",
    "why'd": "why did",
    "why'll": "why will",

    "it's": "it is",
    "it'd": "it would",
    "it'll": "it will",
}
