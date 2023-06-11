import grpc

import yandex.cloud.ai.stt.v3.stt_pb2 as stt_pb2
import yandex.cloud.ai.stt.v3.stt_service_pb2_grpc as stt_service_pb2_grpc


CHUNK_SIZE = 4000


def gen(audio_file_name):
    # Задать настройки распознавания.
    recognize_options = stt_pb2.StreamingOptions(
        recognition_model=stt_pb2.RecognitionModelOptions(
            audio_format=stt_pb2.AudioFormatOptions(
                raw_audio=stt_pb2.RawAudio(
                    audio_encoding=stt_pb2.RawAudio.LINEAR16_PCM,
                    sample_rate_hertz=8000,
                    audio_channel_count=1
                )
            ),
            # Задать автоматическое распознавание языков.
            language_restriction=stt_pb2.LanguageRestrictionOptions(
                restriction_type=stt_pb2.LanguageRestrictionOptions.WHITELIST,
                language_code=['auto']
            ),
        )
    )

    # Отправить сообщение с настройками распознавания.
    yield stt_pb2.StreamingRequest(session_options=recognize_options)

    # Прочитать аудиофайл и отправить его содержимое порциями.
    f = open(audio_file_name, 'rb')
    data = f.read(CHUNK_SIZE)
    for i in range(250):
        if data == b'':
            break
        yield stt_pb2.StreamingRequest(chunk=stt_pb2.AudioChunk(data=data))
        data = f.read(CHUNK_SIZE)


def run(iam_token, audio_file_name):
    prob = dict.fromkeys(['ru-RU', 'en-US'], 0)
    # Установить соединение с сервером.
    cred = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel('stt.api.cloud.yandex.net:443', cred)
    stub = stt_service_pb2_grpc.RecognizerStub(channel)

    # Отправить данные для распознавания.
    it = stub.RecognizeStreaming(gen(audio_file_name), metadata=(
        ('authorization', f'Bearer {iam_token}'),
    ))

    # Обработать ответы сервера и вывести результат в консоль.
    try:
        for r in it:
            event_type, alternatives = r.WhichOneof('Event'), None
            if event_type == 'final':
                # получение языковых меток:
                langs = [a.languages for a in r.final.alternatives]
            # вывод в консоль языковых меток для финальных версий:
            if event_type == 'final':
                for lang in langs:
                    for line in lang:
                        words = f'{line}'.splitlines()
                        if words[0].find('ru-RU') != -1:
                            for word in words:
                                if word.find('probability') == -1:
                                    continue
                                else:
                                    prob['ru-RU'] += float(word[13:])
                        elif words[0].find('en-US') != -1 or words[0].find('en-EN') != -1:
                            for word in words:
                                if word.find('probability') == -1:
                                    continue
                                else:
                                    prob['en-US'] += float(word[13:])
        if prob['ru-RU'] > prob['en-US']:
            return 'ru-RU'
        else:
            return 'en-US'
    except grpc._channel._Rendezvous as err:
        print(f'Error code {err._state.code}, message: {err._state.details}')
        raise err
