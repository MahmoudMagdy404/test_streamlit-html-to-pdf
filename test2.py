from datetime import datetime, timezone
import os
import tempfile
import time
import pandas as pd
from urllib.parse import urlencode, quote_plus
import requests
from PyPDF2 import PdfMerger, PdfReader
import re
import base64
import streamlit as st
import io
import json
# import google.auth
# from faxplus import ApiClient, OutboxApi, OutboxComment, RetryOptions, OutboxOptions, OutboxCoverPage, PayloadOutbox , FilesApi 
# from faxplus.configuration import Configuration
# from faxplus.rest import ApiException
# import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import logging
import random
cgm_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Combined PDF</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            font-size: 12px;
            margin: 40px;
            padding: 20px;
            box-sizing: border-box;
            font-weight: bold;
        }
        .header { display: flex; justify-content: space-between; align-items: center; }
        .header h1 { color: blue; margin: 0; }
        .logo { font-weight: bold; text-align: right; }
        .instructions { font-size: 10px; }
        .patient-info, .diagnosis, .insulin-regimen, .order-detail { margin-bottom: 10px; }
        .order-detail table { width: 100%; border-collapse: collapse; }
        .order-detail th, .order-detail td { border: 1px solid black; padding: 5px; }
        .signature-line { border-top: 1px solid black; width: 200px; margin-top: 20px; }
        .small-print { font-size: 8px; }
        .container { width: 80%; margin: 0 auto; }
        .checkbox-list { list-style-type: none; padding-left: 0; }
        .checkbox-list li { margin-bottom: 5px; }
    </style>
</head>
<body>

    <!-- Page 1 -->
    <div class="header">
        <h1>Standard Written Order <span style="font-size: 24px;">🦋</span><br>for Continuous Glucose Monitoring and Supplies</h1>
        <div class="logo">FreeStyle<br>Libre 2</div>
    </div>

    <div class="instructions">
        <h3>Instructions</h3>
        <ol>
            <li>Complete all fields on this Standard Written Order.</li>
            <li>For Medicare: Use the National Clinician Resource Letter (Continuous Glucose Monitors) to confirm coverage criteria and medical necessity documentation requirements are met*.</li>
            <li>Fax both this order and the patient's most recent medical records that demonstrate coverage criteria are met by a DME supplier that provides the FreeStyle Libre 2 system.</li>
        </ol>
    </div>

    <div class="patient-info">
        <h3>Patient Information</h3>
        <p>Patient Name: ${patient_name}     Date of Birth: ${date_of_birth}</p>
        <p>Phone: ${phone_number}     Email: ${email}</p>
        <p>Address: ${address}  City: ${city} State: ${state} ZIP: ${zip_code}</p>
        <p>Primary Insurance: ${primary_insurance} Primary Insurance Member ID: ${primary_insurance_id}</p>
        <p>Secondary Insurance: ${secondary_insurance} Secondary Insurance Member ID: ${secondary_insurance_id}</p>
        <p>Notes: ${notes}</p>
    </div>

    <div class="diagnosis">
        <h3>Diagnosis (ICD10) Per Provider:</h3>
        <input type="checkbox"> E10.9   <input type="checkbox"> E11.65   <input type="checkbox"> E10.65   <input type="checkbox"> E11.8   <input type="checkbox"> E11.9   <input type="checkbox"> Other: ________
    </div>

    <div class="insulin-regimen">
        <h3>Current Insulin Regimen:</h3>
        <input type="checkbox" checked> Insulin Pump   <input type="checkbox"> Multiple Daily Injections -Number Per Day: ________   <input type="checkbox"> Other: ________
    </div>

    <div class="order-detail">
        <h3>Order Detail</h3>
        <table>
            <tr>
                <th>FreeStyle Libre 2 Reader E2103</th>
                <th>FreeStyle Libre 2 Sensors A4239</th>
            </tr>
            <tr>
                <td>
                    Use per manufacturer guidelines and/or provide further detail here:<br><br>
                    Duration of need: Lifetime - unless specified otherwise:
                </td>
                <td>
                    Change Sensor every 14 days<br>
                    Dispense up to 90 day supply<br>
                    Duration of need: Lifetime - unless specified otherwise:
                </td>
            </tr>
        </table>
    </div>

    <div style="background-color: black; color: white; text-align: center; padding: 5px;">
        DISPENSE AS WRITTEN
    </div>

    <p>I certify that I am the physician identified in the "Physician Information" section below and hereby attest that the medical necessity information on this form is true, accurate and complete, to the best of my knowledge. I understand that any falsification, omission, or concealment of material fact may subject me to administrative, civil, or criminal liability. The patient/caregiver is capable and has successfully completed or will be trained on the proper use of the products prescribed on this order.</p>

    <div class="signature-line"></div>
    <p>Physician Signature: ___________________________ Date: ______________</p>

    <div class="physician-info">
        <h3>Physician Information</h3>
        <p>Physician Name: ${physician_name}   Phone: ${physician_phone}</p>
        <p>NPI: ${npi}   Fax: ${fax}</p>
        <p>Address: ${physician_address_line1}, ${physician_address_line2}, ${physician_city} ${physician_state}</p>
        <p>Office Contact: ___________________________ Notes: ___________________________</p>
    </div>

    <p class="small-print">
        Abbott provides this information as a courtesy. It is subject to change and interpretation. The customer is ultimately responsible for determining the appropriate codes, coverage, and payment policies for individual patients. Abbott does not guarantee third party coverage or payment for our products or reimburse customers for claims that are denied by third party payors.<br>
        *For Local Coverage Determination (L33822)<br>
        Please see https://www.cms.gov/medicare-coverage-database/view/lcd.aspx?lcdid=33822&ver=52 for more information.<br>
        See important safety information on reverse.
    </p>

    <!-- Page 2 -->
    <div class="container">
        <h1>Certification of Medical Necessity Diabetes Supplies: Glucose Sensors</h1>
        
        <p>Date: ${certification_date}</p>
        
        <div class="patient-info">
            <p>Patient's Name: ${patient_name}</p>
            <p>Patient's Date of Birth: ${date_of_birth}</p>
        </div>
        
        <p>To Whom It May Concern:</p>
        
        <p>This letter serves as a Prescription and Letter of Medical Necessity for the above-referenced patient for glucose sensors as part of their diabetes supplies. The following prerequisites have been met:</p>
        
        <ul class="checkbox-list">
            <li><input type="checkbox"> Patient has a history of severe hypoglycemia requiring assistance.</li>
            <li><input type="checkbox"> Patient has experienced unawareness of hypoglycemic episodes.</li>
            <li><input type="checkbox"> Patient has a history of labile glucose control despite optimal therapy regimes.</li>
            <li><input type="checkbox"> Patient has a sub-optimal A1c level or glucose target despite optimal therapy regimes.</li>
            <li><input type="checkbox"> Patient has a history of nocturnal hypoglycemia.</li>
            <li><input type="checkbox"> Patient demonstrates compliance to prescribed regimen and the willingness to attend regular medical follow-up exams.</li>
            <li><input type="checkbox"> Patient agrees to work with their physician, nurse educator and dietitian to ensure correct device use.</li>
        </ul>
        
        <p>I certify that this information is correct. The use of Continuous Glucose sensing technology has been proven to lower HbA1c resulting in improved diabetes control, decrease of the risk of hypoglycemia, and reduction of diabetes-related complications. The necessity of these supplies is to ensure the patient’s ability to maintain proper glycemic control and reduce the long-term risk of complications associated with diabetes.</p>
        
        <div class="signature-line"></div>
        <p>Physician's Signature: ___________________________</p>
        <p>Date: ___________________________</p>
    </div>

</body>
</html>
"""


def display_cgm_form():
    st.title("CGM Form Submission")
    st.header("Patient and Doctor Information")
    # Create rows with aligned fields
    with st.container():
                        # Row 1
        col1, col2, col3 = st.columns([1, 1, 1])  # Adjust proportions if needed

        with col1:
            st.subheader("Patient Information")
        with col2:
            st.subheader("Patient Metrics")
        with col3:
            st.subheader("Doctor Information")
        col1, col2,col3 = st.columns(3)
        
        with col1:
            date = st.date_input("Date")
            pt_name = st.text_input("Full Name")
            ptPhone = st.text_input("Patient Phone Number")
            ptAddress = st.text_input("Patient Address")
            ptCity = st.text_input("Patient City")
            ptState = st.text_input("Patient State")
            ptZip = st.text_input("Patient Zip Code")

        with col2:
            ptDob = st.text_input("Date of Birth")
            primary_insurance_name = st.text_input("Primary Insurance Name")
            primary_insurance_id = st.text_input("Primary Insurance ID")
            secondary_insurance_name = st.text_input("Secondary Insurance Name")
            secondary_insurance_id = st.text_input("Secondary Insurance ID")
        with col3:
            drName = st.text_input("Doctor Name")
            drAddress = st.text_input("Doctor Address")
            drCity = st.text_input("Doctor City")
            drState = st.text_input("Doctor State")
            drZip = st.text_input("Doctor Zip Code")
            drPhone = st.text_input("Doctor Phone Number")
            drFax = st.text_input("Doctor Fax Number")
            drNpi = st.text_input("Doctor NPI")
            notes = st.text_area("Notes")

        # Submit Button
        st.markdown("<br>", unsafe_allow_html=True)
        

    def validate_all_fields():
        required_fields = [
            date, pt_name, ptPhone, ptAddress,
            ptCity, ptState, ptZip, ptDob, primary_insurance_name,
            primary_insurance_id, secondary_insurance_name, secondary_insurance_id,
            drName, drAddress, drCity, drState, drZip,
            drPhone, drFax, drNpi, notes
        ]
        for field in required_fields:
            if not field:
                st.warning(f"{field} is required.")
                return False
        return True

    if st.button("Submit", use_container_width=True):
        if not validate_all_fields():
            st.warning("Please fill out all required fields.")
        else:
            form_data = {
                "entry.700175772": date.strftime("%m/%d/%Y"),  # Date
                "entry.1992907553": pt_name,        # PT Name
                "entry.1178853697": ptPhone,                   # Phone
                "entry.478400313": ptAddress,                  # PT Address
                "entry.1687085318": ptCity,                    # PT City
                "entry.1395966108": ptState,                   # PT State
                "entry.1319952523": ptZip,                     # PT Postal Code
                "entry.1553550428": ptDob,                     # PT DOB
                "entry.287019030": primary_insurance_name,     # Primary Insurance Name
                "entry.1122949100": primary_insurance_id,      # Primary Insurance ID
                "entry.2102408689": secondary_insurance_name,  # Secondary Insurance Name
                "entry.1278616009": secondary_insurance_id,    # Secondary Insurance ID
                "entry.2090908898": drName,                    # DR Name
                "entry.198263517": drAddress,                  # DR Address
                "entry.1349410133": drCity,                    # DR City
                "entry.847367280": drState,                    # DR State
                "entry.1652935364": drZip,                     # DR Postal Code
                "entry.756850883": drPhone,                    # DR Phone Number
                "entry.1725680069": drFax,                     # DR Fax
                "entry.314880762": drNpi,                      # DR NPI
                "entry.1322384700": notes                      # Notes
            }

            encoded_data = urlencode(form_data, quote_via=quote_plus)
            form_url = "https://docs.google.com/forms/d/e/1FAIpQLSeLh1vfsBq6bQYmUy_FsRssgj2PGwGL0tHGNn4QhzJOprreYA/formResponse"
            full_url = f"{form_url}?{encoded_data}"
            
            # Test the URL
            try:
                response = requests.get(full_url)
                if response.status_code == 200:
                    st.write(f"[Click here to open the CGM form](<{full_url}>)")
                else:
                    st.error(f"Failed to access the CGM form. Status Code: {response.status_code}")
            except Exception as e:
                st.error(f"Error accessing the CGM form: {e}")

            st.success("The CGM form is ready for submission. Please click the link above to submit.")


def get_brace_type(brace_code):
    for brace_type, brace_data in brace_info.items():
        if brace_code in brace_data:
            return brace_type
    return "Unknown"  # Return this if no matching brace type is found


style = """
<style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 30px;
                font-size: 16px;
                max-width: 210mm; /* A4 width */
                min-height: 297mm; /* A4 height */
            }
            h1 {
                font-size: 48px;
                font-weight: bold;
                margin-bottom: 30px;
            }
            .grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 30px;
            }
            .full-width {
                grid-column: 1 / -1;
            }
            .section {
                margin-bottom: 20px;
            }
            .label {
                font-weight: bold;
                font-size: 18px;
                margin-bottom: 5px;
            }
            .content {
                font-size: 16px;
            }
            .checkbox-group {
                margin: 30px 0;
                border-top: 2px solid #000;
                border-bottom: 2px solid #000;
                padding: 15px 0;
                font-size: 18px;
            }
            .checkbox-label {
                margin-right: 30px;
            }
            .message-label {
                font-weight: bold;
                font-size: 20px;
                margin-bottom: 10px;
            }
            .message-content {
                font-size: 16px;
            }
        </style>
"""
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prior Authorization Prescription Request Form</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.4; font-size: 12px; width: 210mm; height: 297mm; margin: 0; padding: 10mm 10mm 15mm; box-sizing: border-box;">

    <div style="text-align: center; margin-bottom: 15px;">
        <h2 style="font-size: 14px; margin: 0 0 10px; font-weight: bold;">PRIOR AUTHORIZATION PRESCRIPTION REQUEST FORM FOR {brace_type} ORTHOSIS</h2>
        <p style="margin: 0; font-size: 10px; font-weight: bold;">PLEASE SEND THIS FORM BACK IN 3 BUSINESS DAYS</p>
        <p style="margin: 0; font-size: 10px;font-weight: bold;">WITH THE PT CHART NOTES (RECENT MEDICAL RECORDS) AND THE FAX COVER SHEET</p>
    </div>

    <div style="display: flex; margin-top: 15px;">
        <div style="width: 48%; border: 1px solid black; padding: 5px; box-sizing: border-box;"> <!-- Reduced padding -->
            <div style="display: flex; justify-content: space-between;">
                <div style="width: 48%;">
                    <div style="margin-bottom: 4px;"><span style="font-weight: bold;">Date:</span> {date}</div>
                    <div style="margin-bottom: 4px;"><span style="font-weight: bold;">First:</span> {fname}</div>
                    <div style="margin-bottom: 4px;"><span style="font-weight: bold;">DOB:</span> {dob}</div>
                    <div style="margin-bottom: 4px;"><span style="font-weight: bold;">Address:</span> {address}</div>
                    <div style="margin-bottom: 4px;"><span style="font-weight: bold;">City:</span> {city}</div>
                    <div style="margin-bottom: 4px;"><span style="font-weight: bold;">State:</span> {state}</div>
                    <div style="margin-bottom: 4px;"><span style="font-weight: bold;">Postal Code:</span> {zip}</div>
                    <div style="margin-bottom: 4px;"><span style="font-weight: bold;">Patient Phone:</span> {phone}</div>
                    <div style="margin-bottom: 4px;"><span style="font-weight: bold;">Primary Ins:</span> Medicare</div>
                    <div style="margin-bottom: 4px;"><span style="font-weight: bold;">Weight:</span> {weight}</div>
                </div>
                <div style="width: 48%;">
                    <div style="margin-bottom: 4px;"><span style="font-weight: bold;">&nbsp;</span></div>
                    <div style="margin-bottom: 4px;"><span style="font-weight: bold;">Last:</span> {lname}</div>
                    <div style="margin-bottom: 4px;"><span style="font-weight: bold;">Gender:</span> {gender}</div>
                    <div style="margin-bottom: 4px;"><span style="font-weight: bold;">&nbsp;</span></div>
                    <div style="margin-bottom: 4px;"><span style="font-weight: bold;">&nbsp;</span></div>
                    <div style="margin-bottom: 4px;"><span style="font-weight: bold;">&nbsp;</span></div>
                    <div style="margin-bottom: 4px;"><span style="font-weight: bold;">&nbsp;</span></div>
                    <div style="margin-bottom: 4px;"><span style="font-weight: bold;">&nbsp;</span></div>
                    <div style="margin-bottom: 4px;"><span style="font-weight: bold;">Policy #:</span> {medID}</div>
                    <div style="margin-bottom: 4px;"><span style="font-weight: bold;">Height:</span> {height}</div>
                </div>
            </div>
        </div>
        <div style="width: 48%; border: 1px solid black; padding: 5px; box-sizing: border-box;"> <!-- Reduced padding -->
            <div style="margin-bottom: 4px;"><span style="font-weight: bold;">Physician Name:</span> {doctor_name}</div>
            <div style="margin-bottom: 4px;"><span style="font-weight: bold;">NPI:</span> {doctor_npi}</div>
            <div style="margin-bottom: 4px;"><span style="font-weight: bold;">Address:</span> {doctor_address}</div>
            <div style="margin-bottom: 4px;"><span style="font-weight: bold;">City:</span> {doctor_city}</div>
            <div style="margin-bottom: 4px;"><span style="font-weight: bold;">State:</span> {doctor_state}</div>
            <div style="margin-bottom: 4px;"><span style="font-weight: bold;">Postal Code:</span> {doctor_zip}</div>
            <div style="margin-bottom: 4px;"><span style="font-weight: bold;">Phone Number:</span> {doctor_phone}</div>
            <div style="margin-bottom: 4px;"><span style="font-weight: bold;">Fax Number:</span> {doctor_fax}</div>
        </div>
    </div>

    <div style="display: grid; gap: 3px; font-size: 8px;"> <!-- Reduced gap between checkboxes -->
        This patient is being treated under a comprehensive plan of care for lance pain.
I, the undersigned, certify that the prescribed orthosis is medically necessary for the patient’s overall well-being. In my opinion, the following lance orthosis products are both reasonable and necessary in reference to treatment of the patient ’s condition and/or rehabilitation. My patient has been in care regarding the diagnosis below. This is the treatment I see fit for this patient at this time. I certify that this information is true and correct.
    </div>
    <div style="font-weight: bold; margin-top: 15px; margin-bottom: 10px;">DIAGNOSIS: Provider can specify all of the diagnoses they feel are appropriate</div>
    <div style="display: grid; gap: 6px;"> <!-- Reduced gap between checkboxes -->
        {diagnosis}
    </div>


        <div style="font-weight: bold; margin-top: 15px; margin-bottom: 10px;">AFFECTED AREA</div>
        {affected_areas}

        <p style="margin-top: 15px;">Our evaluation of the above patient has determined that providing the following Back orthosis products will benefit this patient.</p>

        <div style="font-weight: bold; margin-top: 15px; margin-bottom: 10px;">DISPENSE</div>
        <p style="margin-bottom: 10px; font-size: 10px;">{Selected_Brace} - {Brace_info}</p>
        <p>____________________________________________________________________________________________________________</p>
        <p>Length of need is 99 months unless otherwise specified: ____________ 99-99 (LIFETIME)</p>

        <table style="width: 100%; margin-top: 20px; font-size: 10px;"> <!-- Adjusted margin-top and font-size -->

            <tbody>
                <tr>
                    <td > <!-- Adjusted padding -->
                        <div style="font-weight: bold;">Physician Name: {doctor_name}</div> 
                        <div style="margin-top: 8px;">Physician Signature: _________________________</div>
                    </td>
                    <td > <!-- Adjusted padding -->
                        <div style="font-weight: bold;">NPI: {doctor_npi}</div> 
                        <div style="margin-top: 8px;">Date signed: _________________________</div>
                    </td>
                </tr>
            </tbody>
        </table>
    </body>
    </html>
    """
def get_affected_areas(brace_code):
    if brace_code in ['L0457-G', 'L0637','L0651-G']:
        return '<div style="margin-bottom: 5px;"><input type="checkbox" class="custom-checkbox" checked>Back</div>'
    elif brace_code in ['L1845', 'L1852-G', 'L1833-G']:
        return '<div style="display: inline-block; margin-right: 30px;"><input type="checkbox" class="custom-checkbox" checked>Left Knee</div>' \
               '<div style="display: inline-block;margin-left: 60px;"><input type="checkbox" class="custom-checkbox" checked>Right Knee</div>'
    elif brace_code == 'L3761':
        return '<div style="display: inline-block; margin-right: 30px;"><input type="checkbox" class="custom-checkbox" checked>Left Elbow</div>' \
               '<div style="display: inline-block;margin-left: 60px;"><input type="checkbox" class="custom-checkbox" checked>Right Elbow</div>'
    elif brace_code in ['L3960','L3660-G']:
        return '<div style="display: inline-block; margin-right: 30px;"><input type="checkbox" class="custom-checkbox" checked>Left Shoulder</div>' \
               '<div style="display: inline-block;margin-left: 60px;"><input type="checkbox" class="custom-checkbox" checked>Right Shoulder</div>'
    elif brace_code in ['L1971', 'L1906']:
        return '<div style="display: inline-block; margin-right: 30px;"><input type="checkbox" class="custom-checkbox" checked>Left Ankle</div>' \
               '<div style="display: inline-block;margin-left: 60px;"><input type="checkbox" class="custom-checkbox" checked>Right Ankle</div>'
    elif brace_code == 'L3916':
        return '<div style="display: inline-block; margin-right: 30px;"><input type="checkbox" class="custom-checkbox" checked>Left Wrist</div>' \
               '<div style="display: inline-block;margin-left: 60px;"><input type="checkbox" class="custom-checkbox" checked>Right Wrist</div>'
    elif brace_code == 'L0174':
        return '<div style="margin-bottom: 5px;"><input type="checkbox" class="custom-checkbox" checked>Neck</div>'
    # Add other conditions for different brace codes
    else:
        return ''  # Default case if no match


# PDFShift API request
def pdfshift_request(api_key, html_body):
    response = requests.post(
        'https://api.pdfshift.io/v3/convert/pdf',
        auth=('api', api_key),
        json={
            "source": html_body,
            "landscape": False,
            "use_print": False
        }
    )
    return response

# html2pdf.app API request
def html2pdf_request(api_key, html_body, document_url=None):
    data = {
        "apiKey": api_key,
        "html": html_body,
        "permissions": ["print", "modify", "copy"]
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        url="https://api.html2pdf.app/v1/generate", headers=headers, json=data
    )
    return response

# RapidAPI html2pdf API request
def html2pdf_rapidapi(api_key, html_body, document_url=None):
    url = "https://html2pdf2.p.rapidapi.com/html2pdf"
    payload = {"html": html_body}
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "html2pdf2.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response

# Function to create a download link
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

# Load API keys from secrets
html2pdf_apis = st.secrets["html2pdf_apis"]
pdfshift_apis = st.secrets["pdfshift_apis"]
rapidapi_html2pdf = st.secrets["rapidapi_html2pdf"]

# Combine all API keys into a single list with corresponding API type
all_api_keys = [
    ("html2pdf_apis", key) for key in html2pdf_apis.values()
] + [
    ("pdfshift_apis", key) for key in pdfshift_apis.values()
] + [
    ("rapidapi_html2pdf", key) for key in rapidapi_html2pdf.values()
]

def generate_pdf(html_body):
    api_type, api_key = random.choice(all_api_keys)
    
    if api_type == "html2pdf_apis":
        response = html2pdf_request(api_key, html_body)
    elif api_type == "pdfshift_apis":
        response = pdfshift_request(api_key, html_body)
    elif api_type == "rapidapi_html2pdf":
        response = html2pdf_rapidapi(api_key, html_body)
    else:
        st.error("API key not recognized")
        return None
    
    # Handle the response
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type', '')
        
        if 'application/json' in content_type:
            try:
                json_response = response.json()
                if 'pdf' in json_response:
                    pdf_content = base64.b64decode(json_response['pdf'])
                    html = create_download_link(pdf_content, "result")
                elif 'url' in json_response:
                    pdf_url = json_response['url']
                    html = create_download_link(pdf_url, "result")
                else:
                    st.error(f"Unexpected JSON response format: {json_response}")
                    return None
            except json.JSONDecodeError:
                st.error(f"Invalid JSON response: {response.text}")
                return None
        elif 'application/pdf' in content_type:
            pdf_content = response.content
            html = create_download_link(pdf_content, "result")
        else:
            st.error(f"Unexpected content type: {content_type}")
            return None
        
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.error(f"Error generating PDF: {response.status_code} - {response.text}")
        return None


def merge_pdfs(pdf_files):
    # Initialize the merger object
    merger = PdfMerger()

    # Combine all generated PDFs into a single PDF
    combined_pdf_filename = f"combined_brace_forms_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    for pdf_file in pdf_files:
        merger.append(pdf_file)

    merger.write(combined_pdf_filename)
    merger.close()

    # Provide download button for the combined PDF
    with open(combined_pdf_filename, "rb") as pdf_file:
        st.download_button(
            label="Download Combined Brace Forms PDF",
            data=pdf_file,
            file_name=combined_pdf_filename,
            mime="application/pdf"
        )

    # Clean up individual PDF files and combined file
    for pdf_file in pdf_files:
        os.unlink(pdf_file)

    os.unlink(combined_pdf_filename)

    st.success(f"{len(pdf_files)} PDF form(s) are ready for download. Please click the download button above.")


def generate_cover_page_html(chaser_name, to_name, fax_subject, fax_message, date, sender_email, receiver_number ):
    html_body = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fax Cover Sheet</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.8; margin: 0; padding: 40px; font-size: 18px; max-width: 210mm; min-height: 297mm; position: relative;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px;">
        <h1 style="font-size: 60px; font-weight: bold;">FAX</h1>
        <div style="text-align: right;">
            <div style="font-weight: bold; font-size: 22px;">InCall Medical Supplies</div>
            <div>Fax1: (510) 890-3073</div>
            <div>Fax2: (888) 851-6047</div>
        </div>
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 40px;">
        <div style="margin-bottom: 30px;">
            <div style="font-weight: bold; font-size: 22px; margin-bottom: 10px;">To</div>
            <div style="font-size: 18px;">
                Name: {to_name}<br>
                Fax number: {receiver_number}
            </div>
        </div>
        <div style="margin-bottom: 30px;">
            <div style="font-weight: bold; font-size: 22px; margin-bottom: 10px;">From</div>
            <div style="font-size: 18px;">
                Name: {chaser_name}<br>
                Fax number: 737 241 2558
            </div>
        </div>
    </div>
    <div style="margin-bottom: 30px;">
        <div style="font-weight: bold; font-size: 22px; margin-bottom: 10px;">Number of pages: 2</div>
        <div style="font-size: 18px;"></div>
    </div>
    <div style="margin-bottom: 30px;">
        <div style="font-weight: bold; font-size: 22px; margin-bottom: 10px;">Subject: </div>
        <div style="font-size: 18px;">{fax_subject}</div>
    </div>
    <div style="margin-bottom: 30px;">
        <div style="font-weight: bold; font-size: 22px; margin-bottom: 10px;">Date:</div>
        <div style="font-size: 18px;">{date}</div>
    </div>
    <div style="margin: 40px 0; border-top: 2px solid #000; border-bottom: 2px solid #000; padding: 20px 0; font-size: 22px;">
        <span style="margin-right: 40px; font-weight: bold;">☐ Urgent</span>
        <span style="margin-right: 40px; font-weight: bold;">☐ For Review</span>
        <span style="margin-right: 40px; font-weight: bold;">☐ Please Reply</span>
        <span style="font-weight: bold;">☑ Confidential</span>
    </div>
    <div style="margin-bottom: 30px;">
        <div style="font-weight: bold; font-size: 24px; margin-bottom: 15px;">Message:</div>
        <div style="font-size: 18px;">{fax_message}</div>
    </div>
</body>
</html> 
    """
    return html_body


# Define the Braces and brace_info as provided
Braces = ["Back", "Knees", "Elbow", "Shoulder", "Ankle", "Wrists", "Neck"]
brace_info = {
    "Back": {
        'L0637': [
            "LUMBAR ORTHOSIS, SAGITTAL-CORONAL CONTROL, WITH RIGID ANTERIOR AND POSTERIOR PANELS, POSTERIOR EXTENDS FROM SACROCOCCYGEAL JUNCTION TO T-9 VERTEBRA, PRODUCES INTRACAVITARY PRESSURE TO REDUCE LOAD ON THE INTERVERTEBRAL DISCS, INCLUDES STRAPS, CLOSURES, MAY INCLUDE PADDING, SHOULDER STRAPS, PENDULOUS ABDOMEN DESIGN, PREFABRICATED, INCLUDES FITTING AND ADJUSTMENT",
            "Lumbar Intervertebral Disc Degeneration (M51.36)",
            "Other intervertebral disc displacement, lumbar region (M51.26)",
            "Spinal Stenosis, lumbar region (M48.06)",
            "Spinal instability, lumbosacral region (M53.2X7)",
            "Other intervertebral disc disorders, lumbosacral region (M51.87)",
            "Low back pain (M54.5)"
        ],
        'L0457-G': [
            "lumbar-Sacral Orthosis, Sagittal-Coronal Control, With Rigid Anterior And Posterior Frame/Panel(S), Posterior Extends From Sacrococcygeal Junction To 7-9 Vertebra, Lateral Strength Provided By Rigid Lateral Frame/Panel(S), Produces Intracavitary Pressure To Reduce Load On Intervertebral Discs, Includes Straps, Closures, May Include Padding Shoulder Straps, Pendulous Abdomen Design, Prefabricated, Off-The-Shelf.",
            "Lumbar Intervertebral Disc Degeneration (M51.36)",
            "Other intervertebral disc degeneration, lumbosacral region (M51.37)",
            "Spinal Stenosis, lumbar region (M48.06)",
            "Spinal stenosis, lumbosacral region (M48.07)",
            "Other Intervertebral disc disorders, lumbosacral region (M51.87)",
            "Low back pain (M54.5)"
        ],
        'L0651-G': ["lumbar-Sacral Orthosis, Sagittal-Coronal Control, With Rigid Anterior And Posterior Frame/Panel(S), Posterior Extends From Sacrococcygeal Junction To 7-9 Vertebra, Lateral Strength Provided By Rigid Lateral Frame/Panel(S), Produces Intracavitary Pressure To Reduce Load On Intervertebral Discs, Includes Straps, Closures, May Include Padding Shoulder Straps, Pendulous Abdomen Design,  Prefabricated, Off-The-Shelf.",
            "Lumbar/ Lumbosacral Intervertebral Disc Degeneration (M51.36)",
            "Other intervertebral disc degeneration, lumbosacral region (M51.37)",
            "Spinal Stenosis, lumbar region (M48.06)",
            "Spinal stenosis, lumbosacral region (M48.07)",
            "Other Intervertebral disc disorders, lumbosacral region (M51.87)",
            "Low back pain (M54.5)"
        ]
    },
    "Knees": {
        'L1843': ['Knee orthosis, double upright, thigh and calf, with adjustable flexion and extension joint (unicentric or    polycentric), medial-lateral and rotation control, with or without varus/valgus adjustment, prefabricated item that has been trimmed, bent, molded, assembled, or otherwise customized to fit a specific patient by an individual with expertise; includes L2397 Suspension Sleeve.',
                    "Hypermobility Syndrome (M35.7) (check below that apply)",
                    "Grade < 2mm Tight with firm end-feel",
                    " Grade I 3-5mm Nominal increase in laxity compared to contralateral knee.",
                    "Grade II 6-9mm Slight increase in anterior translation compared to contralateral knee.",
                    "Grade III > 10mm Excessive anterior translation compared to contralateral knee.",
                    "Other spontaneous disruption of anterior cruciate ligament of unspecified knee. (M23.619) (check below)",
                    "Pivot Shift Normal Knee Grace I Grade II Grade III",
                    "Medial Plateau 3mm 5mm 10mm 15mm",
                    "Lateral Plateau 5mm 12mm 18mm 22mm",
                    "Chronic instability of knee, right knee (M23.51)",
                    "Chronic instability of knee, left knee (M23.52)",
                    "Other /Explain: " ],
        
        'L1852-G': ['Adjustable Flexion & Extension Joint (Unicentric or Polycentric), Medial-Lateral & Rotation Control,+/- Varus/Valgus Adjustment, Prefabricated, Off the Shelf, includes L2397 Suspension Sleeve',
                    "Hypermobility Syndrome (M35.7) (check below that apply)",
                    "Grade < 2mm Tight with firm end-feel",
                    " Grade I 3-5mm Nominal increase in laxity compared to contralateral knee.",
                    "Grade II 6-9mm Slight increase in anterior translation compared to contralateral knee.",
                    "Grade III > 10mm Excessive anterior translation compared to contralateral knee.",
                    "Other spontaneous disruption of anterior cruciate ligament of unspecified knee. (M23.619) (check below)",
                    "Pivot Shift Normal Knee Grace I Grade II Grade III",
                    "Medial Plateau 3mm 5mm 10mm 15mm",
                    "Lateral Plateau 5mm 12mm 18mm 22mm",
                    "Chronic instability of knee, right knee (M23.51)",
                    "Chronic instability of knee, left knee (M23.52)",
                    "Other /Explain: "  
            ],
        'L1833-G': [' KNEE ORTHOSIS, ADJUSTABLE KNEE JOINTS (UNICENTRIC OR POLYCENTRIC), POSITIONAL ORTHOSIS, RIGID SUPPORT, PREFABRICATED, OFF-THE SHELF. includes L2397 Suspension Sleeve',
                    "Hypermobility Syndrome (M35.7) (check below that apply)",
                    "Grade < 2mm Tight with firm end-feel",
                    " Grade I 3-5mm Nominal increase in laxity compared to contralateral knee.",
                    "Grade II 6-9mm Slight increase in anterior translation compared to contralateral knee.",
                    "Grade III > 10mm Excessive anterior translation compared to contralateral knee.",
                    "Other spontaneous disruption of anterior cruciate ligament of unspecified knee. (M23.619) (check below)",
                    "Pivot Shift Normal Knee Grace I Grade II Grade III",
                    "Medial Plateau 3mm 5mm 10mm 15mm",
                    "Lateral Plateau 5mm 12mm 18mm 22mm",
                    "Chronic instability of knee, right knee (M23.51)",
                    "Chronic instability of knee, left knee (M23.52)",
                    "Other /Explain: "]
    },
    "Elbow": {
        'L3761': ['Elbow orthosis (eo), with adjustable position locking joint(s), prefabricated, off-the-shelf',
                "Cubital Tunnel Syndrome (G56.2)",
                "Rheumatoid bursitis, right elbow (M06.221)",
                "Rheumatoid bursitis, left elbow (M06.222)",
                "Pain in right elbow (M25.521)",
                "Pain in left elbow (M25.522)",
                "Unspecified sprain of right elbow (S53.401)", 
                "Unspecified sprain of left elbow (S53.402)",
                "Disorder of ligament, right elbow (M24.221)",
                "Disorder of ligament, left elbow (M24.222)",
]
    },
    "Shoulder": {
        'L3960': ['Shoulder elbow wrist hand orthosis, abduction positioning, airplane design, prefabricated, includes fitting and adjustment',
                  "M75.31 Calcific tendinitis of left shoulder",
                    "M75.32 Calcific tendinitis of right shoulder",
                    "M75.41 Impingement syndrome of left shoulder", 
                    "M75.42 Impingement syndrome of right shoulder", 
                    "G56.11 Other lesions of median nerve, right upper limb", 
                    "G56.12 Other lesions of median nerve, left upper limb", 
                    "G56.31 Lesion of radial nerve, right upper limb", 
                    "G56.32 Lesion of radial nerve, left upper limb", 
                    "M25.511 Pain in right Shoulder",
                    "M25.512 Pain in Left Shoulder"
                  ],
        'L3660-G': ['SHOULDER ORTHOSIS, FIGURE OF EIGHT DESIGN ABDUCTION RESTRAINER, CANVAS AND WEBBING, PREFABRICATED, OFF-THE-SHELF.',
                  "M75.31 Calcific tendinitis of left shoulder",
                    "M75.32 Calcific tendinitis of right shoulder",
                    "M75.41 Impingement syndrome of left shoulder", 
                    "M75.42 Impingement syndrome of right shoulder", 
                    "G56.11 Other lesions of median nerve, right upper limb", 
                    "G56.12 Other lesions of median nerve, left upper limb", 
                    "G56.31 Lesion of radial nerve, right upper limb", 
                    "G56.32 Lesion of radial nerve, left upper limb", 
                    "M25.511 Pain in right Shoulder",
                    "M25.512 Pain in Left Shoulder"
                  ]
    },
    "Ankle": {
        'L1971': ['Ankle foot orthosis, plastic or other material with ankle joint, prefabricated, includes fitting and adjustment',
                  "Primary osteoarthritis, right ankle and foot (M19.071)",
                    "Primary osteoarthritis, left ankle and foot (M19.072)", 
                    "Unspecified disorder of synovium and tendon, unspecified site (M67.90)",
                    "Other instability, right ankle and foot (M25.371)",
                    "Other instability, left ankle and foot (M25.372)", 
                    "Displaced trimalleolar fracture of unspecified lower leg (S82.853A)",
                    "Spontaneous rupture of other tendons, unspecified ankle and foot (M66.879)",
                    "Pain in right ankle and joints of right foot (M25.571)",
                    "Pain in left ankle and joints of left foot (M25.572)",
                    "Flat foot [pes planus] (acquired), unspecified foot (M21.40)",
                    "Sprain of unspecified ligament of right ankle (S93.401)",
                    "Sprain of unspecified ligament of left ankle (S93.402)",
                  ],
        "L1906": [ "Ankle/Foot Orthosis, Plastic or other material w/Ankle Joint, PREFABRICATED. INCLUDES FITTING & ADJUSTMENT.  OFF-THE-SHELF",
"Primary osteoarthritis, right ankle and foot (M19.071)",
 "Primary osteoarthritis, left ankle and foot (M19.072)" ,
 "Unspecified disorder of synovium and tendon, unspecified site (M67.90)",
 "Other instability, right ankle and foot (M25.371)",
 "Other instability, left ankle and foot (M25.372) ",
"Displaced trimalleolar fracture of unspecified lower leg (S82.853A)",
 "Spontaneous rupture of other tendons, unspecified ankle and foot (M66.879)" ,
"Pain in right ankle and joints of right foot (M25.571)",
 "Pain in left ankle and joints of left foot (M25.572)",
 "Flat foot [pes planus] (acquired), unspecified foot (M21.40)" ,
 "Sprain of unspecified ligament of right ankle (S93.401)",
 "Sprain of unspecified ligament of left ankle (S93.402)"]
    },
    "Wrists": {
        'L3916': ['Wrist hand orthosis, includes one or more nontorsion joint(s), elastic bands, turnbuckles, may include soft interface, straps, prefabricated, off-the-shelf',
                  "Primary Osteoarthritis, Right wrist (M19.031)",
                    "Primary Osteoarthritis, Left wrist (M19.032)",
                    "Primary Osteoarthritis, Right Hand (M19.41)",
                    "Primary Osteoarthritis, Left Hand (M19.42)",
                    "Carpal Tunnel Syndrome, Right Upper Limb (G56.01)",
                    "Pain In Right Wrist (M25.531)", 
                    "Carpal Tunnel Syndrome, Left Upper Limb (G56.02)",
                    "Pain In Left Wrist (M25.532)",
                  ]
    },
    "Neck": {
        "L0174": ['Cervical, collar, semi-rigid, thermoplastic foam, two piece with thoracic extension, prefabricated, off-the-shelf.',
                  "Radirulopathy, Cervical Region (M54.12)", 
                    "Radiculopathy, Cervical Thoracic Region (M54.13)", 
                    "Radiculapathy, Occipito -Atlanto-Axial Regio (M54.11)", 
                    "Cervicalgia (M54.2)", 
                    "Cervical disc disorder with myelopathy, High Cervical Region (M50.01)", 
                    "Spinal stenosis, Cervical region (M48.02)",
                    "Other/Explain (Include Code) :",

                  ]
    }
}

chasers_dict = {
    "Olivia Smith":"(941) 293-1794" , "Mia Martin":"(352) 718-1524",
    "Lexi Thomas":"(607) 383-2941" , "Mark Wilson":"(754) 250-1426",
    "Kendrick Adams":"(941) 293-1462" , "Ken Adams":"(352) 718-1436",
    "Anne Mathew":"(727) 910-2808" , "Linda Williams":"(620) 203-2088",
    "Tom miles":"(786) 891-7322" , "Rose Johnson":"(904) 515-1558",
    "Emma Winslet":"(386) 487-2910" , "Hannah Adams":"(904) 515-1565",
}


chasers_emails = {
    "Olivia Smith": "olivia.smith.incall@gmail.com",
    "Mia Martin": "mia.martin.incall@gmail.com",
    "Lexi Thomas": "lexi.thomas.incall@gmail.com",
    "Mark Wilson": "mark.wilson.incall@gmail.com",
    "Kendrick Adams": "kendrick.adams.incall@gmail.com",
    "Anne Mathew": "anne.mathew.incall@gmail.com",
    "Linda Williams": "linda.william.incall@gmail.com",
    "Tom Miles": "tom.miles.incall@gmail.com",
    "Rose Johnson": "rose.johnson.incall@gmail.com",
    "Emma Winslet": "emma.winselt.incall@gmail.com",
    "Hannah Adams": "hannah.adams.incall@gmail.com",
    "Adam Wayne": "adam.wayne.incall@gmail.com",
    "Cassie Albert": "cassie.albert.incall@gmail.com",
    "Chloe Wilson": "chloe.wilson.incall@gmail.com",
    "Harvey Gabriel": "harvey.gabriel.incall@gmail.com",
    "Lauren Adams": "lauren.adams.incall@gmail.com"
}



def handle_srfax(combined_pdf, receiver_number, fax_message, fax_subject, to_name, chaser_name, uploaded_cover_sheet,user,password):
    # API credentials
    if user and password:
        access_id = user
        access_pwd = password
    else:
        access_id = st.secrets["sr_access_id"]["access_id"]
        access_pwd = st.secrets["sr_access_pwd"]["access_pwd"]

    # Fax details
    caller_id = "8888516047"
    sender_email = "Alvin.freeman.italk@gmail.com"

    # Cover page details
    cp_from_name = chaser_name
    cp_to_name = to_name
    cp_subject = fax_subject
    cp_comments = fax_message
    cp_organization = "InCall Medical Supplies"
    cp_from_header = "From InCall Medical Supplies"

    # Encode the main PDF file
    encoded_file = base64.b64encode(combined_pdf.getvalue()).decode()

    # API endpoint
    url = "https://www.srfax.com/SRF_SecWebSvc.php"

    # Base payload
    payload = {
        "action": "Queue_Fax",
        "access_id": access_id,
        "access_pwd": access_pwd,
        "sCallerID": caller_id,
        "sSenderEmail": sender_email,
        "sFaxType": "SINGLE",
        "sToFaxNumber": receiver_number,
        "sFileName_1": "combined.pdf",
        "sFileContent_1": encoded_file,
    }

    if uploaded_cover_sheet is not None:
        # If a cover sheet is uploaded, use it as a separate file
        encoded_cover_page = base64.b64encode(uploaded_cover_sheet.read()).decode()
        payload.update({
            "sFileName_2": "cover_page.pdf",
            "sFileContent_2": encoded_cover_page,
        })
    else:
        # If no cover sheet is uploaded, use the text fields to generate a cover page
        payload.update({
            "sCoverPage": "Standard",
            "sCPFromName": cp_from_name,
            "sCPToName": cp_to_name,
            "sCPOrganization": cp_organization,
            "sCPSubject": cp_subject,
            "sCPComments": cp_comments,
            "sFaxFromHeader": cp_from_header,
        })

    response = requests.post(url, data=payload)
    time.sleep(5)
    if response.status_code == 200:
        try:
            response_data = response.json()
            if response_data.get("Status") == "Success":
                return True
            else:
                return False
        except ValueError:
            return False
    else:
        return False

def handle_humblefax(combined_pdf, receiver, fax_message, fax_subject, to_name, chaser_name, uploaded_cover_sheet):

    access_key = st.secrets["humble_access_key"]["access_key"]
    secret_key = st.secrets["humble_secret_key"]["secret_key"]
    # Step 1: Create a temporary fax
    create_tmp_fax_url = "https://api.humblefax.com/tmpFax"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{access_key}:{secret_key}'.encode()).decode()}"
    }
    create_tmp_fax_payload = {
        "toName": to_name,
        "recipients": [receiver],
        "fromName": chaser_name,
        "subject": fax_subject,
        "message": fax_message,
        "includeCoversheet": uploaded_cover_sheet is None,
        "companyInfo": (
            "InCall Medical Supplies\n"
            "Fax 1: +1 (888) 851-6047\n"
            "Fax 2: +1 (510) 890-3073\n"
            "Phone: +1 (352) 718-1524"
        ),
        "pageSize": "A4",
        "resolution": "Fine",
        "fromNumber": "12139056868"
    }

    create_tmp_fax_response = requests.post(create_tmp_fax_url, headers=headers, json=create_tmp_fax_payload)
    if create_tmp_fax_response.status_code == 200:
        tmp_fax_data = create_tmp_fax_response.json().get("data", {}).get("tmpFax", {})
        tmp_fax_id = tmp_fax_data.get("id")
        print(f"tmpFaxId obtained: {tmp_fax_id}")
    else:
        print(f"Failed to create temporary fax: {create_tmp_fax_response.text}")
        return False

    # Step 2: Upload the main PDF file
    files = {'file': ('combined.pdf', combined_pdf.getvalue(), 'application/pdf')}
    upload_response = requests.post(f'https://api.humblefax.com/attachment/{tmp_fax_id}', headers=headers, files=files)
    if upload_response.status_code == 200:
        main_file_data = upload_response.json().get("data", {})
        main_file_id = main_file_data.get("id")
        print(f"Main file uploaded successfully. File ID: {main_file_id}")
    else:
        print(f"Failed to upload main file: {upload_response.text}")
        return False

    # Step 3: Upload the cover page PDF file if it was uploaded
    if uploaded_cover_sheet is not None:
        cover_page_files = {'file': ('cover_page.pdf', uploaded_cover_sheet.read(), 'application/pdf')}
        cover_page_upload_response = requests.post(f'https://api.humblefax.com/attachment/{tmp_fax_id}', headers=headers, files=cover_page_files)
        if cover_page_upload_response.status_code == 200:
            cover_page_data = cover_page_upload_response.json().get("data", {})
            cover_page_id = cover_page_data.get("id")
            print(f"Cover page uploaded successfully. File ID: {cover_page_id}")
        else:
            print(f"Failed to upload cover page file: {cover_page_upload_response.text}")
            return False

    # Step 4: Send the temporary fax
    send_fax_url = f"https://api.humblefax.com/tmpFax/{tmp_fax_id}/send"
    send_response = requests.post(send_fax_url, headers=headers)

    # Check the response
    if send_response.status_code == 200:
        response_data = send_response.json()
        if response_data.get("result") == "success":
            fax_id = response_data.get("data", {}).get("id")
            print(f"Fax sent successfully. Fax ID: {fax_id}")
            return True
        else:
            print(f"Failed to send fax: {response_data.get('message')}")
            return False
    else:
        print(f"HTTP Error: {send_response.status_code} - {send_response.text}")
        return False
#TODO
def handle_hallofax(combined_pdf, receiver_number, fax_message, fax_subject, to_name, chaser_name, uploaded_cover_sheet):
    # Implement HalloFax logic here
    print(f"Sending fax to {receiver_number} using HalloFax")
    # Use the provided parameters to send the fax
    # Return True if successful, False otherwise
    return True
#TODO -> Try to fix it


def handle_faxplus(uploaded_file, receiver_number, fax_message, fax_subject, to_name, chaser_name, uploaded_cover_sheet):
    try:
        sender_email = st.secrets["gmail_creds"]["address"]
        email_password = st.secrets["gmail_creds"]["pass"]
        
        # Create email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = f"{receiver_number}@fax.plus"
        msg['Subject'] = fax_subject
        
        # Generate cover page HTML
        cover_page_html = generate_cover_page_html(chaser_name, to_name, fax_subject, fax_message, datetime.now().strftime('%b %d, %Y'), sender_email , receiver_number)
        
        # Add the HTML body as the cover sheet
        body = MIMEText(cover_page_html, 'html')
        msg.attach(body)
        
        # Attach the cover sheet if provided
        if uploaded_cover_sheet:
            cover_sheet = MIMEApplication(uploaded_cover_sheet.getvalue())
            cover_sheet.add_header('Content-Disposition', 'attachment; filename="cover_sheet.pdf"')
            msg.attach(cover_sheet)
        
        # Attach the main file
        if uploaded_file:
            main_attachment = MIMEApplication(uploaded_file.getvalue())
            main_attachment.add_header('Content-Disposition', f'attachment; filename="Main File"')
            msg.attach(main_attachment)
        
        # Send the email (SMTP configuration required)
        import smtplib
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, email_password)
        server.sendmail(sender_email, f"{receiver_number}@fax.plus", msg.as_string())
        server.quit()
        
        st.success("Fax sent successfully")
    except Exception as e:
        st.error(f"Failed to send fax: {e}")

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', filename)

def get_srfax_outbox():
    access_id = st.secrets["sr_access_id"]["access_id"]
    access_pwd = st.secrets["sr_access_pwd"]["access_pwd"]
    
    url = "https://www.srfax.com/SRF_SecWebSvc.php"
    payload = {
        "action": "Get_Fax_Outbox",
        "access_id": access_id,
        "access_pwd": access_pwd,
        "sResponseFormat": "JSON",
        "sPeriod": "ALL",
        "sIncludeSubUsers": "Y"
    }
    
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return None
#TODO
    return
def get_hallo_outbox():
    return
# Function to get outbox faxes from FaxPlus
def get_faxplus_outbox():
    # Your Personal Access Token
    access_token = st.secrets["faxplus_secret_key"]["secret_key"]
    user_id = st.secrets["faxplus_uid"]["user_id"]

    # Base URL for the API
    base_url = 'https://restapi.fax.plus/v3'
    # Endpoint for listing outbox faxes
    endpoint = f'/accounts/{user_id}/outbox'

    # Full URL
    url = base_url + endpoint

    # Headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Make the GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        outbox_faxes = response.json()
        print("Outbox faxes:", outbox_faxes)
    else:
        print(f"Error: {response.status_code}, {response.text}")

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def retrieve_srfax(fax_file_name, direction):
    access_id = st.secrets["sr_access_id"]["access_id"]
    access_pwd = st.secrets["sr_access_pwd"]["access_pwd"]
    
    url = "https://www.srfax.com/SRF_SecWebSvc.php"
    payload = {
        "action": "Retrieve_Fax",
        "access_id": access_id,
        "access_pwd": access_pwd,
        "sFaxFileName": fax_file_name,
        "sDirection": direction,
        "sResponseFormat": "JSON",
        "sFaxFormat": "PDF"
    }
    
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def send_srfax(to_fax_number, file_content, sender_email, caller_id):
    access_id = st.secrets["sr_access_id"]["access_id"]
    access_pwd = st.secrets["sr_access_pwd"]["access_pwd"]
    
    url = "https://www.srfax.com/SRF_SecWebSvc.php"
    
    # The file_content is already base64 encoded, so we don't need to encode it again
    payload = {
        "action": "Queue_Fax",
        "access_id": access_id,
        "access_pwd": access_pwd,
        "sToFaxNumber": to_fax_number,
        "sResponseFormat": "JSON",
        "sFaxType": "SINGLE",
        "sFileName_1": "combined.pdf",
        "sFileContent_1": file_content,  # Already base64 encoded
        "sSenderEmail": sender_email,
        "sCallerID": caller_id
    }
    
    logger.debug(f"Attempting to send fax with type: SINGLE")
    logger.debug(f"Sending fax to: {to_fax_number}")
    logger.debug(f"Sender email: {sender_email}")
    logger.debug(f"Caller ID: {caller_id}")
    logger.debug(f"Fax content type: {type(file_content)}")
    logger.debug(f"Fax content preview: {file_content[:100]}")
    
    response = requests.post(url, data=payload)
    logger.debug(f"SRFax API response status code: {response.status_code}")
    logger.debug(f"SRFax API response content: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        if result['Status'] == 'Success':
            return result
        else:
            logger.error(f"Failed to send fax. Error: {result['Result']}")
    else:
        logger.error(f"HTTP error when sending fax. Status code: {response.status_code}")
    
    return {"Status": "Failed", "Result": "Failed to send fax"}
def resend_srfax(fax_id):
    logger.debug(f"Attempting to resend fax with ID: {fax_id}")
    
    outbox = get_srfax_outbox()
    if not outbox or outbox['Status'] != 'Success':
        logger.error("Failed to get outbox")
        return {"Status": "Failed", "Result": "Failed to get outbox"}
    
    fax_to_resend = next((fax for fax in outbox['Result'] if fax['FileName'] == fax_id), None)
    
    if not fax_to_resend:
        logger.error(f"Fax with ID {fax_id} not found in outbox")
        return {"Status": "Failed", "Result": "Fax not found in outbox"}
    
    logger.debug(f"Fax to resend details: {fax_to_resend}")
    
    retrieved_fax = retrieve_srfax(fax_to_resend['FileName'], "OUT")
    if not retrieved_fax or retrieved_fax['Status'] != 'Success':
        logger.error("Failed to retrieve fax content")
        return {"Status": "Failed", "Result": "Failed to retrieve fax content"}
    
    fax_content = retrieved_fax['Result']
    logger.debug(f"Retrieved fax content type: {type(fax_content)}")
    logger.debug(f"Retrieved fax content preview: {fax_content[:100]}")
    
    # Check if the content is valid base64
    try:
        base64.b64decode(fax_content)
    except:
        logger.error("Retrieved fax content is not valid base64")
        return {"Status": "Failed", "Result": "Invalid fax content"}
    
    sender_email = "Alvin.freeman.italk@gmail.com"
    caller_id = "8888516047"
    
    result = send_srfax(fax_to_resend['ToFaxNumber'], fax_content, sender_email, caller_id)
    
    logger.debug(f"Resend result: {result}")
    return result



#TODO
    return

def resend_hallo(fax_id):
    return
def resend_faxplus(fax_id):
    return


# Streamlit secrets
HUMBLEFAX_API_BASE_URL = "https://api.humblefax.com"
access_key = st.secrets["humble_access_key"]["access_key"]
secret_key = st.secrets["humble_secret_key"]["secret_key"]
def get_humblefax_details(fax_id):
    url = f"{HUMBLEFAX_API_BASE_URL}/sentFax/{fax_id}"
    auth = (access_key, secret_key)
    try:
        response = requests.get(url, auth=auth)
        response.raise_for_status()
        
        fax_data = response.json().get("data", {}).get("sentFax", {})
        
        # Extract relevant details and return them in a structured format
        recipient = fax_data.get("recipients", [{}])[0]  # Get the first recipient's details
        
        fax_details = {
            'ToFaxNumber': recipient.get('toNumber', ''),
            'DateSent': datetime.utcfromtimestamp(int(fax_data.get('timestamp', 0))).strftime('%Y-%m-%d %H:%M:%S'),
            'SentStatus': fax_data.get('status', ''),
            'FileName': fax_data.get('subject', ''),  # Assuming subject as file name as there's no file name in response
            'Service': 'HumbleFax'
        }
        
        return fax_details

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve fax details for fax_id {fax_id}: {e}")
        return None
def get_humble_outbox():
    url = "https://api.humblefax.com/sentFaxes"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{access_key}:{secret_key}'.encode()).decode()}"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Failed to get HumbleFax outbox: {response.text}")
        return None

def retrieve_humble_fax(fax_id):
    url = f"https://api.humblefax.com/fax/{fax_id}"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{access_key}:{secret_key}'.encode()).decode()}"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Failed to retrieve HumbleFax: {response.text}")
        return None

def create_humble_tmp_fax(payload):
    url = "https://api.humblefax.com/tmpFax"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{access_key}:{secret_key}'.encode()).decode()}"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Failed to create temporary fax: {response.text}")
        return None

def get_humble_attachment(fax_id, attachment_id):
    url = f"https://api.humblefax.com/fax/{fax_id}/attachment/{attachment_id}"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{access_key}:{secret_key}'.encode()).decode()}"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        logger.error(f"Failed to get attachment: {response.text}")
        return None

def upload_humble_attachment(tmp_fax_id, file_content, file_name):
    url = f"https://api.humblefax.com/attachment/{tmp_fax_id}"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{access_key}:{secret_key}'.encode()).decode()}"
    }
    
    files = {'file': (file_name, file_content, 'application/pdf')}
    response = requests.post(url, headers=headers, files=files)
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Failed to upload attachment: {response.text}")
        return None

def send_humble_tmp_fax(tmp_fax_id):
    url = f"https://api.humblefax.com/tmpFax/{tmp_fax_id}/send"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{access_key}:{secret_key}'.encode()).decode()}"
    }
    
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if result.get("result") == "success":
            return result.get("data", {}).get("id")
    logger.error(f"Failed to send temporary fax: {response.text}")
    return None

def resend_humble(fax_id):
    logger.debug(f"Attempting to resend HumbleFax with ID: {fax_id}")
    
    # Retrieve the original fax details
    fax_details = retrieve_humble_fax(fax_id)
    if not fax_details or fax_details.get("result") != "success":
        logger.error(f"Failed to retrieve fax details for ID: {fax_id}")
        return {"Status": "Failed", "Result": "Failed to retrieve fax details"}
    
    fax_data = fax_details.get("data", {})
    
    # Prepare the payload for creating a new temporary fax
    create_tmp_fax_payload = {
        "toName": fax_data.get("toName"),
        "recipients": fax_data.get("recipients"),
        "fromName": fax_data.get("fromName"),
        "subject": fax_data.get("subject"),
        "message": fax_data.get("message"),
        "includeCoversheet": fax_data.get("includeCoversheet", True),
        "companyInfo": fax_data.get("companyInfo"),
        "pageSize": fax_data.get("pageSize", "A4"),
        "resolution": fax_data.get("resolution", "Fine"),
        "fromNumber": fax_data.get("fromNumber")
    }
    
    # Create a new temporary fax
    tmp_fax = create_humble_tmp_fax(create_tmp_fax_payload)
    if not tmp_fax or tmp_fax.get("result") != "success":
        logger.error("Failed to create temporary fax")
        return {"Status": "Failed", "Result": "Failed to create temporary fax"}
    
    tmp_fax_id = tmp_fax.get("data", {}).get("tmpFax", {}).get("id")
    
    # Upload the original attachments to the new temporary fax
    for attachment in fax_data.get("attachments", []):
        attachment_id = attachment.get("id")
        attachment_content = get_humble_attachment(fax_id, attachment_id)
        if attachment_content:
            upload_result = upload_humble_attachment(tmp_fax_id, attachment_content, attachment.get("name"))
            if not upload_result:
                logger.error(f"Failed to upload attachment: {attachment.get('name')}")
                return {"Status": "Failed", "Result": "Failed to upload attachment"}
    
    # Send the new fax
    send_result = send_humble_tmp_fax(tmp_fax_id)
    if send_result:
        logger.debug(f"HumbleFax resent successfully. New Fax ID: {send_result}")
        return {"Status": "Success", "Result": send_result}
    else:
        logger.error("Failed to send HumbleFax")
        return {"Status": "Failed", "Result": "Failed to send fax"}



# Constants and secrets
HUMBLEFAX_API_BASE_URL = "https://api.humblefax.com"
access_key = st.secrets["humble_access_key"]["access_key"]
secret_key = st.secrets["humble_secret_key"]["secret_key"]
CSV_URL = "https://raw.githubusercontent.com/MahmoudMagdy404/files_holder/main/humble_outbox.csv?token=GHSAT0AAAAAACU33HXMATERVLTKMIHDCDSEZVHWI5Q"

def get_humblefax_details(fax_id):
    url = f"{HUMBLEFAX_API_BASE_URL}/sentFax/{fax_id}"
    auth = (access_key, secret_key)
    try:
        response = requests.get(url, auth=auth)
        response.raise_for_status()

        fax_data = response.json().get("data", {}).get("sentFax", {})
        recipient = fax_data.get("recipients", [{}])[0]

        fax_details = {
            'FaxID': fax_id,
            'ToFaxNumber': recipient.get('toNumber', ''),
            'DateSent': datetime.datetime.utcfromtimestamp(int(fax_data.get('timestamp', 0))).strftime('%Y-%m-%d %H:%M:%S'),
            'SentStatus': fax_data.get('status', ''),
            'FileName': fax_data.get('subject', ''),  # Assuming subject as file name
            'Service': 'HumbleFax'
        }
        return fax_details

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve fax details for fax_id {fax_id}: {e}")
        return None

def list_sent_faxes():
    url = f"{HUMBLEFAX_API_BASE_URL}/sentFaxes"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{access_key}:{secret_key}'.encode()).decode()}"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get HumbleFax outbox: {response.text}")
        return None

def check_and_save_fax_details(fax_details):
    try:
        # Read the existing CSV file
        df = pd.read_csv(CSV_URL)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=['FaxID', 'ToFaxNumber', 'DateSent', 'SentStatus', 'FileName', 'Service'])
    
    # Check if the fax ID already exists
    if fax_details['FaxID'] in df['FaxID'].values:
        print("Fax ID already exists. No new faxes sent.")
        return df

    # Append new fax details
    df = df.append(fax_details, ignore_index=True)

    # Save back to CSV
    df.to_csv(CSV_URL, index=False)
    
    return df

def on_row_select():
    if 'selected_fax_index' in st.session_state and st.session_state['selected_fax_index'] is not None:
        selected_fax = st.session_state['faxes_df'].iloc[st.session_state['selected_fax_index']]
        st.session_state['selected_fax_info'] = f"Selected fax: To {selected_fax['To']} sent on {selected_fax['Date']}"
    else:
        st.session_state['selected_fax_info'] = "No fax selected"



# TOKEN_FOLDER_ID = '1HDwNvgFv_DSEH2WKNfLNheKXxKT_hDM9'
# CREDENTIALS_FILE_NAME = 'credentials.json'
# TOKEN_FILE_NAME = 'token.json'
# SCOPES = ["https://www.googleapis.com/auth/drive"]
# # credentials_json = st.secrets["google_credentials"]["credentials_json"]



# # Constants
# SCOPES = ["https://www.googleapis.com/auth/drive"]
# FOLDER_ID = "15I95Loh35xI2PcGa36xz7SgMtclo-9DC"
# GITHUB_USER = 'MahmoudMagdy404'
# GITHUB_PAO = st.secrets["github_token"]["token"]
# TOKEN_FILE_URL = "https://api.github.com/repos/MahmoudMagdy404/files_holder/contents/token.json"

# def read_token_from_github():
#     """Read the token from GitHub repository."""
#     github_session = requests.Session()
#     github_session.auth = (GITHUB_USER, GITHUB_PAO)
#     try:
#         response = github_session.get(TOKEN_FILE_URL)
#         response.raise_for_status()
#         content = response.json()['content']
#         decoded_content = base64.b64decode(content).decode('utf-8')
#         return json.loads(decoded_content)
#     except Exception as e:
#         st.error(f"Failed to read token from GitHub: {e}")
#         return None

# def write_token_to_github(token_data):
#     """Write the token to GitHub repository."""
#     github_session = requests.Session()
#     github_session.auth = (GITHUB_USER, GITHUB_PAO)
#     try:
#         response = github_session.get(TOKEN_FILE_URL)
#         response.raise_for_status()
#         current_file = response.json()
        
#         content = base64.b64encode(json.dumps(token_data).encode()).decode()
        
#         data = {
#             "message": "Update token.json",
#             "content": content,
#             "sha": current_file['sha']
#         }
        
#         response = github_session.put(TOKEN_FILE_URL, json=data)
#         response.raise_for_status()
#         st.success("Token updated successfully in GitHub.")
#     except Exception as e:
#         st.error(f"Failed to write token to GitHub: {e}")

# def get_drive_service(creds):
#     """Get Google Drive service."""
#     return build('drive', 'v3', credentials=creds)

# def get_credentials():
#     """Get or refresh Google credentials."""
#     token_data = read_token_from_github()
    
#     if not token_data:
#         st.warning("No token found in GitHub. Initiating new authentication flow.")
#         flow = InstalledAppFlow.from_client_config(
#             json.loads(st.secrets["google_credentials"]["credentials_json"]),
#             SCOPES
#         )
#         creds = flow.run_local_server(port=0)
#         write_token_to_github(json.loads(creds.to_json()))
#         return creds
    
#     creds = Credentials.from_authorized_user_info(token_data, SCOPES)
    
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#             write_token_to_github(json.loads(creds.to_json()))
#         else:
#             flow = InstalledAppFlow.from_client_config(
#                 json.loads(st.secrets["google_credentials"]["credentials_json"]),
#                 SCOPES
#             )
#             creds = flow.run_local_server(port=0)
#             write_token_to_github(json.loads(creds.to_json()))
    
#     return creds

# def combine_pdfs(fname):
#     """Combine PDFs from Google Drive folder."""
#     creds = get_credentials()
#     if not creds:
#         return None, "Failed to obtain valid credentials. Please try authenticating again."

#     try:
#         service = get_drive_service(creds)
#         query = f"'{FOLDER_ID}' in parents"

#         st.info("Querying Google Drive...")
#         results = service.files().list(q=query, pageSize=20, fields="nextPageToken, files(id, name, mimeType)").execute()
#         items = results.get("files", [])

#         if not items:
#             return None, "No files found in the specified folder."

#         fname = fname.strip().lower()
#         target_files = [file for file in items if fname in file["name"].lower()]

#         st.info(f"Searching for files with name containing: {fname}")
#         for file in items:
#             st.info(f"Found file: {file['name']}")

#         if not target_files:
#             return None, "No matching files found."

#         st.info(f"Found {len(target_files)} matching files. Combining PDFs...")

#         merger = PdfMerger()
#         for target_file in target_files:
#             mime_type = target_file.get("mimeType")
#             file_id = target_file.get("id")

#             st.info(f"Processing file: {target_file['name']}")

#             if mime_type.startswith("application/vnd.google-apps."):
#                 request = service.files().export_media(fileId=file_id, mimeType="application/pdf")
#             else:
#                 request = service.files().get_media(fileId=file_id)

#             fh = io.BytesIO()
#             downloader = MediaIoBaseDownload(fh, request)
#             done = False
#             while not done:
#                 status, done = downloader.next_chunk()
#                 st.info(f"Download {int(status.progress() * 100)}%")
#             fh.seek(0)

#             pdf_reader = PdfReader(fh)
#             merger.append(pdf_reader)

#         st.info("Finalizing PDF...")
#         output = io.BytesIO()
#         merger.write(output)
#         merger.close()
#         output.seek(0)
#         st.info("PDF combination complete!")

#         return output, None
#     except Exception as error:
#         st.error(f"An error occurred: {str(error)}")
#         return None, str(error)

    
def main():
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Braces Form Submission", "CGM Form", "Send Fax"])
    
    # Adding a note in the sidebar with new color
    st.sidebar.markdown("---")
    st.sidebar.markdown("<h3>Ankle States → L1906</h3>", unsafe_allow_html=True)
    states = ["AR", "TN", "MN", "IL", "NJ", "OH", "KY"]
    for state in states:
        st.sidebar.markdown(f"<p>- {state}</p>", unsafe_allow_html=True)

    if page == "Braces Form Submission":
        st.title("Brace Form Submission")
        st.header("Select Braces")
        brace_columns = st.columns(len(Braces))
        selected_forms = {}
        # Create two rows of columns: 3 columns in the first row, 4 columns in the second row
        col1, col2, col3 = st.columns(3)
        col4, col5, col6, col7 = st.columns(4)

        # Function to handle displaying the braces and their forms
        def display_brace(brace, column):
            if brace not in st.session_state:
                st.session_state[brace] = "None"

            with column:
                st.subheader(f"{brace} Brace")
                brace_options = ["None"] + list(brace_info[brace].keys())
                selected_forms[brace] = st.radio(
                    f"Select {brace} Brace",
                    brace_options,
                    key=brace,
                    index=brace_options.index(st.session_state[brace])
                )

        # Display the first 3 braces in the first row
        for idx, brace in enumerate(Braces[:3]):
            display_brace(brace, [col1, col2, col3][idx])

        # Display the remaining 4 braces in the second row
        for idx, brace in enumerate(Braces[3:]):
            display_brace(brace, [col4, col5, col6, col7][idx])
        # Create containers for each section
        with st.container():
            st.title("Patient and Doctor Information")
                # Row 1
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("Patient Information")
            with col2:
                st.subheader("Patient Metrics")
            with col3:
                st.subheader("Doctor Information")
            
            col1, col2, col3 = st.columns([1, 1, 1])  # Adjust proportions if needed
            
            with col1:
                date = st.date_input("Date")
                fname = st.text_input("First Name")
                lname = st.text_input("Last Name")
                ptPhone = st.text_input("Patient Phone Number")
                ptAddress = st.text_input("Patient Address")
                ptCity = st.text_input("Patient City")
                ptState = st.text_input("Patient State")
                
            
            with col2:
                ptZip = st.text_input("Patient Zip Code")
                ptDob = st.text_input("Date of Birth")
                medID = st.text_input("MBI")
                ptHeight = st.text_input("Height")
                ptWeight = st.text_input("Weight")
                ptGender = st.selectbox("Gender", ["Male", "Female"])

                # Apply any desired styling here
                # st.markdown("""
                # <style>
                # .css-1d391kg {
                #     width: 100% !important;
                # }
                # </style>
                # """, unsafe_allow_html=True)
            
            with col3:
                
                drName = st.text_input("Doctor Name")

                drAddress = st.text_input("Doctor Address")
                drCity = st.text_input("Doctor City")
                drState = st.text_input("Doctor State")
                drZip = st.text_input("Doctor Zip Code")
                drPhone = st.text_input("Doctor Phone Number")
                drFax = st.text_input("Doctor Fax Number")
                drNpi = st.text_input("Doctor NPI")

        # Submit Button
        st.markdown("<br>", unsafe_allow_html=True)

        def validate_all_fields():
            required_fields = [
                fname, lname, ptPhone, ptAddress,
                ptCity, ptState, ptZip, ptDob, medID,
                ptHeight, ptWeight, drName,
                drAddress, drCity, drState, drZip,
                drPhone, drFax, drNpi
            ]
            return all(required_fields)

        if st.button("Generate PDF"):
            if not validate_all_fields():
                st.warning("Please fill out all required fields.")
            else:
                selected_braces = [(brace_code, brace_info[brace_type][brace_code]) 
                                for brace_type, brace_code in selected_forms.items() 
                                if brace_code != "None"]

                if not selected_braces:
                    st.warning("Please select at least one brace.")
                else:
                    for brace_code, brace_description in selected_braces:

                        patient_data = {
                            "date": date.strftime("%m/%d/%Y"),
                            "fname": fname,
                            "lname": lname,
                            "dob": ptDob,
                            "address": ptAddress,
                            "city": ptCity,
                            "state": ptState,
                            "zip": ptZip,
                            "phone": ptPhone,
                            "medID": medID,
                            "height": ptHeight,
                            "weight": ptWeight,
                            "gender": ptGender
                        }

                        doctor_data = {
                            "name": drName,
                            "npi": drNpi,
                            "address": drAddress,
                            "city": drCity,
                            "state": drState,
                            "zip": drZip,
                            "phone": drPhone,
                            "fax": drFax
                        }
                        
                        # To store generated PDFs
                        pdf_files = []


                        
                        # Loop through each selected brace and generate individual PDFs
                        for brace_code, brace_description in selected_braces:
                            diagnoses = "".join(
                                f'<div style="display: inline-block; margin-bottom: 2px; font-size: 12px;"><input type="checkbox" style="margin-right: 2px; width: 14px; height: 14px; accent-color: black;"> {diagnosis}</div>'
                                for diagnosis in brace_description[1:]
                            )

                            affected_area = get_affected_areas(brace_code)

                            html_filled = html_code.format(
                                brace_type = get_brace_type(brace_code),
                                date=patient_data["date"],
                                fname=patient_data["fname"],
                                lname=patient_data["lname"],
                                dob=patient_data["dob"],
                                address=patient_data["address"],
                                city=patient_data["city"],
                                state=patient_data["state"],
                                zip=patient_data["zip"],
                                phone=patient_data["phone"],
                                medID=patient_data["medID"],
                                height=patient_data["height"],
                                weight=patient_data["weight"],
                                gender=patient_data["gender"],
                                doctor_name=doctor_data["name"],
                                doctor_npi=doctor_data["npi"],
                                doctor_address=doctor_data["address"],
                                doctor_city=doctor_data["city"],
                                doctor_state=doctor_data["state"],
                                doctor_zip=doctor_data["zip"],
                                doctor_phone=doctor_data["phone"],
                                doctor_fax=doctor_data["fax"],
                                Selected_Brace=brace_code,
                                Brace_info=brace_description[0],
                                diagnosis = diagnoses,
                                affected_areas = affected_area
                            )

                            generate_pdf(html_filled)  # Call the function to generate PDF
    
    elif page == "CGM Form":
        display_cgm_form()
        
    elif page == "Send Fax":
        st.title("Send Fax")
        
        # Improved Subheader Design for Uploading PDFs
        st.subheader("**Upload PDF Files to be Sent**")
        st.markdown("You can upload multiple PDF files here. These files will be combined and processed before sending them via fax.")

        uploaded_files = st.file_uploader("Upload PDF Files", type="pdf", accept_multiple_files=True)

        if uploaded_files:
            st.write(f"Uploaded {len(uploaded_files)} file(s):")
            for uploaded_file in uploaded_files:
                st.write(f"- {uploaded_file.name}")
                
            if st.button("Process Uploaded PDFs"):
                with st.spinner("Processing uploaded PDFs..."):
                    from PyPDF2 import PdfMerger
                    merger = PdfMerger()
                    
                    for uploaded_file in uploaded_files:
                        merger.append(uploaded_file)
                    
                    combined_output = io.BytesIO()
                    merger.write(combined_output)
                    merger.close()
                    combined_output.seek(0)
                    
                    st.session_state['uploaded_pdfs'] = combined_output
                    st.session_state['uploaded_pdfs_names'] = [file.name for file in uploaded_files]
                    st.success("Uploaded PDFs processed successfully.")
                    st.experimental_rerun()

        if 'uploaded_pdfs' in st.session_state:
            st.download_button(
                label="Download Combined PDF",
                data=st.session_state['uploaded_pdfs'].getvalue(),
                file_name="combined_uploaded_files.pdf",
                mime="application/pdf"
            )
            st.success("Uploaded PDF(s) are ready for further processing (e.g., sending faxes).")
        # Improved Subheader Design for Uploading Cover Sheet
        st.subheader("Upload Cover Sheet :red[**(Optional)**]")
        st.markdown("If you have a pre-prepared cover sheet, you can upload it here. Otherwise, you'll need to fill out the information below to generate one.")

        uploaded_cover_sheet = st.file_uploader("Upload Cover Sheet", type="pdf")
        # Improved Subheader Design for Fax Service Selection
        st.subheader("**Select Fax Service**")

        fax_service = st.radio(
            "Choose a fax service:",
            ["SRFax", "HumbleFax", "FaxPlus"],
            horizontal=True
        )


        receiver_number = st.text_input("Receiver Fax Number")

        if fax_service == "SRFax":
            st.subheader(":red[**Enter SRFax Credentials**]")
            st.markdown("If you don't have an account, you can leave these fields empty. Otherwise, please provide your SRFax login credentials.")

            user = st.text_input("Fax User")
            password = st.text_input("Fax Password", type="password")

        if not uploaded_cover_sheet:
            st.subheader(":blue[**Fill Out Cover Sheet Information**]")
            st.markdown("Since you haven't uploaded a cover sheet, please provide the following information to generate one.")

            fax_message = st.text_area("Fax Message")
            fax_subject = st.text_input("Fax Subject")
            to_name = st.text_input("To (Recipient Name)")
            chaser_name = st.selectbox("From (Sender Name)", list(chasers_dict.keys()))

        else:
            fax_message = None
            fax_subject = None
            to_name = None
            chaser_name = None
        

            
        if st.button("Send Fax"):
            if not uploaded_cover_sheet and (not receiver_number or not fax_message or not fax_subject or not to_name or not chaser_name):
                st.error("Please provide all required fields to generate a cover sheet.")
            elif 'uploaded_pdfs' not in st.session_state:
                st.error("Please combine PDFs before sending a fax.")
            else:
                combined_pdf = st.session_state.get('uploaded_pdfs')
                chaser_number = chasers_dict.get(chaser_name, "")
                
                chaser_email = chasers_emails.get(chaser_name, "")
                if chaser_name=="INCALL":
                    chaser_email = st.text_input("Enter Your Email")
                fax_message_with_number = f"{fax_message}<br><br><b>From: {chaser_name}</b><br><b>Phone: {chaser_number}<b><br><b>Email: {chaser_email}<b>" if fax_message else ""
                
                if fax_service == "SRFax":
                    result = handle_srfax(combined_pdf, receiver_number, fax_message_with_number, fax_subject, to_name, chaser_name, uploaded_cover_sheet,user,password)
                elif fax_service == "HumbleFax":
                    result = handle_humblefax(combined_pdf, receiver_number, fax_message_with_number, fax_subject, to_name, chaser_name, uploaded_cover_sheet)
                elif fax_service == "HalloFax":
                    result = handle_hallofax(combined_pdf, receiver_number, fax_message_with_number, fax_subject, to_name, chaser_name, uploaded_cover_sheet)
                elif fax_service == "FaxPlus":
                    result = handle_faxplus(combined_pdf, receiver_number, fax_message_with_number, fax_subject, to_name, chaser_name, uploaded_cover_sheet)

                if result:
                    st.success(f"Fax sent successfully using {fax_service}.")
                else:
                    st.error(f"Failed to send fax using {fax_service}. Please check the logs for more information.")

    elif page == "Sent Faxes List":
        st.title("Sent Faxes List")
        st.header("Refax Option")

        # Fax service selection using radio buttons
        st.subheader("Select Fax Service")
        fax_service = st.radio(
            "Choose a fax service:",
            ["SRFax", "HumbleFax", "HalloFax", "FaxPlus"],
            horizontal=True
        )

        if st.button("List Sent Faxes"):
            all_faxes = []

            if fax_service == 'SRFax':
                all_faxes = []
                outbox = get_srfax_outbox()
                if outbox and outbox['Status'] == 'Success':
                    faxes = outbox['Result']
                    for fax in faxes:
                        fax['Service'] = 'SRFax'
                    all_faxes.extend(faxes)

            elif fax_service == 'HumbleFax':
                all_faxes = []
                outbox = get_humble_outbox()
                if outbox:
                    faxes = outbox["data"].get("sentFaxIds", [])
                    print(faxes)
                    for fax_id in faxes[:10]:
                        # Assuming you have a way to get details for each fax_id
                        print(fax_id)
                        fax_details = get_humblefax_details(fax_id)  # You need to implement this function
                        print(fax_details)
                        if fax_details:
                            fax_details['Service'] = 'HumbleFax'
                            all_faxes.append(fax_details)

            elif fax_service == 'HalloFax':
                all_faxes = []
                outbox = get_hallo_outbox()
                if outbox and outbox['Status'] == 'Success':
                    faxes = outbox['Result']
                    for fax in faxes:
                        fax['Service'] = 'HalloFax'
                    all_faxes.extend(faxes)

            elif fax_service == 'FaxPlus':
                all_faxes = []
                outbox = get_faxplus_outbox()
                if outbox:
                    for fax in outbox:
                        fax['Service'] = 'FaxPlus'
                    all_faxes.extend(outbox)

            if all_faxes:
                # Create a DataFrame from the faxes data
                df = pd.DataFrame(all_faxes)
                df = df[['ToFaxNumber', 'DateSent', 'SentStatus', 'FileName', 'Service']]  # Include FileName for resending
                df.columns = ['To', 'Date', 'Status', 'FileName', 'Service']  # Rename columns for display

                # Store the DataFrame in session state for later use
                st.session_state['faxes_df'] = df
                st.session_state['selected_fax_index'] = None
                st.session_state['selected_fax_info'] = "No fax selected"

        if 'faxes_df' in st.session_state:
            # Display the DataFrame
            st.dataframe(
                st.session_state['faxes_df'].drop(columns=['FileName']),
                height=300
            )

            # Add a number input for row selection
            selected_index = st.number_input("Select a row number", min_value=1, max_value=len(st.session_state['faxes_df']), value=1, step=1) - 1

            if st.button("Confirm Selection"):
                st.session_state['selected_fax_index'] = selected_index
                on_row_select()

            # Display the selected fax information
            st.write(st.session_state.get('selected_fax_info', "No fax selected"))
            
            # Check if any row is selected
            if st.session_state.get('selected_fax_index') is not None:
                if st.button("Resend Selected Fax"):
                    selected_fax = st.session_state['faxes_df'].iloc[st.session_state['selected_fax_index']]
                    service = selected_fax['Service']
                    if service == 'SRFax':
                        result = resend_srfax(selected_fax['FileName'])
                    elif service == 'HumbleFax':
                        result = resend_humble(selected_fax['FileName'])
                    elif service == 'HalloFax':
                        result = resend_hallo(selected_fax['FileName'])
                    elif service == 'FaxPlus':
                        result = resend_faxplus(selected_fax['FileName'])
                    else:
                        st.error("Unknown fax service.")
                        return
                    
                    if result and result['Status'] == 'Success':
                        st.success("Fax resent successfully!")
                    else:
                        st.error(f"Failed to resend fax. Reason: {result.get('Result', 'Unknown error')}")

if __name__ == "__main__":
    main()