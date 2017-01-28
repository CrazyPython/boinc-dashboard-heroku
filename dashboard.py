import web, time

urls = (
    '/internals/v0.01-ping(.*)', 'Ping',
    '/', 'Dash',
)
app = web.application(urls, globals())

dash_html = '''


<!DOCTYPE html>
<html >

<head>
  <meta charset="UTF-8">
  <title>BOINIC on Heroku Dashboard</title>
      <style>
      .number-center {
  font-size: 10em;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
    </style>
</head>

<body translate="no" >

    <html>
    <head>
      <link href="http://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
      <link type="text/css" rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.98.0/css/materialize.min.css"  media="screen,projection"/>

      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    </head>

    <body class="indigo lighten-1">
      <script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
      <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.98.0/js/materialize.min.js"></script>
      <span class="white-text number-center">
        {content}
        </span>
    </body>
  </html>
'''


pokes = []

def new_poke():
    pokes.append(time.time())

class Ping(object):
    def POST(self, uuid):
        new_poke()
        return 'Success'

class Dash(object):
    def GET(self):
        current_time = time.time()
        if (start_time + 15) < time.time():
            return dash_html.replace('{content}', '<i class="material-icons">autorenew</i>')

        result = 0
        for poke in pokes:
            if (current_time - poke) < 10:
                result += 1
            else:
                pokes.remove(poke)
        return dash_html.replace('{content}', str(result))

if __name__ == "__main__":
    start_time = time.time()
    app.run()
