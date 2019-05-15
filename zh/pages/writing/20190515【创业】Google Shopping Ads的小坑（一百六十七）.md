#【创业】Google Shopping Ads的小坑

昨天发现，在Website 上增加Product 的标识，对于Google Shopping Ads 来说，其实并不是必要的。我还和小伙伴用https://search.google.com/structured-data/testing-tool 测试了半天我们的网站呢，这功夫有些浪费了，或许将来更新时才用得到这个吧。

**最关键的一步是在Google Merchant Center里增加Products。**

**增加的第一步，必须是增加Feeds**，那么我选择的是使用Google Sheet，Google Merchant Center为我自动生成了一个模版。紧接着，我就犯了几个错误：

1. 在Google product category 这一栏，不需要直接填数字（我还专门Google了半天，找到我们家产品的合适类别编号，不需要），先安装好Google Merchant Center Addon，这一栏会变成下拉框，直接选择。

2. 软件订阅类的产品，Google 只支持以年为期的订阅。

3. 必须要有正确的GTIN（UPC，EAN，JAN，ISBN-13）都行，好在这个编号我们早就申请（买）过。

4. 必须要把税设置好（Google 有两篇帮助讲这个https://support.google.com/merchants/answer/160162  https://support.google.com/merchants/answer/7052209）。

5. 必须把运费设置好。

   

然后，耐心的等待Google 批准。之前没想到还有这个过程。后来在Products->List里发现红色的Disapproved 的信号灯，上网一搜，才知道有很多人遇到这问题。而且还只能修改Feeds，Upload，等待看红灯是否变绿灯。最夸张的一个人上传500多商品，总有几十个不通过，怎么对比也不知道为什么，Google 也不能告诉他为什么。

正琢磨着呢，再刷新了一下我的List，发现Surface across Google 已经变成了绿灯（Active）状态，Shopping Ads变成了Pending 。原来这个时延长，估计之前Disapproved 是我还没输入正确的那些产品信息吧。然后，这个Pending 一直等到了今天，还是Pending，不知道什么时候才能Active。只能继续等待...

官方关于**Pending**的说法如下：

> An item that's pending won't show in ads because it's being processed by Google. Your item might be pending for any of these reasons:
>
> * **You're new to Merchant Center**. When you've uploaded product data to your account for the first time, our specialists review your account to ensure it meets our [requirements](https://support.google.com/merchants/answer/188494) and [Shopping ads policies](https://support.google.com/merchants/answer/188484). This processing can take up to 3 business days  for Shopping ads and can take up to a few weeks for other programs. 
> * **Your item has a pending image crawl**. You don't need to do anything right now. Your image will automatically appear once we've fetched it. If we encounter any problems, we'll let you know. This processing can take up to 3 business days. 
> * **You submitted products for a beta target country**. If you submit a feed to a beta country, it may take significantly longer for your items to be reviewed. [Learn more about beta target countries](https://support.google.com/merchants/answer/7101265)

3个工作日，或者a few weeks...且等一切调通之后，再优化产品图片和说明信息吧。