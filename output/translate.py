import requests
import json


def translate(iam_token, target_lang, text):
    folder_id = 'b1gv1soaclkl271kvsbu'

    body = {
        "targetLanguageCode": target_lang,
        "texts": text,
        "folderId": folder_id,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(iam_token)
    }

    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                             json=body,
                             headers=headers
                             )

    return json.loads(response.text)['translations'][0]['text']
