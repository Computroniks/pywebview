import webview
import threading
import time
import sys
import random
import json

'''
This example demonstrates how to create a pywebview api without using a web server
'''

html='''
<!DOCTYPE html>
<html>
<head lang="en">
<meta charset="UTF-8"> 

<style>
    #response-container {
        display: none;
        padding: 3rem;
        margin: 3rem 5rem;
        font-size: 120%;
        border: 5px dashed #ccc;
    }
    
    button {
        font-size: 100%;
        padding: 0.5rem;
        margin: 0.3rem;
        text-transform: uppercase;
    }

</style>
</head>
<body>


<h1>JS API Example</h1>
<button onClick="initialize()">Init App</button><br/>
<button onClick="doHeavyStuff()">Perform a heavy operation</button><br/>
<button onClick="getRandomNumber()">Get a random number</button><br/>

<div id="response-container"></div>
<script>
function showResponse(response) {
    var container = document.getElementById('response-container')
    
    container.innerText = response.message
    container.style.display = 'block'
}

function initialize() {
    pywebview.api.init().then(showResponse)
}

function doHeavyStuff() {
    pywebview.api.do_heavy_stuff().then(showResponse)
    showResponse({message: 'Working...'})
}

function getRandomNumber() {
    pywebview.api.get_random_number().then(showResponse)
}

</script>
</body>
</html>
'''


class Api:
    def init(self, params):
        response = {
            'message': 'Hello from Python {0}'.format(sys.version)
        }
        return response

    def get_random_number(self, params):
        response = {
            'message': 'Here is a random number cortesy of randint: {0}'.format(random.randint(0, 100000000))
        }
        return response


    def do_heavy_stuff(self, params):
        time.sleep(0.1) # sleep to prevent from the ui thread from freezing for a moment
        now = time.time()
        for i in range(0, 100000000):
            pass
        then = time.time()
        response = {
            'message': 'Operation took {0:.1f} seconds on the thread {1}'.format((then - now), threading.current_thread())
        }
        return response


def create_app():
    webview.load_html(html)
    api = Api()
    webview.set_js_api(api)


if __name__ == '__main__':
    t = threading.Thread(target=create_app)
    t.start()

    webview.create_window('API example', debug=True)

