# coding=utf-8
import socket
import pickle
import threading
import time

class myThread (threading.Thread):
   def __init__(self, threadID,name,data):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.data=data
      
   def run(self):
        print ("Starting " + self.name)
        print(self.data)
        encrypted_char=[(ord(char) ** e) % n for char in self.data]
        
        enc = pickle.dumps(encrypted_char)
        
        connexion_avec_serveur.sendall(enc)
        print("Exiting " + self.name)

if __name__=='__main__':

   hote = "localhost"
   port = 12800
   connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   connexion_avec_serveur.connect((hote, port))
   print("Connexion établie avec le serveur sur le port {}".format(port))


   e = connexion_avec_serveur.recv(1024)
   e = int(e.decode())

   n = connexion_avec_serveur.recv(1024)
   n = int(n.decode())

   print(e,n)

   message = input("Enter a message to encrypt with your public key: ")
   connexion_avec_serveur.send((str(len(message))).encode())
   print(len(message))

   threadList = ["Thread-{}".format(i) for i in range(1,len(message)+1)]
   chars=[message[i]+str(i) for i in range(len(message))]
   threads = []
   threadID = 0
   # Create new threads
   time.sleep(1)
   for tName in threadList:
       thread = myThread(threadID, tName,chars[threadID])
       thread.start()
       thread.join()
       threads.append(thread)
       threadID += 1

   # Wait for all threads to complete
   for t in threads:
      t.join()
   print ("Exiting Main Thread")
   

   print("Fermeture de la connexion")
   connexion_avec_serveur.close()
