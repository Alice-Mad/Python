from requests.auth import HTTPBasicAuth
import requests
import json
import urllib3

# !!! import dpath
# from easygui import passwordbox
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(IncureRequestWarning)


def bbapi_getjson(dir_name: str, mdl_name: str, commit_first: str, commit_second: str,
                  mdl_number: str, username: str, password: str) -> str:
    """Функция даёт запрос в BitBucket, позволяющий получить информацию об изменения,
    введённых в ПО от одной до другой версии, в то числе коммиты и номер ишью"""
    urllib3.disable_warnings()

    while True:

        BITBUCKET_URL = "https://spb-bitbucket.spb.rpkb.ru/rest/api/1.0"
        BITBUCKET_AUTH = HTTPBasicAuth(username, password)
        BITBUCKET_HEADERS = {"content-type": "application/json"}

        url = f"https://spb-bitbucket.spb.rpkb.ru/rest/api/1.0/projects/{dir_name}/repos/{mdl_name}" \
              f"/commits?followRenames=false&" \
              f"ignoreMissing=true&merges=only&" \
              f"since={commit_first}&until={commit_second}&withCounts=true"

        response = requests.get(url,
                                verify=False,
                                params={
                                    "pagalen": 100
                                },
                                auth=BITBUCKET_AUTH,
                                headers=BITBUCKET_HEADERS)
        response.encoding = "utf-8"

        my_json = response.json()
        if my_json == {'errors': [{'context': None, 'message': 'Authentication failed.'
                                                               ' Please check your credentials and try again.',
                                   'exceptionName': 'com.atlassian.bitbucket.'
                                                    'auth.IncorrectPasswordAuthenticationException'}]}:
            print("Login и/или password неверны")
        else:
            break

    with open(f"C:/python_test/merge_module{mdl_number}.json", mode="w", encoding="utf-8") as outfile:
        json.dump(my_json, outfile, indent=4, ensure_ascii=False)
    outfile.close()
    filename = f"merge_module{mdl_number}.json"
    return filename
