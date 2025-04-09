
import requests
import logging


from models.User import User
from models import dbsession

class Platforms:
  challenge_api = 'localhost:8080'
  dbsession = dbsession


  @classmethod
  def startPlatforms(cls):
    users = User.all()

    req = []

    for i in users:
      req.append(i.uuid)

    if not req:
      return
    
    r = requests.post(f'http://{cls.challenge_api}/create-platforms', json=req)

    logging.info(f"POST response:{r.status_code}, {r.text}")


    res = r.json()

    for i in res:
      user = User.by_uuid(i['user'])


      user.platform = i['ip']

      cls.dbsession.add(user)
      cls.dbsession.commit()

  @classmethod
  def killPlatforms(cls):
    r = requests.delete(f'http://{cls.challenge_api}/remove-platforms')
    logging.info(f"DELETE response:{r.status_code}, {r.text}")

    res = r.json()

    if not res:
      return

    for i in res:
      user = User.by_uuid(i['Name'])
      if user is not None:
        user.platform = ''

        cls.dbsession.add(user)
        cls.dbsession.commit()