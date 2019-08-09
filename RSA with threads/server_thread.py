# coding=utf-8
import socket
import pickle
import random
import time
import queue
import threading
from Crypto.Util import number

def decrypt(pk, ciphertext):
    #Unpack the key into its components
    key, n = pk[0],pk[1]
    #Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((int(elt) ** key) % n) for elt in ciphertext]
    #Return the array of bytes as a string
    return ''.join(plain)
   
class myThread (threading.Thread):
   def __init__(self, threadID,clientsocket,n,d):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.clientsocket = clientsocket
      self.n=n
      self.d=d
      
   def run(self):
       print ("Starting thread-{}".format(self.threadID))
       enc=self.clientsocket.recv(1024)
       encrypted_msg = pickle.loads(enc)
       car = chr((encrypted_msg[0]**self.d)%n)
       # ou tout simplement : car=decrypt((self.d,self.n),encrypted_msg[0])
       pos=decrypt((self.d,self.n),encrypted_msg[1:])
       msg_dec=car+pos
       l.append(msg_dec)
       print ("Exiting thread-{}".format(self.threadID))



'''
Euclid's algorithm for determining the greatest common divisor
Use iteration to make it faster for larger integers
'''
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

'''
Euclid's extended algorithm for finding the multiplicative inverse of two numbers
'''
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

'''
Tests to see if a number is prime.
'''
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
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    #n = pq
    n = p * q

    #Phi is the totient of n
    phi = (p-1) * (q-1)

    #Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    #Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    #Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    
    #Return public and private keypair
    #Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))
if __name__=='__main__':
   start = time.time()

   hote = ''
   port = 12800
   connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   connexion_principale.bind((hote, port))
   connexion_principale.listen(5)
   #print("Le serveur écoute à présent sur le port {}".format(port))

   connexion_avec_client, infos_connexion = connexion_principale.accept()

   p = int(input("Enter a prime number (17, 19, 23, etc): "))
   q = int(input("Enter another prime number (Not one you entered above): "))

   #p=number.getPrime(10)
   #q=number.getPrime(10)

   print(q,p)
   print("Generating your public/private keypairs now . . .")
   public, private = generate_keypair(p, q)
   print ("Your public key is ", public ," and your private key is ", private)

   e=public[0]
   n=public[1]


   connexion_avec_client.send((str(e)).encode())
   connexion_avec_client.send((str(n)).encode())
   longueur = connexion_avec_client.recv(1024)
   longueur = int(longueur.decode())

   global l
   l=[]
   threads = []
   for i in range(longueur):
       print( "En écoute...")
       newthread = myThread(i,connexion_avec_client,n,private[0])
       newthread.start()
       threads.append(newthread)

   # Wait for all threads to complete
   for t in threads:
      t.join()
   print ("Exiting Main Thread")

   print("l=   ",l)

   dict={int(l[i][1:]):l[i][0] for i in range(len(l))}
   ch=""
   for cl in range(len(l)):
       ch=ch+str(dict[cl])


   print
   print("Your message is:")
   print(ch)
   
   end = time.time()
   print("the program lasts ",end - start)
   print
   print("Fermeture de la connexion")
   connexion_avec_client.close()
   connexion_principale.close()

