# BurpSuite Plugin
通过字符集编码绕过waf的burp插件

因为小伙伴在实战中有这么个需求（利用字符集编码绕过waf），所以我借着他的这个需求也学习了下burp插件的编写。
# 预览
## ASP.NET+IIS
![enter description here](https://photo.o0o0.club/Charset_encoding_converter__Burp插件/wafg01.gif)

# 使用说明
其实这种方法很早就出来了，但并不通用，感觉也有IIS+ASP.NET的时候可以试一试。
测试环境：Windows10
Burp版本：1.7.36
Jython版本：Jython-standalone-2.7.0

1. burp加载Python运行环境（Python）
![enter description here](https://photo.o0o0.club/Charset_encoding_converter__Burp插件/1616412431734.png)

2. 加载此插件
![enter description here](https://photo.o0o0.club/Charset_encoding_converter__Burp插件/1616412464696.png)

3. 在burp proxy或repeater等选项卡 中右键开启相关选项
![enter description here](https://photo.o0o0.club/Charset_encoding_converter__Burp插件/1616412589499.png)

![enter description here](https://photo.o0o0.club/Charset_encoding_converter__Burp插件/1616412639010.png)

不通用
Nginx+php	 No</br>
Apache+php	 No</br>
IIS+ASP.NET勉强能用

中文无解（比如上传场景）。。。

# 支持列表如下
Target |Post</br>(application/x-www-form-urlencoded)|Note(s)
-|:-:|:-:
Nginx,uWSGI-Django-Python3 | IBM037, IBM500, cp875, IBM1026, IBM273|[x] query string and body were encoded</br>[x] url-decoded parameters in query string and body afterwards</br>[x] equal sign and ampersand needed to be encoded as well (no url-encoding
Nginx,uWSGI-Django-Python2|IBM037, IBM500, cp875, IBM1026, utf-16, utf-32, utf-32BE, IBM424|[x] query string and body were encoded</br>[x] url-encoded parameters in query string and body</br>[x] equal sign and ampersand should not be encoded in any way
Apache-TOMCAT8-JVM1.8-JSP|IBM037, IBM500, IBM870, cp875, IBM1026, IBM01140, IBM01141, IBM01142, IBM01143, IBM01144, IBM01145, IBM01146, IBM01147, IBM01148, IBM01149, utf-16, utf-32, utf-32BE, IBM273, IBM277, IBM278, IBM280, IBM284, IBM285, IBM290, IBM297, IBM420, IBM424, IBM-Thai, IBM871, cp1025|[x] query string in its original format (not encoded – could be url- encoded as usual)</br>[x] equal sign and ampersand should not be encoded in any way</br>[x] body could be sent with/without url-encoding
Apache-TOMCAT7-JVM1.6-JSP|IBM037, IBM500, IBM870, cp875, IBM1026, IBM01140, IBM01141, IBM01142, IBM01143, IBM01144, IBM01145, IBM01146, IBM01147, IBM01148, IBM01149, utf-16, utf-32, utf-32BE, IBM273, IBM277, IBM278, IBM280, IBM284, IBM285, IBM297, IBM420, IBM424, IBM-Thai, IBM871, cp1025|[x] query string in its original format (not encoded)</br>[x] equal sign and ampersand should not be encoded</br>[x] body could be sent with/without url-encoding
Apache -PHP5(mod_php & FastCGI)|None|N/A
IIS8-PHP7.1-FastCGI|None|N/A
IIS6, 7.5, 8, 10 -ASP Classic|None|N/A
IIS6, 7.5, 8, 10 -ASPX (v4.x)|IBM037, IBM500, IBM870, cp875, IBM1026, IBM01047, IBM01140, IBM01141, IBM01142, IBM01143, IBM01144, IBM01145, IBM01146, IBM01147, IBM01148, IBM01149, utf-16, unicodeFFFE, utf-32, utf-32BE, IBM273, IBM277, IBM278, IBM280, IBM284, IBM285, IBM290, IBM297, IBM420,IBM423, IBM424, x-EBCDIC-KoreanExtended, IBM-Thai, IBM871, IBM880, IBM905, IBM00924, cp1025|[x] query string and body were encoded</br>[x] equal sign and ampersand should not be encoded</br>[x] body could be sent with/without url-encoding

# 参考资料
https://www.nccgroup.com/uk/about-us/newsroom-and-events/blogs/2017/august/request-encoding-to-bypass-web-application-firewalls/

# 食用说明
开袋不即食，需要蘸着jython吃