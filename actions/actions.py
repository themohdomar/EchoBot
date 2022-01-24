# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk.events import AllSlotsReset
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import TimesheetBot
import GoogleSearchBot


#
#
class ActionPrompt(Action):

    def name(self) -> Text:
        return "action_prompt"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entity = tracker.get_slot("PERSON")
        if entity:
            GoogleSearchBot.SearchBot(entity)
            print("Browser not to close")
            dispatcher.utter_message(text="Here is what I found")
        else:
            dispatcher.utter_message(text="Entity not found.... Maybe entity is not a PERSON")

        print("Entity :+", entity)
        dispatcher.utter_message(text="What else can I do for you?")

        return [AllSlotsReset()]


class ActionFillTimesheet(Action):

    def name(self) -> Text:
        return "action_fill_timesheet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            #dispatcher.utter_message(text="Running Action Fill Timesheet")

            Bot = TimesheetBot.Timesheetbot()
            Bot.fill_time()

            dispatcher.utter_message(text="Timesheet Entry done")
            dispatcher.utter_message(text="What else can I help you with?")