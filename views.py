# Create your views here.
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import Context
from django.template import RequestContext
from django.template import loader
from django_contact.forms import ContactForm
from django_contact.models import Contact
from recaptcha.client import captcha


def send(contact_form):
    site = Site.objects.get(id=settings.SITE_ID)
    contact = Contact.objects.all()[0]

    # construct email
    from_email = '"%s" <%s>' % (contact_form.cleaned_data['name'], contact_form.cleaned_data['email'])
    send_to = '"%s" <%s>' % (contact.user.first_name + ' ' + contact.user.last_name, contact.user.email)
    subject = '[' + site.name + ' contact] ' + contact_form.cleaned_data['subject']

    if contact_form.cleaned_data['website']:
        message = 'website: %s\n\n' % (contact_form.cleaned_data['website'])
    else:
        message = ''

    message += contact_form.cleaned_data['message']

    #send email
    email = EmailMessage(subject, message, from_email, (send_to,), headers={'Reply-To': from_email})
    #email.send(fail_silently=False)
    email.send()


# Create your views here.
def contact(request):
    template_vars = {}
    template_vars['CONTACTEXTEND'] = settings.CONTACTEXTEND
    template_vars['CONTACTURL'] = settings.CONTACTURL
    template_vars['RECAPTCHA_PUBLIC_KEY'] = settings.RECAPTCHA_PUBLIC_KEY

    if request.POST:
        contact_form = ContactForm(request.POST)
        template_vars['contact_form'] = contact_form

        # Check the form captcha.  If not good, pass the template an error code
        captcha_response = captcha.submit(
                                          request.POST.get("recaptcha_challenge_field", None),
                                          request.POST.get("recaptcha_response_field", None),
                                          settings.RECAPTCHA_PRIVATE_KEY,
                                          request.META.get("REMOTE_ADDR", None))

        if not captcha_response.is_valid:
            template_vars['captcha_error'] = "&error=%s" % captcha_response.error_code

        elif contact_form.is_valid():
            send(contact_form)
            return HttpResponseRedirect('/success')

    else:
        contact_form = ContactForm()
        template_vars['contact_form'] = contact_form

    return render_to_response('contact.html',
                              template_vars,
                              context_instance=RequestContext(request))