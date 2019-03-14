$(document).ready(function () {
    $('.hov').hover(function () {
        if ($(this).hasClass("hov-border")) {
            $(this).removeClass("hov-border");
        } else {
            $(this).addClass("hov-border");
            }
    });
    $('#katakana').popover();
    $('#kanji').popover();
});

document.querySelector('.carousel-item').classList.add('active');
