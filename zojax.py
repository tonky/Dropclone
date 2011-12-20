import os
from urllib import urlencode, quote as urlquote, unquote_plus as unquote

import jinja2
import webapp2

from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers, RequestHandler
from google.appengine.ext.webapp import template


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class UpFile(db.Model):
    name = db.StringProperty(required=True)
    # owner = db.UserProperty()
    uploaded = db.DateTimeProperty()
    content = db.ByteStringProperty()
    size = db.IntegerProperty()
    blob_key = blobstore.BlobReferenceProperty()
    blob_key_string = db.StringProperty()
    ct = db.StringProperty()


class DelFile(webapp2.RequestHandler):
    def post(self, blob_key_string):
        upfile = UpFile.gql("WHERE blob_key_string = '%s'" % blob_key_string).get()

        blob_info = blobstore.BlobInfo.get(upfile.blob_key_string)
        blob_info.delete()
        upfile.delete()
        self.redirect('/')


class GetFile(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        # self.send_blob(blob_info)
        self.send_blob(blobstore.BlobInfo.get(blob_info.key()), save_as=True)


class UploadFile(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file_upload')
        blob_info = upload_files[0]

        upfile = UpFile(name=blob_info.filename)

        upfile.uploaded = blob_info.creation
        upfile.size = blob_info.size
        upfile.blob_key = blob_info.key()
        upfile.blob_key_string = str(blob_info.key())
        upfile.ct = blob_info.content_type

        upfile.put()

        self.redirect('/')


class MainPage(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload')

        files = db.GqlQuery("SELECT * "
                            "FROM UpFile "
                            "ORDER BY uploaded DESC")

        template_values = {
                'files': files,
                'upload_url': upload_url,
                'url_linktext': "asdfsdf",
                "nickname": False
                }

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/upload', UploadFile),
    ('/get/([^/]+)?', GetFile),
    ('/del/([^/]+)?', DelFile),
], debug=True)
