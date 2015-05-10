from mock_server.api import FilesMockProvider, Response
from email.parser import Parser
import requests

class CollectorProvider(FilesMockProvider):

    def __call__(self, request, status_code=200, format="json"):
        self._request = request
        self._status_code = status_code
        self._format = format

        target = self.routing(request)

        response = self.send_request(target, request)

        self.output(request, response)

        return response

    def routing(self, request):
        pass

    def send_request(self, target, request):
        response = Response()
        res = requests.get("http://%s:80/%s" % (target, request.path), headers=request.headers)
        response.content = res.text
        headers = []
        for key, value in res.headers.iteritems():
            headers.append("%s: %s" % (key, value))

        strip = lambda s: s if len(s) == 0 \
                   else s[0] + s[1:].strip()
        # response.headers = Parser().parsestr(
        #             "\r\n".join(map(strip, headers))).items() ##TODO
        return response

    def output(self, request, response):
        pass


provider = CollectorProvider(u"./a")
