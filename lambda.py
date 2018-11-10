"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import requests

alexaSkillId = "amzn1.ask.skill.ed8c6f34-2a4d-417d-a7f6-a643b1873ef8"
igdbKey = 'd1213aa0fa52512b50fcf362367e19ea'
endpoint = 'https://api-endpoint.igdb.com'
header = {
    'user-key' : igdbKey,
    'accept' : 'application/json'
}

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Game Query. " \
                    "You can ask about the rating for your favorite game. " \
                    "Try saying: 'What is the rating for Super Mario Brothers 3?'"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Try saying: 'What is the rating for Super Mario Brothers 3?'"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using Game Query. " \
                    "Have a nice day!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def getRating(intent, session):
    search = intent['slots']['gameName']['value']
    print('searching for ' + search)

    gamesUrl = endpoint + '/games/'
    params = {
        'search' : search,
        'limit' : 3,
        'filter[rating][exists]' : ''
    }
    r = requests.get(url = gamesUrl, headers = header, params = params)
    games = r.json()


    params = {
        'fields' : 'name,rating'
    }
    filteredGames = []
    for game in games:
        gameUrl = endpoint + '/games/' + str(game['id'])
        r = requests.get(url = gameUrl, headers = header, params=params)
        gameInfo = r.json()[0]
        if 'rating' in gameInfo:
            filteredGames.append(gameInfo)

    numGames = len(filteredGames)

    if numGames == 0:
        speech_output = "I couldn't find anything by that name."
    elif numGames == 1:
        speech_output = filteredGames[0]['name'] + " has a rating of " + str(round(filteredGames[0]['rating']))
    elif numGames > 1:
        speech_output = "I found a couple of games that match that name, here are the ratings for the top " + str(numGames) + ". "
        firstTime = ' has a rating of '
        for game in filteredGames:
            speech_output = speech_output + game['name'] + firstTime + str(round(game['rating'])) + ". "
            firstTime = ': '


    card_title = 'Here are you ratings'
    session_attributes = {}
    should_end_session = True
    reprompt_text = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "getRating":
        return getRating(intent, session)
    elif intent_name == "AMAZON.FallbackIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] != alexaSkillId):
         raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
