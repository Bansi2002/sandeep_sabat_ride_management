import frappe
import requests
import os
import json

def insert_files(self, method=None):
    try:
        file_hosting_records = frappe.get_doc('File Hosting')
        docSettings = frappe.get_single("File Hosting")
        source = docSettings.get_password('secret_key')
        target = docSettings.get_password('target_key')
        file_hosting_records.secret_key = source
        file_hosting_records.target_key = target
        if not self.file_url or (self.file_url).startswith(file_hosting_records.target_url):
            pass
        else:
            try: 
                download_result = transfer_file(self.file_url, file_hosting_records)
                if download_result["status"] == "error":
                    return download_result
                upload_file_to_target(download_result["content"], download_result["filename"], self.is_private, self, file_hosting_records)
                delete_file_from_source(self.file_url, self.is_private, file_hosting_records)
                frappe.db.set_value('File', self.name, 'file_url', file_hosting_records.target_url + self.file_url)
            except Exception as e:
                frappe.log_error(message=frappe.get_traceback(), title="File Hosting Error")
    except Exception as err:
        frappe.log_error(message=frappe.get_traceback(), title="File Hosting Error")

def transfer_file(file_url, file_hosting_records):
    try:
        source_site = {
            'url': file_hosting_records.source_url,
            'user': file_hosting_records.user_id,
            'password': file_hosting_records.secret_key
        }
        
        auth_response = requests.post(
            f"{source_site['url']}/api/method/login",
            data={'usr': source_site['user'], 'pwd': source_site['password']}
        )
        auth_response.raise_for_status()

        file_response = requests.get(f"{source_site['url']}{file_url}", cookies=auth_response.cookies)
        file_response.raise_for_status()
        file_content = file_response.content

        return {"status": "success", "content": file_content, "filename": file_url.split("/")[-1]}

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}


def upload_file_to_target(file_content, filename, private, self, file_hosting_records):
    try:
        target_site = {
            'url': file_hosting_records.target_url,
            'user': file_hosting_records.target_id,
            'password': file_hosting_records.target_key
        }

        auth_response = requests.post(
            f"{target_site['url']}/api/method/login",
            data={'usr': target_site['user'], 'pwd': target_site['password']}
        )
        auth_response.raise_for_status()
        upload_response = requests.post(
            f"{target_site['url']}/api/method/upload_file",
            files={'file': (filename, file_content)},
            cookies=auth_response.cookies,
            data={'is_private': private, 'folder': self.folder, 'doctype':self.attached_to_doctype, 'docname':self.attached_to_name}
        )
        upload_response.raise_for_status()

        return {"status": "success", "message": "File uploaded successfully"}

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}
    
def delete_file_from_source(file_url, private, file_hosting_records):
    try:
        source_site = {
            'url': file_hosting_records.source_url,
            'user': file_hosting_records.user_id,
            'password': file_hosting_records.secret_key
        }

        auth_response = requests.post(
            f"{source_site['url']}/api/method/login",
            data={'usr': source_site['user'], 'pwd': source_site['password']}
        )
        auth_response.raise_for_status()
        if private:
            file_path = frappe.get_site_path("private", 'files', file_url.split('/')[-1])
        else:
            file_path = frappe.get_site_path("public", 'files', file_url.split('/')[-1])

        if os.path.exists(file_path):
            os.remove(file_path)
        

        return {"status": "success", "message": "File deleted successfully"}

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}
