# -*- coding: utf-8 -*-

from requests.status_codes import _codes as codes

descriptions = {

    # Informational.
    100: 'Continue with the request.',
    101: 'Server is switching to a different protocol.',
    102: 'Server has received and is processing the request, but no response is available yet.',
    #103: ('checkpoint',),
    #122: ('uri_too_long', 'request_uri_too_long'),
    200: 'Request was successful.',
    201: 'Request was successful, and a new resource has been created.',
    202: 'Request has been accepted but not yet acted upon.',
    203: 'Request was successful, but server is returning information that may be from another source.',
    204: 'There is no content to send for this request, but the headers may be useful.',
    205: 'Server successfully processed the request, but is not returning any content.',
    206: 'Download is separated into multiple streams, due to range header.',
    207: 'Message body that follows is an XML message and can contain a number of separate response codes.',
    208: 'Response is a representation of the result of one or more instance-manipulations applied to the current instance.',

    # Redirection.
    300: 'Request has more than one possible response.',
    301: 'URI of this resource has changed.',
    302: 'URI of this resource has changed, temporarily.',
    303: 'Client should get this resource from another URI.',
    304: 'Response has not been modified, client can continue to use a cached version.',
    305: 'Requested resource may only be accessed through a given proxy.',
    306: 'No longer used. Requested resource may only be accessed through a given proxy.',
    307: 'URI of this resource has changed, temporarily. Use the same HTTP method to access it.',
    #308: ('resume_incomplete', 'resume'),

    # Client Error.
    400: 'Server could not understand the request, due to invalid syntax.',
    401: 'Authentication is needed to access the given resource.',
    402: 'Some form of payment is needed to access the given resource.',
    403: 'Client does not have rights to access the content.',
    404: 'Server cannot find requested resource.',
    405: 'Server has disabled this request method and cannot be used.',
    406: 'Requested resource is only capable of generating content not acceptable according to the Accept headers sent.',
    407: 'Authentication by a proxy is needed to access the given resource.',
    408: 'Server would like to shut down this unused connection.',
    409: 'Request could not be processed because of conflict in the request, such as an edit conflict.',
    410: 'Requested content has been delected from the server',
    411: 'Server requires the Content-Length header to be defined.',
    412: 'Client has indicated preconditions in its headers which the server does not meet.',
    413: 'Request entity is larger than limits defined by server.',
    414: 'URI requested by the client is too long for the server to handle.',
    415: 'Media format of the requested data is not supported by the server.',
    416: "Range specified by the Range header in the request can't be fulfilled.",
    417: "Expectation indicated by the Expect header can't be met by the server.",
    418: 'HTCPCP server is a teapot; the resulting entity body may be short and stout.',
    422: 'Request was well-formed but was unable to be followed due to semantic errors.',
    423: 'Resource that is being accessed is locked.',
    424: 'Request failed due to failure of a previous request (e.g. a PROPPATCH).',
    #425: ('unordered_collection', 'unordered'),
    426: 'Client should switch to a different protocol such as TLS/1.0.',
    428: 'Origin server requires the request to be conditional.',
    429: 'User has sent too many requests in a given amount of time.',
    431: 'Server rejected the request because either a header, or all the headers collectively, are too large.',
    444: 'Server has returned no information to the client and closed the connection (Ngnix).',
    449: 'Request should be retried after performing the appropriate action (Microsoft).',
    450: 'Windows Parental Controls are turned on and are blocking access to the given webpage.',
    499: 'Connection has been closed by client while the server is still processing its request (Nginx).',

    # Server Error.
    500: "Server has encountered a situation it doesn't know how to handle.",
    501: 'Request method is not supported by the server and cannot be handled.',
    502: 'Server, while working as a gateway to get a response needed to handle the request, got an invalid response.',
    503: 'Server is not yet ready to handle the request.',
    504: 'Server is acting as a gateway and cannot get a response in time.',
    505: 'HTTP version used in the request is not supported by the server.',
    506: 'Transparent content negotiation for the request results in a circular reference.',
    507: 'Server is unable to store the representation needed to complete the request.',
    #509: 'This status code, while used by many servers, is not specified in any RFCs.',
    510: 'Further extensions to the request are required for the server to fulfill it.',
}

names = {

    # Informational.
    200: 'OK',
    207: 'Multi-Status',
    208: "I'm Used",
    203: 'Non-Authoritative Info',

    # Client Error.
    414: 'Request-URI Too Long',
    418: "I'm a Teapot",

    # Server Error.
    505: 'HTTP Version Not Supported',

}

for (code, titles) in list(codes.items()):
    if code not in names:
        names[code] = titles[0].replace('_', ' ').title()


class Status(object):
    """Holds an HTTP status code, and provides an easy way to access its name and description"""

    def __init__(self, code=None):
        self.code = code

    @property
    def name(self):
        """Returns the current status code's name."""
        if self.code in names:
            return names[self.code]
        else:
            return ''

    @property
    def description(self):
        """Returns the current status code's description."""
        if self.code in descriptions:
            return descriptions[self.code]
        else:
            return ''
