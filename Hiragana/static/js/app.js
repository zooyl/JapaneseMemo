$(document).ready(function () {
    $('.hov').hover(function () {
        if ($(this).hasClass("hov-border")) {
            $(this).removeClass("hov-border");
        } else {
            $(this).addClass("hov-border");
        }
    });
    $('[data-toggle="popover"]').popover({placement: 'top'});
    $(".quest-answer-fade").css({"position": "relative", "opacity": 0});
    $(".quest-answer-fade").animate({left: 0, opacity: 1}, 2000);
});

document.querySelector('.carousel-item').classList.add('active');
