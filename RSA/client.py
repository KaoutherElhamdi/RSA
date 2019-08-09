# coding=utf-8
import socket
import pickle


def encrypt(pk, plaintext):
    #Déballez la clé dans ses composants
    key, n = pk[0],pk[1]
    #Convertissez chaque lettre du texte en texte clair en nombres basés sur le caractère en utilisant a ^ b mod m
    cipher=[(ord(char) ** key) % n for char in plaintext]
    #Renvoie le tableau d'octets
    return cipher

if __name__=='__main__':
    print("je suis le client")
    hote = "localhost"
    port = 12800
    connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_avec_serveur.connect((hote, port))
    print("Connexion établie avec le serveur sur le port {}".format(port))

    #le client reçoit le clé publique (e,n) du serveur
    e = connexion_avec_serveur.recv(1024)
    e = int(e.decode())

    n = connexion_avec_serveur.recv(1024)
    n = int(n.decode())
    public=(e,n)
    print("Clé publique est : (e,n) = ({},{})".format(e,n))

    message = input("Entrez un message à chiffrer avec votre clé publique: ")
    encrypted_msg = encrypt(public, message)

    print("message crypté")
    print(''.join(map(lambda x: str(x), encrypted_msg)))

    #le client envoie le message crypté au serveur
    enc = pickle.dumps(encrypted_msg)
    connexion_avec_serveur.send(enc)

    print("Fermeture de la connexion")
    connexion_avec_serveur.close()
