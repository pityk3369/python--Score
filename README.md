# python--Score
这次的爬虫既有账号密码登录，也有验证码和登录角色选择，有点难度了，搞了两天才搞定，看来还是才疏学浅了，通过这个博客将知识点已经坑点等方面进行总结，也是一个学习的过程。
大体思路：
一.确认教务处官网
1.随便登录用户密码，确认From Data
2.确定验证码链接
二.初步访问
4.构造自己的data，确认访问形式是post
5.打开网页，获取Cookie，获取验证码图片，完善data并用它post访问教务处官网
6.获取登陆后自己姓名，确认是否登录成功
三.成绩查询
7.确认成绩查询页面，完善Headers
8.初步访问获取网页验证，得到referer
9.构造data，并且使用它爬取历年成绩
四.瞅瞅全是60分飘过，心好累
