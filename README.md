# MiniMallProject
A MiniMall Project created by Lu and Lu
前端页面：
    一个主页，不要求登陆
        页面顶部有一个导航栏
        主体上方：排序功能，分别提供类型，价格，时间
        页面主体是方格，内容是商品图片及简介，下方有悬浮的加购物车按钮
        底部：切换页面的状态栏
        最底部关于信息

        点击商品图片，进入商品详情页面
            详情页有大图（若干张），和更详细的商品描述
            同时具有加入购物车的功能
        
    一个登陆和一个注册页面

    商品详情页面
        xiangqing/<int:id>
        对应商品的图片，介绍
        选择数量，加入购物车

    购物车结算页面
        for，把所有购物车里的东西显示出来
        计算每种商品的价格和数量，给出总价
        //适当提供几种支付方式
        点击结算，提示付款成功

    如果有时间：
        按品类筛选的下拉菜单
        右侧悬浮功能栏，回到顶部之类的功能



大概流程：
    前端搭完
    写管理员账户相关功能
    测试上传信息
    写普通用户相关功能
    debugg





后端逻辑：
    游客用户可以正常浏览主页，浏览商品详情，筛选，排序
    购物车和登录状态绑定，当游客需要使用购物车功能跳转至登陆页面

    用户信息：
        用户名，密码，邮箱，手机号
        地址：一个model，包含姓名，电话，国家，城市，街道，邮编
        购物车，商品收藏

        forms.py:
        add_form

        models.py
        shangpin class
            number(剩余库存)
            picture
            text

        address class
            姓名，电话，国家，城市，街道，邮编
        简单一点的地址方案：大平层
        Profile class
            姓名
            电话
            国家
            城市
            街道
            邮编
        复杂一点的地址方案，mtmf
        Profile class
            user = foreignKey(User, )
            text
            email
            phone
            address = ManyToManyField(address, )

        views.py
            还有很多
    



