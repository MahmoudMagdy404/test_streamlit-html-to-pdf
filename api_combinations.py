html_body = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prior Authorization Prescription Request Form</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.4; font-size: 12px; width: 210mm; height: 297mm; margin: 0 auto; padding: 15mm 10mm; box-sizing: border-box;">
    <div style="text-align: center; margin-bottom: 15px;">
        <h2 style="font-size: 14px; margin: 0 0 10px; font-weight: bold;">PRIOR AUTHORIZATION PRESCRIPTION REQUEST FORM FOR BACK ORTHOSIS</h2>
        <p style="margin: 0; font-size: 10px; font-weight: bold;">PLEASE SEND THIS FORM BACK IN 3 BUSINESS DAYS</p>
        <p style="margin: 0; font-size: 10px;font-weight: bold;">WITH THE PT CHART NOTES (RECENT MEDICAL RECORDS) AND THE FAX COVER SHEET</p>
    </div>

    <div style="display: flex; margin-top: 15px;">
        <div style="width: 48%; border: 1px solid black; padding: 10px; box-sizing: border-box;">
            <div style="display: flex; justify-content: space-between;">
                <div style="width: 48%;">
                    <div style="margin-bottom: 8px;"><span style="font-weight: bold;">Date:</span> {date}</div>
                    <div style="margin-bottom: 8px;"><span style="font-weight: bold;">First:</span> {fname}</div>
                    <div style="margin-bottom: 8px;"><span style="font-weight: bold;">DOB:</span> {dob}</div>
                    <div style="margin-bottom: 8px;"><span style="font-weight: bold;">Address:</span> {address}</div>
                    <div style="margin-bottom: 8px;"><span style="font-weight: bold;">City:</span> {city}</div>
                    <div style="margin-bottom: 8px;"><span style="font-weight: bold;">State:</span> {state}</div>
                    <div style="margin-bottom: 8px;"><span style="font-weight: bold;">Postal Code:</span> {zip}</div>
                    <div style="margin-bottom: 8px;"><span style="font-weight: bold;">Patient Phone:</span> {phone}</div>
                    <div style="margin-bottom: 8px;"><span style="font-weight: bold;">Primary Ins:</span> Medicare</div>
                    <div style="margin-bottom: 8px;"><span style="font-weight: bold;">Weight:</span> {weight}</div>
                </div>
                <div style="width: 48%;">
                    <div style="margin-bottom: 8px;"><span style="font-weight: bold;">&nbsp;</span></div>
                    <div style="margin-bottom: 8px;"><span style="font-weight: bold;">Last:</span> {lname}</div>
                    <div style="margin-bottom: 8px;"><span style="font-weight: bold;">Gender:</span> {gender}</div>
                    <div style="margin-bottom: 8px;"><span style="font-weight: bold;">&nbsp;</span></div>
                    <div style="margin-bottom: 8px;"><span style="font-weight: bold;">&nbsp;</span></div>
                    <div style="margin-bottom: 8px;"><span style="font-weight: bold;">&nbsp;</span></div>
                    <div style="margin-bottom: 8px;"><span style="font-weight: bold;">&nbsp;</span></div>
                    <div style="margin-bottom: 8px;"><span style="font-weight: bold;">&nbsp;</span></div>
                    <div style="margin-bottom: 8px;"><span style="font-weight: bold;">Policy #:</span> {medID}</div>
                    <div style="margin-bottom: 8px;"><span style="font-weight: bold;">Height:</span> {height}</div>
                </div>
            </div>
        </div>
        <div style="width: 48%; border: 1px solid black; padding: 10px; box-sizing: border-box;">
            <div style="margin-bottom: 8px;"><span style="font-weight: bold;">Physician Name:</span> {doctor_name}</div>
            <div style="margin-bottom: 8px;"><span style="font-weight: bold;">NPI:</span> {doctor_npi}</div>
            <div style="margin-bottom: 8px;"><span style="font-weight: bold;">Address:</span> {doctor_address}</div>
            <div style="margin-bottom: 8px;"><span style="font-weight: bold;">City:</span> {doctor_city}</div>
            <div style="margin-bottom: 8px;"><span style="font-weight: bold;">State:</span> {doctor_state}</div>
            <div style="margin-bottom: 8px;"><span style="font-weight: bold;">Postal Code:</span> {doctor_zip}</div>
            <div style="margin-bottom: 8px;"><span style="font-weight: bold;">Phone Number:</span> {doctor_phone}</div>
            <div style="margin-bottom: 8px;"><span style="font-weight: bold;">Fax Number:</span> {doctor_fax}</div>
        </div>
    </div>
    <div style="display: grid; gap: 3px; font-size: 8px;">
        This patient is being treated under a comprehensive plan of care for lance pain.
        I, the undersigned, certify that the prescribed orthosis is medically necessary for the patient's overall well-being. In my opinion, the following lance orthosis products are both reasonable and necessary in reference to treatment of the patient's condition and/or rehabilitation. My patient has been in care regarding the diagnosis below. This is the treatment I see fit for this patient at this time. I certify that this information is true and correct.
    </div>
    <div style="font-weight: bold; margin-top: 15px; margin-bottom: 10px;">DIAGNOSIS: Provider can specify all of the diagnoses they feel are appropriate</div>
    <div style="display: grid; gap: 6px;">
        <div><input type="checkbox" style="margin-right: 5px;">Lumbar Intervertebral Disc Degeneration (M51.36)</div>
        <div><input type="checkbox" style="margin-right: 5px;">Other intervertebral disc displacement, lumbar region (M51.26)</div>
        <div><input type="checkbox" style="margin-right: 5px;">Spinal Stenosis, lumbar region (M48.06)</div>
        <div><input type="checkbox" style="margin-right: 5px;">Spinal instability, lumbosacral region (M53.2X7)</div>
        <div><input type="checkbox" style="margin-right: 5px;">Other intervertebral disc disorders, lumbosacral region (M51.87)</div>
        <div><input type="checkbox" style="margin-right: 5px;">Low back pain (M54.5)</div>
    </div>

    <div style="font-weight: bold; margin-top: 15px; margin-bottom: 10px;">AFFECTED AREA</div>
    <div><input type="checkbox" style="margin-right: 5px;">Back</div>

    <p style="margin-top: 15px;">Our evaluation of the above patient has determined that providing the following Back orthosis products will benefit this patient.</p>

    <div style="font-weight: bold; margin-top: 15px; margin-bottom: 10px;">DISPENSE</div>
    <p style="margin-bottom: 10px; font-size: 10px;">{Selected_Brace} - {Brace_info}</p>
    <p>____________________________________________________________________________________________________________</p>
    <p>Length of need is 99 months unless otherwise specified: ____________ 99-99 (LIFETIME)</p>

    <table style="width: 100%; margin-top: 20px; font-size: 10px;">
        <tbody>
            <tr>
                <td>
                    <div style="font-weight: bold;">Physician Name: {doctor_name}</div> 
                    <div style="margin-top: 8px;">Physician Signature: _________________________</div>
                </td>
                <td>
                    <div style="font-weight: bold;">NPI: {doctor_npi}</div> 
                    <div style="margin-top: 8px;">Date signed: _________________________</div>
                </td>
            </tr>
        </tbody>
    </table>
</body>
</html>
    """




'''
jimmyross.incall
mahmoodmagdy0
mahmoodmagdy9
mahmoud.ismail02@eng-st.cu.edu.eg
clansmclash
gacc1746
'''

#600
#bad format
pdfzone_apis = [
    "ecacc4b008de61997f40fbe7cee3ca54",
    "5d9cdf114c7018e1f457c66150da8449",
    "aaea4f134b51eff8c726b6d137c3f5b4",
    "b3fd9a23b7f5a10b4a405c6d5b2d22b3",
    "1dbb79142bffc31082dd7ad01246decd",
    "017caae97de98745897e27692d7f8178",

]
#600--Done
html2pdf_apis = [
    "RVmMwrJE4qYEJ8ecSx5FiDj8qNrXT0LWL3mAZxmUQmqfrUPfXJmC4ODAAWeLhPOt",
    "I3FdbrKGuP3pchk4s8N7ebgaLdxY8RFEzsj37CETM7sYHkrXaU3PsuUm69Nrjgdf",
    "fw91rYNv92tXW03wxHpxCqvBZDJh56NZBoF6lw0TgTemxvxV7Rcm7Y43PrUAmUiG",
    "3l5z6Mo4DdXXfvmXeYJPZ2YbUP8WfKZz31Pi4ndiGgrfxFF82lWOoOlqTnKdiTme",
    "GNE9ouYeVk1gY8dDlkoeTo0CS1b1dP3mG09Lrk57yMLKDF1dN7BYu9fdWVo6cirj",
    "rKwARuw7JvZI8pdXKNuJH61vgfrduSjocaEku75zvGHdZbYguamWzp67FVSFHlkT",
]


#600
#bad format
pdflayer_apis = [
    "0f481c639c8c5b0e760dbe883ae6c43a",
    "2e7ac19928118d7bc11791ffde644d2c",
    "7a50d5e790acb42a69a8e76015a67df6",
    "f7c98ffd190eee89a2e5f1fec3a12e46",
    "a42708f50f6ebdefee36b8f7058b2fb0",
    "5a9d71c2da2b55594b677d5edf284c8c",

]


#300--Done
pdfshift_apis = [
    
    "sk_936040effdad68ec1c289f852f896fa776e49e82",
    "sk_2cd1735aacdab71534de2aea859fd568c0319ec3",
    "sk_5d0c9b0e8a20181969dfbe65cc9c2bf406406b4e",
    "sk_e0245bf44df037679826706cebedaa3a7875eb78",
    "sk_1412ed9ec421b21cc847a26209230355ae70245a",
    "sk_b2f608ef156ad4c3b4862b3c892de6dfc94eb7d2",
 
]
#250 / api 
#https://rapidapi.com/rhodium/api/html2pdf2/playground/apiendpoint_9b1017c6-2f56-4b7e-80d5-0fe24937d398
rapidapi_html2pdf = [
    "8f9d8213a1mshf4d5b4dc3114c2cp13bd70jsn5c6833d67b85",
    "071f529cf4mshc3fddeacd226129p10e5b5jsnc5cfee106eba",
    "c8956886femsh11204b56cabb1bep1262a7jsnef7b1828fc5a",
    "4cf8a69d3fmsh36c9746b748981ap1c3c04jsn69ee7200b469",
    "8c2a57e3ebmsh5165cca494f2787p15f6bcjsnf8a3bd7d077f",
    "5f91b37572msh52ba8395747d7cfp128e9fjsn0354eefd6737",

]

# 2400 Total Request
import requests





import json
import requests
import base64
import streamlit as st

def html2pdf_rapidapi(api_key, html_body, document_url=None):
    url = "https://html2pdf2.p.rapidapi.com/html2pdf"
    payload = {"html": html_body}
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "html2pdf2.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response)
    return response



def create_download_link(content, filename):
    if isinstance(content, bytes):
        # If content is binary, assume it's PDF data that needs to be base64 encoded
        b64 = base64.b64encode(content).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}.pdf">Download PDF</a>'
    elif isinstance(content, str):
        # If content is a string, assume it's a URL
        href = f'<a href="{content}" download="{filename}.pdf">Download PDF</a>'
    else:
        raise ValueError("Content type not supported for download link.")
    return href


def pdfshift_request(api_key, html_body, document_url=None):
    response = requests.post(
        'https://api.pdfshift.io/v3/convert/pdf',
        auth=('api', api_key),
        json={
            "source": html_body,
            "landscape": False,
            "use_print": False
        }
    )
    print (response.json())
    return response


def pdfzone_request(api_key, html_body, document_url=None):
    API_URL = "https://pdfzoneapi.com/api/v1/convert"
    payload = {
        "access_key": api_key,
        "document_html": html_body,
    }
    if document_url:
        payload["document_url"] = document_url
    return requests.post(API_URL, data=payload)

def html2pdf_request(api_key: str, html_body: str, document_url: str = None ) -> requests.Response:
    html_url = html_body
    user_password = "user"
    owner_password = "owner"
    permissions = ["print", "modify", "copy"]

    # Prepare the request data
    data = {
        "apiKey": api_key,
        "html": html_url,
        # "userPassword": user_password,
        # "ownerPassword": owner_password,
        "permissions": permissions
    }

    # Set the headers
    headers = {'Content-Type': 'application/json'}

    # Send the POST request
    response = requests.post(
        url="https://api.html2pdf.app/v1/generate", headers=headers, json=data
    )
    print(response.json)
    return response

def pdflayer_request(api_key: str, html_body: str, document_url: str = None) -> requests.Response:
    API_URL = f"https://api.pdflayer.com/api/convert?access_key={api_key}"
    payload = {
        "document_html": html_body,
        "inline": 1,
        "export": 1,
    }
    if document_url:
        payload["document_url"] = document_url
    
    # Print the URL and payload for debugging
    st.write(f"API URL: {API_URL}")
    st.write(f"Payload: {payload}")
    
    response = requests.post(API_URL, data=payload)
    
    # # Print debug information
    # st.write(f"Response status code: {response.status_code}")
    # st.write(f"Response headers: {response.headers}")
    # st.write(f"Response content length: {len(response.content)}")
    # st.write(f"Response content: {response.text}")
    
    return response



def main():
    
    html_body = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Prior Authorization Prescription Request Form</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.4;
                font-size: 12px;
                width: 210mm;
                height: 297mm;
                margin: 0 auto;
                padding: 15mm 10mm;
                box-sizing: border-box;
            }

            h2 {
                font-size: 14px;
                margin: 0 0 10px;
                font-weight: bold;
            }

            p {
                margin: 0;
                font-size: 10px;
                font-weight: bold;
            }

            .container {
                text-align: center;
                margin-bottom: 15px;
            }

            .flex-container {
                display: flex;
                margin-top: 15px;
            }

            .half-width {
                width: 48%;
                border: 1px solid black;
                padding: 10px;
                box-sizing: border-box;
            }

            .inner-container {
                display: flex;
                justify-content: space-between;
            }

            .inner-half {
                width: 48%;
            }

            .grid {
                display: grid;
                gap: 3px;
                font-size: 8px;
            }

            .bold {
                font-weight: bold;
                margin-top: 15px;
                margin-bottom: 10px;
            }

            .checkbox-container {
                display: grid;
                gap: 6px;
            }

            input[type="checkbox"] {
                margin-right: 5px;
            }

            table {
                width: 100%;
                margin-top: 20px;
                font-size: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>PRIOR AUTHORIZATION PRESCRIPTION REQUEST FORM FOR BACK ORTHOSIS</h2>
            <p>PLEASE SEND THIS FORM BACK IN 3 BUSINESS DAYS</p>
            <p>WITH THE PT CHART NOTES (RECENT MEDICAL RECORDS) AND THE FAX COVER SHEET</p>
        </div>

        <div class="flex-container">
            <div class="half-width">
                <div class="inner-container">
                    <div class="inner-half">
                        <div style="margin-bottom: 8px;"><span class="bold">Date:</span> {date}</div>
                        <div style="margin-bottom: 8px;"><span class="bold">First:</span> {fname}</div>
                        <div style="margin-bottom: 8px;"><span class="bold">DOB:</span> {dob}</div>
                        <div style="margin-bottom: 8px;"><span class="bold">Address:</span> {address}</div>
                        <div style="margin-bottom: 8px;"><span class="bold">City:</span> {city}</div>
                        <div style="margin-bottom: 8px;"><span class="bold">State:</span> {state}</div>
                        <div style="margin-bottom: 8px;"><span class="bold">Postal Code:</span> {zip}</div>
                        <div style="margin-bottom: 8px;"><span class="bold">Patient Phone:</span> {phone}</div>
                        <div style="margin-bottom: 8px;"><span class="bold">Primary Ins:</span> Medicare</div>
                        <div style="margin-bottom: 8px;"><span class="bold">Weight:</span> {weight}</div>
                    </div>
                    <div class="inner-half">
                        <div style="margin-bottom: 8px;"><span class="bold">&nbsp;</span></div>
                        <div style="margin-bottom: 8px;"><span class="bold">Last:</span> {lname}</div>
                        <div style="margin-bottom: 8px;"><span class="bold">Gender:</span> {gender}</div>
                        <div style="margin-bottom: 8px;"><span class="bold">&nbsp;</span></div>
                        <div style="margin-bottom: 8px;"><span class="bold">&nbsp;</span></div>
                        <div style="margin-bottom: 8px;"><span class="bold">&nbsp;</span></div>
                        <div style="margin-bottom: 8px;"><span class="bold">&nbsp;</span></div>
                        <div style="margin-bottom: 8px;"><span class="bold">&nbsp;</span></div>
                        <div style="margin-bottom: 8px;"><span class="bold">Policy #:</span> {medID}</div>
                        <div style="margin-bottom: 8px;"><span class="bold">Height:</span> {height}</div>
                    </div>
                </div>
            </div>
            <div class="half-width">
                <div style="margin-bottom: 8px;"><span class="bold">Physician Name:</span> {doctor_name}</div>
                <div style="margin-bottom: 8px;"><span class="bold">NPI:</span> {doctor_npi}</div>
                <div style="margin-bottom: 8px;"><span class="bold">Address:</span> {doctor_address}</div>
                <div style="margin-bottom: 8px;"><span class="bold">City:</span> {doctor_city}</div>
                <div style="margin-bottom: 8px;"><span class="bold">State:</span> {doctor_state}</div>
                <div style="margin-bottom: 8px;"><span class="bold">Postal Code:</span> {doctor_zip}</div>
                <div style="margin-bottom: 8px;"><span class="bold">Phone Number:</span> {doctor_phone}</div>
                <div style="margin-bottom: 8px;"><span class="bold">Fax Number:</span> {doctor_fax}</div>
            </div>
        </div>
        <div class="grid">
            This patient is being treated under a comprehensive plan of care for lance pain.
            I, the undersigned, certify that the prescribed orthosis is medically necessary for the patient's overall well-being. In my opinion, the following lance orthosis products are both reasonable and necessary in reference to treatment of the patient's condition and/or rehabilitation. My patient has been in care regarding the diagnosis below. This is the treatment I see fit for this patient at this time. I certify that this information is true and correct.
        </div>
        <div class="bold">DIAGNOSIS: Provider can specify all of the diagnoses they feel are appropriate</div>
        <div class="checkbox-container">
            <div><input type="checkbox">Lumbar Intervertebral Disc Degeneration (M51.36)</div>
            <div><input type="checkbox">Other intervertebral disc displacement, lumbar region (M51.26)</div>
            <div><input type="checkbox">Spinal Stenosis, lumbar region (M48.06)</div>
            <div><input type="checkbox">Spinal instability, lumbosacral region (M53.2X7)</div>
            <div><input type="checkbox">Other intervertebral disc disorders, lumbosacral region (M51.87)</div>
            <div><input type="checkbox">Low back pain (M54.5)</div>
        </div>

        <div class="bold">AFFECTED AREA</div>
        <div><input type="checkbox">Back</div>

        <p style="margin-top: 15px;">Our evaluation of the above patient has determined that providing the following Back orthosis products will benefit this patient.</p>

        <div class="bold">DISPENSE</div>
        <p style="margin-bottom: 10px; font-size: 10px;">{Selected_Brace} - {Brace_info}</p>
        <p>____________________________________________________________________________________________________________</p>
        <p>Length of need is 99 months unless otherwise specified: ____________ 99-99 (LIFETIME)</p>

        <table>
            <tbody>
                <tr>
                    <td>
                        <div class="bold">Physician Name: {doctor_name}</div> 
                        <div style="margin-top: 8px;">Physician Signature: _________________________</div>
                    </td>
                    <td>
                        <div class="bold">NPI: {doctor_npi}</div> 
                        <div style="margin-top: 8px;">Date signed: _________________________</div>
                    </td>
                </tr>
            </tbody>
        </table>
    </body>
    </html>"""
    st.title("PDF Converter")

    # Get input from user
    html_body = html_body
    document_url = st.text_input("Or enter a URL to convert (optional)")

    if st.button("Convert to PDF"):
        # Randomly choose an API key (this is just an example, you should implement a proper key management system)
        api_key = "GNE9ouYeVk1gY8dDlkoeTo0CS1b1dP3mG09Lrk57yMLKDF1dN7BYu9fdWVo6cirj"

        # Determine which service the API key belongs to
        if api_key in pdfzone_apis:
            response = pdfzone_request(api_key, html_body, document_url)
        elif api_key in pdfshift_apis:
            response = pdfshift_request(api_key, html_body, document_url)
        elif api_key in html2pdf_apis:
            response = html2pdf_request(api_key, html_body, document_url)
        elif api_key in pdflayer_apis:
            response = pdflayer_request(api_key, html_body, document_url)
        elif api_key in rapidapi_html2pdf:
            response = html2pdf_rapidapi(api_key, html_body, document_url)
        else:
            st.error("API key not recognized")
            st.stop()

        # Handle the response
        if response.status_code == 200:
            try:
                json_response = response.json()
                if 'pdf' in json_response:
                    # The PDF content is base64 encoded
                    pdf_content = base64.b64decode(json_response['pdf'])
                    html = create_download_link(pdf_content, "result")  # Base64 decoded content
                elif 'url' in json_response:
                    pdf_url = json_response['url']
                    html = create_download_link(pdf_url, "result")  # Direct URL link
                else:
                    st.error("Unexpected response format.")
                    st.stop()
            except json.JSONDecodeError:
                st.error("Error decoding JSON response.")
                st.stop()

            st.markdown(html, unsafe_allow_html=True)
        else:
            st.error(f"Error generating PDF: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main()




