$(function() {
    $("nav .nav-link[href='" + window.location.pathname + "']").addClass("active");
    setTimeout(function() {
        $(".alert").fadeOut();
    }, 5000);
});