import logging
import flowTrigger
import azure.function as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    url = req.params.get('url')
    if not url:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            url = req_body.get('url')

    if url:
        return func.HttpResponse(f"Hello {url}!")
    else:
        return func.HttpResponse(
             "Please pass a url on the query string or in the request body",
             status_code=400
        )
    flowTrigger.run(url)
