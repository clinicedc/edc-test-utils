def get_webtest_form(response):
    try:
        form = response.form
    except TypeError:
        form = response.forms[1]
    return form
