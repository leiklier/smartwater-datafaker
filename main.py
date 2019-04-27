#!/usr/bin/env python3

import json
import requests
import websocket
import random

# CONSTANTS

API_URL = '{}vannovervakning.com:5000/api/v1/measurements/'
NODEID_SOURCE = 7 # Sett denne til gruppenummer du vil stjele data fra
NODEID_TARGET = 2 # Her skriver du ditt eget gruppenummer
DELTA_MAX = 0.12
MODE = 'HIJACK'

WS_CONFIG_MESSAGE = {
    'type': "WEBSOCKET_MEASUREMENTS_TX",
    'payload': {
        'action': "ADD_SUBSCRIPTIONS",
        'types': {
            NODEID_SOURCE: [
                "BATTERY",
                "LID",
                "TEMPERATURE",
                "TURBIDITY",
                "DISSOLVED_OXYGEN",
                "PH",
                "CONDUCTIVITY"
            ]
        }
    }
}

def ws_on_message(ws, message):
    payload = json.loads(message)['payload']
    if payload['action'] == 'INCOMING_DATA':
        print("Kok mottatt")
        data = payload['data']
        data.pop('nodeId')
        data.pop('timeCreated')
        data['value'] = round(data['value'] * random.uniform(1 - DELTA_MAX, 1 + DELTA_MAX), 2)
        print("Ferdig med å skrive om koken med litt andre verdier")
        requests.post(API_URL.format('http://') + str(NODEID_TARGET), json=data)
        print("Leverte inn koken\n")

def ws_on_open(ws):
    print("Koblet til API-server")
    ws.send(json.dumps(WS_CONFIG_MESSAGE))
    print("Sendte konfigurasjonsmelding\n")

print("Kok Alt - Alltid\nForfatter: Leik Lima-Eriksen\nVersjon: v1.0.0\n\n")
if MODE == 'HIJACK':
    ws = websocket.WebSocketApp(API_URL.format('ws://'), on_message=ws_on_message)
    ws.on_open = ws_on_open
    ws.run_forever()
