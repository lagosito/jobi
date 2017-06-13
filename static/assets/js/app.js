window.sr = ScrollReveal({reset: true});
sr.reveal('.home-content h1, .navbar-default', {duration: 1500});

$(document).ready(function () {


    $(".job-post .job-title h3 i").on('click', function () {
        $(this).toggleClass("liked");
    });
    $("body").tooltip({selector: '[data-toggle=tooltip]'});
    $(".circle").on("click", function () {
        $(".menu-links").toggleClass("active");
    });
    $(".close-menu").on("click", function () {
        $(".menu-links").toggleClass("active");
    });

});


function sliderInit() {

    $(".slick").slick({
        dots: true,
        arrows: true,
        infinite: true,
        slidesToShow: 1,
        autoplay: false,
        slidesToScroll: 1,

    });
    $(".job-slider").slick({
        dots: false,
        arrows: true,
        infinite: true,
        slidesToShow: 4,
        autoplay: false,
        slidesToScroll: 1,
        responsive: [
            {
                breakpoint: 1300,
                settings: {
                    slidesToShow: 3,
                }
            },
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 2,
                }
            },

            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 1
                }
            },
            {
                breakpoint: 360,
                settings: {
                    arrows: false,
                    slidesToShow: 1
                }
            }
        ]

    });
}

$(function () {


    $("#logos_section").hide();
    $("#search_jobs_section").hide();
    $("#jobs_section").hide();
    $("#contact_section").hide();
    $("#main-footer").hide();



    var job_post = '';
    var recent_job_post = '';
    var all_modal = '';
    var server_address = "";
    var recent_job_api_url = server_address + '/se/recent_jobs/';
    var newsletter_subscription_api_url = server_address + '/newsletter_add_subscription/';


    function create_recent_job_posts(job_title, job_post_time, organization, job_location, job_url) {
        recent_job_post = recent_job_post + '<div>' +
            '<a href="' + job_url + '" data-toggle="tab">' +
            '<div>' +
            '<p>posted at ' + job_post_time + '</p>' +
            '<p><strong>' + job_title + '</strong></p>' +
            '<p>' + organization + '</p>' +
            '<p>' + job_location + '</p>' +
            '</div>' +
            '</a>' +
            '</div>';
    }

    function create_job_posts(organization, job_location, job_post_time, job_description, job_url, count) {
        job_post = job_post + '<div class="job-post">' +
            '<div class="job-count">'+
            // '<a href="' + job_url + '">' +
            '<div class="job-title clearfix">' +
            '<div class="pull-left">' +
            '<h3>' + organization + '&nbsp;&#124;&nbsp;</h3>' +
            '<h1>' + job_location + '</h1>'+
            '</div>' +
            '<div class="pull-right">' +
            '<span>posted at ' + job_post_time + '</span>' +
            '</div>' +
            '</div>' +
            '<div class="job-description" data-toggle="modal" data-target="#job_modal' + count + '">' +
            '<p>' + job_description + '</p>' +
            '</div>' +
            // '</a>' +
            '</div>'+
            '</div>';

    }

    function create_modals(organization, job_role, job_location, job_post_time, job_description, job_description2, job_url, count){
        all_modal = all_modal + 
                '<div class="modal fade job_modal_style" id="job_modal'+ count +'"> \
                    <div class="modal-dialog modal-lg" role="document"> \
                        <div class="modal-content"> \
                            <div class="modal-body"> \
                                <div class="menu-links"> \
                                    <div class="container"> \
                                        <a href="javascript:;" class="close-menu"><i class="fa fa-times"></i> </a> \
                                        <div class="row"> \
                                            <div class="col-sm-6"> \
                                                <ul class="nav nav-tabs"> \
                                                    <li> \
                                                        <a href="#about-s" data-toggle="tab">About</a> \
                                                    </li> \
                                                    <li> \
                                                        <a href="#contact-s" data-toggle="tab">Contact</a> \
                                                    </li> \
                                                </ul> \
                                                <div class="social-links"> \
                                                    <a href="#"><i class="fa fa-facebook"></i></a> \
                                                    <a href="#"><i class="fa fa-twitter"></i></a> \
                                                    <a href="#"><i class="fa fa-linkedin"></i></a> \
                                                </div> \
                                                <div class="quick-links"> \
                                    <span> \
                                        <a href="#">Privacy policy</a> \
                                        <a href="#">Copyright Notification</a> \
                                    </span> \
                                    <span> \
                                         <a href="#">Term of use</a> \
                                    <a href="#">I want to join the team</a> \
                                    </span> \
                                                </div> \
                                            </div> \
                                            <div class="col-sm-6"> \
                                                <div class="tab-content"> \
                                                    <div class="tab-pane active"> \
                                                        <img src="/static/assets/images/big_logo.png" class="img-responsive" alt=""> \
                                                    </div> \
                                                    <div class="tab-pane" id="about-s"> \
                                                        <p class="normal-text"> \
                                                            Businesses that partner with Google come in all shapes, sizes and market caps, and no one Google advertising solution works for all. \
                                                        </p> \
                                                        <p class="normal-text"> \
                                                            Your knowledge of o our range of product offerings can grow their business. Working with them, you set the vision and the strategy for how their advertising can reach thousands of users. \
                                                            Lea \
                                                        </p> \
                                                    </div> \
                                                    <div class="tab-pane" id="contact-s"> \
                                                        <div class="contact-form"> \
                                                            <form action=""> \
                                                                <div class="form-group"> \
                                                                    <label>Your Name</label> \
                                                                    <input type="text" class="form-control"/> \
                                                                </div> \
                                                                <div class="form-group"> \
                                                                    <label>Your eMail</label> \
                                                                    <input type="text" class="form-control"/> \
                                                                </div> \
                                                                <div class="form-group"> \
                                                                    <label>Your eMail</label> \
                                                                    <textarea class="form-control"></textarea> \
                                                                </div> \
                                                                <div class="text-center submit-btn"> \
                                                                    <button type="submit">Submit</button> \
                                                                </div> \
                                                            </form> \
                                                        </div> \
                                                    </div> \
                                                </div> \
                                            </div> \
                                        </div> \
                                    </div> \
                                </div>  \
                                <nav class="navbar navbar-default">  \
                                    <div class="container col-lg-12"> \
                                    <div class="col-lg-12"> \
                                        <div class="header-content text-center"> \
                                            <div class="pull-left"> \
                                                <div class="menu-toggle"> \
                                                    <a class="circle" href="#"> \
                                                        <div class="lines"> \
                                                            <i></i> \
                                                            <i></i> \
                                                            <i class="no-margin"></i> \
                                                        </div> \
                                                    </a> \
                                                </div> \
                                            </div> \
                                            <div class="logo"> \
                                                <img src="/static/assets/images/logo.jpg"/> \
                                            </div> \
                                            <div class="pull-right"> \
                                                <div class="lang-links"> \
                                                    <ul class="list-unstyled"> \
                                                        <li><a href="#"><img src="/static/assets/images/login-image.png" alt=""></a></li> \
                                                        <li><span></span></li> \
                                                        <li><a href="#">EN</a></li> \
                                                    </ul> \
                                                </div> \
                                            </div> \
                                        </div> \
                                    </div> \
                                    </div> \
                                </nav>'+
                                '<div class="job-post job-detail"> \
                                    <div class="job-title clearfix"> \
                                        <div class="pull-left">' +
                                            '<h2>'+ organization + '&nbsp;&#124;&nbsp;' + job_role + '&nbsp;&#124;&nbsp;' +  job_location + '</h2>' +
                                        '</div> \
                                        <div class="pull-right"> \
                                            <span>' + job_post_time + '</span>'+
                                        '</div> \
                                    </div> \
                                    <div class="job-details-content"> \
                                        <div class="row"> \
                                            <div class="col-sm-6"> \
                                                <p class="job-text">'+
                                                job_description + 
                                                '</p> \
                                            </div> \
                                            <div class="col-sm-6"> \
                                                <p class="job-text">'+
                                                    job_description2 + 
                                                '</p> \
                                            </div> \
                                        </div> \
                                        <div class="action-button"> \
                                            <a href="' + job_url + '">Apply</a>'+
                                            '<a href="#" data-dismiss="modal">Back</a> \
                                        </div> \
                                    </div> \
                                </div> \
                                <div class="similar-text hidden-sm hidden-xs"> \
                                    Similar Offers \
                                </div> \
                                <section class="job-section hidden-sm hidden-xs"> \
                                    <div class="nav nav-tabs"> \
                                        <div class="row"> \
                                            <div class="col-md-3"> \
                                                <a href="#" data-toggle="tab"> \
                                                    <div> \
                                                        <p>posted at 4:32 pm</p> \
                                                        <p><strong>Creative Director Digital</strong></p> \
                                                        <p>IBM Company</p> \
                                                        <p>Berlin / Deutshland</p> \
                                                    </div> \
                                                </a> \
                                            </div> \
                                            <div class="col-md-3"> \
                                                <a href="#" data-toggle="tab"> \
                                                    <div> \
                                                        <p>posted at 4:32 pm</p> \
                                                        <p><strong>Creative Director Digital</strong></p> \
                                                        <p>IBM Company</p> \
                                                        <p>Berlin / Deutshland</p> \
                                                    </div> \
                                                </a> \
                                            </div> \
                                            <div class="col-md-3"> \
                                                <a href="#" data-toggle="tab"> \
                                                    <div> \
                                                        <p>posted at 4:32 pm</p> \
                                                        <p><strong>Creative Director Digital</strong></p> \
                                                        <p>IBM Company</p> \
                                                        <p>Berlin / Deutshland</p> \
                                                    </div> \
                                                </a>  \
                                            </div>  \
                                            <div class="col-md-3">  \
                                                <a href="#" data-toggle="tab">  \
                                                    <div>  \
                                                        <p>posted at 4:32 pm</p>  \
                                                        <p><strong>Creative Director Digital</strong></p>  \
                                                        <p>IBM Company</p>  \
                                                        <p>Berlin / Deutshland</p> \
                                                    </div> \
                                                </a> \
                                            </div> \
                                        </div> \
                                    </div> \
                                </section> \
                            </div> \
                        </div> \
                    </div> \
                </div>';

    }

    //----------------------------------------------------------------------------
    //-----------------------------RECENT JOBS PULL-------------------------------

    $.ajax({
        type: 'GET',
        url: recent_job_api_url,
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        success: function (response) {

            recent_job_posts_entries = response['hits']['hits'];

            // console.log(Object.keys(recent_job_posts_entries).length);
            // console.log(recent_job_posts_entries[0]['_source']);

            for (i = 0; i < Object.keys(recent_job_posts_entries).length; i++) {


                job_title = recent_job_posts_entries[i]['_source']['job_title'];
                if (job_title.length > 20)
                            job_title = job_title.substr(0,20) + '...';
                job_url = recent_job_posts_entries[i]['_source']['link'];
                job_post_time = recent_job_posts_entries[i]['_source']['create_time'];
                var local_time = new Date(job_post_time);
                job_post_time = local_time.toLocaleTimeString('en-US', {
                    hour: 'numeric',
                    minute: 'numeric',
                    hour12: true
                });

                organization = recent_job_posts_entries[i]['_source']['organisation'];
                job_location = recent_job_posts_entries[i]['_source']['location'];


                create_recent_job_posts(job_title, job_post_time, organization, job_location, job_url);
                // console.log('-------------------------------------------------------------------------');
                // console.log(recent_job_post);

            }
            // recent_job_post = recent_job_post + '</div>';
            $('#recent_jobs_container').append(recent_job_post);
            sliderInit();


        },
        error: function (error) {
            console.log(error);
        }
    });

    //----------------------------------------------------------------------------
    //------------------------------RECENT JOBS PULL END--------------------------

    //---------------------------------------------------------------------------
    //-------------------------CONTACT FORM SUBMISSION---------------------------

    $("#contact_form").on("submit", function (event) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: newsletter_subscription_api_url,
            data: $(this).serialize(),
            dataType: "json",
            success: function (data) {
                // console.log(data);
            },
            error: function () {
                // alert('error handing here');
            }
        });
    });

    //---------------------------------------   -------------------------------------
    //-----------------------CONTACT FORM SUBMISSION END--------------------------

    //----------------------------------------------------------------------------
    //----------------------------JOB SEARCH SUGGESTION---------------------------



    $( "#keyword" ).keyup(function() {
        suggest_api_url = server_address + "/se/suggest/?role=" + $(this).val();
        $.ajax({
            type: 'GET',
            url: suggest_api_url,
            dataType: 'json',
            success: function (data) {
                results = '';
                $.each(data.role_suggestions, function (key, val) {
                    results = results + '<option value="' + val['value'] + '">';
                })
                $('#role-datalist').html(results);
            }
        });
    });

    $( "#job_type" ).keyup(function() {
        suggest_api_url = server_address + "/se/suggest/?job_type=" + $(this).val();
        $.ajax({
            type: 'GET',
            url: suggest_api_url,
            dataType: 'json',
            success: function (data) {
                results = '';
                $.each(data.job_type_suggestions, function (key, val) {
                    results = results + '<option value="' + val['value'] + '">';
                })
                $('#type-datalist').html(results);
            }
        });
    });

    $( "#location" ).keyup(function() {
        suggest_api_url = server_address + "/se/suggest/?location=" + $(this).val();
        $.ajax({
            type: 'GET',
            url: suggest_api_url,
            dataType: 'json',
            success: function (data) {
                results = '';
                $.each(data.location_suggestions, function (key, val) {
                    results = results + '<option value="' + val['value'] + '">';
                })
                $('#location-datalist').html(results);
            }
        });
    });



    //----------------------------------------------------------------------------
    //----------------------------JOB SEARCH SUGGESTION END---------------------------


    //----------------------------------------------------------------------------
    //-----------------------------JOB SEARCH FORM--------------------------------


    $("#job_search_form").on("submit", function (event) {

        event.preventDefault();
        //console.log("Form Submitted Hurray");

        job_post = '';
        all_modal = '';
        keyword_val = $("#keyword").val();
        location_val = $("#location").val();
        job_type_val = $("#job_type").val();

        final_url = server_address + "/se/search_jobs/?role=" + keyword_val + "&location=" + location_val + "&job_type=" + job_type_val;
        //final_url = server_address + "/se/search_jobs/?role=abbrucharbeiter";

        $.ajax({
            type: 'GET',
            url: final_url,
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            success: function (response) {

                 //console.log(response);
                // console.log('-------------------------------------------------------------------------');

                $("#logos_section").show();
                $("#search_jobs_section").show();
                $("#jobs_section").show();
                $("#contact_section").show();
                $("#main-footer").show();


                job_posts_entries = response['hits']['hits'];

                // console.log(Object.keys(job_posts_entries).length);
                // console.log(job_posts_entries[0]['_source']);

                var no_of_jobs = Object.keys(job_posts_entries).length;

                if (no_of_jobs > 0) {
                    count = 0
                    job_posts_entries.forEach(function(item, i) {
                        if (count === 50) {
                            return false;
                          }

                        job_title = job_posts_entries[i]['_source']['job_title'];
                        if (job_title.length > 20)
                            job_title = job_title.substr(0,20) + '...';


                        job_url = job_posts_entries[i]['_source']['link'];

                        job_description = job_posts_entries[i]['_source']['msg'];
                        job_description2 = '';
                        if ((job_description.length > 100) && (job_description.length < 3000)){
                            job_description = job_description.substr(0, job_description.length/2) + '...';
                            job_description2 = job_description.substr((job_description.length/2) + 1 ,job_description.length - 1 ) ;
                        }

                        else if((job_description.length < 3000)){
                            job_description = job_description.substr(0, job_description.length/2) + '...';
                            job_description2 = job_description.substr((job_description.length/2) + 1 ,job_description.length - 1 ) + '...';
                        }

                        job_post_time = job_posts_entries[i]['_source']['create_time'];
                        job_location = job_posts_entries[i]['_source']['location'];
                        organization = job_posts_entries[i]['_source']['organisation'];
                        job_role = job_posts_entries[i]['_source']['role'];


                        var local_time = new Date(job_post_time);
                        job_post_time = local_time.toLocaleTimeString('en-US', {
                            hour: 'numeric',
                            minute: 'numeric',
                            hour12: true
                        });
                        create_job_posts(organization, job_location, job_post_time, job_description, job_url, count);
                        create_modals(organization, job_role, job_location, job_post_time, job_description, job_description2, job_url, count);
                        // console.log('-------------------------------------------------------------------------');
                        // console.log(job_post);
                        count++;

                    });

                }
                else {
                    job_post = job_post + '<div class="job-post">' +
                        '<div class="job-count">'+
                        '<a href="#">' +
                        '<div class="job-description">' +
                        '<p><text-center>Sorry, we couldn\'t find any job matching your criterion. Please try with some other parameters. </p>' +
                        '</div>' +
                        '</a>' +
                        '</div>' +
                        '</div>';
                }

                $('#jobs_container').html(job_post);
                $('#all_modal').html(all_modal);

                $('html, body').stop().animate({
                    scrollTop: $("#logos_section").offset().top
                }, 1000);

            },
            error: function (error) {
                // console.log(error);
            }
        });

    });

    //----------------------------------------------------------------------------
    //---------------------------JOB SEARCH FORM END------------------------------


});

