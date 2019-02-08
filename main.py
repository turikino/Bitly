import requests
import os
import json
import argparse
from dotenv import load_dotenv

def create_parser():
    parser = argparse.ArgumentParser(description='Создает bitlink из обычной ссылки.\
    Показывает количество кликов, если введен bitlink.')
    parser.add_argument('-l','--link', help='Ваша ссылка:')
    return parser

def create_bitlink(user_url):
  '''Создает bitlink из обычной ссылки.'''
  url = 'https://api-ssl.bitly.com/v4/bitlinks'
  headers = {
    'Authorization':'Bearer {}'.format(os.getenv("TOKEN"))
    }
  data = {
    'long_url':user_url
  }
  response_post = requests.post(url, json=data, headers=headers )
  if response_post.ok:
    return response_post.json()['link']
  else:
    return None

def fetch_bitlink_clicks(user_url):
  '''Возвращает количество кликов по bitlink.'''
  url_template = 'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
  url = url_template.format(bitlink = user_url)
  headers = {
    'Authorization':'Bearer {}'.format(os.getenv("TOKEN"))
    }
  response_get = requests.get(url, headers=headers)
  if response_get.ok:
    return response_get.json()['total_clicks']
  else:
    return None

def check_url_is_bitlink(user_url):
  '''Проверяет, является ли ссылка битлинком.'''
  url_template = 'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
  url = url_template.format(bitlink = user_url)
  headers = {
    'Authorization':'Bearer {}'.format(os.getenv("TOKEN"))
    }
  data = {
  }
  response_get_bitlink = requests.get(url, params=data, headers=headers)
  return response_get_bitlink.ok

def check_url_response(user_url):
  '''Проверяет верность ссылки.'''
  url = user_url
  try:
    response_get = requests.get(url)
    return response_get.ok
  except requests.exceptions.MissingSchema:
    return False

if __name__=='__main__':
  load_dotenv()
  parser = create_parser()
  args = parser.parse_args()
  user_url=args.link
  user_url=user_url.replace('http://', '')
  if check_url_is_bitlink(user_url):
    bitlink_clicks = fetch_bitlink_clicks(user_url)
    print("Количество кликов: "+str(bitlink_clicks))
  elif check_url_response(user_url):
    user_bitlink = create_bitlink(user_url)
    if user_bitlink is None:
      print("Вы допустили ошибку при вводе. Попробуйте еще раз.")
    else:
      print(user_bitlink)
  else:
    print("Вы допустили ошибку при вводе. Попробуйте еще раз.")
