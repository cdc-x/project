from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

# 用户信息表
class UserInfo(AbstractUser):
    phone = models.BigIntegerField(verbose_name="手机号", null=True)
    # 头像
    # 给 avatar 字段传文件对象，该文件会存储到avatar文件夹下，然后字段只保存文件路径
    # 不传文件默认使用avatar/default.png
    avatar = models.FileField(upload_to="avatar", default="avatar/default.png", verbose_name="头像")
    create_time = models.DateField(auto_now_add=True)

    # 一对一个人站点表
    blog = models.OneToOneField(to="Blog", null=True, on_delete=models.CASCADE)


# 个人站点表
class Blog(models.Model):
    site_name = models.CharField(verbose_name="站点名称", max_length=32)
    site_title = models.CharField(verbose_name="站点标题", max_length=32)
    # 简单模拟样式内部原理，该字段存放css/js文件路径
    site_theme = models.CharField(verbose_name="站点样式", max_length=64)


# 文章分类表
class Category(models.Model):
    name = models.CharField(verbose_name="文章分类", max_length=32)

    # 一对多个人站点表
    blog = models.ForeignKey(to="Blog", null=True, on_delete=models.CASCADE)


# 文章标签表
class Tag(models.Model):
    name = models.CharField(verbose_name="文章标签", max_length=32)

    # 一对多个人站点表
    blog = models.ForeignKey(to="Blog", null=True, on_delete=models.CASCADE)


# 文章表
class Article(models.Model):
    title = models.CharField(verbose_name="文章标题", max_length=64)
    desc = models.CharField(verbose_name="文章简介", max_length=255)
    # 文章内容比较多，一般用 TextField 字段
    content = models.TextField(verbose_name="文章内容")

    # 数据库字段优化设计
    up_num = models.BigIntegerField(verbose_name="点赞数", default=0)
    down_num = models.BigIntegerField(verbose_name="点踩数", default=0)
    comment_num = models.BigIntegerField(verbose_name="评论数", default=0)

    # 一对多文章站点表
    blog = models.ForeignKey(to="Blog", null=True, on_delete=models.CASCADE)
    # 一对多文章分类表
    category = models.ForeignKey(to="Category", null=True, on_delete=models.CASCADE)
    # 多对多文章标签表
    tags = models.ManyToManyField(to="Tag", through='Article2Tag', through_fields=("article", "tag"))


class Article2Tag(models.Model):
    article = models.ForeignKey(to="Article", on_delete=models.CASCADE)
    tag = models.ForeignKey(to="Tag", on_delete=models.CASCADE)


# 点赞点踩表
class UpDown(models.Model):
    user = models.ForeignKey(to="UserInfo", on_delete=models.CASCADE)
    article = models.ForeignKey(to="Article", on_delete=models.CASCADE)
    is_up = models.BooleanField()


# 评论表
class Comment(models.Model):
    user = models.ForeignKey(to="UserInfo", on_delete=models.CASCADE)
    article = models.ForeignKey(to="Article", on_delete=models.CASCADE)
    content = models.CharField(verbose_name="评论内容", max_length=255)
    comment_time = models.DateTimeField(verbose_name="评论时间", auto_now_add=True)
    # 自关联
    parent = models.ForeignKey(to='self', null=True, on_delete=models.CASCADE)
