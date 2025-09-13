import requests, json

def main():
    api_key = "6fa6g2pdXGIyHRhVlGh7U56Ada1eF"
    template_id = "79667b2b1876e347"

    data = {
      "body": "<h1> hello world {{name}} </h1>",
      "css": "<style>.bg{background: red};</style>",
      "data": {
        "name": "This is a title"
      },
      "settings": {
        "paper_size": "A4",
        "orientation": "1",
        "header_font_size": "9px",
        "margin_top": "40",
        "margin_right": "10",
        "margin_bottom": "40",
        "margin_left": "10",
        "print_background": "1",
        "displayHeaderFooter": True,
        "custom_header": "<style>#header, #footer { padding: 0 !important; }</style>\n<table style=\"width: 100%; padding: 0px 5px;margin: 0px!important;font-size: 15px\">\n  <tr>\n    <td style=\"text-align:left; width:30%!important;\"><span class=\"date\"></span></td>\n    <td style=\"text-align:center; width:30%!important;\"><span class=\"pageNumber\"></span></td>\n    <td style=\"text-align:right; width:30%!important;\"><span class=\"totalPages\"></span></td>\n  </tr>\n</table>",
        "custom_footer": "<style>#header, #footer { padding: 0 !important; }</style>\n<table style=\"width: 100%; padding: 0px 5px;margin: 0px!important;font-size: 15px\">\n  <tr>\n    <td style=\"text-align:left; width:30%!important;\"><span class=\"date\"></span></td>\n    <td style=\"text-align:center; width:30%!important;\"><span class=\"pageNumber\"></span></td>\n    <td style=\"text-align:right; width:30%!important;\"><span class=\"totalPages\"></span></td>\n  </tr>\n</table>"
      }
    }

    response = requests.post(
        F"https://rest.apitemplate.io/v2/create-pdf-from-html",
        headers = {"X-API-KEY": F"{api_key}"},
        json= data
    )
    
    print(response.json())

if __name__ == "__main__":
    main()
