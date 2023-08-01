# A WPS server using PyWPS + Gunicorn + Nginx inside Docker.

1. Install Docker, Docker compose.

2. Clone this repo, run cmd below to host WPS server inside Docker:

Install all libraries were listed in requirements.txt. It is advisable to run it in a python virtual environment.

```console
pip install -r pywps/requirements.txt
```

Build and run docker as a Production environment. Port 80.

```console
bash run_docker.sh
```

Flask application in  `./pywps/app.py` was used as a Development environment. Port 5000.

```console
python app.py -a
```

Nginx: proxy server port 80.

Gunicorn: application server port 5000. Notice: this port is in docker network.

## Code in `./pywps/processes` folder.

Example request:

```
http://localhost/wps?request=Execute&service=WPS&identifier=say_hello&version=1.0.0&dataInputs=name=world
```

Response:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<wps:ExecuteResponse xmlns:wps="http://www.opengis.net/wps/1.0.0" xmlns:ows="http://www.opengis.net/ows/1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wps/1.0.0 ../wpsExecute_response.xsd" service="WPS" version="1.0.0" xml:lang="en-US" serviceInstance="http://localhost:5000/wps?request=GetCapabilities&amp;amp;service=WPS" statusLocation="">
    <wps:Process wps:processVersion="1.3.3.7">
        <ows:Identifier>say_hello</ows:Identifier>
        <ows:Title>Process Say Hello</ows:Title>
        <ows:Abstract>Returns a literal string output             with Hello plus the inputed name</ows:Abstract>
	</wps:Process>
    <wps:Status creationTime="2023-07-29T05:10:19Z">
        <wps:ProcessSucceeded>PyWPS Process Process Say Hello finished</wps:ProcessSucceeded>
	</wps:Status>
	<wps:ProcessOutputs>
		<wps:Output>
            <ows:Identifier>response</ows:Identifier>
            <ows:Title>Output response</ows:Title>
            <ows:Abstract></ows:Abstract>
			<wps:Data>
                <wps:LiteralData uom="urn:ogc:def:uom:OGC:1.0:unity" dataType="string">Hello             world, 8516ee06677c</wps:LiteralData>
			</wps:Data>
		</wps:Output>
	</wps:ProcessOutputs>
</wps:ExecuteResponse>
```