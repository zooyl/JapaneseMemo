$(document).ready(function () {
    $('[data-toggle="popover"]').popover({placement: 'top'});
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
    var slide = $('.extend');
    slide.click(function () {
        $('#levels').slideToggle(function () {
            if (slide.text() === 'Show') {
                slide.text('Hide')
            } else {
                slide.text('Show')
            }
        });
    });
    $('#myModal').modal({
        backdrop: 'static',
        keyboard: false
    })
});

document.querySelector('.carousel-item').classList.add('active');
