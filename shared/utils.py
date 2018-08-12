from django.http import JsonResponse


def choices_zip(choices):
    """
    Creates a container compatible with Django's modelField.choices when both the databa

    :param choices: An iterable of the choices for the modelField
    :return: An iterable of two-item tuples, both items identical
    """
    return [(c, c) for c in choices]


# https://docs.djangoproject.com/en/1.8/topics/class-based-views/generic-editing/#ajax-example
class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

class PreventCapFirst(unicode):
    def upper(self):
        return self
    def __getitem__(self, key):
        return self.__class__(super(PreventCapFirst, self).__getitem__(key))
