from django.db import models

# Create your models here.

class DB_tucao(models.Model):
    """
    类变量会被orm当作是表内的字段
    按照此格式，调用models下的各种方法定义字段
    括号内就是约束条件。
    CharField 是字符串。
    DateTimeField是时间。
    max_length是最大允许长度，null=True ，是允许为Null,
    auto_now ,是自动填入时间无需我们手动填入了
    """
    user = models.CharField(max_length=30,null=True) # 吐槽人姓名
    text = models.CharField(max_length=1000,null=True) # 吐槽内容
    ctime = models.DateTimeField(auto_now=True) # 创建时间

    def __str__(self):
        """
        在admin后台 想要操作数据库，里面的具体记录列表 并不会像mysql的客户端一样，
        显示所有内容，是需要我们自定义的去设计要显示什么，
        理解起来就像 我们要在这个__str__函数内设计一个view视图。
        return self.text 就是创建一个视图，让我们之后在后台管理平台，
        这个表的内容时，先显示text 也就是吐槽内容，然后我们点进去就可以看到全部内容了
        :return:
        """
        return self.text+str(self.ctime)


class DB_home_href(models.Model):
    """
    存储连接入口
    """

    name = models.CharField(max_length=30,null=True) # 超链接名字
    href = models.CharField(max_length=2000,null=True) # 超链接内容

    def __str__(self):
        return self.name

class DB_project(models.Model):
    name = models.CharField(max_length=100,null=True) # 项目名称
    remark = models.CharField(max_length=1000,null=True) # 项目备注
    user = models.CharField(max_length=15,null=True) # 项目创建者
    other_user = models.CharField(max_length=200,null=True)# 项目其他创建者

    def __str__(self):
        return self.name