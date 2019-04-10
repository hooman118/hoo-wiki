#【创业】用MailGun和GMail实现自己域名的邮件（一百二十六）

其实目标很简单，就是因为要测试一个新业务注册了一个域名，做了一个简单的销售网页测试效果。需要用类似info@mydomain.com 这样的地址接收和发送邮件。安装一套box 邮件系统固然可行，但是这样太麻烦。在Godaddy买他们的邮件服务，又贵又不好用。Google App的邮件系统不错，但也要几美金一个账号，在这个业务的测试阶段，非常不划算。

上网搜索了一下，找到一个解决方案。Kevin Monahan写了一篇详细的指导[Use your custom email domain with Gmail and GoDaddy for FREE](<https://medium.com/@kevinmonahan/use-your-custom-email-domain-with-gmail-and-godaddy-for-free-84ea8c5ea4ed>)。照着操作，简单搞定！

简单来说也就6步：

1. 先在Maigun注册一个免费账号。
2. 在Maigun创建一个域名（千万不要用子域名，比如我的域名是thundersurf.net，maigun推荐用**mg.thundersurf.net**，还说了一堆理由。不要听他的，只管用**thundersurf.net**。这个非常重要，我就是在这里不听Kevin的劝，走了弯路，最后Gmail里发送邮件时报错`550 5.7.1 Relaying denied！`）
3. 在Godaddy设置好DNS的TXT，MX，CNAME记录
4. 在Maigun设置好Route（实现邮件地址转发到Gmail）
5. 在Maigun设置好SMTP credential
6. 在Gmail里添加发送邮件的账号，smtp用上面在Mailgun里设置好的认证信息

然后就好了！想添加多少邮件地址就添加多少Route即可。**全免费**！

