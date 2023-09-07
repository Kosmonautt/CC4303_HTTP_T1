import json
import aux_functions as aux

string = '''{ 
        "atributos": [ 
            { 
    "Age":"197374", 
"Cache-Control":"max-age=604800", 
"Content-Type":"text/html; charset=UTF-8", 
"Date":"Wed, 06 Sep 2023 23:51:59 GMT", 
"Etag":""3147526947+ident"", 
"Expires":"Wed, 13 Sep 2023 23:51:59 GMT", 
"Last-Modified":"Thu, 17 Oct 2019 07:18:26 GMT", 
"Server":"ECS (mic/9A9C)", 
"Vary":"Accept-Encoding", 
"X-Cache":"HIT", 
"Content-Length":"1256"
 }
     ]
    }''' 




string = '''{ 
        "atributos": [ 
            { 
    "Age":"197374", 
"Cache-Control":"max-age=604800", 
"Content-Type":"text/html; charset=UTF-8", 
"Date":"Wed, 06 Sep 2023 23:51:59 GMT", 
"Etag":""3147526947+ident"", 
"Expires":"Wed, 13 Sep 2023 23:51:59 GMT", 
"Last-Modified":"Thu, 17 Oct 2019 07:18:26 GMT", 
"Server":"ECS (mic/9A9C)", 
"Vary":"Accept-Encoding", 
"X-Cache":"HIT", 
"Content-Length":"1256"
 }
     ]
    }''' 

string2 = '''
HTTP/1.1 200 OK\r
Age: 504141\r
Cache-Control: max-age=604800\r
Content-Type: text/html; charset=UTF-8\r
Date: Thu, 07 Sep 2023 00:02:43 GMT\r
Etag: "3147526947+gzip+ident"\r
Expires: Thu, 14 Sep 2023 00:02:43 GMT\r
Last-Modified: Thu, 17 Oct 2019 07:18:26 GMT\r
Server: ECS (mic/9A9E)\r
Vary: Accept-Encoding\r
X-Cache: HIT\r
Content-Length: 1256\r
\r
<!doctype html>
<html>
<head>
    <title>Example Domain</title>

    <meta charset="utf-8" />
    <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style type="text/css">
    body {
        background-color: #f0f0f2;
        margin: 0;
        padding: 0;
        font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;
        
    }
    div {
        width: 600px;
        margin: 5em auto;
        padding: 2em;
        background-color: #fdfdff;
        border-radius: 0.5em;
        box-shadow: 2px 3px 7px 2px rgba(0,0,0,0.02);
    }
    a:link, a:visited {
        color: #38488f;
        text-decoration: none;
    }
    @media (max-width: 700px) {
        div {
            margin: 0 auto;
            width: auto;
        }
    }
    </style>    
</head>

<body>
<div>
    <h1>Example Domain</h1>
    <p>This domain is for use in illustrative examples in documents. You may use this
    domain in literature without prior coordination or asking for permission.</p>
    <p><a href="https://www.iana.org/domains/example">More information...</a></p>
</div>
</body>
</html>

'''

strcuture = aux.parse_HTTP_message(string2)