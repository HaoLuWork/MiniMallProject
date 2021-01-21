# MiniMallProject
A MiniMall Project created by Lu and Lu
前端页面：
    一个主页，不要求登陆
        -页面顶部有一个导航栏
            注册和登陆页面，以及可能存在的其他导航位置
        -主体上方：排序功能，分别提供类型，价格，时间
        x页面主体是方格，内容是商品图片及简介，下方有悬浮的加购物车按钮
            对应的购物车功能还没写（前后端都没写）
            css还需要完善（只差前端）
        x底部：切换页面的状态栏
        -最底部关于信息

        点击商品图片，进入商品详情页面
            详情页有大图（若干张），和更详细的商品描述
            同时具有加入购物车的功能
        
    一个登陆和一个注册页面

    商品详情页面
        
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


后端逻辑:
    游客用户可以正常浏览主页，浏览商品详情，筛选，排序
    购物车和登录状态绑定，当游客需要使用购物车功能跳转至登陆页面

    用户信息:
        用户名，密码，邮箱，手机号
        地址：一个model，包含姓名，电话，国家，城市，街道，邮编
        购物车，商品收藏

        forms.py:
        add_form

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



大概流程：
    前端搭完
    x写管理员账户相关功能
    x测试上传信息
    写普通用户相关功能
    购物车和结算相关功能
    debugg



19号目标：
x登陆页面，注册页面，悬浮购物车页面，商品详情页面，的前端html
x和主页的css布局调整
-卡片高度
前端的自动分页功能
结账（单独的购物车）页面

购物车功能


20号小总结
    x目前遇到的小问题：主页卡片高度不一致，显示效果不美观

登陆页面的逻辑：
    主页上按照登陆状态显示账户下拉菜单的内容：
        未登录时：显示登陆按钮
        已经登陆后：显示订单，账户管理，和登出


20号目标
购物车后端功能实现出来
x购物车的model

x登陆功能的后端
x用户的model

-商品分类的model
x详情页的显示，以及主页和详情页的链接功能


x导航栏：
    x account按钮的位置，尽量挪到右边
    x 下拉菜单区分登陆状态：
        未登录显示:logind
        已登录显示用户名（或者加上头像）

x用户个人主页
    x个人中心：显示用户名，邮箱，头像等
    x修改信息：修改邮箱，修改头像
    x修改密码：修改当前账户密码
    -我的订单：显示全部订单
        包括：订单编号，总金额，联系电话，收货地址，订单状态
        还可以有：创建时间，支付时间，发货时间，收货时间
    -我的收藏：显示我的收藏

x购物车页面
    显示当前购物车中的物品，数量，及总价


20号小结
    x导航栏里需要一个明确的标志来提醒用户当前是否登陆
    x商品详情页面的图片宽度，应该是被css限制住了，会默认显示全屏，可能需要去bootstrap里改

21号目标：
    把购物车写完
    -buy now 功能

    主页的标签切换，的图像显示
    前端的小问题改正：
        购物车图标的下拉菜单
        登陆和注册按钮，根据登陆状态变化

    研究一下购物车的查询功能怎么才能实现

21号总结：
    购物车的大体构架完成了
    但是细节还没完全写完


