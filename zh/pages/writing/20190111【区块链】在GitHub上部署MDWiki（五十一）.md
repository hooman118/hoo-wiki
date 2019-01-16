#【区块链】在GitHub上部署MDWiki（五十一）

> 严格来说，MDWiki和区块链没关系，GitHub当然也没有，其实IPFS也可以和区块链没关系。只是暂时都归入这个类别吧，毕竟是因为区块链才开始深入了解这些东西。

为了在IPFS上发表文章，我找到了MDWiki这个接近目标的开源方案。然后发现，其实只要完成在GitHub上部署MDWiki，就已经可以公开发表文章了。

MDWiki的网站上有一份[不完全指导](http://dynalon.github.io/mdwiki/#!tutorials/github.md)，照着做了才知道，自己对于GitHub有多么的无知！以下就是

##仍然可能不完整的具体步骤

### 第一步：创建GitHub账号

我以前就有账号了。没有的话，去<http://www.github.com/signup> 注册也很简单。

### 第二步：Fork MDWiki-Seed 这个项目

https://github.com/exalted/mdwiki-seed 从这个链接进去，点击"fork"，就创建了一个自己的MDWiki-Seed项目。自己这个分支项目的链接就变成了https://github.com/hooman118/hoo-wiki/。当然，`hooman118`是我的用户名，你的肯定和我的不一样。`hoo-wiki`是我修改后的项目名，你可以在项目Setting里把它修改成任何你中意的名字，比如`your-project-wiki`。

修改好名字之后，注意检查一下`setting` 里**GitHub Pages**这一部分，确保source 是 `gh-pages branch`。然后，记下你的网站地址，一般来说是这样的格式： `http://<username>.github.io/<your-project-wiki>/`

### 第三步：参考ReadMe里的说明进行必要地修改

**这一步很重要，没改之前，网站是显示不出来的**，我放到Mac Book本地修改，所以下面的步骤涉及到一些Git 的基本命令与操作，参考了***set-up-git***[^1]，***caching-your-github-password-in-git***[^2]和***git-handbook***[^3]。

#### 3.0 在本地准备Git 环境

1. [下载安装Git的最终版本](https://git-scm.com/downloads).

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

#### 3.1 把网站整个拿到Mac Book本地准备修改

我这里是参考GitHub Flow 为我(`hooman118`)的项目`hoo-wiki`新建了一个Branch `the-one`，你执行以下命令时，需要把用户名、项目名和Branch名都换成你的。如果不新建分支，操作会更简单一点。

```
# download a repository on GitHub.com to our machine
git clone https://github.com/hooman118/hoo-wiki/

# change into the `hoo-wiki` directory
cd hoo-wiki

# create a new branch to store any new changes
git branch the-one

# switch to that branch (line of development)
git checkout the-one
```

#### 3.2 修改ll_CC目录和index.html

详细参考项目的README.md，一般这个地址就能访问到`https://github.com/<username>/<your-project-wiki>/`

1. 根据你想要使用的语言，复制ll_CC这个目录。比如我想用中文写文章，就复制ll_CC 到zh，或者en，或者明确的指名简体中文zh_CN，英国英语en_GB等等任何你计划使用的语言符号。完整的ll_CC 可以参考MSDN[^4]。记住保留ll_CC这个目录不要动，这样将来需要时还能参考。

   ```
   $cp -r ll_CC zh
   ```

2. 用文本编辑器打开项目根目录下的`index.html`文件（**注意**：不是ll_CC 目录下的`index.html`，也不是zh或任何你复制的语言目录下的`index.html`）

   ```
   $vi index.html
   ```

   找到这段话

   ```
   <!--
       Override `ll_CC` below with your default language and country code
   -->
   <meta http-equiv="refresh" content="0; url=ll_CC/" />
   ```

   把其中的`ll_CC` 修改为国家语言代码，比如`zh`，注意结尾的`/`一定要保留。改完后像这样

   ```
   <!--
       Override `ll_CC` below with your default language and country code
   -->
   <meta http-equiv="refresh" content="0; url=zh/" />
   ```

   保存，退出。

#### 3.3 把修改提交到Git Hub

1. 提交刚刚所做的修改

   ```
   # stage the changed files
   git add index.html zh_CN
   
   # take a snapshot of the staging area (anything that's been added)
   git commit -m "changed index.html and added zh"
   
   # push changes to github
   git push --set-upstream origin the-one
   ```

2. 合并修改到主分支

   ```
   $git checkout -b the-one origin/the-one
   $git merge gh-pages
   $git checkout gh-pages
   $git merge --no-ff the-one
   ```

3. 删除the-one分支（为了洁癖的需要）

   ```
   $git branch --delete the-one
   ```

#### 3.4 没有了

现在你的http://<username>.github.io/<your-project-wiki>/ 应该就可以访问了。

至于怎么用MD-wiki，我还没仔细研究。README.md里说得已经足够详细了。

我的理解是，只需要一个额外的Markdown编辑器（比如Typora）来编辑文章，然后再把修改提交到GitHub就可以了（比如用命令行的git）！



下一步再研究MDwiki具体的使用，以及如何改造来适应IPFS！

----

[^1]: https://help.github.com/articles/set-up-git/
[^2]: https://help.github.com/articles/caching-your-github-password-in-git/
[^3]: https://guides.github.com/introduction/git-handbook/ 
[^4]: <https://docs.microsoft.com/en-us/previous-versions/commerce-server/ee825488(v=cs.20)>