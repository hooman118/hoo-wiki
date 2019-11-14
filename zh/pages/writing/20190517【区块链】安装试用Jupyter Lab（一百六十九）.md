#【区块链】安装试用Jupyter Lab（一百六十九）

这篇本来和区块链也没啥关系，但是和[李笑来](https://github.com/xiaolai)有点关系。就暂且放这里吧。

想要安装[Juypter Lab](https://github.com/jupyterlab/jupyterlab)，起因是看到了这本《[自学是门手艺](https://github.com/selfteaching/the-craft-of-selfteaching)》。本来只是在GitHub上浏览一下，但是发现他的Markdwon版本许多图片显示不对，既然书的第一章就提到让安装Jupyter Lab以便有更好的阅读体验，那就装一下吧。正好了解一下啥是[Juypter Lab](https://github.com/jupyterlab/jupyterlab)。

话说，简单了解后发现[Juypter Lab](https://github.com/jupyterlab/jupyterlab)原来是挺多程序员和数据分析人员热爱的笔记本工具。本来呢，在李笑来的书里，专门有一张附录[Jupyterlab 的安装与配置](https://github.com/selfteaching/the-craft-of-selfteaching/blob/master/T-appendix.jupyter-installation-and-setup.ipynb)，但是我并不喜欢安装那些巨大的发行包，比如这附录里第一步就要求按装的[Anaconda](https://www.anaconda.com/)。我的Mac 上自带Python，而且我还有自己更偏爱的Home Brew。结果当然，这点偏爱害我多折腾了半天，虽然并非不值得。以下是我折腾的记录

###安装Jupyter Lab（参考[官方安装文档](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html)使用PIP的部分）

文档说，如果使用PIP，执行下面这条命令即可

```bash
pip install jupyterlab
```

其实，对我来说，可没这么简单。Juypter Lab 需要的是Python3，而我Mac上自带的是Python 2.7，怎么知道的？如下，/usr/bin/python就是Mac 自带的了。

```$ python --version
$ python --version
Python 2.7.10
$ which python
/usr/bin/python
```

####用How brew 安装Phtyon3

再一次，不能直接运行`brew install python3`，会有提示权限错误导致安装失败。都是因为Mac最近的更新修改了/usr/local/ 目录的权限，github 上有提到这个[issue #19286](https://github.com/Homebrew/homebrew-core/issues/19286)。先执行以下命令

```bash
sudo mkdir /usr/local/Frameworks
sudo chown $(whoami):admin /usr/local/Frameworks
sudo chown -R $(whoami) $(brew --prefix)/*
```

然后再安装

```bash
brew install python3
```

####用Pip3 安装Jupyter Lab

```bash
pip3 install --user jupyterlab
```

###运行Jupyter Lab

因为上面是以user 模式安装的，记得要把先把Python 的路径加到Path里，

```bash
export PATH="$PATH:/usr/local/mysql/bin:/Users/Hooman/Library/Python/3.7/bin"
```

然后在ipynb所在的目录，执行 `jupyter lab`，会自动打开一个浏览器。接下来，就可以直接看书了。我还照着[Jupyterlab 的安装与配置](https://github.com/selfteaching/the-craft-of-selfteaching/blob/master/T-appendix.jupyter-installation-and-setup.ipynb)里关于*Jupyter Lab Theme*的章节调整了显示主题（直接使用支持 [Stylus](https://github.com/openstyles/stylus) 这类终端 CSS 定制插件的浏览器）。后来，又安装了两个小插件（并不重要）。

###Jupyter Lab超级小白的困惑

紧接着，我遇到了一个只有超级小白才会遇到的困惑。Jupyter Lab的笔记里，有一个基本单位叫做Cell。可以是Markdown，也可以是Code。在Cell上双击或按`Enter`就进入编辑模式，按`Esc`就退出编辑模式进入所谓命令模式。但是，我发现，一个Markdown的Cell，当我双击之后，他就从下面这样

------

##### 这是主题

这是正文，这是**加粗**，还有*斜体*

-----

变成了下面这样

----

```markdown
#####这是主题
这是正文，这是**加粗**，还有*斜体*
```

----

而且，再怎么按`Esc`键，他就永远是这样了！Google 百度，中文/英文搜索了许久都没有找到答案。直到我放弃寻找这个问题。开始玩Jupyter Lab时，才发现窍门！窍门就是

***按`Ctrl`+`Enter` 或者`Shift`+`Enter`***

原因，我也瞬间明白了。上面两个快捷键是执行Cell 的代码，直接选择菜单上的执行按钮▶️是一样的效果。Markdown的执行，不就是渲染之后显示效果吗？难怪没人提及这事，因为实在太简单了！

这时，我发现了自己一个重要的弊病，被Google/Baidu等网络搜索工具惯的：

> **遇到问题，不是去先尝试自己摸索，而是先搜索网络，看看有没有现成的解决方案**

不忘初心！不忘初心啊！回想小时候玩日文游戏，初学DOS，在没有帮助，书籍缺失的情况下，不就是一个个选项尝试，一个个命令把玩学会的吗？居然把这种能力给忘记了，引以为戒啊！