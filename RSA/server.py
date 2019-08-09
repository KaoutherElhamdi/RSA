# coding=utf-8
import socket
import pickle
import random
from Crypto.Util import number
import time
'''
Algorithme d'Euclide pour déterminer le plus grand commun diviseur
Utilisez l'itération pour accélérer les grands entiers
'''
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a
'''Algorithme étendu d'Euclid pour trouver l'inverse multiplicatif de deux nombres'''
def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2- temp1* x1
        y = d - temp1 * y1
        
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if temp_phi == 1:
        return d + phi
'''Des tests pour voir si un nombre est premier.'''
def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Les deux nombres doivent être premiers.')
    elif p == q:
        raise ValueError('p et q ne peuvent pas être égaux')
    #n = pq
    n = p * q

    #Phi est le total de n
    phi = (p-1) * (q-1)

    #Choisissez un entier a tel que e et phi (n) soient coprimes
    e = random.randrange(1, phi)

    #Utilisez l'algorithme d'Euclid pour vérifier que e et phi (n) sont coprimes
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    #Utiliser l'algorithme d'Euclid étendu pour générer la clé privée
    d = multiplicative_inverse(e, phi)
    
    #Retour de la paire de clés publique et privée
    #La clé publique est (e, n) et la clé privée est (d, n)
    return ((e, n), (d, n))

def decrypt(pk, ciphertext):
    #Déballez la clé dans ses composants
    key, n = pk[0],pk[1]
    #Générez le texte en clair en fonction du texte chiffré et de la clé à l'aide de a ^ b mod m
    plain = [chr((int(elt) ** key) % n) for elt in ciphertext]
    #Renvoie le tableau d'octets sous forme de chaîne
    return ''.join(plain) 

if __name__=='__main__':
    start= time.time()
    print("je suis le serveur")
    hote = ''
    port = 12800
    connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_principale.bind((hote, port))
    connexion_principale.listen(5)
    print("Le serveur écoute à présent sur le port {}".format(port))
    connexion_avec_client, infos_connexion = connexion_principale.accept()
    #Ici soit on donne le choix des nombres premiers p et q au utilisateur tout en vérifiant
    #si les 2 valeurs donnés sont premiers ou pas (gràce à la fonction is_prime )
    #Soit on les générent automatiquement avec la fonction number.getprime(n_bits)
    #p = int(input("Entrez un nombre premier (17, 19, 23, etc): "))
    #q = int(input("Entrez un autre nombre premier (Pas celui que vous avez entré ci-dessus): "))
    p=number.getPrime(10)
    q=number.getPrime(10)
    print(q,p)
    print("Générer vos paires de clés publiques / privées maintenant . . .")
    public, private = generate_keypair(p, q)
    print ("Votre clé publique est ", public ," et votre clé privée est ", private)
    #le serveur envoit son clé publique(e,n) au client
    e=public[0]
    n=public[1]
    connexion_avec_client.send((str(e)).encode())
    connexion_avec_client.send((str(n)).encode())
    #le serveur reçoit ainsi le message crypté envoyé par le client
    enc = connexion_avec_client.recv(4096)
    encrypted_msg = pickle.loads(enc)
    print
    print ("Votre message crypté est: ")
    print (''.join(map(lambda x: str(x), encrypted_msg)),"\n")
    #Decryptage
    print("\nDéchiffrer un message avec une clé privée ", private)
    print
    print("\nVotre message est:")
    print(decrypt(private, encrypted_msg))
    #calculer le temps d'exécution
    end = time.time()
    print("\nle programme a duré ",end - start,"\n")
    print("Fermeture de la connexion")
    connexion_avec_client.close()
    connexion_principale.close()
