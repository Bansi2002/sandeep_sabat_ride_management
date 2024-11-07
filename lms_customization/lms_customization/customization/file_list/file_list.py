import frappe
from lms_customization.lms_customization.customization.file_list.doc_events.utility import insert_files, delete_files

def insert_file(self, method=None):
    insert_files(self, method)

def delete(doc, method=None):
    delete_files(doc, method)