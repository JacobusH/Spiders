# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class ArtistryPipeline(object):

    def __init__(self):
        # cred = credentials.Certificate('firestoreCreds.json')
        self.cred = credentials.Certificate(
          {
            "type": "service_account",
            "project_id": "crawl-63a5c",
            "private_key_id": "5a626166009f871025b41c104b94f6bcc5658ce9",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDJ2t0VqY/JAhYA\nxTQ8SuKAIw2T4uSov5b18fwb5Ps8eVqavcAkGqUBHH8G3LSj3v99PsWA2JTh7Wf4\nbD9SZCCRYbXMRZYRAAJy2NjBwu+tR00HBloZseWpcbGkBCgntLdKWFwPECh8/oVA\nz6npZLUnnH6onPKWLK2UzcjKjTvbV+DiG8aIZmCWuxWl3HvHUAUFZhSrfrniolkA\nb4FgldGXcFtjex/qaYn5O2bmBLHqGX2xBT14rKKdUthxSh4YVvZe2FQUccP8pZRz\npBe5HS9AltJTpSkMcEi009W82IX9KzH6xmZtwvzRXEUD2zgWK8Kcgp9Fq67ITzl/\nzFCk16grAgMBAAECggEATdwVESkBZDhgwlVOy77a1TAwKY4IQyr7kMyRQTU2z2HD\n2BI/De4VHXOfb8csClWW2Pmgdw2Th/3p78HZPu+OPGWjGTLyKoaFa0VHfp2xk3YA\nOShzEpwzCQPo0GomDwK+/HdOsyS5aVVHkvNHB9anparQlDtNuy1qmw4xWCfYIcd5\ncTYrqvlK9ABLoluyhKhPGToqdi76qOo1yBEGeYKJvuHqoYK7+Yeg90ITYbeapH6+\nxO0MvJ0CANOIDgdajl9ZbymTScYtK9EBUAUueSn8Xf4weke4gUEk1Nm5Iqv5AtBx\nPSPb6PtJ+gGisD3bCrLi41xRcSYVWNf1BdD+PdcgiQKBgQDpkpHz+qt9XPDmrIOu\nMoVcCU+lw8PkSPVUZBE65F77bRKTtbUaFQQk2UbgjKmOF2ojYFwm76+u19gQID5f\n89AIIS2hp1fMtv45DzAjJU9LGgwALEodxuY4eehoe6IAKa2EsaVHzJg8ek1a9gI9\nwih2s+DrCiud17jDumWnpjnT5QKBgQDdPKU1Abb6tQ2Kr/5pLcBX2h56KbFJRZKU\nXEv7A3W+KQhx4PEEXMw/8I97Pel7LWYH3+iT1vVUm3esuZpTIjV9y7pedbb8Ppfs\nE4shjDwZCKwSuo84bZhXcXKkc/K0oAVgwAoXIx/isBQP1s/hhYZAshXsXI890sVU\nPjIMxG7qzwKBgQCgTA/QojrpCUzm8oRYm6F8fYNk3wpkdFGx/g75HNu2r69tIepN\nIRk79MW4u7BtrNIRv0LfEeW/F7DXuFk2Xsxpl+OKKp+OBhRIsoy1whg+EX0k7UBc\nWTGMltWSRy7x76h/Ba/Jq7ba4pCOGYGGQuakOGTmyY8Pf4n1AcpcGS9cpQKBgQCv\nHE5ja00KmX3zdSP42kaxAqs25IM3zMKdfYSCVRXAAzh08qeyXUUpot3enX2NiryE\npRywz+b1Je0OoQXeoWgXfsav95pzg5O6PynTzuzOn8ebN2EfN9fp9pjYRBIqF7LK\nBpa2A448XkQy2UNHbOl7kbm6kPSr6YVZDbWN13k3jwKBgEMuJ6IFo73BpPR1e1ha\neeqMNvnYiUcfPUy/vguqlA9n7ahvuG3KM9Cy96dETARvqHtH/xDqZ25qxGm43nW+\ncUquxq8etBqvj9LMGU0d8PpkIdmmSj4ujwhBN2S1tkENKvG6AtgVV6Ot2U6pXLT5\nJbnK/9f7z3Etjtl91qQIg5Xj\n-----END PRIVATE KEY-----\n",
            "client_email": "crawl-63a5c@appspot.gserviceaccount.com",
            "client_id": "101537549869813096218",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://accounts.google.com/o/oauth2/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/crawl-63a5c%40appspot.gserviceaccount.com"
          }
        )
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()

    def process_item(self, item, spider):
        doc_ref = self.db.collection(u'artists').document(u'test')
        doc_ref.set({
            u'first': u'Ada',
            # u'last': u'Lovelace',
            # u'born': 1815
        })
        return item
