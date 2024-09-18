
<!-- PROJECT LOGO -->
<br />
<div align="center" style="background-color: white;">
  <a>
    <img src="https://s32.picofile.com/file/8477408350/logo_stand.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Stadino</h3>

  <p align="center">
    سایت فروشگاه کتاب
    <br />
    <a href="https://stadino.pythonanywhere.com/">دیدن سایت</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->


<!-- ABOUT THE PROJECT -->
## About The Project

![Screenshot 2024-07-04 210023](https://github.com/MohsenSangSefidi/Stadino/assets/160093991/d7f7492c-44bd-4d2a-a146-db96632a7032)

این پروژه یک سایت فروشگاهی مخصوص فروش کتاب است. این یک پروژه تمرینی است و قسمت Back-End این سایت با فریمورک Django طراحی شده است و در قسمت Front-End آن از یک قالب آماده استفاده شده است. قسمت های مختلف سایت و قابلیت های آن به شرح زیر است :

  `صفحه سبد خرید و انتخاب آدرس ارسال محصول`
  `صفحه سرچ محصول و اعمال فیلتر قیمت و دسته بندی روی متن جستجو شده`
  `صفحه پنل کاربری`
  `صفحه ورود و ثبت نام و قابلیت ارسال ایمیل برای فعال سازی حساب کاربری`
  `صفحه اصلی - صفحه محصولات - و صفحه جزئیات محصول`



### Built With

* Django
* Django-Rest-Framework
* Python

<!-- GETTING STARTED -->
## Product Rest-Api

در این سایت یک Api برای دریافت و ثبت محصول ایجاد شده است که به صورت زیر می توانید در پایتون از آن استفاده کنید :

### Get

برای دریافت لیست محصولات سایت میتوانید از آدرس "https://stadino.pythonanywhere.com/product/product-api/"

با توکن "Stadino ddfd2b32b7e26df767b0d2fd51672d38b2d0f367" آن را دریافت کنید.


   ```sh
   import requests

   endpoint = 'https://mohsensangsefidi.ir/product/product-api/'

   headers = {
     'Authorization': 'Stadino ddfd2b32b7e26df767b0d2fd51672d38b2d0f367'
   }

   response = requests.get(endpoint, headers=headers)
   ```

### Post

برای ثبت محصول در سایت میتوانید از آدرس "https://stadino.pythonanywhere.com/product/product-api/"

با توکن "Stadino ddfd2b32b7e26df767b0d2fd51672d38b2d0f367" آن را ثبت کنید.


   ```sh
   import requests

   endpoint = 'https://mohsensangsefidi.ir/product/product-api/'

   headers = {
     'Authorization': 'Stadino ddfd2b32b7e26df767b0d2fd51672d38b2d0f367'
  }

  response = requests.post(endpoint, headers=headers, json={
     'name': 'محصول ۱',
     'page': 10,
     'price': 250000,
     'detail': 'توضیحات محصول ۱',
     'is_active': True,
     'publisher': 1, # این قسمت برای ثبت ناشر کتاب است که یک جدول مشخص دارد و آیدی ناشر در این قسمت قرار میگیرد
     'slug':'محصول-۱'
   })
   ```

   
  به دلیل زیاد بودن تعداد فیلد های محصول در دیتابیس فقط مقدار مشخص از آنها رو در اینجا قرار دادم و بعد از ثبت محصول میتوانید آن را در سایت جستو و جو کنید.

<!-- CONTACT -->
## Contact

Mohsen Sang Sefidi - [@Linkedin](www.linkedin.com/in/mohsen-sang-sefidi-67624a217) - [@Telegram](https://t.me/mohsensangsefidi) - sangsefidimohsen84@gmail.com
