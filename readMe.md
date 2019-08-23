
这个python程序需要配置运行可以搜集某个微博用户的原创微博，配置执行方法如下：

1. 安装python

在windows下点击安装[Miniconda2-latest-Windows-x86_64.exe](https://repo.anaconda.com/miniconda/Miniconda2-latest-Windows-x86_64.exe)，注意添加`python.exe`到环境变量里

2. 安装程序的依赖项（需要联网）

打开命令行(WIN+R 输入cmd 回车)，在命令行执行如下命令

```cmd
pip install beautifulsoup
pip install lxml
conda install numpy pandas

```

3. 配置程序文件
   
- 打开谷歌浏览器，访问`weibo.cn`
- 使用自己的微博账户登录
- 按`F12`，打开浏览器的`network`资源监视器，按`F5`刷新

    点击每个资源项目，找到`cookie`，将其复制到代码对应的位置  



- 找到用户的`ID`，也就是用户主页的url后面的那部分，将其复制到代码对应的位置



4. 运行程序
  
可以使用如下方法，打开命令行，执行`CD`命令到代码所在的文件夹，运行代码，

```cmd
python getWeibosOfUser.py
```

5. 程序中断处理办法
   
可以设置 start的值，制定重新开始搜集的页码
