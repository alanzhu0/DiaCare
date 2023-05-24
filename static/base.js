function googleTranslateElementInit() {
    new google.translate.TranslateElement(
        { pageLanguage: 'en' },
        'google_translate_element'
    );
}

$(function() {
    $("nav .nav-link[href='" + window.location.pathname + "']").addClass("active");
    setTimeout(function() {
        $(".alert").fadeOut();
    }, 5000);
});

