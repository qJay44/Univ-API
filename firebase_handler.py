import firebase_admin
from config import FIREBASE_KEY
from firebase_admin import credentials
from firebase_admin import firestore


class FirebaseHandler:

    def __init__(self):
        cred = credentials.Certificate(f'{FIREBASE_KEY}.json')
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def addData(self, coll, doc, data):
        """
        Parameters:
            @coll - firestore collection
            @doc  - firestore collection document
            @data - data to set in firestore
        """

        doc_ref = self.db.collection(coll).document(doc)
        doc_ref.set(data)

    def readData(self, coll):
        coll_ref = self.db.collection(coll)
        docs = coll_ref.stream()

        result = {}
        for doc in docs:
            result[doc.id] = doc.to_dict()

        return result

