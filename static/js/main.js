$(function () {

    ///نمایش زیر منو
    $(".showSubMenu").click(function () {
        $(this).nextAll("ul").toggleClass("show");
        $(this).toggleClass('open');
    })

    ///نمایش مگامنو آپدیدت جدید
    $(".main-menu-head").hover(function () {
        $(this).children().find(".main-menu-sub").first().addClass('main-menu-sub-active');
        $(this).children().addClass('active');
    })
    $(".main-menu-head").mouseleave(function () {
        $(this).children().find(".main-menu-sub").first().removeClass('main-menu-sub-active');
        $(this).children().removeClass('active');
    })
    $(".main-menu li").mouseover(function () {

        $(".main-menu li").removeClass("main-menu-sub-active-li");
        $(this).addClass("main-menu-sub-active-li");
        $(".main-menu-sub").removeClass('main-menu-sub-active');
        $(this).children('ul').removeClass('main-menu-sub-active');
        $(this).children('ul').addClass('main-menu-sub-active');
    });
    $(".main-menu-sub-active").mouseleave(function () {
        $(".main-menu-sub-active").removeClass("main-menu-sub-active");
    })

    // /شمارنده محصول برای اضافه کردن به سبد خرید
    // $("input.counter").TouchSpin({
    //     min: 1,
    //     max: '1000000000000000',
    //     buttondown_class: "btn-counter waves-effect waves-light remove-button",
    //     buttonup_class: "btn-counter waves-effect waves-light add-button",
    // });

    ///انتخاب گر رنگ
    $(".category-sort .form-checks .form-check").click(function () {
        $(".category-sort .form-checks .form-check").removeClass("active");
        $(this).addClass('active');
        $(".category-sort .form-checks .form-check").children("input[type=radio]").attr('checked', false);
        $(this).children("input[type=radio]").attr('checked', true);
    })


    ///انتخاب زمان ارسال
    $(".send-item").click(function () {
        $(".send-item").removeClass("active");
        $(this).addClass('active');
    })

    ///انتخاب روش پستی
    $(".shipping-item").click(function () {
        $(".shipping-item").removeClass("active");
        $(this).addClass('active');
    })

    ///انتخاب روش پرداخت
    $(".bank-item").click(function () {
        $(".bank-item").removeClass("active");
        $(this).addClass('active');
    })


    jQuery('[data-bs-toggle="tooltip"]').tooltip();
    jQuery('[data-bs-toggle="modal"][title]').tooltip();

});

/**
 * open search form flaot
 */

$(document).ready(function () {

    /**
     * open
     */
    $(".header-search").click(function () {
        $(".search-float").toggleClass("open");
    });

    /**
     * close
     */

    $(".search-float-close").click(function () {
        $(".search-float").toggleClass("open");
    });


});

/**
 * open basket float with click
 */

$(document).ready(function () {

    /**
     * open
     */
    $(".header-cart-icon-toggle").click(function () {
        $(".min-cart").toggleClass("open");
    });

});


/**
 * config floating contact
 //  */
$('#btncollapzion').Collapzion({
    _child_attribute: [{
        'label': 'پشتیبانی تلفنی',
        'url': 'tel:0930555555555',
        'icon': 'bi bi-telephone'
    },
        {
            'label': 'پشتیبانی تلگرام',
            'url': 'https://tlgrm.me',
            'icon': 'bi bi-telegram'
        },
        {
            'label': 'پشتیبانی واتس آپ',
            'url': 'https://wa.me/444444444',
            'icon': 'bi-whatsapp'
        },

    ],
});


// When the user clicks on the button, scroll to the top of the document
// function topFunction() {
//     document.body.scrollTop = 0; // For Safari
//     document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
// }

/*
*
* mega menu floating
*
* */
$(function () {
    var lastScrollTop = 0, delta = 5;
    $(window).scroll(function () {
        var nowScrollTop = $(this).scrollTop();
        if (Math.abs(lastScrollTop - nowScrollTop) >= delta) {
            if (nowScrollTop > lastScrollTop) {
                // ACTION ON
                // SCROLLING DOWN
                $(".top-menu-parent").addClass("mx-0");
            } else {
                // ACTION ON
                // SCROLLING UP
                $(".top-menu-parent").removeClass("mx-0");
            }
            lastScrollTop = nowScrollTop;
        }
    });
});


/**
 * delivery item form check
 */

$(document).ready(function () {

    $(".delivery-item").click(function () {
        $(this).find('input').prop("checked", true);
    });

    $(".delivary-payment-bank-item").click(function () {
        $(".delivary-payment-bank-item").removeClass("active");
        $(this).addClass("active");
    });
});


/*
* فرم چند مرحله ای ورود / ثبت نام
*/

$(document).ready(function () {
    ///disable fild password in load form
    $(".step-passwd").hide();
    ///disable button submit in step one
    $(".step-two").hide();

    ///show filed password in step two form
    $(".step-one").click(function () {

        ///check empty fild username
        if ($(".step-username #username").val() != "") {
            ///hide username filed
            $(".step-username").hide();
            ///show password filed
            $(".step-passwd").show();
            ///hide button step one
            $(this).hide();
            ///show button submit
            $(".step-two").show();
        } else {
            $(".step-username #username").addClass("border-danger border-2");
        }


        ///check empty fild password

        $(".btnForm").click(function () {
            if ($(".step-passwd #passwd").val() != "") {
                $("#form-auth").submit();
            } else {
                $(".step-passwd #passwd").addClass("border-danger border-2");
            }
        })
    })
})

function addProduct(productCount){
    let count = document.getElementById('product-Count')
    let int = parseInt(count.value)
    int += 1
    if (int > productCount) {
        count.value = productCount
    }else {
        count.value = int
    }
}

function minesProduct(){
    let count = document.getElementById('product-Count')
    let int = parseInt(count.value)
    int -= 1
    if (int < 1) {
        count.value = 1
    }else {
        count.value = int
    }

}

function add_to_order(id) {
    let count = $('#product-Count').val()
    $.get('/order/add-to-order/', {
        'productId': id,
        'count': count
    }).then(res => {
        if (res.status == "success") {
            Swal.fire({
                position: "center",
                icon: "success",
                title: "محصول با موفقیت به اضافه شد",
                showConfirmButton: false,
                timer: 1500
            });
            setInterval(function () {
                location.reload()
            }, 1500);
        } else if (res.status == "count_error") {
            Swal.fire({
                position: "center",
                icon: "error",
                title: "مشکلی در اضافه کردن محصول رخ داده است.",
                showConfirmButton: false,
                timer: 1500
            });
        } else if (res.status == "count_biger_error") {
            Swal.fire({
                position: "center",
                icon: "error",
                title: "این تعداد محصول در انبار موجود نیست.",
                showConfirmButton: false,
                timer: 1500
            });
        } else if (res.status == "not_login") {
            Swal.fire({
                title: "خطای ورود",
                text: "لطفا برای اضافه کردن محصول وارد حساب خود شوید",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#3085d6",
                cancelButtonColor: "#d33",
                confirmButtonText: "ورود",
                cancelButtonText: "لغو"
            }).then((result) => {
                if (result.isConfirmed) {
                    location.href = '/user/login/'
                }
            });
        }
    })
}

// function sumDelevary(post) {
//     let delivary = document.getElementById('delivery')
//     let total_delivery = document.getElementById('total-delivery')
//     let price = parseInt(document.getElementById('totalBasketPrice').value)
//     if (post == 'post-1') {
//         let total = price += 10000
//         let split3 = new Intl.NumberFormat('en-US', {style: "decimal"}).format(total);
//         total_delivery.innerHTML = `${split3} تومان`
//         delivary.value = 'normal'
//     } else if (post == 'post-2') {
//         let total = price += 50000
//         let split3 = new Intl.NumberFormat('en-US', {style: "decimal"}).format(total);
//         total_delivery.innerHTML = `${split3} تومان`
//         delivary.value = 'special'
//     }
// }

function removeAddress(id) {
    Swal.fire({
        title: "مطمئن هستید؟",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "بله، پاک شود.",
        cancelButtonText: "خیر"
    }).then((result) => {
        if (result.isConfirmed) {
            $.get('/user/user-delete/', {
                'id': id
            }).then(res => {
                if (res.status == 'success') {
                    Swal.fire({
                        title: "حذف!",
                        text: "آدرس با موفقیت حذف شد.",
                        icon: "success",
                        showConfirmButton: false
                    });
                    setInterval(function () {
                        location.reload()
                    }, 2000);
                } else if (res.status == 'cant') {
                    Swal.fire({
                        title: "حذف!",
                        text: "مشکلی در حذف بوجود آمد.",
                        icon: "warning",
                        showConfirmButton: false
                    });
                }
            })
        }
    });
}

function remove_product_from_basket(product_id) {
    Swal.fire({
        title: "حذف !",
        text: "آیا از حذف محصول مطمئن هستید ؟",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "بله",
        cancelButtonText: "خیر"
    }).then((result) => {
        if (result.isConfirmed) {
            $.get('/order/remove_product/', {
                'product_id': product_id
            }).then(res => {
                if (res.status == 'success') {
                    Swal.fire({
                        position: "center",
                        icon: "success",
                        title: "محصول با موفقیت حذف شد.",
                        showConfirmButton: false,
                        timer: 1500
                    });
                    setInterval(function () {
                        location.reload()
                    }, 2000);
                } else if (res.status == 'id_isnt_valid') {
                    Swal.fire({
                        position: "center",
                        icon: "error",
                        title: "در حذف محصول مشکلی رخ داده است.",
                        showConfirmButton: false,
                        timer: 1500
                    });
                    setInterval(function () {
                        location.reload()
                    }, 2000);
                }
            })
        }
    });
}

function change_count(product_id, state) {
    let content = document.getElementById('content-holder')
    let total = document.getElementById('total')
    let total_discount = document.getElementById('total_discount')
    let total_delivery = document.getElementById('total-delivery')
    $.get('/order/change-count/', {
        'product_id': product_id,
        'state': state
    }).then(res => {
        if (res.status == 'Success') {
            content.innerHTML = res.body
            let split1 = new Intl.NumberFormat('en-US', {style: "decimal"}).format(res.totalPrice);
            total.innerHTML = `${split1} تومان`
            let split2 = new Intl.NumberFormat('en-US', {style: "decimal"}).format(res.totlaDiscount);
            total_discount.innerHTML = `${split2} تومان`
            let split3 = new Intl.NumberFormat('en-US', {style: "decimal"}).format(res.totalWithDelivery);
            total_delivery.innerHTML = `${split3} تومان`
        } else if (res.status == 'Not_Found') {
            Swal.fire({
                position: "center",
                icon: "error",
                title: "در تغییر تعداد محصول مشکلی رخ داده است.",
                showConfirmButton: false,
                timer: 1500
            });
        } else if (res.status == 'Count_Not_Valid') {
            Swal.fire({
                position: "center",
                icon: "error",
                title: "موجودی انبار کافی نیست.",
                showConfirmButton: false,
                timer: 1500
            });
        } else if (res.status == 'Minimom_Count') {
            Swal.fire({
                position: "center",
                icon: "error",
                title: "تعداد محصول بیشتر از این کم نمیشود.",
                showConfirmButton: false,
                timer: 1500
            });
        }
    })
}

function set_id_address(address_id) {
    let input = document.getElementById('delivery_id')
    input.value = address_id
    console.log(input)
    console.log(address_id)
}

function addProductToFavorite(product_id) {
    $.get('/product/add-product-to-favorite/', {
        'id': product_id
    }).then(res => {
        if (res.status == 'add') {
            Swal.fire({
                position: "center",
                icon: "success",
                title: "محصول به موارد مورد علاقه اضافه شد.",
                showConfirmButton: false,
                timer: 1500
            });
            setInterval(function () {
                location.reload()
            }, 1500);
        } else if (res.status == 'remove') {
            Swal.fire({
                position: "center",
                icon: "success",
                title: "محصول از موارد مورد علاقه حذف شد.",
                showConfirmButton: false,
                timer: 1500
            });
            setInterval(function () {
                location.reload()
            }, 1500);
        }else if (res.status == 'Error') {
            Swal.fire({
                position: "center",
                icon: "error",
                title: "مشکلی در انجام عملیات رخ داده.",
                showConfirmButton: false,
                timer: 1500
            });
        }
    })
}

function send_Code() {
    let token = document.getElementById("userToken").value
    $.get('/user/resend-code/', {
        'token' : token
    }).then(res => {
        if (res.status == 'success') {
            location.reload()
        }
    })
}