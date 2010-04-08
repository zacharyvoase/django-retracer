# `django-retracer`

`django-retracer` is a Django application which allows you to store and restore
old locations. It’s useful in scenarios where you want to remember where the
client was before, show them a number of pages and then redirect them to the old
location.

## Example

Here’s an example of how interaction might work:

*   Your user is on a page on your website, say `/somepage/`. They click the
    ‘Submit Feedback’ link in the footer, because they love your site so much
    they want to tell you about it. This takes them to `/feedback/`.

*   The view at `/feedback/` stores the old location from the HTTP `Referer`
    [sic] header, and then displays the form to the user:
    
        def feedback(request):
            if request.method == 'GET':
                request.stash_referrer()
                form = FeedbackForm()
                return render_to_response('feedback/feedback.html',
                  {'form': form})
            elif request.method == 'POST':
                # ... process the form ...

*   When the client submits a valid form, set a flash notice and redirect to the
    old location:
    
        def feedback(request):
            if request.method == 'GET':
                # ... see above ...
            elif request.method == 'POST':
                form = FeedbackForm(request.POST)
                if form.is_valid():
                    form.save()
                    request.notices.success("Thank you for your feedback!")
                    # `request.unstash_location_with_default()` returns a 
                    # temporary redirect, using the given parameters to generate
                    # a default URL if no previous location is stored.
                    return request.unstash_location_with_default('/')
                else:
                    # ... handle invalid forms ...

This stashing/unstashing of locations is especially useful when used in
conjunction with ‘flash notices’. In Django v1.2, these are available in the
[messages framework][]; [a backport also exists][gh-django-messages-framework]
for Django v1.1.1.

  [messages framework]: http://docs.djangoproject.com/en/dev/ref/contrib/messages/#ref-contrib-messages
  [gh-django-messages-framework]: http://github.com/mikexstudios/django-messages-framework

## Installation

*   Getting the app onto your Python path is as easy as:
    
    *   `easy_install django-retracer`, or
    *   `pip install django-retracer`

*   Add `'djretr'` to your `INSTALLED_APPS` setting. `'django.contrib.session'`
    must also be installed for `django-retracer` to work.

*   Add `djretr.middleware.RetracerMiddleware` to your `MIDDLEWARE_CLASSES`
    setting. This must come *after* `SessionMiddleware`.

## Configuration

You can set the `RETRACER_SESSION_KEY` attribute to a string specifying what key
in the session dictionary you want the currently stashed location to be stored
under. By default, this is `'_location'`.

## Usage

### Stashing Locations

    def myview(request):
        # stash an absolute location:
        request.stash_location('/somewhere/')
        # stash the current referrer, falling back on a default:
        request.stash_referrer('/default/')

### Unstashing Locations

    def myview(request):
        # Temporary Redirect (302):
        return request.unstash_location()
        # Permanent Redirect (301):
        return request.unstash_location(permanent=True)
        # Unstashing with a default fallback:
        return request.unstash_location_with_default(
            'someview', args=(arg1, arg2), kwargs={'key1': 'value1'},
            permanent=False)
        # Unstashing with a randomly-generated query parameter, to avoid
        # caching issues:
        return request.unstash_location(nonce=True)

## (Un)license

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this
software, either in source code form or as a compiled binary, for any purpose,
commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this
software dedicate any and all copyright interest in the software to the public
domain. We make this dedication for the benefit of the public at large and to
the detriment of our heirs and successors. We intend this dedication to be an
overt act of relinquishment in perpetuity of all present and future rights to
this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
