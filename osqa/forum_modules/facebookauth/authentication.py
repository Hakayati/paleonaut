# -*- coding: utf-8 -*-

import cgi
import logging

from urllib import urlopen,  urlencode
from forum.authentication.base import AuthenticationConsumer, ConsumerTemplateContext, InvalidAuthentication

from django.conf import settings as django_settings
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _

import settings

try:
    from json import load as load_json
except Exception:
    from django.utils.simplejson import JSONDecoder

    def load_json(json):
        decoder = JSONDecoder()
        return decoder.decode(json.read())

class FacebookAuthConsumer(AuthenticationConsumer):

    def prepare_authentication_request(self, request, redirect_to):
        args = dict(
            client_id=settings.FB_API_KEY,
            redirect_uri="%s%s" % (django_settings.APP_URL, redirect_to),
            scope="email"
        )
        logging.warn('------------------> %s', args)
        facebook_api_authentication_url = "https://graph.facebook.com/oauth/authorize?" + urlencode(args)

        return facebook_api_authentication_url
    
    def process_authentication_request(self, request):
        #try:
            redirect_uri = "%s%s" % (django_settings.APP_URL, reverse('auth_provider_done', prefix='/', kwargs={'provider': 'facebook'}))
            args = dict(client_id=settings.FB_API_KEY, redirect_uri=redirect_uri)
            args["client_secret"] = settings.FB_APP_SECRET  #facebook APP Secret

            args["code"] = request.GET.get("code", None)
            code = args["code"]
            fb_url = "https://graph.facebook.com/oauth/access_token?" + urlencode(args)
            response = cgi.parse_qs(urlopen(fb_url).read())
            logging.warn('------------> access_token : %s', response["access_token"])
            access_token = response["access_token"][-1]

            #raise ValueError('just testing!')
            user_data = self.get_user_data(access_token, response)
            assoc_key = user_data["id"]

            # Store the access token in cookie
            request.session["access_token"] = access_token
            request.session["assoc_key"] = assoc_key

            # Return the association key
            return assoc_key
        #except Exception, e:
        #    logging.error("Problem during facebook authentication: %s" % e)
        #    raise InvalidAuthentication(_("Something wrond happened during Facebook authentication, administrators will be notified"))

    def get_user_data(self, access_token2, response):
        fb_url = "https://graph.facebook.com/me?" + urlencode(dict(access_token=access_token2))
        profile = load_json(urlopen(fb_url))
        name = profile["name"]

        # Check whether the length if the email is greater than 75, if it is -- just replace the email
        # with a blank string variable, otherwise we're going to have trouble with the Django model.
        email = smart_unicode(profile['email'])
        if len(email) > 75:
            email = ''

        # If the name is longer than 30 characters - leave it blank
        if len(name) > 30:
            name = ''

        # Return the user data.
        return {
            'id' : profile['id'],
            'username': name,
            'email': email,
        }

class FacebookAuthContext(ConsumerTemplateContext):
    mode = 'BIGICON'
    type = 'CUSTOM'
    weight = 100
    human_name = 'Facebook'
    code_template = 'modules/facebookauth/button.html'
    extra_css = []

    API_KEY = settings.FB_API_KEY