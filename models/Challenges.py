
import requests
import logging


from models.Box import Box
from models.IpAddress import IpAddress
from models import dbsession

class Challenges:
  challenge_api = 'localhost:8080'
  dbsession = dbsession

  @classmethod
  def getChallenges(cls):
    r = requests.get(f'http://{cls.challenge_api}/get-challenges')

    challenges = r.json()
    out = []
    for i in challenges:
      out.append(i['name'])

    return out


  @classmethod
  def startChallenges(cls):
    boxes = Box.all()
    req = []


    for i in boxes:
      flaglist = i.flags
      if len(flaglist) == 0:
        continue

      challenge = {
        "name": i.uuid,
        "challenge": i.challenge,
        "flag": flaglist[0].token
      }
      req.append(challenge)
      

      
    if not req:
      return 
    
    r = requests.post(f'http://{cls.challenge_api}/create-challenges', json=req)
    logging.info(f"POST response:{r.status_code}, {r.text}")
    res = r.json()

    for i in res:
      ip = IpAddress(box_id=i['Name'], address=i['Ip'])
      box = Box.by_uuid(i['Name'])

      box.ip_addresses.append(ip)

      cls.dbsession.add(ip)
      cls.dbsession.add(box)
      cls.dbsession.commit()
    
    
    

  @classmethod
  def killChallenges(cls):
    r = requests.delete(f'http://{cls.challenge_api}/remove-challenges')
  
  
    logging.info(f"DELETE response:{r.status_code}, {r.text}")
    
    res = r.json()
    if not res:
      return

    for i in res:
      ip = IpAddress.by_address(i['Ip'])
      if ip is not None:
          logging.info("Deleted IP address: '%s'" % str(ip))
          cls.dbsession.delete(ip)
          cls.dbsession.commit()

