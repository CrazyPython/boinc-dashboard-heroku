import web, time

urls = (
    '/internals/v0.01-ping(.*)', 'Ping',
    '//internals/v0.01-ping(.*)', 'Ping',
    '/', 'Dash',
)
app = web.application(urls, globals())

dash_html = '''


<!DOCTYPE html>
<html >

<head>
  <meta charset="UTF-8">
  <title>Boincoku Dashboard</title>
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
<script>
setTimeout("location.reload(true);", 60000);
</script>
      <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.98.0/js/materialize.min.js"></script>
      <span class="white-text number-center">
        {content}
        </span>
    </body>
  </html>
'''

last_seen_uuid = {}

def new_poke(uuid):
    last_seen_uuid[uuid] = time.time()

class Ping(object):
    def POST(self, uuid):
        new_poke(uuid)
        return 'Success'

class Dash(object):
    def GET(self):
        current_time = time.time()
        import vars_namespace
        if (vars_namespace.start_time + 15) > time.time():
            return dash_html.replace('{content}', '<i class="material-icons">autorenew</i>')

        result = 0
        seen_uuids = []
        for ping_uuid, ping_time in last_seen_uuid.items():
            # the below considers only pings within the last 15 secs
            if (current_time - ping_time) < 15:
                result += 1
                seen_uuids.append(ping_uuid)
            else:
                del last_seen_uuid[ping_uuid]
        print("UUIDs: " + str(seen_uuids))
        return dash_html.replace('{content}', str(result))

if __name__ == "__main__":
    import vars_namespace
    vars_namespace.start_time = time.time()
    app.run()
