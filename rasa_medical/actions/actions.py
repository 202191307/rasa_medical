# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import sqlite3


class ActionEmployee(Action):

    def name(self) -> Text:
        return "action_employee"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = sqlite3.connect("D:/pyWorkSpace/rasa_medical/actions/DepartmentList.db")
        cursor = conn.cursor()

        de_name = tracker.get_slot('department')
        query1 = "SELECT Employee FROM DepartmentList WHERE Department= ?"
        cursor.execute(query1, (str(de_name),))
        rows = cursor.fetchall()
        if len(list(rows)) < 1:
            dispatcher.utter_message(text="You can send a complain to this mailbox: xxxxxx@163.com. We will "
                                          "handle your situation with in two working days.")

        else:
            for row in rows:
                dispatcher.utter_message(text="The employee list of the department is here: " + row[0] + ". Click the "
                                                                                                         "corresponding "
                                                                                                         "name to give "
                                                                                                         "feedback")


class ActionOrder(Action):
    def name(self) -> Text:
        return "action_order_num"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = sqlite3.connect("D:/pyWorkSpace/rasa_medical/actions/OrderInformation.db")
        cursor = conn.cursor()

        userID = tracker.get_slot('user_ID')
        orderID = tracker.get_slot('order_ID')

        query1 = "SELECT EstimatedDeliveryDate FROM OrderList WHERE userID = ? and orderID = ?"
        cursor.execute(query1, (str(userID), str(orderID),))

        rows = cursor.fetchall()
        if len(list(rows)) < 1:
            dispatcher.utter_message(text="Sorry, there is no relevant information, please confirm that you have "
                                          "entered the correct user ID and Order number.")

        else:
            for row in rows:
                dispatcher.utter_message(text="Successfully obtained the order message. The system is loading latest "
                                              "status of the order for you.")
                dispatcher.utter_message(text="Your order is expected to be delivered in " + row[0] + ".")
