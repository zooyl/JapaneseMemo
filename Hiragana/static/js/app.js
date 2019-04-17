$(document).ready(function () {
    $('[data-toggle="popover"]').popover({placement: 'top'});
    $(".quest-answer-fade").css({"position": "relative", "opacity": 0});
    $(".quest-answer-fade").animate({left: 0, opacity: 1}, 2000);
    $('.counter').each(function () {
        var $this = $(this),
            countTo = $this.attr('data-count');

        $({countNum: $this.text()}).animate({
                countNum: countTo
            },

            {

                duration: 8000,
                easing: 'linear',
                step: function () {
                    $this.text(Math.floor(this.countNum));
                },
                complete: function () {
                    $this.text(this.countNum);
                    //alert('finished');
                }

            });


    });
});

document.querySelector('.carousel-item').classList.add('active');
