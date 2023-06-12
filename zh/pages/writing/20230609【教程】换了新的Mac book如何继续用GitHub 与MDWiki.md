# 【教程】换了新的Mac book如何继续用GitHub 与MDWiki

**【写作课作业D.010】**

### 关键字：New MacBook、iCloud、GitHub、MDWiki、Keychain

之前用在Github搭建了个MDWiki存放自2018年11月以来所有写作练习的文稿。不知不觉，那台2015年买来，伴随我许久的MacBook Pro越来越经常出现电池问题，无法开机。所以，我征用了大宝的MacBook Air当我日常工作的电脑用。

把文章目录移到iCloud，很轻松就实现了在两台电脑上写作环境无缝切换。但是遗留了一个问题，大宝的MacBook Air上没有GitHub环境，要怎样才能继续更新GitHub 上搭建的MDWiki呢？

我一直以为会很麻烦，等研究了半天自己过去写的文章，一动手才知道，其实很简单。不得不感慨，实在是因为自己用得太少，太不熟悉工具，想太多了。

### 1. 在终端下找到iCloud的工作目录

在命令行终端下访问iCloud文件的路径是比较啰嗦的，用户目录下有一个 ``Library/Mobile\ Documents/com~apple~CloudDocs/``

为了方便起见，我为自己的工作目录建了一个符号链接：

```
ln -s /Users/my-user-name/Library/Mobile\ Documents/com~apple~CloudDocs/Work Work
```

### 2. 准备Git环境

参考***set-up-git***[^1]，***caching-your-github-password-in-git***[^2]和***git-handbook***[^3]，整个过程其实非常简单

1. [下载安装Git的最终版本](https://git-scm.com/downloads).

   我运行了一下git，结果发现报错

   ```
   $git
   xcrun: error: invalid active developer path (/Library/Developer/CommandLineTools), missing xcrun at: /Library/Developer/CommandLineTools/usr/bin/xcrun
   ```

   上网一查，原来是开发环境没装好，运行以下命令就好了

   ``` 
   xcode-select --install

2. [设置Git用户名](https://help.github.com/articles/setting-your-username-in-git).

   ```
   $git config --global user.name "Mona Lisa"
   ```

3. [设置Git提交用的邮件地址](https://help.github.com/articles/setting-your-commit-email-address-in-git).

   ```
   $git config --global user.email "email@example.com"
   ```

4. [在Git里缓存GitHub的密码](https://help.github.com/articles/caching-your-github-password-in-git/)

   ```
   $git credential-osxkeychain
   $git config --global credential.helper osxkeychain
   ```



### 3. 提交修改

因为iCloud把所有文件都同步了，包括原先旧电脑上的Github那些隐藏目录。因此，直接向Github提交修改就好：

```
git add zh/*
git commit -m "Daily writing 20230609"
git push
```

这是第一次Push，Git 会提示输入用户名和密码，千万记得，密码要输入你在GitHub网站专门为命令行设置的Token，具体可参考我之前写的[Github命令行即将弃用密码怎么办](https://hooman118.github.io/hoo-wiki/zh/#!pages/writing/20210625%E3%80%90%E5%8C%BA%E5%9D%97%E9%93%BE%E3%80%91Github%E5%91%BD%E4%BB%A4%E8%A1%8C%E5%8D%B3%E5%B0%86%E5%BC%83%E7%94%A8%E5%AF%86%E7%A0%81%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%88%E4%B9%9D%E4%B8%80%E4%BA%8C%EF%BC%89.md)，或GitHub的相关帮助文章[^4][^5][^6]。

----

[^1]: https://help.github.com/articles/set-up-git/
[^2]: https://help.github.com/articles/caching-your-github-password-in-git/
[^3]: https://guides.github.com/introduction/git-handbook/
[^4]: https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token
[^5]: https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git
[^6]: https://docs.github.com/en/get-started/getting-started-with-git/updating-credentials-from-the-macos-keychain#updating-your-credentials-via-keychain-access