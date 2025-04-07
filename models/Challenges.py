
import requests
import logging


from models.Box import Box

class Challenges:
  challenge_api = 'localhost:8080'

  @classmethod
  def getChallenges(cls):
    r = requests.get(f'http://{cls.challenge_api}/get-challenges')

    challenges = r.json()
    out = []
    for i in challenges:
      out.append(i['name'])

    return out
  
  @classmethod
  def killChallenges(cls):
    r= requests.delete(f'http://{cls.challenge_api}/remove-challenges')
  
  
    logging.info(f"DELETE response:{r.status_code}, {r.text}")

  @classmethod
  def startChallenges(cls):
    boxes = Box.all()
    req = []


    for i in boxes:
      flaglist = i.flags
      # flaglist = i.flaglist(i.uuid)
      print(flaglist)
      print(len(flaglist) == 0)
      if len(flaglist) == 0:
        print("I'm supposed to stop")
        continue

      challenge = {
        "name": i.uuid,
        "challenge": i.challenge,
        "flag": flaglist[0].token
      }
      req.append(challenge)
      # problem for next time:
      # insert the ip addrs
      
    if req:
      r = requests.post(f'http://{cls.challenge_api}/create-challenges', json=req)
      logging.info(f"POST response:{r.status_code}, {r.text}")
    

