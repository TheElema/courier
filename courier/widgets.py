# -*- coding: utf-8 -*-
from enum import Enum

class CourierWidget:
	pass

class Message(CourierWidget):

	def __init__(self, fbid, message):
		self.fbid = fbid
		self.message = message

	def to_json(self):
		return {
			'recipient': {
				'id': self.fbid
			},
			'message': {
				'text': self.message
			}
		}

class MessageWidget:
    def __init__(self, fbid, message):
        self.fbid = fbid
        self.message = message

    def to_json(self):
        message = self.message.to_json()
        payload = {
            'recipient': {
                'id': self.fbid
            }, 
            'message': {}
        }
        payload['message'].update(self.message.to_json())
        return payload

class Button:
    """
    Creates a button element can be of any type with any arguments
    """
    def __init__(self, type , title = None):
        self.type  = type
        self.title = title

    def to_json(self):
        json = {'type': self.type}
        if self.title is not None: json["title"] = self.title
        return json


class ShareButton(Button):
    """This button is a trigger for the account unlinking flow.
    """
    def __init__(self):
        super().__init__("element_share")


class UnlinkAccount(Button):
    """
    Creates a share button
    """
    def __init__(self):
        super().__init__("account_unlink")


class LoginButton(Button):
    """
    Creates a share button
    """
    def __init__(self, url):
        super().__init__("account_link")
        self.url = url

    def to_json(self):
        json = super().to_json()
        json.update({"url": self.url})
        return json


class CallButton(Button):
    """.The Call Button can be used to initiate a phone call.
        This button can be used with the Button and Generic Templates.
    """
    def __init__(self, title, phonenumber):
        super().__init__("phone_number")
        self.title = title
        self.phonenumber = phonenumber

    def to_json(self):
        json = super().to_json()
        json.update({
            "title": self.title,
            "payload": self.phonenumber
        })
        return json


class PostbackButton(Button):
    """.The Call Button can be used to initiate a phone call.
        This button can be used with the Button and Generic Templates.
    """

    def __init__(self, title, payload):
        super().__init__("postback")
        self.title = title
        self.payload = payload

    def to_json(self):
        json = super().to_json()
        json.update({
            "title": self.title,
            "payload": self.payload
        })
        return json


class URLButton(Button):
    """.The Call Button can be used to initiate a phone call.
        This button can be used with the Button and Generic Templates.
    """
    class WebviewHeightRatio(Enum):
        compact = "compact"
        tall = "tall"
        full = "full"

    def __init__(self, title, url, webview_height_ratio: WebviewHeightRatio = None,
                 messenger_extensions: bool = None, fallback_url = None, webview_share_button = None):
        super().__init__("web_url")
        self.title = title
        self.url = url
        self.webview_height_ratio = webview_height_ratio
        self.messenger_extensions = messenger_extensions
        self.fallback_url = fallback_url
        self.webview_share_button = webview_share_button

    def to_json(self):
        json = super().to_json()
        json.update({
            "title": self.title,
            "url": self.url
        })

        if self.webview_height_ratio is not None: json["webview_height_ratio"] = self.webview_height_ratio.value
        if self.messenger_extensions is not None: json["messenger_extensions"] = self.messenger_extensions
        if self.fallback_url is not None: json["fallback_url"] = self.fallback_url
        if self.webview_share_button is not None: json["webview_share_button"] = self.webview_share_button
        return json


class RequestedUserInfo:
    """Information requested from person that will render in the dialog.
    """
    def __init__(self, shipping_address: bool = False, contact_name: bool = False,
                 contact_phone: bool = False, contact_email: bool = False):
        self.shipping_address = shipping_address
        self.contact_name = contact_name
        self.contact_phone = contact_phone
        self.contact_email = contact_email

    def to_json(self):
        json = []
        if self.shipping_address: json.append("shipping_address")
        if self.contact_name: json.append("contact_name")
        if self.contact_phone: json.append("contact_phone")
        if self.contact_email: json.append("contact_email")


class PaymentType(Enum):
    FIXED_AMOUNT = "FLEXIBLE_AMOUNT"
    FLEXIBLE_AMOUNT = "FLEXIBLE_AMOUNT"


class PriceField:
    """List of objects used to calculate total price.
        Each label is rendered as a line item in the checkout dialog.
    """
    def __init__(self, label, amount):
        self.label = label
        self.amount = amount

    def to_json(self):
        return {
            "label": self.label,
            "amount": self.amount
        }


class BuyButton(Button):

    class PaymentSummary:
        """Fields used in the checkout dialog.
        """

        def __init__(self, currency, payment_type: PaymentType, merchant_name,
                     requested_user_info: RequestedUserInfo, price_list: list , is_test_payment: bool = None):
            self.currency = currency
            self.merchant_name = merchant_name
            self.requested_user_info = requested_user_info
            self.price_list = price_list
            self.is_test_payment = is_test_payment
            self.payment_type = payment_type

        def to_json(self):
            json = {
                "payment_type": self.payment_type,
                "currency": self.currency,
                "merchant_name": self.merchant_name,
                "requested_user_info": self.requested_user_info,
                "price_list": self.price_list
            }
            if self.is_test_payment is not None: json.update({"is_test_payment":
                                                              self.is_test_payment})

    def __init__(self, title, payload, payment_summary: PaymentSummary):
        super().__init__("payment")
        self.title = title
        self.payload = payload
        self.payment_summary = payment_summary

    def to_json(self):
        return {
            "title": self.title,
            "payload": self.payload,
            "payment_summary": self.payment_summary
        }


class QuickReply:
    """
    Creates a quick reply element
    """
    def __init__(self, reply_title, reply_payload):
        self.reply_title = reply_title
        self.reply_payload = reply_payload

    def to_json(self):
        return {'content_type': 'text', 'title': self.reply_title, 'payload': self.reply_payload}


class QuickReplyImage:
    """
    Creates a quick reply element  with an image
    """
    def __init__(self, reply_title, reply_payload, reply_image):
        self.reply_title = reply_title
        self.reply_payload = reply_payload

    def to_json(self):
        return {'content_type': 'text', 'title': self.reply_title, 'payload': self.reply_payload, 'image_url': self.reply_image}


class QuickLocation:
    """
    Creates a quick reply location getter element
    """
    def __init__(self):
        pass

    def to_json(self):
        return {'content_type': 'location'}


class SenderAction:
    """"
        Return a sender action:
            mark_seen, typing_on , typing_off
    """
    def __init__(self, action):
        self.action = action

    def to_json(self):
        return {'sender_action': self.action}


class DefaultAction:
    """"
        Adds clickable events to various widgets
    """
    TYPE_WEB_URL = "web_url"
    WEB_HEIGHT_TALL = "tall"

    def __init__(self, type, url = None, messenger_extensions = True,
                 web_view_ratio = TYPE_WEB_URL, fallback_url = None):
        self.type = type
        self.url = url
        self.messenger_extensions = messenger_extensions
        self.web_view_ratio = web_view_ratio
        self.fallback_url = fallback_url

    def to_json(self):
        json = {
            "type": self.type,
            "messenger_extensions": self.messenger_extensions,
            "webview_height_ratio": self.web_view_ratio
        }
        if self.type == self.TYPE_WEB_URL :
            json["url"] = self.url
            json["fallback_url"] = self.fallback_url if self.fallback_url is not None else self.url

        return json


class ListItem:
    """"
        Standard widget for items in a list template
    """
    def __init__(self, title, subtitle = None, default_action: DefaultAction = None, button: Button = None,
                 image_url = None):
        self.title = title
        self.subtitle = subtitle
        self.default_action = default_action
        self.button = button
        self.image_url = image_url


    def to_json(self):
        json = {
            "title": self.title
        }
        if self.subtitle is not None: json["subtitle"] = self.subtitle
        if self.default_action is not None: json["default_action"] = self.default_action.to_json()
        if self.button is not None: json["button"] = [self.button.to_json()]
        if self.image_url is not None: json["image_url"] = self.image_url
        return json


class ReceiptItem:
    """
        This class repressents the goods which have been sold in the order
    """

    def __init__(self, title, price, quantity = None,currency = None, subtitle = None,
                 image_url = None):
        self.title = title
        self.subtitle = subtitle
        self.quantity = quantity
        self.price = price
        self.currency = currency
        self.image_url = image_url

    def to_json(self):
        json = {
            "title": self.title,
            "price": self.price
        }
        if self.subtitle is not None: json["subtitle"] = self.subtitle
        if self.quantity is not None: json["quantity"] = [self.quantity]
        if self.currency is not None: json["currency"] = self.currency
        if self.image_url is not None: json["image_url"] = self.image_url
        return json


class Address:
    """
        Shipping address: Repressents the address of the buyer of an item
    """
    def __init__(self, street_1, city, postal_code, state, country, street_2 = None):
        self.street_1 = street_1
        self.street_2 = street_2
        self.postal_code = postal_code
        self.city = city
        self.state = state
        self.country = country

    def to_json(self):
        json = {
            "street_1": self.street_1,
            "postal_code": self.postal_code,
            "city": self.city,
            "state": self.state,
            "country": self.country
        }
        if self.street_2 is not None: json["street_2"] = self.street_2
        return json


class Summary:
    """
        Payment summary: Repressents a brief description of a transaction
    """

    def __init__(self, total_cost, subtotal = None, shipping_cost = None, total_tax = None):
        self.total_cost = total_cost
        self.subtotal = subtotal
        self.shipping_cost = shipping_cost
        self.total_tax = total_tax

    def to_json(self):
        json = {
            "total_cost": self.total_cost
        }
        if self.subtotal is not None: json["subtotal"] = [self.subtotal]
        if self.shipping_cost is not None: json["shipping_cost"] = self.shipping_cost
        if self.total_cost is not None: json["image_url"] = self.total_cost
        return json


class Adjustment:
    """
        Payment adjustments: allow a way to insert adjusted pricing (e.g., sales). Adjustments are optional
    """
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def to_json(self):
        return {
            "name": self.name,
            "amount": self.amount
        }


class Airport:
    """
        An object repressenting an actual airport
    """

    def __init__(self, airport_code, city, terminal = None, gate = None):
        self.airport_code = airport_code
        self.city = city
        self.terminal = terminal
        self.gate = gate

    def to_json(self):
        json =  {
            "airport_code": self.airport_code,
            "city": self.city
        }
        if self.terminal is not None: json["terminal"] = self.terminal
        if self.gate is not None: json["qr_code"] = self.gate
        return json


class FlightSchedule:
    """
        Schedule for the flight
    """
    def __init__(self, boarding_time, departure_time, arrival_time):
        self.boarding_time = boarding_time
        self.departure_time = departure_time
        self.arrival_time = arrival_time


    def to_json(self):
        return {
            "boarding_time": self.boarding_time,
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time
        }


class FlightInfo:
    """
        Boarding passes for passengers
    """
    def __init__(self, flight_number, departure_airport: Airport, arrival_airport: Airport,
                 flight_schedule: FlightSchedule):
        self.flight_number = flight_number
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.flight_schedule = flight_schedule


    def to_json(self):
        return {
            "flight_number": self.flight_number,
            "departure_airport": self.departure_airport,
            "arrival_airport": self.arrival_airport,
            "flight_schedule": self.flight_schedule
        }


class Field:
    """
        An object for holding an object with labels and values
    """

    def __init__(self, label, value):
        self.label = label
        self.value = value

    def to_json(self):
        return {
            "label": self.label,
            "value": self.value
        }


class BoardingPass:
    """
        Boarding passes for passengers
    """
    def __init__(self, passenger_name, pnr_number, logo_image_url, flight_info: FlightInfo,
                 travel_class = None, seat = None,  auxiliary_fields: list = None,
                 secondary_fields: list = None, header_text_field = None,
                 header_image_url = None, qr_code = None, barcode_image_url = None,
                 above_bar_code_image_url = None):
        self.passenger_name = passenger_name
        self.pnr_number = pnr_number
        self.travel_class = travel_class
        self.seat = seat
        self.auxiliary_fields = auxiliary_fields
        self.secondary_fields = secondary_fields
        self.logo_image_url = logo_image_url
        self.header_image_url = header_image_url
        self.header_text_field = header_text_field
        self.qr_code = qr_code
        self.barcode_image_url = barcode_image_url
        self.above_bar_code_image_url = above_bar_code_image_url
        self.flight_info = flight_info


    def to_json(self):
        json = {
            "passenger_name": self.passenger_name,
            "pnr_number": self.pnr_number,
            "logo_image_url": self.logo_image_url,
            "flight_info": self.flight_info
        }

        if self.travel_class is not None: json["travel_class"] = [self.travel_class]
        if self.seat is not None: json["seat"] = self.seat
        if self.auxiliary_fields is not None: json["auxiliary_fields"] = self.auxiliary_fields
        if self.secondary_fields is not None: json["secondary_fields"] = self.secondary_fields
        if self.header_image_url is not None: json["header_image_url"] = self.header_image_url
        if self.header_text_field is not None: json["header_text_field"] = self.header_text_field
        if self.qr_code is not None: json["qr_code"] = self.qr_code
        if self.barcode_image_url is not None: json["barcode_image_url"] = self.barcode_image_url
        if self.above_bar_code_image_url is not None: json["above_bar_code_image_url"] = self.above_bar_code_image_url
        return json


class PassengerInfo:
    """Information unique to passenger/segment pair
    """


    def __init__(self, passenger_id, name, ticket_number = None):
        self.passenger_id = passenger_id
        self.name = name
        self.ticket_number = ticket_number


    def to_json(self):
        json = {
            "passenger_id": self.passenger_id,
            "name": self.name
        }
        if self.ticket_number is not None: json["ticket_number"] = self.ticket_number
        return json


class IteneraryFlightInfo:
    """
        Boarding passes for passengers
    """

    class TravelClass(Enum):
        economy = "economy"
        business = "business"
        first_class = "first_class"


    def __init__(self,connection_id, segment_id, flight_number, departure_airport: Airport, arrival_airport: Airport,
                 flight_schedule: FlightSchedule, travel_class: TravelClass, aircraft_type: None):
        self.connection_id = connection_id
        self.segment_id = segment_id
        self.flight_number = flight_number
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.flight_schedule = flight_schedule
        self.travel_class = travel_class
        self.aircraft_type = aircraft_type


    def to_json(self):
        json =  {
            "connection_id": self.connection_id,
            "segment_id": self.segment_id,
            "flight_number": self.flight_number,
            "departure_airport": self.departure_airport,
            "arrival_airport": self.arrival_airport,
            "flight_schedule": self.flight_schedule,
            "travel_class": self.travel_class.value
        }
        if self.aircraft_type is not None: json["aircraft_type"] = self.aircraft_type
        return json


class ProductInfo(object):
    """List of products the passenger purchased
    """

    def __init__(self, title, value):
        self.title = title
        self.value = value

    def to_json(self):
        return {
            "label": self.title,
            "value": self.value
        }


class PassengerSegmentInfo:
    """
        Information unique to passenger/segment pair
    """

    def __init__(self, segment_id, passenger_id, seat, seat_type, product_info: list):
        self.segment_id = segment_id
        self.passenger_id = passenger_id
        self.seat = seat
        self.seat_type = seat_type
        self.product_info = product_info


    def to_json(self):
        json =  {
            "segment_id": self.segment_id,
            "passenger_id": self.passenger_id,
            "seat": self.seat,
            "seat_type": self.seat_type
        }
        if self.product_info is not None: json["product_info"] = self.product_info
        return json

class PriceInfo():
    """Itemization of the total price
    """

    def __init__(self, title, amount, currency = None):
        self.title = title
        self.amount = amount
        self.currency = currency

    def to_json(self):
        json = {
            "label": self.title,
            "value": self.value
        }
        if self.currency is not None: json["currency"] = self.currency
        return json