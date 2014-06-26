import os
import time
import urllib
import json
from collections import defaultdict

import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

import medievia.item.parse
import medievia.item.item
import  medievia.item.item_summary
import medievia.search
import medievia.admin.administrator
import medievia.admin.message
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
        grouped_items = defaultdict(list)
        template_values = {
            'is_admin_user': is_admin_user(),
            'user': users.get_current_user(),
            'signInUrl': users.create_login_url('/'),
            'signOutUrl': users.create_logout_url('/'),
            'grouped_items': grouped_items,
            'query': query
        }

        if query:
            items = medievia.search.run_search(query)

            for item in items:
                if item is not None:
                    grouped_items[item.name].append(item)

        template = jinja_environment.get_template('templates/search.html')
        self.response.out.write(template.render(template_values))


class SearchHandler2(webapp2.RequestHandler):
    def get(self):
        query = self.request.get('q')

        if query:
            items = medievia.search.run_new_search(query)

        template_values = {
            'is_admin_user': is_admin_user(),
            'user': users.get_current_user(),
            'signInUrl': users.create_login_url('/'),
            'signOutUrl': users.create_logout_url('/'),
            'items': items,
            'query': query
        }

        template = jinja_environment.get_template('templates/search2.html')
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


class AdminUpdateIndexesHandler(webapp2.RequestHandler):
    def post(self):
        if is_admin_user():
            medievia.search.update_indexes()
            medievia.admin.message.log("Index has been updated.")
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


class AdminItemHandler(webapp2.RequestHandler):
    def get(self):
        if is_admin_user():
            item_key = self.request.get('item_key')
            item = medievia.item.item.get_item(item_key)

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

            template = jinja_environment.get_template('templates/admin/singleparse.html')
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


# upload file
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


class ToolsHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'is_admin_user': is_admin_user(),
            'user': users.get_current_user(),
            'signInUrl': users.create_login_url('/'),
            'signOutUrl': users.create_logout_url('/')
        }
        template = jinja_environment.get_template('templates/tools/tools.html')
        self.response.out.write(template.render(template_values))


class CalculateXPXPHandler(webapp2.RequestHandler):
    def get(self):
        moon = self.request.get('moon')
        eclipse = self.request.get('eclipse')
        full_text = self.request.get('full_text')

        self.response.write(json.dumps(medievia.xpxp.parse(moon, eclipse, full_text)))


def is_admin_user():
    try:
        user = users.get_current_user()
        if user:
            email = user.email()
            return medievia.admin.administrator.is_admin(email) or users.is_current_user_admin()
        else:
            return False
    except Exception as e:
        print e
        return False

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/search', SearchHandler),
    ('/search2', SearchHandler2),
    ('/tools', ToolsHandler),
    ('/tools/xpxp/calculate', CalculateXPXPHandler),

    ('/admin', AdminHandler),
    ('/admin/updateIndexes', AdminUpdateIndexesHandler),
    ('/admin/addadmin', AdminAddAdminHandler),
    ('/admin/removeadmin', AdminRemoveAdminHandler),

    # Parse - single item
    ('/admin/singleParse', SingleParseHandler),
    ('/admin/singleParse/doParse', SingleParseDoParseHandler),
    ('/admin/singleParse/upload', SingleParseUploadHandler),

    # Parse - file
    ('/admin/fileUpload', FileUploadHandler),
    ('/admin/fileUpload/callback', FileUploadCallbackHandler),
    ('/admin/fileParse/upload', FileParseUploadHandler),
    ('/admin/fileParse/([^/]+)?', FileParseBlobHandler),

    ('/admin/item', AdminItemHandler)], debug=True)
