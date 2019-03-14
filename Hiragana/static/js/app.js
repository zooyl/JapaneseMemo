$(document).ready(function () {
    $('.hov').hover(function () {
        if ($(this).hasClass("hov-border")) {
            $(this).removeClass("hov-border");
        } else {
            $(this).addClass("hov-border");
            }
    });
    $('[data-toggle="popover"]').popover();
});

document.querySelector('.carousel-item').classList.add('active');
