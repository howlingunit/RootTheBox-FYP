
import requests
import logging


from models.Box import Box
from models.Team import Team
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
    teams = Team.all()
    req = []

    count = 0
    for j in teams:
      count +=1
      for i in boxes:
        flaglist = i.flags
        if len(flaglist) == 0:
          continue

        challenge = {
          "name": f"{i.uuid}{count}",
          "team": j.uuid,
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
      ip.team_id = i['Team']
      boxName = i['Name'][:-1]
      box = Box.by_uuid(boxName)

      box.ip_addresses.append(ip)

      cls.dbsession.add(ip)
      cls.dbsession.add(box)
      cls.dbsession.commit()
    
    
    

  @classmethod
  def killChallenges(cls):
    # create loop for team!

    teams = Team.all()
    for i in teams:
      r = requests.delete(f'http://{cls.challenge_api}/remove-challenges/{i.uuid}')
    
    
      logging.info(f"DELETE response:{r.status_code}, {r.text}")
      
      res = r.json()
      if not res:
        return

      for i in res:
        ip = IpAddress.by_team(i['Team'])
        if ip is not None:
            logging.info("Deleted IP address: '%s'" % str(ip))
            cls.dbsession.delete(ip)
            cls.dbsession.commit()

