import os
import time
import urllib
import json
import re
import logging
from collections import defaultdict

import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

import medievia.item.parse
import medievia.item.item
import medievia.item.item_base
import medievia.item.item_summary
import medievia.search
import medievia.admin.administrator
import medievia.admin.message
import medievia.admin.artifact
import medievia.xpxp

jinja_environment = jinja2.Environment(autoescape=True,
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__))))


# todo: add auto-complete in search bar
# re: http://blog.startuptale.com/2012/10/partial-search-on-gae-with-search-api.html
# re: http://stackoverflow.com/questions/10960384/google-app-engine-python-search-api-string-search


class HomeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/home.html')
        template_values = {
            'is_admin_user': is_admin_user(),
            'user': users.get_current_user(),
            'signInUrl': users.create_login_url('/'),
            'signOutUrl': users.create_logout_url('/')
        }
        self.response.out.write(template.render(template_values))


class SearchHandler(webapp2.RequestHandler):
    def get(self):
        query = self.request.get('q')

        if query:
            items = medievia.search.run_new_search(query)
        else:
            items = None

        template_values = {
            'is_admin_user': is_admin_user(),
            'user': users.get_current_user(),
            'signInUrl': users.create_login_url('/'),
            'signOutUrl': users.create_logout_url('/'),
            'items': items,
            'query': query
        }

        template = jinja_environment.get_template('templates/search.html')
        self.response.out.write(template.render(template_values))


class BrowseHandler(webapp2.RequestHandler):
    def get(self):
        items = medievia.search.browse_all()

        template_values = {
            'is_admin_user': is_admin_user(),
            'user': users.get_current_user(),
            'signInUrl': users.create_login_url('/'),
            'signOutUrl': users.create_logout_url('/'),
            'items': items
        }

        template = jinja_environment.get_template('templates/browse.html')
        self.response.out.write(template.render(template_values))


class ItemHandler(webapp2.RequestHandler):
    def get(self, url_key):
        # get the item summary from the url key
        item_summary = medievia.item.item_base.get_item(url_key)

        # get all of the related items from the summary
        items = medievia.item.item.get_all_items(item_summary)

        # build up dictionaries that will hold computed values
        modifier_computed_values = defaultdict(list)
        affect_computed_values = defaultdict(list)
        for min_modifier in item_summary.min_modifiers:
            modifier_computed_values[min_modifier.display_name()].append(min_modifier.value)
        for max_modifier in item_summary.min_modifiers:
            modifier_computed_values[max_modifier.display_name()].append(max_modifier.value)
        for base_modifier in item_summary.base_modifiers:
            modifier_computed_values[base_modifier.display_name()].append(base_modifier.value)

        for min_affect in item_summary.min_affects:
            affect_computed_values[min_affect.name].append(min_affect.value)
        for max_affect in item_summary.max_affects:
            affect_computed_values[max_affect.name].append(max_affect.value)
        for base_affect in item_summary.base_affects:
            affect_computed_values[base_affect.name].append(base_affect.value)

        # build up dictionaries that will hold individual values
        modifier_values = defaultdict(list)
        affect_values = defaultdict(list)
        for item in items:
            for modifier in item.modifiers:
                modifier_values[modifier.display_name()].append(modifier.value)
            for affect in item.affects:
                affect_values[affect.name].append(affect.value)

        template_values = {
            'is_admin_user': is_admin_user(),
            'user': users.get_current_user(),
            'signInUrl': users.create_login_url('/'),
            'signOutUrl': users.create_logout_url('/'),
            'itemSummary': item_summary,
            'items': items,
            'modifierComputedValues': modifier_computed_values,
            'affectComputedValues': affect_computed_values,
            'modifierValues': modifier_values,
            'affectValues': affect_values
        }

        template = jinja_environment.get_template('templates/item.html')
        self.response.out.write(template.render(template_values))


class AdminHandler(webapp2.RequestHandler):
    def get(self):
        if is_admin_user():
            # get total number of items in database
            total_in_db = medievia.item.item.get_item_count()

            # get total number of items in index
            total_in_index = medievia.search.index_count()

            # get all messages in admin message
            recent_messages = medievia.admin.message.get()

            template_values = {
                'is_admin_user': is_admin_user(),
                'user': users.get_current_user(),
                'signInUrl': users.create_login_url('/'),
                'signOutUrl': users.create_logout_url('/'),
                'admins': medievia.admin.administrator.get(),
                'total_items': total_in_db,
                'total_index': total_in_index,
                'messages': recent_messages
            }

            template = jinja_environment.get_template('templates/admin/admin.html')
            self.response.out.write(template.render(template_values))
        else:
            self.abort(401)


class AdminAddAdminHandler(webapp2.RequestHandler):
    def post(self):
        if is_admin_user():
            alias = self.request.get('alias')
            email = self.request.get('email')
            medievia.admin.administrator.create_or_update(medievia.admin.administrator.Administrator(
                    alias=alias,
                    email=email))
            medievia.admin.message.log("Added administrator: {0}.".format(alias))
        else:
            self.abort(401)


class AdminRemoveAdminHandler(webapp2.RequestHandler):
    def get(self):
        if is_admin_user():
            key = self.request.get('key')
            alias = medievia.admin.administrator.delete(key)
            medievia.admin.message.log("Removed administrator: {0}".format(alias))
            time.sleep(0.2)
            self.redirect('/admin')
        else:
            self.abort(401)


class AdminRemoveItemHandler(webapp2.RequestHandler):
    def post(self):
        #todo: need to handle deleting of the last item.
        if is_admin_user():
            url_key = self.request.get('url_key')
            item = medievia.item.item_base.get_item(url_key)

            # for logging
            deleted_item_name = item.name
            deleted_item_key = item.key.urlsafe()

            old_item_summary = item.summary_item_key.get()

            # delete the item
            item.key.delete()

            # rebuild the item summary
            new_item_summary_url_key = medievia.item.item_summary.rebuild_item_summary(old_item_summary,
                                                                                       medievia.item.item.get_all_items(
                                                                                           old_item_summary))

            medievia.admin.message.log("Removed item: {0} ({1})".format(deleted_item_name, deleted_item_key))
            return self.redirect('/item/' + new_item_summary_url_key)
        else:
            self.abort(401)


class AdminItemHandler(webapp2.RequestHandler):
    def get(self):
        if is_admin_user():
            item_key = self.request.get('item_key')
            item = medievia.item.item_base.get_item(item_key)

            template_values = {
                'is_admin_user': is_admin_user(),
                'item': item,
                'query': self.request.get('query')
            }

            template = jinja_environment.get_template('templates/admin/item.html')
            self.response.out.write(template.render(template_values))
        else:
            self.abort(401)


class SingleParseHandler(webapp2.RequestHandler):
    def get(self):
        if is_admin_user():

            template_values = {
                'is_admin_user': is_admin_user(),
                'user': users.get_current_user(),
                'signInUrl': users.create_login_url('/'),
                'signOutUrl': users.create_logout_url('/')
            }

            template = jinja_environment.get_template('templates/admin/singleParse.html')
            self.response.out.write(template.render(template_values))
        else:
            self.abort(401)


class SingleParseDoParseHandler(webapp2.RequestHandler):
    def get(self):
        if is_admin_user():
            input_string = self.request.get('input')
            item = medievia.item.parse.parse(input_string.splitlines())[0]

            self.response.write(item.to_string())
        else:
            self.abort(401)


class SingleParseUploadHandler(webapp2.RequestHandler):
    def post(self):
        if is_admin_user():
            input_string = self.request.get('input')

            # create the item via parsing
            items = medievia.item.parse.parse(input_string.splitlines())

            # create the item summary from an existing item
            item_summary = medievia.item.item_summary.create_or_update_item_summary(items[0])

            if items and items[0]:
                medievia.item.item.create_or_update_item(items[0], item_summary)
        else:
            self.abort(401)


class FileUploadHandler(webapp2.RequestHandler):
    def get(self):
        if is_admin_user():
            upload_url = blobstore.create_upload_url('/admin/fileUpload/callback')
            template_values = {
                'is_admin_user': is_admin_user(),
                'user': users.get_current_user(),
                'signInUrl': users.create_login_url('/'),
                'signOutUrl': users.create_logout_url('/'),
                'upload_url': upload_url
            }
            template = jinja_environment.get_template('templates/admin/fileupload.html')
            self.response.out.write(template.render(template_values))
        else:
            self.abort(401)


# initial input screen for direct input
class DirectParseHandler(webapp2.RequestHandler):
    def get(self):
        if is_admin_user():

            template_values = {
                'is_admin_user': is_admin_user(),
                'user': users.get_current_user(),
                'signInUrl': users.create_login_url('/'),
                'signOutUrl': users.create_logout_url('/')
            }

            template = jinja_environment.get_template('templates/admin/directParse.html')
            self.response.out.write(template.render(template_values))
        else:
            self.abort(401)


# process the input, client side will redirect to results
class DirectParseDoParseHandler(webapp2.RequestHandler):
    def post(self):
        if is_admin_user():
            input_string = self.request.get('input')
            admin_alias = medievia.admin.administrator.get(email=users.get_current_user().email()).alias

            artifact = medievia.admin.artifact.Artifact(value=input_string, submitter=admin_alias)
            artifact_key = artifact.put()

            self.response.out.write(artifact_key.urlsafe())
        else:
            self.abort(401)


class DirectParseShowResultHandler(webapp2.RequestHandler):
    def get(self, resource):
        if is_admin_user():
            resource = str(urllib.unquote(resource))
            artifact = medievia.admin.artifact.get(resource)
            if artifact:
                # parse the string
                items = medievia.item.parse.parse(artifact.value.splitlines())
                item_dicts = [x.to_dict() for x in items]

                template_values = {
                    'is_admin_user': is_admin_user(),
                    'user': users.get_current_user(),
                    'signInUrl': users.create_login_url('/'),
                    'signOutUrl': users.create_logout_url('/'),
                    'items': items,
                    'item_dicts': item_dicts
                }

                template = jinja_environment.get_template('templates/admin/fileparse.html')
                self.response.out.write(template.render(template_values))
                # else:
                # return a message saying bad key

        else:
            self.abort(401)


# blobstore calls back to the app after the file has finished uploading
class FileUploadCallbackHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        blob_info = upload_files[0]
        medievia.admin.message.log("Uploaded file: <a href='/admin/fileParse/{0}'>/admin/fileParse/{0}</a>"
                                   .format(blob_info.key()))
        self.redirect('/admin/fileParse/%s' % blob_info.key())


# the file parse page, which was redirected to by the callback
class FileParseBlobHandler(webapp2.RequestHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        blob_reader = blobstore.BlobReader(blob_info)

        if is_admin_user():
            items = medievia.item.parse.parse(blob_reader)
            item_dicts = [x.to_dict() for x in items]

            template_values = {
                'is_admin_user': is_admin_user(),
                'user': users.get_current_user(),
                'signInUrl': users.create_login_url('/'),
                'signOutUrl': users.create_logout_url('/'),
                'items': items,
                'item_dicts': item_dicts
            }

            template = jinja_environment.get_template('templates/admin/fileparse.html')
            self.response.out.write(template.render(template_values))
        else:
            self.abort(401)


# uploading items from the file parse page
class FileParseUploadHandler(webapp2.RequestHandler):
    def post(self):
        if is_admin_user():
            item_json = self.request.get('items')
            item_list = json.loads(item_json)

            # determine how many were duplicates
            new_count = 0
            dup_count = 0

            for item_properties in item_list:
                item = medievia.item.item.Item(**item_properties)
                item_summary = medievia.item.item_summary.create_or_update_item_summary(item)
                if medievia.item.item.create_or_update_item(item, item_summary):
                    new_count += 1
                else:
                    dup_count += 1

            # return the response with counts
            self.response.out.write("Number of new items: {0}\nNumber of duplicates: {1}".format(new_count, dup_count))
            medievia.admin.message.log("Uploaded new items: {0} (new); {1} (duplicates)".format(new_count, dup_count))
        else:
            self.abort(401)


class RemoteItemUploadHandler(webapp2.RequestHandler):
    def post(self):
        if is_admin_user(self.request.remote_addr):
            try:
                # get the post body
                blobdata = (x.group(0) for x in re.finditer('(.*\n|.+$)', self.request.get('itemdata')))

                # run it through the item parser
                items = medievia.item.parse.parse(blobdata)

                new_count = 0
                dup_count = 0

                # for each item create an item summary and upload to database
                for item in items:
                    item_summary = medievia.item.item_summary.create_or_update_item_summary(item)
                    if medievia.item.item.create_or_update_item(item, item_summary):
                        new_count += 1
                    else:
                        dup_count += 1

                medievia.admin.message.log("Uploaded new items: {0} (new); {1} (duplicates)".format(new_count, dup_count))
            except Exception as e:
                logging.exception(e.message)
                self.abort(400)


class ToolsXPXPHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'is_admin_user': is_admin_user(),
            'user': users.get_current_user(),
            'signInUrl': users.create_login_url('/'),
            'signOutUrl': users.create_logout_url('/')
        }
        template = jinja_environment.get_template('templates/tools/xpxp.html')
        self.response.out.write(template.render(template_values))


class CalculateXPXPHandler(webapp2.RequestHandler):
    def get(self):
        moon = self.request.get('moon')
        eclipse = self.request.get('eclipse')
        full_text = self.request.get('full_text')

        self.response.write(json.dumps(medievia.xpxp.parse(moon, eclipse, full_text)))


class ToolsAutoQuestHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'is_admin_user': is_admin_user(),
            'user': users.get_current_user(),
            'signInUrl': users.create_login_url('/'),
            'signOutUrl': users.create_logout_url('/')
        }
        template = jinja_environment.get_template('templates/tools/autoquest.html')
        self.response.out.write(template.render(template_values))


class ToolsCTMapHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'is_admin_user': is_admin_user(),
            'user': users.get_current_user(),
            'signInUrl': users.create_login_url('/'),
            'signOutUrl': users.create_logout_url('/')
        }
        template = jinja_environment.get_template('templates/tools/ct_map.html')
        self.response.out.write(template.render(template_values))


class MailHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender)


def is_admin_user(remote_ip=''):
    try:
        user = users.get_current_user()
        if user:
            email = user.email()
            return medievia.admin.administrator.is_admin(email) or users.is_current_user_admin()
        else:
            # check to see if the user is coming from a trusted IP address
            if remote_ip == '191.233.89.94' or remote_ip == '127.0.0.1':
                return True
            return False
    except Exception as e:
        print e
        return False


app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/search', SearchHandler),
    ('/browse', BrowseHandler),
    ('/item/([^/]+)', ItemHandler),
    ('/tools/xpxp', ToolsXPXPHandler),
    ('/tools/xpxp/calculate', CalculateXPXPHandler),
    ('/tools/autoquest', ToolsAutoQuestHandler),
    ('/tools/ctmap', ToolsCTMapHandler),

    ('/admin', AdminHandler),
    ('/admin/addadmin', AdminAddAdminHandler),
    ('/admin/removeadmin', AdminRemoveAdminHandler),
    ('/admin/removeitem', AdminRemoveItemHandler),

    # Parse - single item
    ('/admin/singleParse', SingleParseHandler),
    ('/admin/singleParse/doParse', SingleParseDoParseHandler),
    ('/admin/singleParse/upload', SingleParseUploadHandler),

    # Parse - direct
    ('/admin/parse/direct', DirectParseHandler),
    ('/admin/parse/direct/doParse', DirectParseDoParseHandler),
    ('/admin/parse/direct/([^/]+)', DirectParseShowResultHandler),

    # Parse - file
    ('/admin/fileUpload', FileUploadHandler),
    ('/admin/fileUpload/callback', FileUploadCallbackHandler),
    ('/admin/fileParse/upload', FileParseUploadHandler),
    ('/admin/fileParse/([^/]+)?', FileParseBlobHandler),

    # Remote - item upload
    ('/remote/upload', RemoteItemUploadHandler),

    ('/admin/item', AdminItemHandler)], debug=True)
