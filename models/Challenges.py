
import requests



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