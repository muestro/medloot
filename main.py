import webapp2
import jinja2
import os
import test
from google.appengine.api import users
from collections import defaultdict
import medievia.parse
import medievia.item
import medievia.search
jinja_environment = jinja2.Environment(autoescape=True,
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__))))

# todo: add auto-complete in search bar
# re: http://blog.startuptale.com/2012/10/partial-search-on-gae-with-search-api.html
# re: http://stackoverflow.com/questions/10960384/google-app-engine-python-search-api-string-search


class HomeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/home.html')
        template_values = {
            'is_admin_user': users.is_current_user_admin()
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
                'is_admin_user': users.is_current_user_admin(),
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
                'is_admin_user': users.is_current_user_admin(),
                'grouped_items': grouped_items,
                'query': query
            }
            template = jinja_environment.get_template('templates/search.html')

        self.response.out.write(template.render(template_values))


class ParseHandler(webapp2.RedirectHandler):
    def get(self):
        template = jinja_environment.get_template('templates/parse.html')
        self.response.out.write(template.render())


class ParseDoParseHandler(webapp2.RequestHandler):
    def get(self):
        input_string = self.request.get('input')
        output_type = self.request.get('type')
        item = medievia.parse.parse(input_string)

        if output_type == "xml":
            self.response.write(item.to_xml())
        else:
            self.response.write(item.to_string())


class ParseUploadHandler(webapp2.RequestHandler):
    def post(self):
        input_string = self.request.get('input')
        item = medievia.parse.parse(input_string)
        medievia.item.create_or_update_item(item)


class RunTestHandler(webapp2.RequestHandler):
    def get(self):
        test.run_test()
        self.response.write("worked")


class AdminHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/admin.html')
        self.response.out.write(template.render())


class AdminUpdateIndexesHandler(webapp2.RequestHandler):
    def post(self):
        medievia.search.update_indexes()


app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/search', SearchHandler),
    ('/admin', AdminHandler),
    ('/admin/updateIndexes', AdminUpdateIndexesHandler),
    ('/admin/parse', ParseHandler),
    ('/admin/parse/doParse', ParseDoParseHandler),
    ('/admin/parse/upload', ParseUploadHandler)], debug=True)


