//start of coupons
// function copyText(button) {
//     var couponCodeInput = button.parentElement.querySelector('.coupon-code');
//     couponCodeInput.select();
//     couponCodeInput.setSelectionRange(0, 99999); 
//     document.execCommand('copy');

//     var alertMessage = button.parentElement.querySelector('.alert');
//     alertMessage.style.display = 'block';

//     setTimeout(function () {
//         alertMessage.style.display = 'none';
//     }, 3000);
// }

// jQuery.noConflict();

// var couponApplied = false;

// document.getElementById('ApplyCoupon').addEventListener('click', function () {
//     if (couponApplied) {
//         console.log("Coupon already applied!");
//         return;
//     }

//     console.log("Applying coupon...");

//     var coupon_code = document.getElementById('coupon').value;
//     var grand_total = document.getElementById('grand_total').innerText;

//     console.log(grand_total, "This is the total value to Checkout");

//     var token = $("[name='csrfmiddlewaretoken']").val();
//     var dataToSend = {
//         key1: coupon_code,
//         key2: grand_total,
//         csrfmiddlewaretoken: token,
//     };

//     $.ajax({
//         url: '/checkout/coupons/',
//         method: 'POST',
//         data: dataToSend,
//         success: function (response) {
//             console.log(document.getElementById('discounts').innerText);
//             document.getElementById('discounts').innerText = +response.discount_amount;

//             console.log(response.total);
//             console.log("this is the discounted amount ", response.discount_amount);
//             console.log("this is the discounted amount1111 ", response.total);

//             document.getElementById('grand_total').innerText = response.total;

//             couponApplied = true;
//         },
//         error: function (error) {
//             console.error('Error:', error);
//         }
//     });
// });







//end of coupons


$(document).ready(function () {

    $('.payWithRazorpay').click(function (e) {
        e.preventDefault();

        var fname = $("[name='fname']").val();
        var lname = $("[name='lname']").val();
        var email = $("[name='email']").val();
        var phone = $("[name='phone']").val();
        var address = $("[name='address']").val();
        var city = $("[name='city']").val();
        var state = $("[name='state']").val();
        var country = $("[name='country']").val();
        var pincode = $("[name='pincode']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();

        if(fname == "" || lname == "" || email == "" || phone == "" || address == "" || city == "" || state == "" || country == "" || pincode == "" )
        {
            swal("Alert!", "All fields are mandatory!", "error");

            return false;
        }
        else
        {
            $.ajax({
                method: "GET",
                url: "/proceed-to-pay",
                success: function (response) {
                    // console.log(response);
                    var options = {
                        "key": "rzp_test_Y1r2PgxSWo4GCH", // Enter the Key ID generated from the Dashboard
                        "amount": 1*100,//response.total_price * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "GOKUL", //your business name
                        "description": "Thank you for buying from us",
                        "image": "https://example.com/your_logo",
                        // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (responseb){
                            alert(responseb.razorpay_payment_id);
                            data = {
                                "fname": fname,
                                "lname": lname,
                                "email": email,
                                "phone": phone,
                                "address": address,
                                "city": city,
                                "state": state,
                                "country": country,
                                "pincode": pincode,
                                "payment_mode": "Paid by Razorpay",
                                "payment_id": responseb.razorpay_payment_id,
                                csrfmiddlewaretoken: token 
                            }
                            $.ajax({
                                method: "POST",
                                url: "/place-order",
                                data: data,
                                success: function (responsec) {
                                    swal("Congratulations!",responsec.status , "success").then((value) => {
                                        window.location.href = '/my-orders'
                                      });
                                }
                            });


                        },
                        "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information, especially their phone number
                            "name": fname+" "+lname, //your customer's name
                            "email": email, 
                            "contact": phone  //Provide the customer's phone number for better conversion rates 
                        },
                       
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                }
            });



        }


        
        rzp1.on('payment.failed', function (response){
                alert(response.error.code);
                alert(response.error.description);
                alert(response.error.source);
                alert(response.error.step);
                alert(response.error.reason);
                alert(response.error.metadata.order_id);
                alert(response.error.metadata.payment_id);
        });
        
    });

});

