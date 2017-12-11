# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class BaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = ('created_at',)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, verbose_name='姓名')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, name=instance.username)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        pass


class Dictionary(BaseModel):
    class Meta:
        verbose_name_plural = 'dictionaries'
        ordering = ('created_at',)

    name = models.CharField(max_length=10, verbose_name='名称')

    def __str__(self):
        return self.name


class Chapter(BaseModel):
    class Meta:
        ordering = ('created_at',)

    name = models.CharField(max_length=10, verbose_name='章节')

    dictionary = models.ForeignKey(Dictionary, related_name='chapters', on_delete=models.CASCADE, verbose_name='所属字典')

    def __str__(self):
        return "%s - %s" % (self.dictionary, self.name)


CHARACTERISTIC_CHOICES = (
    ('0', '名'),
    ('1', '代'),
    ('2', '副'),
    ('3', '形1'),
    ('4', '形2'),
    ('5', '动1'),
    ('6', '动2'),
    ('7', '动3'),
    ('8', '专'),
    ('9', '叹'),
    ('10', '连'),
    ('11', '连体'),
    ('12', '疑'),
    ('99', 'phrase'),  # phrase
)


class Word(BaseModel):
    class Meta:
        ordering = ('created_at',)

    kana = models.CharField(max_length=30, verbose_name='假名')
    kanji = models.CharField(max_length=30, blank=True, verbose_name='汉字')
    marking = models.CharField(max_length=100, blank=True, verbose_name='假名标注')
    characteristic = models.CharField(
        max_length=2,
        choices=CHARACTERISTIC_CHOICES,
        verbose_name='词性'
    )
    meaning = models.TextField(verbose_name='意思')
    # tone 音调
    # characteristic 词性

    chapter = models.ForeignKey(Chapter, related_name='words', on_delete=models.CASCADE, verbose_name='所属章节')

    def __str__(self):
        return self.kanji


# class Plan(BaseModel):
#     """
#     记忆计划
#     - 词组记忆
#     - 复习
#     - 测试
#     """

# class NormalPlan(BaseModel):
#     total = models.IntegerField(verbose_name='选择个数')
#     finished = models.IntegerField(verbose_name='完成个数')

class SelectedWord(BaseModel):
    """
    对词记忆
    - ranks 表达记忆程度，默认为 0，
    - rate  表达正确率，默认 N/A，每次选择都会计算

    次数统计包括每次复习中的次数。
    """

    class Meta:
        ordering = ('created_at',)

    ranks = models.IntegerField(default=0, verbose_name='熟悉度')
    correct_rate = models.IntegerField(null=True, verbose_name='正确率')
    correct_times = models.IntegerField(default=0, verbose_name='正确次数')
    wrong_times = models.IntegerField(default=0, verbose_name='错误次数')
    review_times = models.IntegerField(default=0, verbose_name='复习次数')

    last_review_times_needed = models.IntegerField(default=0, verbose_name='最后所需 Review 次数')
    last_checked_at = models.DateTimeField(null=True, verbose_name='最后记忆时间')
    next_check_point = models.DateTimeField(null=True, verbose_name='下次检查点')
    last_wrong_at = models.DateTimeField(null=True, verbose_name='最后错误时间')
    mem_level = models.IntegerField(default=0, verbose_name='记忆阶段')

    origin = models.OneToOneField(Word, on_delete=models.CASCADE, verbose_name='原词')
    owner = models.ForeignKey(Profile, related_name='selected_words', on_delete=models.CASCADE, verbose_name='所属')
