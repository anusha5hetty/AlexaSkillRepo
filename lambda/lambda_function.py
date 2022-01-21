# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import sys
from pathlib import Path
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.dialog.delegate_directive import DelegateDirective
from ask_sdk_model.dialog.elicit_slot_directive import ElicitSlotDirective
from ask_sdk_model.intent import Intent

from ask_sdk_model import Response

PATH = Path(__file__).resolve().parents[0]
sys.path.append(str(PATH))

import features

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def build_response(message, session_attributes={}):
    response = {}
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    response['response'] = message
    return response

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to Leankit Features. You can go ahead and mess up the board now!!"
        
        # .add_directive(DelegateDirective(updated_intent='NumberOfCards'))

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "You are not pronouncing it right!! Do you need english pronouciation tutorials"
        reprompt = "Can you speak up? I don't have all day!!"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = f"You just triggered {intent_name}. You need to create a lambda function to handle the intent request dum dum!!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Great!! You messed something up!! Fix it now!!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class NumberOfCardsIntentHandle(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("NumberOfCards")(handler_input)
    
    def handle(self, handler_input):
        card_count = features.get_total_cards_count()
        speak_output = "Total number of cards in your board is {}".format(card_count)
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CardsAssignedToUserHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("CardsAssignedToMe")(handler_input)
    
    def handle(self, handler_input):
        current_intent = handler_input.request_envelope.request.intent;
        user_obj = ask_utils.request_util.get_slot(handler_input, "user")
        user_name = user_obj.value
        lstCards = features.get_cards_assigned_to_user(user_name)
        
        if lstCards:
            speak_output = "Cards assigned to {} are {}".format(user_name, ','.join(lstCards))
        else:
            speak_output = "There are no cards assigned."
            
        # .add_directive(DelegateDirective(updated_intent=Intent('NumberOfCardsAssignedToUser')))

        response = (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
        
        return response

class NumberOfCardsAssignedToUserHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("NumberOfCardsAssignedToUser")(handler_input)
    
    def handle(self, handler_input):
        user_obj = ask_utils.request_util.get_slot(handler_input, "user")
        user_name = user_obj.value
        lst_cards = features.get_cards_assigned_to_user(user_name)
        num_of_Cards = len(lst_cards)
        
        if num_of_Cards:
            speak_output = "Number of cards assigned to {} are {}".format(user_name, num_of_Cards)
        else:
            speak_output = "There are no cards assigned."

        response = (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
        
        return response

class CreateCardHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("CreateCard")(handler_input)
    
    def handle(self, handler_input):
        # current_intent = handler_input.request_envelope.request.intent
        
        # if current_intent.confirmation_status.value == 'CONFIRMED':
        card_name = ask_utils.get_slot_value(handler_input, "card_name")
        card_type = ask_utils.get_slot_value(handler_input, "card_type")
        
        session_attr = handler_input.attributes_manager.session_attributes
        
        response = features.create_card(card_name, card_type)

        if response and response.status_code in (200, 201):
            speak_output = f"Card {card_name} is created"
            card_id = response.json()['id']
            session_attr['card_details'] = {'name': card_name, 'card_id': card_id}
        else:
            speak_output = "There was some problem creating the card. Please try again after some time"

        response = (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
            # return response
        # else:
            # speak_output = "Is there anything else I can help you with?"
            # response = (
            #     handler_input.response_builder
            #         .speak(speak_output)
            #         .response
            # )
        return response


class UpdateCardTypeHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("UpdateCardType")(handler_input)
    
    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        current_intent = handler_input.request_envelope.request.intent
        
        card_name = ask_utils.get_slot_value(handler_input, "card_name")
        card_type = ask_utils.get_slot_value(handler_input, "card_type")
        
        card_name = card_name or session_attr.get('card_details', {}).get('name')
        
        if not card_name:
            speak_output = 'Can you provide the card name or is it too much trouble?'
            response = (
            handler_input.response_builder
                .add_directive(ElicitSlotDirective(updated_intent=current_intent, slot_to_elicit='card_name'))
                .speak(speak_output)
                .response
            )
            return response
        
        card_id = features.get_card_id_by_name(card_name)
        
        if card_id:
            response = features.update_card_type(card_id, card_type)
            session_attr['card_details'] = {'name': card_name, 'card_id': card_id}

            if response and response.status_code in (200, 201):
                speak_output = f'"{card_name}" is updated to card type {card_type}'
            else:
                speak_output = "There was some problem updating the card type. Please try again after some time"
        else:
            speak_output = f'Card Update failed!! Card "{card_name}" is either not present or there are more than one cards matching description'

        response = (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
        
        return response
    
class UpdateCardLaneHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("UpdateCardLane")(handler_input)
    
    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        current_intent = handler_input.request_envelope.request.intent
        
        card_name = ask_utils.get_slot_value(handler_input, "card_name")
        lane_name = ask_utils.get_slot_value(handler_input, "lane_name")
        
        card_name = card_name or session_attr.get('card_details', {}).get('name')
        
        if not card_name:
            speak_output = 'Can you provide the card name or is it too much trouble?'
            response = (
            handler_input.response_builder
                .add_directive(ElicitSlotDirective(updated_intent=current_intent, slot_to_elicit='card_name'))
                .speak(speak_output)
                .response
            )
            return response
        
        card_id = features.get_card_id_by_name(card_name)
        
        if not card_id:
            speak_output = f'"{card_name}" is either not present or there are more than one card with matching description.'
            response = (
            handler_input.response_builder
                .speak(speak_output)
                .response
            )
            return response
        
        lane_id = features.get_lane_id_by_name(lane_name)
        
        if not lane_id:
            speak_output = f'Couldn\'t find a lane with name {lane_name}.'
            response = (
            handler_input.response_builder
                .speak(speak_output)
                .response
            )
            return response
        
        response = features.update_lane(card_id, lane_id)

        if response and response.status_code in (200, 201):
            speak_output = f'"{card_name}" is moved to lane {lane_name}'
        else:
            speak_output = "There was some problem in moving the card. Please try again after some time"
            
        session_attr['card_details'] = {'name': card_name, 'card_id': card_id}

        response = (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
        
        return response
    
class AssignUserToCardHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AssignUsersToCard")(handler_input)
    
    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        current_intent = handler_input.request_envelope.request.intent
        
        card_name = ask_utils.get_slot_value(handler_input, "card_name")
        user_name = ask_utils.get_slot_value(handler_input, "user_name")
        
        card_name = card_name or session_attr.get('card_details', {}).get('name')
        
        if not card_name:
            speak_output = 'Can you provide the card name or is it too much trouble?'
            response = (
            handler_input.response_builder
                .add_directive(ElicitSlotDirective(updated_intent=current_intent, slot_to_elicit='card_name'))
                .speak(speak_output)
                .response
            )
            return response
        
        card_id = features.get_card_id_by_name(card_name)
        
        if not card_id:
            speak_output = f'"{card_name}" is either not present or there are more than one card with matching description.'
            response = (
            handler_input.response_builder
                .speak(speak_output)
                .response
            )
            return response
        
        user_details = features.get_user_details_by_name(user_name)
        
        if not user_details:
            speak_output = f'Couldn\'t find the user with name {user_name}. Does this person exist or is it just your imagination?'
            response = (
            handler_input.response_builder
                .speak(speak_output)
                .response
            )
            return response
        
        user_id = user_details['userId']
        
        response = features.update_assignee(card_id, user_id)

        if response and response.status_code in (200, 201):
            user_name = "you" if user_name == 'me' else user_name
            speak_output = f'"{card_name}" is assigned to {user_name}'
        else:
            speak_output = f"There was some problem in assigning user {user_name} to card {card_name}. Please try again after some time"
            
        session_attr['card_details'] = {'name': card_name, 'card_id': card_id}

        response = (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
        
        return response
    
class AddUserToCardHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AddUsersToCard")(handler_input)
    
    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        current_intent = handler_input.request_envelope.request.intent
        
        card_name = ask_utils.get_slot_value(handler_input, "card_name")
        user_name = ask_utils.get_slot_value(handler_input, "user_name")
        
        card_name = card_name or session_attr.get('card_details', {}).get('name')
        
        if not card_name:
            speak_output = 'Can you provide the card name or is it too much trouble?'
            response = (
            handler_input.response_builder
                .add_directive(ElicitSlotDirective(updated_intent=current_intent, slot_to_elicit='card_name'))
                .speak(speak_output)
                .response
            )
            return response
        
        card_id = features.get_card_id_by_name(card_name)
        
        if not card_id:
            speak_output = f'"{card_name}" is either not present or there are more than one card with matching description.'
            response = (
            handler_input.response_builder
                .speak(speak_output)
                .response
            )
            return response
        
        user_details = features.get_user_details_by_name(user_name)
        
        if not user_details:
            speak_output = f'Couldn\'t find the user with name {user_name}.'
            response = (
            handler_input.response_builder
                .speak(speak_output)
                .response
            )
            return response
        
        user_id = user_details['userId']
        
        response = features.add_assignee(card_id, user_id)

        if response and response.status_code in (200, 201):
            user_name = "you" if user_name == 'me' else user_name
            speak_output = f'{user_name} is added to "{card_name}"'
        else:
            speak_output = f"There was some problem in assigning user {user_name} to card {card_name}. Please try again after some time"
            
        session_attr['card_details'] = {'name': card_name, 'card_id': card_id}

        response = (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
        
        return response

class CardStatusHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("CardStatus")(handler_input)
    
    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        current_intent = handler_input.request_envelope.request.intent
        
        card_name = ask_utils.get_slot_value(handler_input, "card_name")        
        card_name = card_name or session_attr.get('card_details', {}).get('name')
        
        if not card_name:
            speak_output = 'Can you provide the card name or is it too much trouble?'
            response = (
            handler_input.response_builder
                .add_directive(ElicitSlotDirective(updated_intent=current_intent, slot_to_elicit='card_name'))
                .speak(speak_output)
                .response
            )
            return response
        
        card_id = features.get_card_id_by_name(card_name)
        
        if not card_id:
            speak_output = f'"{card_name}" is either not present or there are more than one card with matching description.'
            response = (
            handler_input.response_builder
                .speak(speak_output)
                .response
            )
            return response
        
        speak_output = features.get_status_of_card(card_id)
            
        session_attr['card_details'] = {'name': card_name, 'card_id': card_id}

        response = (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(False)
                .response
        )
        
        return response

class NewCardAssignedHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("NewCardsAssigned")(handler_input)
    
    def handle(self, handler_input):        
        user_name = ask_utils.get_slot_value(handler_input, "user_name") 
        user_name = "anusha" if user_name == 'me' else user_name
        
        user_details = features.get_user_details_by_name(user_name)
        
        if not user_details:
            speak_output = f'Couldn\'t find the user with name {user_name}. Does this person exist or is it just your imagination?'
            response = (
            handler_input.response_builder
                .speak(speak_output)
                .response
            )
            return response
        
        user_id = user_details['userId']
        
        lst_card_names = features.get_new_cards_assigned_to_user_today(user_id)
        
        user_name = "you" if user_name == 'me' else user_name
        len_card = len(lst_card_names)
        if len_card > 1:
            speak_output = f"There are {len_card} new cards assigned to {user_name} today. They are {','.join(lst_card_names)}"
        elif len_card == 1:
            speak_output = f"There is a new card assigned to {user_name} today. It is {','.join(lst_card_names)}"
        else:
            speak_output = f"There are no new cards assigned to {user_name}"
            

        response = (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(False)
                .response
        )
        
        return response

class DeleteCardHandle(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("DeleteCard")(handler_input)
    
    def handle(self, handler_input):   
        session_attr = handler_input.attributes_manager.session_attributes
        current_intent = handler_input.request_envelope.request.intent
        
        card_name = ask_utils.get_slot_value(handler_input, "card_name")
        card_name = card_name or session_attr.get('card_details', {}).get('name')
        
        if not card_name:
            speak_output = 'Can you provide the card name you want me to delete?'
            response = (
            handler_input.response_builder
                .add_directive(ElicitSlotDirective(updated_intent=current_intent, slot_to_elicit='card_name'))
                .speak(speak_output)
                .response
            )
            return response
        speak_output = features.delete_card(card_name=card_name)  
        response = (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
        return response
    
    
class SkillCreatorHandle(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("SkillCreator")(handler_input)
    
    def handle(self, handler_input): 
        speak_output = 'This feature is created by Sreeram, Arvind, Geetika and Anusha.'
        response = (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
        return response


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.
sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(NumberOfCardsIntentHandle())
sb.add_request_handler(CardsAssignedToUserHandler())
sb.add_request_handler(NumberOfCardsAssignedToUserHandler())
sb.add_request_handler(CreateCardHandler())
sb.add_request_handler(UpdateCardTypeHandler())
sb.add_request_handler(UpdateCardLaneHandler())
sb.add_request_handler(AssignUserToCardHandler())
sb.add_request_handler(AddUserToCardHandler())
sb.add_request_handler(NewCardAssignedHandler())
sb.add_request_handler(CardStatusHandler())
sb.add_request_handler(DeleteCardHandle())
sb.add_request_handler(SkillCreatorHandle())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()