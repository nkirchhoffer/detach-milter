import Milter
import ipfsapi

# Connectez-vous au daemon IPFS
api = ipfsapi.Client()

class RemoveAttachments(Milter.Base):
    def __init__(self):
        self.signature = "-- \nPièces jointes hébergées sur IPFS :"

    def addheader(self, name, value, mode=None):
        if name.lower() == "to":
            # Réinitialisez la signature avant de traiter chaque courriel
            self.signature = "-- \nPièces jointes hébergées sur IPFS :"

    def eom(self):
        # Récupérez toutes les pièces jointes du courriel
        attachments = self.fp.get_attachments()

        # Pour chaque pièce jointe, hébergez-la sur IPFS et ajoutez un lien à la signature
        for attachment in attachments:
            # Hébergez la pièce jointe sur IPFS
            results = api.add(attachment)
            # Ajoutez un lien vers la pièce jointe dans la signature
            self.signature += f"\n- {attachment.name}: https://ipfs.io/ipfs/{results['Hash']}"

        # Ajoutez la signature au bas du courriel
        self.current.add_signature(self.signature)
        return Milter.CONTINUE

Milter.factory = RemoveAttachments
Milter.runmilter("detach", "./milter.sock", 600)