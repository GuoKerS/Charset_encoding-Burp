#!/usr/bin/env python2
# encoding: utf-8
"""
@file: charset.py
@time: 2020-9-14 17:35
@ide: PyCharm
@author: guoker
@contact: attackesb@gmail.com
"""
import urllib
from burp import IBurpExtender
from burp import IHttpListener
from burp import IExtensionHelpers
from burp import IContextMenuFactory
from burp import IBurpExtenderCallbacks     # 插件接口相关
from javax.swing import JMenu  # 菜单栏相关
from javax.swing import JMenuItem   # 菜单栏相关
from javax.swing import JRadioButtonMenuItem    # 菜单栏相关
from javax.swing import JOptionPane, JFrame, JList, JLabel, JPanel, BoxLayout, JCheckBox, Box
from java.awt import BorderLayout, Dimension


class BurpExtender(IBurpExtender, IHttpListener, IExtensionHelpers, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        """
        注册拓展插件
        :param callbacks:
        :return:
        """
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self._auto = False  # 自动修改的开关
        self._charset = 'IBM037'
        self._encodeEqualSign = False
        self._encodeAmpersand = False
        self._urldecodeInput = True
        self._urlencodeOutput = True

        # 创建窗口
        self._frame = JFrame("Charset setting.")
        self._frame.setDefaultCloseOperation(JFrame.HIDE_ON_CLOSE)
        self._frame.setLocation(100, 100)
        self._frame.setSize(580, 250)

        # 创建列表
        self._list_panle = JPanel()
        self._list_panle.setLayout(BoxLayout(self._list_panle, BoxLayout.Y_AXIS))
        self._code_list = ("IBM037", "IBM500", "IBM1026", "utf-16", "utf-32", "utf-32BE", "cp875")
        self._lst = JList(self._code_list, valueChanged=self.select_charset)
        self._lbl1 = JLabel("Choose code => (*^__^*) ")
        self._list_panle.add(self._lst)

        # 创建复选框
        self._panle = JPanel()
        self._panle.setLayout(BoxLayout(self._panle, BoxLayout.X_AXIS))
        self._box1 = JCheckBox("encodeEqualSign", actionPerformed=self.OnCheckBox)
        self._box2 = JCheckBox("encodeAmpersand", actionPerformed=self.OnCheckBox)
        self._box3 = JCheckBox("urldecodeInput", True, actionPerformed=self.OnCheckBox)
        self._box4 = JCheckBox("urlencodeOutput", True, actionPerformed=self.OnCheckBox)
        self._panle.add(Box.createVerticalGlue())
        self._panle.add(self._box1)
        self._panle.add(Box.createRigidArea(Dimension(25, 0)))
        self._panle.add(self._box2)
        self._panle.add(Box.createRigidArea(Dimension(25, 0)))
        self._panle.add(self._box3)
        self._panle.add(Box.createRigidArea(Dimension(25, 0)))
        self._panle.add(self._box4)

        # 插入控件
        self._frame.add(self._lst, BorderLayout.NORTH)
        self._frame.add(self._panle,BorderLayout.CENTER)
        self._frame.add(self._lbl1, BorderLayout.SOUTH)

        callbacks.setExtensionName("Charset encoding converter.")
        callbacks.registerContextMenuFactory(self)
        callbacks.registerHttpListener(self)
        print Other.banner

    def createMenuItems(self, invocation):
        """
        创建上下文菜单
        :param invocation:
        :return:
        """
        menus = [] # 主菜单
        mainMenu = JMenu("Charset Menu")
        menus.append(mainMenu)

        if invocation.getToolFlag() == IBurpExtenderCallbacks.TOOL_REPEATER or IBurpExtenderCallbacks.TOOL_PROXY:
            mainMenu.add(JMenuItem('Modify', None, actionPerformed=lambda x, y=invocation: self.modify(x, y)))  # 添加子菜单
            mainMenu.add(JMenuItem('Recovery', None, actionPerformed=lambda x, y=invocation: self.recovery(x, y)))
            mainMenu.addSeparator()

        self._auto_modify = JRadioButtonMenuItem("Auto modify", actionPerformed=lambda x, y=invocation: self.auto_modify())
        mainMenu.add(self._auto_modify)
        mainMenu.addSeparator()
        mainMenu.add(JMenuItem('Setting', None, actionPerformed=lambda x, y=invocation: self.setting()))

        if self._auto:
            self._auto_modify.setSelected(True)
        elif not self._auto:
            self._auto_modify.setSelected(False)
        return menus

    def setting(self):
        self._frame.setVisible(True)

    def select_charset(self, event):
        index = self._lst.selectedIndex
        self._lbl1.text = "Choose code => " + self._code_list[index]
        self._charset = self._code_list[index]

    def OnCheckBox(self, event):
        if self._box1.isSelected():
            self._encodeEqualSign = True
        else:
            self._encodeEqualSign = False

        if self._box2.isSelected():
            self._encodeAmpersand = True
        else:
            self._encodeAmpersand = False

        if self._box3.isSelected():
            self._urldecodeInput = True
        else:
            self._urldecodeInput = False

        if self._box4.isSelected():
            self._urlencodeOutput = True
        else:
            self._urlencodeOutput = False

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        """
        当burp发出http请求或响应时，都将调用此方法
        :param toolFlag:
        :param messageIsRequest:
        :param messageInfo:
        :return:
        """
        if not self._auto:  # 默认False、 如果为True就不执行return
            return
        elif not messageIsRequest:
            return
        RequestInfo = self._helpers.analyzeRequest(messageInfo)
        new_headers, new_body = Other.encode_request(self, RequestInfo, messageInfo)
        messageInfo.request = self._helpers.buildHttpMessage(new_headers, new_body)

    def modify(self, x, invocation):
        """
        手动修改
        :param x:
        :param y:   invocation   ==> IContextMenuInvocation
        :return:
        """
        # getSelectedMessages 此方法可用于检索调用上下文菜单时用户显示或选择的HTTP请求/响应的详细信息。
        for HttpRequestResponse in invocation.getSelectedMessages(): # HttpRequestResonese => IHttpRequestResponse类型    用
            request = HttpRequestResponse.getRequest()          # bytes类型      ==>
            RequestInfo = self._helpers.analyzeRequest(bytearray(request))
            new_headers, new_body = Other.encode_request(self, RequestInfo, HttpRequestResponse)
            # 构造HTTP请求
            now_request = self._helpers.buildHttpMessage(new_headers, new_body)
            HttpRequestResponse.setRequest(now_request)

    def recovery(self, x, invocation):
        """
        还原手动修改结果
        :param x:
        :param y:
        :return:
        """
        for HttpRequestResponse in invocation.getSelectedMessages(): # HttpRequestResonese => IHttpRequestResponse类型    用

            request = HttpRequestResponse.getRequest()          # bytes类型      ==>
            RequestInfo = self._helpers.analyzeRequest(bytearray(request))

            # 获取 headers
            now_headers = RequestInfo.getHeaders()

            # # 获取CT 索引
            index = Other.get_header_index(now_headers)

            #去除charset
            new_headers = Other.remove_header(now_headers, index)

            # 获取body
            len_body = RequestInfo.getBodyOffset()
            now_body = HttpRequestResponse.request[len_body:].tostring()

            # 解码
            new_body = Other.decode_charset(text=now_body, self=self)

            # 构造HTTP请求
            now_request = self._helpers.buildHttpMessage(new_headers, bytearray(new_body.encode('utf8')))
            HttpRequestResponse.setRequest(now_request)

    def auto_modify(self):
        """
        将所有burp中的流量都做修改，修改self._auto状态来激活
        :return:
        """
        if self._auto:
            self._auto = False
        elif not self._auto:
            self._auto = True
        print '[*] auto_modify status :', self._auto


class Other(object):
    banner = b'[*] Charset encoding converter..(*^__^*)v0.4 \r\n' \
             b'[*] Load extender ok....\r\n' \
             b'[*] Author: guoker\r\n' \
             b'[*] Ttime: 2020-9-14'

    @staticmethod
    def get_header_index(headers):
        for i in headers:
            if 'Content-Type' in i:
                return headers.index(i)
        return False

    @staticmethod
    def update_header(headers, index, charset):
        head = headers[index].split(': ')
        head[-1] += "; charset=" + charset.lower()
        headers[index] = ': '.join(head)
        return headers

    @staticmethod
    def encode_charset(text, self):
        """
        编码
        https://docs.python.org/3/library/codecs.html#standard-encodings
        :param text:
        :param self:
        :return:
        """
        result =""
        equalSign = "="
        ampersand = "&"
        if self._encodeEqualSign:
            equalSign = equalSign.encode(self._charset)
        if self._encodeAmpersand:
            ampersand = ampersand.encode(self._charset)
        params_list = text.split("&")
        for param_pair in params_list:
            param, value = param_pair.split("=", 1)
            if self._urldecodeInput:
                param = urllib.unquote(param).decode("utf8")
                value = urllib.unquote(value).decode("utf8")
            param = param.encode(self._charset)
            value = value.encode(self._charset)
            if self._urlencodeOutput:
                param = urllib.quote_plus(param)
                value = urllib.quote_plus(value)
            if result:
                result += ampersand
            result += param + equalSign + value
        return result

    @staticmethod
    def decode_charset(text, self):
        result = ""
        equalSign = "="
        ampersand = "&"
        #
        if "&" not in text:
            params_list = text.split(urllib.quote_plus(ampersand.encode(self._charset)))
        else:
            params_list = text.split("&")
        #
        for param_pair in params_list:
            if "=" not in text:
                param, value = param_pair.split(equalSign.encode(self._charset))
            else:
                param, value = param_pair.split("=", 1)
            param = urllib.unquote(param)
            value = urllib.unquote(value)
            param = param.decode(self._charset)
            value = value.decode(self._charset)

            if result:
                result += ampersand
            result += param + equalSign + value
        return result

    @staticmethod
    def remove_header(headers, index):
        head = headers[index].split(': ')
        head[-1] = "application/x-www-form-urlencoded"
        headers[index] = ': '.join(head)
        return headers

    @staticmethod
    def encode_request(self, RequestInfo, messageInfo):
        if RequestInfo.getMethod() != 'POST':
            return

        # 获取header
        now_headers = RequestInfo.headers

        # 获取body
        now_body = messageInfo.request[RequestInfo.getBodyOffset():len(messageInfo.request)]

        # 获取CT索引
        index = Other.get_header_index(now_headers)

        # 判断是否存在CL
        if not index:
            return

        # 根据索引追加charset=ibm037
        new_headers = Other.update_header(now_headers, index, self._charset)

        # 编码body
        now_body = self._helpers.bytesToString(now_body)
        new_body = Other.encode_charset(text=now_body, self=self)

        return new_headers, bytearray(new_body)
