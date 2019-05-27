$(document).ready(function () {
    // levels/alphabet popup
    $('[data-toggle="popover"]').popover({placement: 'top'});
    // counter function
    $('.counter').each(function () {
        var $this = $(this),
            countTo = $this.attr('data-count');

        $({countNum: $this.text()}).animate({
                countNum: countTo
            },

            {

                duration: 7000,
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
    // stats counter
    var fade_exercise = $('#exercise');
    var fade_attempts = $('#attempts');
    var fade_streak = $('#streak');
    var fade_average = $('#average');
    fade_exercise.css({"position": "relative", "opacity": 0, "left": "+=100"});
    fade_exercise.animate({left: 0, opacity: 1}, 3000);
    fade_attempts.css({"position": "relative", "opacity": 0, "right": "+=100"});
    fade_attempts.animate({left: 0, opacity: 1}, 4000);
    fade_average.css({"position": "relative", "opacity": 0, "left": "+=100"});
    fade_average.animate({left: 0, opacity: 1}, 6000);
    fade_streak.css({"position": "relative", "opacity": 0, "right": "+=100"});
    fade_streak.animate({left: 0, opacity: 1}, 7000);
    // levels list
    var slide_signs = $('.extend-signs');
    slide_signs.click(function () {
        $('#levels-signs').slideToggle(function () {
            if (slide_signs.text() === 'Signs') {
                slide_signs.text('Hide')
            } else {
                slide_signs.text('Signs')
            }
        });
    });
    var slide_words = $('.extend-words');
    slide_words.click(function () {
        $('#levels-words').slideToggle(function () {
            if (slide_words.text() === 'Words') {
                slide_words.text('Hide')
            } else {
                slide_words.text('Words')
            }
        });
    });
    // exercise completed modal
    $('#myModal').modal({
        backdrop: 'static',
        keyboard: false
    });
    // reading japanese
    $('#megaphone').click(function () {
        $('#listen').get(0).play()
    })
});

document.querySelector('.carousel-item').classList.add('active');
