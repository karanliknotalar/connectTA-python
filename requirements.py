import importlib


def check_req():
    result = False
    try:
        importlib.import_module('requests')
        requests_installed = True
        result = True
    except ImportError:
        requests_installed = False

    try:
        importlib.import_module('bs4')
        beautifulsoup_installed = True
        result = True
    except ImportError:
        beautifulsoup_installed = False

    if not requests_installed:
        try:
            import subprocess

            subprocess.check_call(['pip', 'install', 'requests'])
            importlib.import_module('requests')
            result = True
        except Exception as e:
            print(f'Requests paketi yüklenirken bir hata oluştu: {str(e)}')

    if not beautifulsoup_installed:
        try:
            import subprocess

            subprocess.check_call(['pip', 'install', 'beautifulsoup4'])
            importlib.import_module('bs4')
            result = True
        except Exception as e:
            print(f'BeautifulSoup paketi yüklenirken bir hata oluştu: {str(e)}')

    return result
