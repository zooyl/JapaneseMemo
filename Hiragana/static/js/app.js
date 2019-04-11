$(document).ready(function () {
    $('.hov').hover(function () {
        if ($(this).hasClass("hov-border")) {
            $(this).removeClass("hov-border");
        } else {
            $(this).addClass("hov-border");
        }
    });
    $('[data-toggle="popover"]').popover({placement: 'top'});
    $(".quest-fade-in-right").css({"position": "relative", "opacity": 0, "left": "+=100"});
    $(".quest-fade-in-right").animate({left: 0, opacity: 1}, 2000);
    $(".quest-fade-in-left").css({"position": "relative", "opacity": 0, "right": "+=100"});
    $(".quest-fade-in-left").animate({right: 0, opacity: 1}, 2000);
});

document.querySelector('.carousel-item').classList.add('active');
