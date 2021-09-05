import requests
import webbrowser
import click

from settings import APP_KEY, APP_SECRET


class AuthDropbox:
    """Class for authorize accounts"""
    app_key = APP_KEY
    app_secret = APP_SECRET
    authorization_url = f'https://www.dropbox.com/oauth2/authorize?client_id={app_key}&token_access_type=offline&response_type=code'

    def get_token(self):
        """function for get token for API"""
        authorization_code = self.get_autorization_code()

        token_url = "https://api.dropboxapi.com/oauth2/token"
        params = {
            "code": authorization_code,
            "grant_type": "authorization_code",
            "client_id": self.app_key,
            "client_secret": self.app_secret
        }
        r = requests.post(token_url, data=params)
        return r.json()['access_token']

    def get_autorization_code(self):
        webbrowser.open(self.authorization_url)
        authorization_code = input('Enter the code:\n')
        return authorization_code


class WorkWithFilesDropbox:
    """Class for upload adn download files on dropbox"""
    auth = AuthDropbox()
    access_token = 'Bearer ' + str(auth.get_token())

    def download_files(self, src_path: str, dst_path: str):
        download_url = "https://content.dropboxapi.com/2/files/download"
        headers = {
            "Authorization": self.access_token,
            "Dropbox-API-Arg": "{\"path\":\"/%s\"}" % src_path
        }
        with open(dst_path, 'w') as f:
            r = requests.post(download_url, headers=headers)
            f.write(r.text.replace('\n', ''))

    def upload_file(self, src_path: str, dst_path: str):
        upload_url = "https://content.dropboxapi.com/2/files/upload"

        headers = {
            "Authorization": self.access_token,
            "Content-Type": "application/octet-stream",
            "Dropbox-API-Arg": "{\"path\":\"%s\"}" % dst_path
        }
        data = open(src_path, "rb").read()
        requests.post(upload_url, headers=headers, data=data)


@click.command(name='testool')
@click.argument('method')
@click.argument('src_path')
@click.argument('dst_path')
def main(method, src_path, dst_path):
    d = WorkWithFilesDropbox()
    if method == 'get':
        d.download_files(src_path, dst_path)
    elif method == 'put':
        d.download_files(src_path, dst_path)
    else:
        print('Missing argument "method"')


if __name__ == '__main__':
    # a = AuthDropbox()
    main()

    # d.upload_file('upload.txt',
    #               'upload/test.txt')
    # # print(a.get_token())
    # # requests.get('https://content.dropboxapi.com/2/files/upload')
