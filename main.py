import webapp2
import jinja2
import os
import time
from google.appengine.api import users
from collections import defaultdict
import medievia.parse
import medievia.item
import medievia.search
import medievia.admin
jinja_environment = jinja2.Environment(autoescape=True,
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__))))

# todo: add auto-complete in search bar
# re: http://blog.startuptale.com/2012/10/partial-search-on-gae-with-search-api.html
# re: http://stackoverflow.com/questions/10960384/google-app-engine-python-search-api-string-search


class HomeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/home.html')
        template_values = {
            'is_admin_user': is_admin_user()
        }
        self.response.out.write(template.render(template_values))


class SearchHandler(webapp2.RequestHandler):
    def get(self):
        query = self.request.get('q')
        if query:
            items = medievia.search.run_search(query)

        # flat list
        if self.request.get('style') == 'flatlist':
            template_values = {
                'is_admin_user': is_admin_user(),
                'items': items,
                'query': query
            }
            template = jinja_environment.get_template('templates/search_flat.html')

        # grouped by item name
        else:
            grouped_items = defaultdict(list)
            for item in items:
                grouped_items[item.name].append(item)
            #grouped_items = {item.name: item for item in items}
            template_values = {
                'is_admin_user': is_admin_user(),
                'grouped_items': grouped_items,
                'query': query
            }
            template = jinja_environment.get_template('templates/search.html')

        self.response.out.write(template.render(template_values))


class AdminHandler(webapp2.RequestHandler):
    def get(self):
        if is_admin_user():
            template_values = {
                'admins': medievia.admin.get()
            }

            template = jinja_environment.get_template('templates/admin/admin.html')
            self.response.out.write(template.render(template_values))
        else:
            self.abort(401)


class AdminUpdateIndexesHandler(webapp2.RequestHandler):
    def post(self):
        if is_admin_user():
            medievia.search.update_indexes()
        else:
            self.abort(401)


class AdminAddAdminHandler(webapp2.RequestHandler):
    def post(self):
        if is_admin_user():
            alias = self.request.get('alias')
            email = self.request.get('email')
            medievia.admin.create_or_update(medievia.admin.Admin(alias=alias, email=email))
        else:
            self.abort(401)


class AdminRemoveAdminHandler(webapp2.RequestHandler):
    def get(self):
        if is_admin_user():
            key = self.request.get('key')
            medievia.admin.delete(key)
            time.sleep(0.2)
            self.redirect('/admin')
        else:
            self.abort(401)


class AdminItemHandler(webapp2.RequestHandler):
    def get(self):
        if is_admin_user():
            item_key = self.request.get('item_key')
            item = medievia.item.get_item(item_key)

            template_values = {
                'is_admin_user': is_admin_user(),
                'item': item,
                'query': self.request.get('query')
            }

            template = jinja_environment.get_template('templates/admin/item.html')
            self.response.out.write(template.render(template_values))
        else:
            self.abort(401)


class ParseHandler(webapp2.RedirectHandler):
    def get(self):
        if is_admin_user():
            template = jinja_environment.get_template('templates/admin/parse.html')
            self.response.out.write(template.render())
        else:
            self.abort(401)


class ParseDoParseHandler(webapp2.RequestHandler):
    def get(self):
        if is_admin_user():
            input_string = self.request.get('input')
            output_type = self.request.get('type')
            item = medievia.parse.parse(input_string)

            if output_type == "xml":
                self.response.write(item.to_xml())
            else:
                self.response.write(item.to_string())
        else:
            self.abort(401)


class ParseUploadHandler(webapp2.RequestHandler):
    def post(self):
        if is_admin_user():
            input_string = self.request.get('input')
            item = medievia.parse.parse(input_string)
            medievia.item.create_or_update_item(item)
        else:
            self.abort(401)


def is_admin_user():
    try:
        user = users.get_current_user()
        if user:
            email = user.email()
            return medievia.admin.is_admin(email) or users.is_current_user_admin()
        else:
            return False
    except:
        return False


app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/search', SearchHandler),
    ('/admin', AdminHandler),
    ('/admin/updateIndexes', AdminUpdateIndexesHandler),
    ('/admin/addadmin', AdminAddAdminHandler),
    ('/admin/removeadmin', AdminRemoveAdminHandler),
    ('/admin/parse', ParseHandler),
    ('/admin/parse/doParse', ParseDoParseHandler),
    ('/admin/parse/upload', ParseUploadHandler),
    ('/admin/item', AdminItemHandler)], debug=True)


