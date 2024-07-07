from django.db import models
from user_module.models import UserModels

# Create your models here.

class CatgoryModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام دسته')
    parent = models.ForeignKey("CatgoryModel", blank=True, null=True, on_delete=models.CASCADE, verbose_name='زیر دسته')
    slug = models.SlugField(allow_unicode=True, verbose_name='عنوان در مرورگر')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'دسته'
        verbose_name_plural = 'دسته بندی ها'

class CatgoryImageModel(models.Model):
    img = models.ImageField(upload_to='product/', verbose_name='عکس')
    catgory = models.ForeignKey(CatgoryModel, on_delete=models.CASCADE, verbose_name='دسته', null=True)

    class Meta:
        verbose_name = 'عکس دسته'
        verbose_name_plural = 'عکس دسته بندی'

class PublisherModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام')
    slug = models.SlugField(allow_unicode=True, verbose_name='عنوان در مرورگر')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ناشر'
        verbose_name_plural = 'انتشارات'

class ProductModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام')
    field = models.CharField(max_length=100, verbose_name='رشته', null=True, blank=True)
    grade = models.CharField(max_length=100, verbose_name='پایه', null=True, blank=True)
    lesson = models.CharField(max_length=100, verbose_name='درس', null=True, blank=True)
    publish_date = models.IntegerField(verbose_name='سال انتشار', null=True, blank=True)
    cut = models.CharField(max_length=100, verbose_name='قطع', null=True, blank=True)
    cover = models.CharField(max_length=100, verbose_name='جلد', null=True, blank=True)
    count = models.IntegerField(null=True, verbose_name='نعداد')
    rating  = models.IntegerField(verbose_name='نظرات', null=True, editable=False)
    page = models.IntegerField(verbose_name='صفحه')
    price = models.IntegerField(verbose_name='قیمت')
    publisher = models.ForeignKey(PublisherModel, on_delete=models.CASCADE, verbose_name='فروشنده')
    detail = models.TextField(verbose_name='توضیحات')
    catgory = models.ManyToManyField(CatgoryModel, verbose_name='دسته بندی')
    is_active = models.BooleanField(verbose_name='فعال/غیرفعال')
    slug = models.SlugField(allow_unicode=True, verbose_name='عنوان در مرورگر')
    is_special = models.BooleanField(default=False, verbose_name='تخفیف ویژه فعال / غیر فعال')
    discount = models.IntegerField(null=True, verbose_name='تخفیف', blank=True)
    special_discount_date = models.DateField(null=True, blank=True, verbose_name='زمان تخفیف')

    def __str__(self):
        self.catgory.all()
        return self.name

    def disCount(self):
        try:
            return int(self.price - ((self.price * self.discount) / 100))
        except:
            return self.price

    def ratingAvrg(self):
        try:
            rating = 0
            count = 0
            for item in self.commentmodel_set.all():
                rating += item.rating
                count+=1
            avrg = rating / count
            return round(avrg, ndigits=1)
        except:
            return 0

    def disCoun_price(self):
        try:
            return int((self.price * self.discount) / 100)
        except:
            return 0

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

class ProductImageModel(models.Model):
    img = models.ImageField(upload_to='product/', verbose_name='عکس')
    book = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name='کتاب', null=True)

    def __str__(self):
        return f'{self.book.name} : {self.id}'

    class Meta:
        verbose_name = 'عکس محصول'
        verbose_name_plural = 'عکس محصولات'

class CommentModel(models.Model):
    text = models.TextField(verbose_name='متن پیام')
    parent = models.ForeignKey('CommentModel', on_delete=models.CASCADE, verbose_name='پاسخ', null=True, blank=True)
    book = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name='کتاب', null=True)
    user = models.ForeignKey(UserModels, on_delete=models.CASCADE, verbose_name='کاربر', null=True)
    create_date = models.DateField(auto_now_add=True, null=True)
    rating = models.IntegerField(verbose_name='امتیاز')

    def ratingRange(self):
        return range(self.rating)

    def disRate(self):
        return range(5 - self.rating)

    def __str__(self):
        return f'{self.book.name} : {self.user.username}'

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

class ProductSliderModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام')
    img = models.ImageField(upload_to='slider/', verbose_name='اسلایدر')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'اسلاید'
        verbose_name_plural = 'اسلاید ها'


class FavoriteProduct(models.Model):
    user = models.ForeignKey(UserModels, on_delete=models.CASCADE, verbose_name='کاربر')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name='محصول')

    def __str__(self):
        return f'{self.user.username} : {self.product.name}'

    class Meta:
        verbose_name = 'محصول مورد علاقه'
        verbose_name_plural = 'محصولات مورد علاقه'