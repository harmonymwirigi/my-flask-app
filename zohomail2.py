from flask import Flask, render_template, request, redirect, url_for, make_response, send_file
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from datetime import datetime, timedelta
from PyPDF2 import  PdfReader, PdfMerger
from datetime import datetime
import requests
import base64
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


app = Flask(__name__)

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  
REPO_NAME = 'Pkkothapelly/TCFiles'  
BASE_URL = 'https://api.github.com'

auth = HTTPBasicAuth()

users = {
    "Wolf": generate_password_hash(os.getenv('ADMIN_PASSWORD')),
    "user": generate_password_hash(os.getenv('USER_PASSWORD'))
}


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def index():
    error_message = request.args.get('error_message')
    success_message = request.args.get('success_message')
    return render_template('index.html', error=error_message, success=success_message)

@app.route('/generate_pdf', methods=['POST'])
@auth.login_required
def generate_pdf():
    try:
        # Extract data from the form
        vehicle_reg_number = request.form.get('vehicle_reg_number').strip()
        title = request.form.get('title').strip()
        First_name = request.form.get('First_name').strip()
        last_name = request.form.get('last_name').strip()
        policy_num = request.form['policy_number'].strip()  # Define policy_num here
        effective_date = request.form.get('effective_date')
        effective_time = request.form.get('effective_time')
        expiry_date = request.form.get('expiry_date')
        expiry_time = request.form.get('expiry_time')
        
        effective_datetime = datetime.strptime(effective_date + ' ' + effective_time, '%Y-%m-%d %H:%M')
        expiry_datetime = datetime.strptime(expiry_date + ' ' + expiry_time, '%Y-%m-%d %H:%M')
        
        # Generate PDF data
        pdf_data = generate_pdf_report(vehicle_reg_number, title, First_name, last_name, effective_datetime, expiry_datetime, policy_num)
        
        # Upload PDF to GitHub
        upload_to_github(pdf_data, "Certificate_of_Motor_Insurance_for_KGM_policy.pdf", policy_num)  # Use policy_num here
        
        # Create response to download the PDF
        response = make_response(pdf_data)
        response.headers['Content-Disposition'] = 'attachment; filename=Certificate_of_Motor_Insurance_for_KGM_policy.pdf'
        response.mimetype = 'application/pdf'
        return response
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return redirect(url_for('index', error_message=error_message))


    
    
@app.route('/generate_pdf2', methods=['POST'])
@auth.login_required
def generate_pdf2():
    try:
        # Extract data from the form
        vehicle_reg_number = request.form.get('vehicle_reg_number').strip()
        title = request.form.get('title').strip()
        First_name = request.form.get('First_name').strip()
        last_name = request.form.get('last_name').strip()
        policy_num = request.form['policy_number'].strip()  # Define policy_num here
        address = request.form['address'].strip()
        address2 = request.form['address2'].strip()
        address3 = request.form['address3'].strip()
        postcode = request.form['postcode'].strip()
        telephone = request.form['telephone'].strip()
        email = request.form['email'].strip()
        sex = request.form['sex'].strip()
        dob = request.form.get('dob')
        make = request.form['make'].strip()
        model = request.form['model'].strip()
        vehicle_value_from = request.form['vehicle_value_from'].strip()
        vehicle_value_to = request.form['vehicle_value_to'].strip()
        effective_date = request.form.get('effective_date')
        effective_time = request.form.get('effective_time')
        expiry_date = request.form.get('expiry_date')
        expiry_time = request.form.get('expiry_time')
        
        effective_datetime = datetime.strptime(effective_date + ' ' + effective_time, '%Y-%m-%d %H:%M')
        expiry_datetime = datetime.strptime(expiry_date + ' ' + expiry_time, '%Y-%m-%d %H:%M')
        
        # Generate PDF data
        pdf_data = generate_additional_pdf_report(title, First_name, last_name, address, address2, address3, postcode, telephone, email, effective_date, effective_time, expiry_date, expiry_time, effective_datetime, expiry_datetime, sex, dob, make, model, vehicle_reg_number, vehicle_value_from, vehicle_value_to)
        
        # Upload PDF to GitHub
        upload_to_github(pdf_data, "Statement_of_Fact_for_KGM_policy.pdf", policy_num)  # Use policy_num here
        
        # Create response to download the PDF
        response = make_response(pdf_data)
        response.headers['Content-Disposition'] = 'attachment; filename=Statement_of_Fact_for_KGM_policy.pdf'
        response.mimetype = 'application/pdf'
        return response
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return redirect(url_for('index', error_message=error_message))




@app.route('/generate_third_pdf', methods=['POST'])
@auth.login_required
def generate_third_pdf():
    try:
        title = request.form.get('title').strip()
        First_name = request.form.get('First_name').strip()
        last_name = request.form.get('last_name').strip()
        policy_num = request.form['policy_number'].strip()  # Define policy_num here
        address = request.form['address'].strip()
        address2 = request.form['address2'].strip()
        address3 = request.form['address3'].strip()
        postcode = request.form['postcode'].strip()
        effective_date = request.form.get('effective_date')
        effective_time = request.form.get('effective_time')
        expiry_date = request.form.get('expiry_date')
        expiry_time = request.form.get('expiry_time')
        vehicle_reg_number = request.form.get('vehicle_reg_number').strip()
        vehicle_value_from = request.form['vehicle_value_from'].strip()
        vehicle_value_to = request.form['vehicle_value_to'].strip()
        make = request.form['make'].strip()
        model = request.form['model'].strip()
        insurance_premium_tax = request.form['insurance_premium_tax'].strip()

        # Generate PDF data
        pdf_data = generate_third_pdf_report(title, First_name, last_name, address, address2, address3, postcode, effective_date, effective_time, expiry_date, expiry_time, vehicle_reg_number, vehicle_value_from, vehicle_value_to, make, model, policy_num,insurance_premium_tax)
        
        # Upload PDF to GitHub
        upload_to_github(pdf_data, "New_Policy_Schedule_for_KGM_policy.pdf", policy_num)  # Use policy_num here

        # Create response to download the PDF
        response = make_response(pdf_data)
        response.headers['Content-Disposition'] = 'attachment; filename=New Policy Schedule for KGM policy.pdf'
        response.mimetype = 'application/pdf'
        return response
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return redirect(url_for('index', error_message=error_message))


@app.route('/store_pdf', methods=['POST'])
@auth.login_required
def store_pdf():
    try:
        # Extract data from the form
        vehicle_reg_number = request.form.get('vehicle_reg_number').strip()
        title = request.form.get('title').strip()
        first_name = request.form.get('First_name').strip()
        last_name = request.form['last_name'].strip()
        policy_num = request.form['policy_number'].strip()  # This will be used as the folder name for the files
        effective_date = request.form.get('effective_date')
        effective_time = request.form.get('effective_time')
        expiry_date = request.form.get('expiry_date')
        expiry_time = request.form.get('expiry_time')
        address = request.form['address'].strip()
        address2 = request.form['address2'].strip()
        address3 = request.form['address3'].strip()
        postcode = request.form['postcode'].strip()
        telephone = request.form['telephone'].strip()
        email = request.form['email'].strip()
        sex = request.form['sex'].strip()
        dob = request.form['dob']
        make = request.form['make'].strip()
        model = request.form['model'].strip()
        vehicle_value_from = request.form['vehicle_value_from'].strip()
        vehicle_value_to = request.form['vehicle_value_to'].strip()
        insurance_premium_tax = request.form['insurance_premium_tax'].strip()

        
        effective_datetime = datetime.strptime(effective_date + ' ' + effective_time, '%Y-%m-%d %H:%M')
        expiry_datetime = datetime.strptime(expiry_date + ' ' + expiry_time, '%Y-%m-%d %H:%M')
        
        # Generate the PDFs
        pdf_data1 = generate_pdf_report(vehicle_reg_number, title, first_name, last_name, effective_datetime, expiry_datetime, policy_num)
        pdf_data2 = generate_additional_pdf_report(title, first_name, last_name, address, address2, address3, postcode, telephone, email, effective_date, effective_time, expiry_date, expiry_time, effective_datetime, expiry_datetime, sex, dob, make, model, vehicle_reg_number, vehicle_value_from, vehicle_value_to)
        pdf_data3 = generate_third_pdf_report(title, first_name, last_name, address, address2, address3, postcode, effective_date, effective_time, expiry_date, expiry_time, vehicle_reg_number, vehicle_value_from, vehicle_value_to, make, model, policy_num, insurance_premium_tax)
        
        # Upload PDFs to the Pkkothapelly/TCFiles repository under the policy number folder
        upload_to_github(pdf_data1, "Certificate of Motor Insurance for KGM policy.pdf", "Pkkothapelly/TCFiles", policy_num)
        upload_to_github(pdf_data2, "Statement of Fact for KGM policy.pdf", "Pkkothapelly/TCFiles", policy_num)
        upload_to_github(pdf_data3, "New Policy Schedule for KGM policy.pdf", "Pkkothapelly/TCFiles", policy_num)
        
        # Generate HTML content for the policy page
        html_content = generate_html_content(policy_num, first_name, last_name, vehicle_reg_number, effective_datetime, expiry_datetime)
        
        # Convert HTML content to bytes
        html_data = html_content.encode('utf-8')
        
        # Upload the HTML file to the Pkkothapelly/Pkkothapelly.github.io repository
        upload_to_github(html_data, f"{policy_num}.html", "Pkkothapelly/Pkkothapelly.github.io")

        success_message = "PDFs and HTML have been successfully stored on GitHub."
        return redirect(url_for('index', success_message=success_message))
    except Exception as e:
        error_message = f"An error occurred while storing PDFs and HTML: {str(e)}"
        return redirect(url_for('index', error_message=error_message))





@app.route('/send_email', methods=['POST'])
@auth.login_required
def send_email():
    try:
        # Retrieve form data
        vehicle_reg_number = request.form['vehicle_reg_number'].strip()
        title = request.form['title'].strip()
        First_name = request.form['First_name'].strip()
        last_name = request.form['last_name'].strip()
        effective_date = request.form['effective_date']
        effective_time = request.form['effective_time']
        expiry_date = request.form['expiry_date']
        expiry_time = request.form['expiry_time']
        email = request.form['email'].strip()
        address = request.form['address'].strip()
        address2 = request.form['address2'].strip()
        address3 = request.form['address3'].strip()
        postcode = request.form['postcode'].strip()
        telephone = request.form['telephone'].strip()
        sex = request.form['sex'].strip()
        dob = request.form['dob']
        make = request.form['make'].strip()
        model = request.form['model'].strip()
        vehicle_value = request.form['vehicle_value'].strip()
        
        dob_date = datetime.strptime(dob, '%Y-%m-%d') if dob else None
        
        effective_datetime = datetime.strptime(effective_date + ' ' + effective_time, '%Y-%m-%d %H:%M')
        expiry_datetime = datetime.strptime(expiry_date + ' ' + expiry_time, '%Y-%m-%d %H:%M')
        
        # Generate PDF document
        pdf_data1 = generate_pdf_report(vehicle_reg_number, title, First_name, last_name, effective_datetime, expiry_datetime)
        pdf_data2 = generate_additional_pdf_report(title, First_name, last_name, address, address2, address3, postcode,telephone, email, effective_date, effective_time, expiry_date, expiry_time ,effective_datetime, expiry_datetime, sex, dob, make, model, vehicle_reg_number, vehicle_value)
        
        pdf_data3 = generate_third_pdf_report(title, First_name, last_name, address, address2, address3, postcode, effective_date, effective_time, expiry_date, expiry_time, vehicle_reg_number, vehicle_value, make, model, insurance_premium_tax)
        
        
        # Send email with the combined PDF attachment
        send_email_with_attachment(pdf_data1, pdf_data2, pdf_data3, email)
        
        # Redirect to the index page with a success message
        return redirect(url_for('index', success_message='Email sent successfully!'))
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return redirect(url_for('index', error_message=error_message))

def add_footer(canvas, logo_path,footer_y_position):
    logo_width = 150
    logo_height = 31.183
    x_position = 230
    
    canvas.drawImage(logo_path, x_position, footer_y_position, width=logo_width, height=logo_height, mask='auto')
    

def generate_pdf_report(vehicle_reg_number, title,  First_name, last_name, effective_datetime, expiry_datetime, policy_num):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Draw logo
    # Update this with the path to your logo file
    logo_path = 'https://raw.githubusercontent.com/Pkkothapelly/test/main/Logo.jpg'
    p.drawImage(logo_path, 40, 712, width=120, height=53.26)
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(350,740,"Claims Hotline: 0333 241 3392")
    
    p.setLineWidth(3)
    p.line(30, 710, letter[0] - 30, 710)

    # Header
    p.setFont("Helvetica-Bold", 16)
    text_width = p.stringWidth("Certification of Motor Insurance", "Helvetica-Bold", 16)
    x_position = (letter[0] - text_width) / 2
    p.drawString(x_position, 690, "Certification of Motor Insurance")

    certificate_number = policy_num
    certificate_text = "Certificate Number: "
    certificate_text_width = p.stringWidth(certificate_text, "Helvetica", 10)
    certificate_number_width = p.stringWidth(certificate_number, "Helvetica", 10)
    total_width = certificate_text_width + certificate_number_width
    x_certificate_text_position = (letter[0] - total_width) / 2
    p.setFont("Helvetica-Bold", 10)
    p.drawString(x_certificate_text_position, 670, certificate_text)
    p.drawString(x_certificate_text_position + certificate_text_width + 5, 670, certificate_number)
    
    p.setFont("Helvetica-Bold", 10)
    p.drawString(30, 642, "(1)   Vehicle Registration Number:")
    p.setFont("Helvetica",10)
    p.drawString(210, 642,  "{}".format(vehicle_reg_number))
    p.setFont("Helvetica-Bold",10)
    p.drawString(30, 617, "(2)   Insured:")
    p.setFont("Helvetica",10)
    full_name = "{} {} {}".format(title, First_name, last_name)
    p.drawString(110, 617,  full_name)
    p.setFont("Helvetica-Bold",10)
    p.drawString(30, 592, "(3)   Effective Time/Date:")
    p.setFont("Helvetica",10)
    p.drawString(150, 592, "{}".format(effective_datetime.strftime("%H:%M %d-%m-%Y")))
    p.setFont("Helvetica-Bold", 10)
    p.drawString(290, 592, "(4)   Expiry Time/Date:")
    p.setFont("Helvetica", 10)
    p.drawString(400, 592, "{}".format(expiry_datetime.strftime("%H:%M %d-%m-%Y")))
    p.setFont("Helvetica-Bold", 10)
    p.drawString(30, 565, "(5)   Persons or Classes of Persons Entitled to Drive")
    p.setFont("Helvetica", 8)
    p.drawString(38, 555, "     (Provided that the person holds a licence to drive such a vehicle and is not disqualified from holding or obtaining such a licence)")
    p.setFont("Helvetica",10)
    p.drawString(50,530, full_name)
    
    p.setFont("Helvetica-Bold", 10)
    p.drawString(30, 510, "(6)   Limitations to use:")
    p.setFont("Helvetica", 10)
    p.drawString(38, 480, "     The policy covers the insured vehicle for social, domestic and pleasure use including travelling to and from a permanent")
    p.drawString(38, 470, "     place business.")
    p.drawString(38, 455, "     Exclusive include use for hiring, racing, pace making, speed testing or competitions, performance testing, the carriage")
    p.drawString(38, 445, "     of goods or passengers for hire and reward, or for any purpose in connection with the motor trade.")
    p.setFont("Helvetica-Bold", 10)
    p.drawString(38, 415, "     This certificate cannot be used as evidence of cover for the purpose of recovering impounded vehicles.")
    p.setFont("Helvetica", 8)
    p.drawString(30, 390, "I hereby certify that the insurance to which this certificate relates satisfies the requirements of the related law applicable in Great Britain, Nothern")
    p.drawString(30, 380, "Ireland, the isle of man, the island of Guernsey, the Island of Jersey and the Island of Alderney.")
    p.drawString(30, 370, "For and on behalf of underwriters subscribing to KGM Motor.")
    p.drawString(100, 320, "KGM Motor")
    p.drawString(100, 310, "2nd floor")
    p.drawString(100, 300, "St James House")
    p.drawString(100, 290, "27-43 Eastern Road")
    p.drawString(100, 280, "Romford")
    p.drawString(100, 270, "Essex RM1 3NH")
    logo_path = 'https://raw.githubusercontent.com/Pkkothapelly/test/main/Signature.jpg'
    p.drawImage(logo_path, 315, 300, width=80, height=20)
    p.drawString(310, 290, "NEIL MANVELL")
    p.drawString(310, 280, "Motor Underwriter")
    p.setFont("Helvetica", 6)
    p.drawString(30, 240, "Note: For full details of the insurance cover reference should be made to the Insurance Document and Schedule.")
    p.drawString(30, 230, "Advice to Third Parties: Nothing contained in this Certificate affects your right as a Third Party to make a claim.")
    p.setLineWidth(3)
    p.line(30, 215, letter[0] - 30, 215)
    
    p.setLineWidth(1)
    p.rect(30, 175, letter[0] - 60, 28)
    
    p.setLineWidth(0.5)
    underline_position = 185 + 28 * 0.2
    p.line(35, underline_position, 35 + p.stringWidth("Important", "Helvetica-Bold", 10)+11, underline_position)
    
    p.setFont("Helvetica-Bold", 10)
    p.drawString(35, 192, "IMPORTANT")
    p.setFont("Helvetica", 6)
    p.drawString(35, 180,"Please read this carefully, and check that it meets with your requirements and keep it safely with policy document.")  
    
    p.setLineWidth(0.5)
    underline_position = 148 + 28 * 0.2
    p.line(30, underline_position, 30 + p.stringWidth("Insurer Information", "Helvetica-Bold", 10), underline_position)
    
    p.setFont("Helvetica-Bold", 10)
    p.drawString(30, 155, "Insurer Information")
    p.setFont("Helvetica-Bold",7.5)
    p.drawString(30, 140, "KGM Motor is a brand name for business written by KGM Underwriting Services Limited. KGM Underwriting Services Limited is authorised and regulated by")
    p.drawString(30, 130, "the Financial Conduct Authority. FCA Firm Refernece Number 799643. Registered in England & Wales, No: 10581020. Registered Office: 2n Floor, St James")
    p.drawString(30, 120, "House, 27-43 Eastern Road, Romford, Essex, RM1 3NH.")
    
    footer_new_y_position = 27
    footer_logo_path = 'https://raw.githubusercontent.com/Pkkothapelly/test/main/TempcoverLogo.jpg'
    add_footer(p,footer_logo_path,footer_new_y_position )
    
    p.showPage()
    p.save()
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data


def generate_additional_pdf_report(title, First_name, last_name, address, address2, address3, postcode,telephone, email, effective_date, effective_time, expiry_date, expiry_time,  effective_datetime, expiry_datetime, sex, dob, make, model, vehicle_reg_number, vehicle_value_from, vehicle_value_to):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    logo_path = 'https://raw.githubusercontent.com/Pkkothapelly/test/main/Logo.jpg'
    p.drawImage(logo_path, 410, 730, width=125, height=55.48)
    
    p.rect(33, 80, letter[0] - 73, 620)
    # Add basic text
    p.setFont("Helvetica-Bold", 12)
    p.drawString(33, 710, "STATEMENT OF FACT - Short Term Insurance")
    
    
    p.setFont("Helvetica-BoldOblique", 8.5)
    p.drawString(65, 658, "Your Agent")
    p.setFont("Helvetica", 8.5)
    p.drawString(65, 646, "Agent")
    p.drawString(230, 646, "Tempcover Limited")
    
    
    p.setFont("Helvetica-BoldOblique", 8.5)
    p.drawString(65, 626, "Your Details - Name Address")
    p.setFont("Helvetica", 8)
    p.drawString(65, 616, "Surname") 
    p.drawString(230, 616, "{}".format(last_name)) 
    p.drawString(65, 603, "Forename(s)") 
    p.drawString(230, 603, "{}".format(First_name))
    p.drawString(65, 590, "Title")
    p.drawString(230, 590, "{}".format(title))
    p.drawString(65, 577, "Address")
    full_address = "{}, {}, {}, {}".format(address, address2, address3, postcode)
    p.drawString(230, 577, full_address)
    p.drawString(65, 564, "Telephone number") 
    p.drawString(230, 564, "{}".format(telephone)) 
    p.drawString(65, 551, "Email address") 
    p.drawString(230, 551, "{}".format(email))
    
    
    p.setFont("Helvetica-BoldOblique", 8.5)
    p.drawString(65, 531, "Your Policy Cover")
    p.setFont("Helvetica", 8.5)
    p.drawString(65, 521, "Effective Date") 
    p.drawString(230, 521, "{}".format(effective_datetime))   
    p.drawString(65, 508, "Expiry Date")  
    p.drawString(230, 508, "{}".format(expiry_datetime))
    p.drawString(65, 495, "Policy Cover")
    p.drawString(230, 495, "FULLY COMPREHENSIVE")
    p.drawString(65, 482, "Number of Drivers(including you)")
    p.drawString(230, 482, "1")
    p.drawString(65, 469, "Class of Use")
    p.drawString(230, 469, "Use for social, domestic and pleasure purposes only.")
    
    p.setFont("Helvetica-BoldOblique", 8.5)
    p.drawString(65, 449, "Driver Details(including You)")
    full_name = "{} {} {}".format(title, First_name, last_name)
    p.setFont("Helvetica", 8.5)
    p.drawString(65, 439, "Full Name") 
    p.drawString(230, 439, full_name) 
    p.drawString(65, 426, "Sex")  
    p.drawString(230, 426, "{}".format(sex))
    p.drawString(65, 413, "Date of birth")  
    p.drawString(230, 413, "{}".format(dob))
    p.drawString(65, 400, "License Type")  
    p.drawString(230, 400, "Full UK licence")
    p.drawString(65, 387, "Occupation")  
    p.drawString(230, 387, "Not required")
    
    p.setFont("Helvetica-BoldOblique", 8.5)
    p.drawString(65, 367, "Vehicle Details")
    p.setFont("Helvetica", 8.5)
    p.drawString(65, 357, "Make")
    p.drawString(230, 357, "{}".format(make))
    p.drawString(65, 344, "Model")  
    p.drawString(230, 344, "{}".format(model))
    p.drawString(65, 331, "Registration number")  
    p.drawString(230, 331, "{}".format(vehicle_reg_number))
    p.drawString(65, 318, "Vehicle Value")  
    p.drawString(230, 318, "£{} to £{}".format(vehicle_value_from, vehicle_value_to))
    
    p.setFillColorRGB(0,0,0)
    p.setLineWidth(1)
    p.rect(40, 88, letter[0] - 90, 16, fill=1)
    
    p.setFillColorRGB(1,1,1)
    p.setFont("Helvetica-Bold",8.7)
    p.drawString(80,93, "IMPORTANT - You also must read the KGM Motor Proposer Declaration & Imporatant Notes on Pages 2 & 3")
    
    footer_new_y_position = 35
    footer_logo_path = 'https://raw.githubusercontent.com/Pkkothapelly/test/main/TempcoverLogo.jpg'
    add_footer(p,footer_logo_path,footer_new_y_position)
    
    
    p.showPage()
    
    logo_path = 'https://raw.githubusercontent.com/Pkkothapelly/test/main/Logo.jpg'
    p.drawImage(logo_path, 410, 738, width=125, height=55.48)
    p.setFont("Helvetica-Bold", 18)
    p.drawString(32, 720, "KGM MOTOR / PROPOSER DECLARATION")
    p.setFont("Helvetica", 9)
    p.drawString(48, 700, "1.")
    p.drawString(65, 700, "I declare that I:")
    p.drawString(82, 688, "a.   Hold a current United Kingdom Driving Licence with a Full Entitlement to drive a Motor Car for at least 6 months.")
    p.drawString(82, 674, "b.   Have no more than 6 penalty points for any motoring convictions endorsed on my driving licence in the past 3")
    p.drawString(97, 664, "years.")
    p.drawString(82, 650, "c.   Am not aware of any pending prosecution or Police enquiry pending for any motoring offences.")
    p.drawString(82, 636, "d.   Am not and have not been disqualified from driving a motor vehicle or had my driving licence revoked within the")
    p.drawString(97, 626, "last 5 years")
    p.drawString(82, 612, 'e.   Have no criminal convictions that are not considered as "spent" (A spend conviction is one which, under the terms')
    p.drawString(97, 602, "of the Rehabilitation of Offenders Act 1974, can be effectively ignored after a specified amount of time). If, however")
    p.drawString(97, 592, "you have received a custodial sentence of four years or more, your conviction will never become spent.")
    p.drawString(82, 578, "f.    Have had no more than 2 accidents, claims or losses in the past 3 years that was considered my fault either")
    p.drawString(97, 568, "partially or fully.")
    p.drawString(82, 554, "g.   Have been a permanent UK resident for at least the last 24 months")
    p.drawString(82, 540, "h.   Have not had any previous insurance policy declined or refused or had any additional terms imposed or had any")
    p.drawString(97, 530, "previous insurance policy cancelled or voided by the insurer.")
    p.drawString(82, 516, "i.    Have not been employed or work within any of the following excluded occupations or trades - Courier workers,")
    p.drawString(97, 506, "Entertainment industry, Sportsperson or connected industry, Bodyguard, Circus proprietor, Circus worker,")
    p.drawString(97, 496, "Fairground worker, Fast food industry, Funfair employee, Mobile caterer, House person or currently unemployed.")
    
    p.drawString(48, 478, "2.")
    p.drawString(65, 478, "I declare that the vehicle:")
    p.drawString(82, 464, "a.   Is not a Van, Lorry, Minibus, Horsebox, Motor Caravan, Motor Home, Recovery Vehicle, Licenced Taxt or Minicab or")
    p.drawString(97, 454, "a Tipper")
    p.drawString(82, 440, "b.   Has no more than 7 seats in total and is right-hand drive only and has a valid MOT certificate (if required) and has")
    p.drawString(97, 430, "not been recorded as a Category A or B insurance total loss.")
    p.drawString(82, 416, "c.   Will only be used by me for Social, Domestic and Pleasure purposes including commuting to one permanent")
    p.drawString(97, 406, " place of business.")
    p.drawString(82, 392, "d.   Will") 
    p.setFont("Helvetica-Bold", 9)
    p.drawString(114, 392, "not")
    p.setFont("Helvetica", 9)
    p.drawString(130, 392, "be used for carriage of goods or passengers for hire and reward, racing, pace-making, speed testing.")
    p.drawString(97, 382, "competitions, rallies or trails, track days, whether on a road, track or at an off-road event, commercial travelling,")
    p.drawString(97, 372, "scrap waste or use for any purpose in relation to the motor trade")
    p.drawString(82, 358, "e.   Will")
    p.setFont("Helvetica-Bold", 9)
    p.drawString(114, 358, "not") 
    p.setFont("Helvetica", 9)
    p.drawString(130, 358,"be used to carry hazardous, corrosive or explosive goods.")
    p.drawString(82, 344, "f.    Has") 
    p.setFont("Helvetica-Bold", 9)
    p.drawString(116, 344, "not") 
    p.setFont("Helvetica", 9)
    p.drawString(132, 344, "been modified or altered from the manufacturer's standard specification. Such modifications could")
    p.drawString(97, 334, "include changes to the bodywork (such as spoilers and body kits), changes to the brakes or suspension")
    p.drawString(97, 324, "(including lowering the vehicle), cosmetic changes (such as alloy wheels or tinted windows), changes affecting")
    p.drawString(97, 314, 'performance (such as engine management enhancements including "chipping" and the exhaust system). This is')
    p.drawString(97, 304, "not a full list of all possible changes and you should seek guidance from a professional if you are in any doubt")
    p.drawString(97, 294, "about changes that may have been made to your vehicle.")
    p.drawString(82, 282, "g.   Will not be exported from the UK during the duration of the policy.")
    p.drawString(82, 268, "h    Has a current market value not exceeding £50,000")
    p.drawString(48, 252, "3.")
    
    p.setLineWidth(1.5)
    underline_position = 245 + 28 * 0.2
    p.line(256, underline_position, 256 + p.stringWidth("cannot", "Helvetica-Bold")-2, underline_position)
    
    p.drawString(65, 252, "I am aware that this temporary insurance policy cannot be used for Hire or Loan Vehicles (i.e. Vehicle Rentals, Vehicle")
    p.drawString(65, 240, "Salvage or Recovery Agents, Credit Hire Vehicles or Companies and Accident Management Companies)")
    p.drawString(48, 224, "4.")
    p.drawString(65, 224, "I declare that the Certificate of Motor Insurance and any other documents will not be used as evidence of insurance for the")
    p.drawString(65, 212, "release of a vehicle impounded or confiscated by the Police or Local Authority.")
    p.drawString(48, 196, "5.")
    
    p.setLineWidth(1.5)
    underline_position = 189 + 28 * 0.2
    p.line(196, underline_position, 196 + p.stringWidth("minimum", "Helvetica-Bold"), underline_position)
    
    p.drawString(65, 196, "I am aware that this policy has a minimum excess in respect of Accidental Damage, Malicious Damage, Fire and Theft")
    p.drawString(65, 184, "claims of £500")
    p.drawString(48, 168, "6.")
    p.drawString(65, 168, "I am aware in the event of an incident resulting in a claim under this policy where there is a non-traceable responsible ")
    
    p.setLineWidth(1.5)
    underline_position = 147 + 28 * 0.2
    p.line(347, underline_position, 347 + p.stringWidth("additional", "Helvetica-Bold")-2, underline_position)
    
    p.drawString(65, 156, "third party, or the incident is a fault incident involving no other party, an additional £500 excess will apply.")
    
    
    p.showPage()
    
    logo_path = 'https://raw.githubusercontent.com/Pkkothapelly/test/main/Logo.jpg'
    p.drawImage(logo_path, 410, 738, width=125, height=55.48)
    p.setFont("Helvetica", 9)
    p.drawString(48, 718, "7.")
    p.drawString(65, 718, "I am aware that the driving of other cars is not permitted under this policy.")
    p.drawString(48, 704, "8.")
    p.drawString(65, 704, "I am aware that no amendments, alterations or changes can be made to this policy or Certificate of Motor Insurance once")
    p.drawString(65, 694, "Issued")
    p.drawString(48, 680, "9.")
    p.drawString(65, 680, "I have read and agree that the above conditions are met and that I have take masonable care not to make any")
    p.drawString(65, 670, "misrepresentation of the information I have provided.")
    p.setFont("Helvetica", 9)
    p.drawString(32, 648, "*I have read and agree that the above conditions are met and that i have taken reasonable care not to make any")
    p.drawString(32, 638, "misrepresentation of the information provided.")
    
    p.drawString(32, 616, "KGM Motor are pro-active in managing Fraud detection in proposals for Motor Insurance policies and claims submitted.")
    p.drawString(32, 606, "Insurers pass information to the Claims and Underwriting Register, and the Motor Insurance Anti-Fraud and Theft Register")
    p.drawString(32, 596, "in order to check information provided and also to prevent fraudulent claims. If any claim is in any way fraudulent, including")
    p.drawString(32, 586, "inflating or exaggerating the claim, or submitting forged or falsified documents, or if you have not given complete or")
    p.drawString(32, 576, "accurate information, then no payment will be made, all cover under this policy will end and the appropriate Authorities will")
    p.drawString(32, 566, "be informed.")
    
    p.setFont("Helvetica-Bold", 12)
    p.drawString(32, 544, "DECLARATION")
    
    p.setFont("Helvetica", 8.5)
    p.drawString(32, 530, "I declare that the answers given on this document are complete and correct to the best my knowledge and belief. I agree to accept the policy")
    p.setFont("Helvetica", 8.4)
    p.drawString(32, 520, "subject to the terms, conditions and exceptions contained within. I also declare that if a third party (such as an insurance broker) has completed")
    p.drawString(32, 510, "this form on my behalf that I have checked that all of the questions have been answered correctly.")
    p.setFont("Helvetica", 8.3)
    p.drawString(32, 500, "I Understand that you will pass information I have provided on this form to the Motor Insurance Database (MID), the Claims and Underwriting")
    p.setFont("Helvetica", 8.45)
    p.drawString(32, 490, "Exchange Register and the Motor Insurance Anti-Fraud and Theft Register for the purposes described below and consent to the data transfer.")
    
    p.setFont("Helvetica-Bold", 12)
    p.drawString(32, 470, "WARNING")
    p.setFont("Helvetica-Bold", 8.5)
    p.drawString(32, 456, "Detecting and Preventing Fraud")
    p.setFont("Helvetica", 8.4)
    p.drawString(32, 447, "In order to keep premiums as low was possible for all of our customers, we participate in a number of industry initiatives to aid the prevention and")
    p.setFont("Helvetica", 8.45)
    p.drawString(32, 438, "detection of crime, especially insurance related fraud. We pass information to the Claims and Underwriting Exchange Register and the Motor")
    p.setFont("Helvetica", 8.5)
    p.drawString(32, 429, "Insurance Anti-Fraud and Theft Register operated by The Motor Insurers Bureau (MIB). We may search these registers and any other relevant ")
    p.drawString(32, 420, "databases in order to make decisions regarding the provision and administration of insurance and, when you make a claim, to validate your claims")
    p.setFont("Helvetica", 8.55)
    p.drawString(32, 411, "history or that of any person or property likely to be involved in the claim.")
    
    p.setFont("Helvetica-Bold", 8.5)
    p.drawString(32, 394, "Motor Insurance Database")
    p.setFont("Helvetica", 8.5)
    p.drawString(32, 385, "Information relating to your insurance policy will be added to the Motor Insurance Database (MID) which is managed by the Motor Insurers' Bureau")
    p.setFont("Helvetica", 8.44)
    p.drawString(32, 376, "(MIB). MID and the data stored on it may be used by certain statutory and/or authorised bodies including the Police, the DVLA, the DVANI, the")
    p.setFont("Helvetica", 8.5)
    p.drawString(32, 367, "Insurance Fraud Bureau and other bodies permitted by law for purposes not limited to but including Electronic Licensing, Continuous Insurance")
    p.setFont("Helvetica", 8.64)
    p.drawString(32, 358, "Enforcement, law enforcement (prevention, detection, apprehension and/or prosecution of offenders) and the provision of government services")
    p.setFont("Helvetica", 8.56)
    p.drawString(32, 349, "and or other services aimed at reducing the level and incidence of uninsured driving. If you are involved in a road traffic accident (either in the UK,")
    p.setFont("Helvetica", 8.46)
    p.drawString(32, 340, "the EEA or certain other territories), insurers and/or the MIB may search the MID to obtain relevant information. Persons (including their appointed")
    p.drawString(32, 331, "representatives) pursuing a claim in respect of a road traffic accident (including citizens of other countries) may also obtain relevant information")
    p.drawString(32, 322, "which is held on the MID. It is vital that the MID holds your correct registration number. If it is incorrectly shown on the MID you are at risk of having")
    p.drawString(32, 313, "your vehicle seized by the Police. You can check that your correct registration number details are shown on the MID at www.askmid.com.")
    
    p.setFont("Helvetica-Bold", 8.55)
    p.drawString(32, 295, "Complaints")
    p.setFont("Helvetica", 8.65)
    p.drawString(82, 295, "If you have an enquiry about any aspect of your insurance policy then please refer to your Broker in the first instance. If you need to")
    p.setFont("Helvetica", 8.3)
    p.drawString(32, 286, "make a complaint then please contact, KGM Motor, 2nd Floor, St James House, 27-43 Eastern Road, Romford, Essex, RM1 3NH. Tel:020 8530")
    p.drawString(32, 277, "7351; Fax: 020 8530 7037; e-mail: compliance.kgm@kgmus.co.uk.")
    
    p.setFont("Helvetica", 8.66)
    p.drawString(32, 259, "We will attempt to resolve your complaint as soon as possible within 3 days, however if this is not possible we will get in touch and advise you of")
    p.drawString(32, 250, "the next step: If we are unable to resolve your complaint or you are dissatisfied with out decision you may have the right to refer your complaint")
    p.setFont("Helvetica", 8.5)
    p.drawString(32, 241, "to the FinanciaOmbudsman Service. The Financial Ombudsman Service is an independent service in the UK for settling disputes between")
    p.setFont("Helvetica", 8.58)
    p.drawString(32, 232, "consumers and businesses providing financial services. You can find more information on the Financial Ombudsman Service at www.financial-")
    p.setFont("Helvetica", 8.35)
    p.drawString(32, 223, "ombudsman.org.uk. The Financial Ombudsman Service, Exchange Tower, London E14 9SR. Tel: 0800 023 4567 or 0300 123 9 123; e-mail:")
    p.setFont("Helvetica", 8.5)
    p.drawString(32, 214, "complaint.info@financial-ombudsman.org.uk. Further details will be provided at the appropriate stage of the complaint process. This procedure is")
    p.setFont("Helvetica", 8.57)
    p.drawString(32, 205, "without prejudice to your rights to take legal proceedings.")
    
    p.setFont("Helvetica", 8.5)
    p.drawString(32, 187, "KGM Motor is a brand name for business written by KGM Underwriting Services Limited. KGM Underwriting Services Limited is authorised and")
    p.setFont("Helvetica", 8.40)
    p.drawString(32, 178, "regulated by the Financial Conduct Authority, FCA Firm Reference Number 799643. Registered in England & Wales, No 10581020. Registered")
    p.drawString(32, 169, "Office: 2nd Floor, St James House, 27-43 Eastern Road, Romford, Essex, RM1 3NH.")

    
    
    
    p.setFillColorRGB(0,0,0)
    p.setLineWidth(1)
    p.rect(31, 97, letter[0] - 57, 60, fill=1)
    
    p.setFillColorRGB(1,1,1)
    p.setFont("Helvetica-Bold",12)
    p.drawString(272,145, "IMPORTANT")
    p.setFont("Helvetica-Bold",11.62)
    p.drawString(48,130, "There is no need to sign this document, as by agreeing to the declaration during the quotation")
    p.setFont("Helvetica-Bold",11.64)
    p.drawString(62,115, "process you have confirmed that you have read and agree to the KGM Motor / Proposer's")
    p.drawString(272,100, "Declaration")
    

    p.showPage()
    p.save()
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data

def generate_third_pdf_report(title, First_name, last_name, address, address2, address3, postcode, effective_date, effective_time, expiry_date, expiry_time, vehicle_reg_number, vehicle_value_from, vehicle_value_to, make, model, policy_num, insurance_premium_tax):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    logo_path = 'https://raw.githubusercontent.com/Pkkothapelly/test/main/Logo.jpg'
    p.drawImage(logo_path, 33, 730, width=128, height=56.79)
    
    p.rect(30, 720, letter[0] - 68, -192)
    
    p.setLineWidth(1)
    p.line(30, 691, letter[0] - 38, 691) # Horizontal Line
    
    p.setFont("Helvetica-Bold", 10)
    p.drawString(44, 703,"SHORT TERM INSURANCE - KGM MOTOR")
    
    p.setLineWidth(1)
    p.line(357, 720, 357, 691) #Vertical Line
    
    p.setFont("Helvetica-Bold", 10)
    p.drawString(395, 703,"NEW BUSINESS SCHEDULE")
    
    p.setLineWidth(1)
    p.line(30, 659, letter[0] - 38, 659) # Horizontal Line
    
    p.setFont("Helvetica-Bold", 8.5)
    p.drawString(37, 679,"Policy Number:")
    p.drawString(200, 679,"Date Issued:")
    
    p.drawString(310, 679,"Agent:")
    p.drawString(37, 647,"Insured:")
    
    p.drawString(310, 647,"Effective Time/Date:")
    p.drawString(310, 630,"Expiry Time/Date:")
    p.drawString(310, 610,"Reason for Issue:")
    p.drawString(310, 590,"Premium(inc. ipt):")
    p.drawString(37, 569,"Insured Vehicle:      Registration Number:")
    p.setLineWidth(1.5)
    underline_position = 563 + 28 * 0.2
    p.line(37, underline_position, 37 + p.stringWidth("Insured Vehicle", "Helvetica-Bold")+3, underline_position)
    p.drawString(365, 569,"Cover:")
    
    p.drawString(37, 549,"Vehicle Value:")
    p.drawString(205, 549,"Make and Model of Vehicle:")
    
    p.setFont("Helvetica", 12)
    p.drawString(37,630,"{}".format(address))
    p.drawString(37,617,"{}, {}".format(address2, address3))
    p.drawString(37,604,"{}".format(postcode))
    
    p.setFont("Helvetica", 8.5)
    p.drawString(37, 668, "{}".format(policy_num))
    
    date_object = datetime.strptime(effective_date, "%Y-%m-%d")
    formatted_date = date_object.strftime("%d/%m/%Y")
    p.drawString(200,668, formatted_date)
    
    p.drawString(310,668,"Tempcover Limited")
    
    full_name = "{} {} {}".format(title, First_name, last_name)
    p.drawString(75,647, full_name)
    
    date_time_string = effective_date + ' ' + effective_time
    effective_datetime = datetime.strptime(date_time_string, '%Y-%m-%d %H:%M')
    formatted_datetime = effective_datetime.strftime('%H:%M %d %B %Y')
    p.drawString(458,647, formatted_datetime)
    
    date_time_string = expiry_date + ' ' + expiry_time
    expiry_datetime = datetime.strptime(date_time_string, '%Y-%m-%d %H:%M')
    formatted_datetime1 = expiry_datetime.strftime('%H:%M %d %B %Y')
    p.drawString(458,630, formatted_datetime1)
    
    p.drawString(478, 610, "New Business")
    p.drawString(506, 590, f"£{insurance_premium_tax}")
    
    p.drawString(210, 569, "{}" .format(vehicle_reg_number))
    
    p.drawString(396, 569, "FULLY COMPREHENSIVE")
    
    p.drawString(37,537, "£{} to £{}" .format(vehicle_value_from, vehicle_value_to))
    
    p.drawString(205, 537, "{}, {}" .format(make, model))

    
    p.setLineWidth(1)
    p.line(195, 691, 195, 659) #Vertical Line
    
    
    p.setLineWidth(1)
    p.line(301, 691, 301, 581) #Vertical Line
    
    p.setLineWidth(1)
    p.line(30, 643, letter[0] - 38, 643) # Horizontal Line
    
    p.setLineWidth(1)
    p.line(301, 623, letter[0] - 38, 623) # Horizontal Line
    
    p.setLineWidth(1)
    p.line(301, 602, letter[0] - 38, 603) # Horizontal Line
    
    p.setLineWidth(1)
    p.line(30, 581, letter[0] - 38, 581) # Horizontal Line
    
    p.setLineWidth(1)
    p.line(30, 563, letter[0] - 38, 563) # Horizontal Line
    
    p.setLineWidth(1)
    p.line(357, 581, 357, 563) #Vertical Line
    
    p.setLineWidth(3)
    p.line(29, 522, letter[0] - 40, 523) # Horizontal Thick Line
    
    p.setLineWidth(1)
    p.rect(30, 516, letter[0] - 68, -131) #Second Box
    
    p.setFont("Helvetica-Bold", 9)
    p.drawString(37,504,"ENDORSEMENTS APPLICABLE (Full wordings shown within ENDORSEMENTS)")
    
    p.setLineWidth(1.5)
    underline_position = 497 + 28 * 0.2
    p.line(37, underline_position, 37 + p.stringWidth("ENDORSEMENTS APPLICABLE (Full wordings shown within ENDORSEMENTS)", "Helvetica-Bold"), underline_position)
    #p.setLineWidth(2)
    #p.line(29, 499, letter[0] - 38, 499) # Horizontal Thick Line
    
    p.setFont("Helvetica", 8.5)
    p.drawString(37, 486, "XDO - EXCLUDING DRIVING OTHER CARS")
    p.drawString(37, 474, "NTTP - ADDITIONAL EXCESS")
    p.drawString(37, 462, "XSDH - SELF DRIVE HIRE")
    p.drawString(37, 450, "XIMV - IMPOUNDED VEHICLES")
    p.drawString(37, 438, "XAMD - ALTERATIONS")
    
    p.drawString(37, 421 ,"Compulsory Excess Amount:    £500.00")
    p.drawString(37, 411, "Voluntary Excess Amount:            £0.00")
    
    p.setLineWidth(1.5)
    underline_position = 400 + 28 * 0.2
    p.line(37, underline_position, 37 + p.stringWidth("Total Excess Amount:         £500.00", "Helvetica-Bold")+7, underline_position)
    
    p.setFont("Helvetica-Bold", 8.5)
    p.drawString(37, 393, "Total Excess Amount:            £500.00")
    
    p.setLineWidth(3)
    p.line(29, 379, letter[0] - 40, 379) # Horizontal Thick Line
     
    p.setLineWidth(1)
    p.rect(30, 373, letter[0] - 68, -153.5) #Third Box
    
    p.setFont("Helvetica-Bold", 8.5)
    p.drawString(37, 361, "ENDORSEMENTS - only apply if noted in the ENDORSEMENTS APPLICABLE above")
    p.setLineWidth(1.5)
    underline_position = 353 + 28 * 0.2
    p.line(37, underline_position, 37 + p.stringWidth("ENDORSEMENTS - only apply if noted in the ENDORSEMENTS APPLICABLE above")+0.5, underline_position)
    
    
    
    p.setFont("Helvetica-Bold", 6.5)
    p.drawString(37,344,"XDO-EXCLUDING DRIVING OTHER CARS")
    p.setLineWidth(1.5)
    underline_position = 338 + 28 * 0.2
    p.line(37, underline_position, 37 + p.stringWidth("XDO-EXCLUDING DRIVING OTHER CARS")+0.5, underline_position)
    p.drawString(37,323,"NTTP-ADDITIONAL EXCESS")
    p.setLineWidth(1.5)
    underline_position = 316 + 28 * 0.2
    p.line(37, underline_position, 37 + p.stringWidth("NTTP-ADDITIONAL EXCESS"), underline_position)
    p.drawString(37,278,"XSDH-SELF DRIVE HIRE")
    underline_position = 271 + 28 * 0.2
    p.line(37, underline_position, 37 + p.stringWidth("XSDH-SELF DRIVE HIRE"), underline_position)
    p.drawString(37,255,"XIMV-IMPOUNDED VEHICLES.")
    underline_position = 248 + 28 * 0.2
    p.line(37, underline_position, 37 + p.stringWidth("XIMV-IMPOUNDED VEHICLES."), underline_position)
    p.drawString(37,232,"XAMD - ALTERATIONS")
    underline_position = 224 + 28 * 0.2
    p.line(37, underline_position, 37 + p.stringWidth("XAMD - ALTERATIONS"), underline_position)
    
    
    p.setFont("Helvetica", 6)
    p.drawString(37,336,"The driving of other cars is not permitted under this insurance")
    
    p.drawString(37,315,"In the event of an incident resulting in a claim under the policy where:")
    p.drawString(37,308,"i) there is a non-traceable responsible third party: or")
    p.drawString(37,301,"ii) the incident is a fault incident involving no other party")
    p.drawString(37,294,"an excess of £500 will apply. This excess will be in addition to any other excess shown elsewhere in this policy document or on your policy schedule or in any endorsement.")
    
    p.drawString(37,270,"There is no cover under this policy when the insured vehicle is owned by, operated by, supplied by, hired or rented from any Claims, Credit hire or Accident Management Company.")
    p.drawString(37,247,"This policy cannot be used for the purpose of recovering an impounded or confiscated vehicle.")
    p.drawString(37,223,"No amendments, alterations or changes can be made to this policy or certificate of insurance once issued.")
    
    
    p.setFont("Helvetica-Bold", 9)
    p.drawString(37, 197, "Motor Insurance Database")
    p.setLineWidth(1.5)
    underline_position = 190 + 28 * 0.2
    p.line(37, underline_position, 37 + p.stringWidth("Motor Insurance Database")+0.5, underline_position)
    p.setFont("Helvetica", 5.5)
    p.drawString(37,186,"Information relating to your insurance policy will be added to the Motor Insurance Database (MID) which is managed by the Motor Insurers' Bureau (MIB). MID and the data stored on it may be used by certain statutory")
    p.setFont("Helvetica", 5.6)
    p.drawString(37,178,"and/or authorised bodies including the Police, the DVLA, the DVANI, the Insurance Fraud Bureau and other bodies permitted by law for purposes not limited to but including Electronic Licensing, Continuous")
    p.setFont("Helvetica", 5.5)
    p.drawString(37,170,"Insurance Enforcement, law enforcement (prevention, detection, apprehension and/or prosecution of offenders) and the provision of government services and or other services aimed at reducing the level and")
    p.setFont("Helvetica", 5.53)
    p.drawString(37,162,"incidence of uninsured driving. If you are involved in a road traffic accident (either in the UK, the EEA or certain other territories), insurers and/or the MIB may search the MID to obtain relevant information. Persons")
    p.setFont("Helvetica", 5.6)
    p.drawString(37,154,"(including their appointed representatives) pursuing a claim in respect of a road traffic accident (including citizens of other countries) may also obtain relevant information which is held on the MID. It is vital that the")
    p.setFont("Helvetica", 5.53)
    p.drawString(37,146,"MID holds your correct registration number. If it is incorrectly shown on the MID you are at risk of having your vehicle seized by the Police. You can check that your correct registration number details are shown on the")
    p.setFont("Helvetica", 5.56)
    p.drawString(37,139,"MID at www.askmid.com. You should show this notice to anyone insured to drive the vehicle covered under this policy")
    
    p.setFont("Helvetica-Bold", 9)
    p.drawString(37, 105, "Insurer Information")
    p.setLineWidth(1.5)
    underline_position = 98 + 28 * 0.2
    p.line(37, underline_position, 37 + p.stringWidth("Insurer Information")+0.5, underline_position)
    p.setFont("Helvetica", 5.5)
    p.drawString(37,93,"KGM Motor is a brand name for business written by KGM Underwriting Services Limited. KGM Underwriting Services Limited is authorised and regulated by the Financial Conduct Authority, FCA Firm Reference")
    p.drawString(37,85,"Number 799643. Registered in England & Wales, No: 10581020. Registered Office: 2nd Floor, St James House, 27-43 Eastern Road, Romford, Essex, RM1 3NH.")
    
    p.setLineWidth(3)
    p.line(29, 214, letter[0] - 40, 214) # Horizontal Thick Line
    
    p.setLineWidth(1)
    p.rect(30, 208, letter[0] - 68, -77.3) #Fourth Box
    
    p.setLineWidth(3)
    p.line(29, 125, letter[0] - 40, 125) # Horizontal Thick Line
    
    p.setLineWidth(1)
    p.rect(30, 119, letter[0] - 68, -59) #Fifth Box
    
    p.setLineWidth(3)
    p.line(29, 54, letter[0] - 40, 54) # Horizontal Thick Line
    
    
    footer_new_y_position = 10
    footer_logo_path = 'https://raw.githubusercontent.com/Pkkothapelly/test/main/TempcoverLogo.jpg'
    add_footer(p,footer_logo_path,footer_new_y_position)
    
    p.showPage()
    p.save()
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data


def send_email_with_attachment(pdf_data1, pdf_data2, pdf_data3, recipient_email):
    try:
        from_email = "noreply@tempcover.ac"  # Your Zoho Mail address for authentication
        display_name = "No Reply"
        sender_email = from_email  # The email address you want the recipient to see
        smtp_server = "smtp.zoho.eu"
        smtp_port = 587
        smtp_username = from_email  # Your Zoho Mail address for authentication
        smtp_password = "Tempcoverac@1"  # Your Zoho Mail password or application-specific password

        msg = MIMEMultipart()
        msg['From'] = f"{display_name} <{sender_email}>"
        msg['To'] = recipient_email
        msg['Subject'] = "Insurance Certificate Documents"
        msg.add_header('reply-to', sender_email)

        # Attach the first PDF content to the email
        attachment1 = MIMEBase('application', 'octet-stream')
        attachment1.set_payload(pdf_data1)
        encoders.encode_base64(attachment1)
        attachment1.add_header('Content-Disposition', 'attachment', filename='insurance_certificate_1.pdf')
        msg.attach(attachment1)

        # Attach the second PDF content to the email
        attachment2 = MIMEBase('application', 'octet-stream')
        attachment2.set_payload(pdf_data2)
        encoders.encode_base64(attachment2)
        attachment2.add_header('Content-Disposition', 'attachment', filename='insurance_certificate_2.pdf')
        msg.attach(attachment2)

        # Attach the third PDF content to the email
        attachment3 = MIMEBase('application', 'octet-stream')
        attachment3.set_payload(pdf_data3)
        encoders.encode_base64(attachment3)
        attachment3.add_header('Content-Disposition', 'attachment', filename='insurance_certificate_3.pdf')
        msg.attach(attachment3)

        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.set_debuglevel(1)  # Enable debug output
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
    except smtplib.SMTPException as e:
        print("SMTP error occurred: ", str(e))
        raise
    except Exception as e:
        print("An error occurred while sending the email:", str(e))
        raise

def generate_html_content(policy_number, first_name, last_name, vehicle_reg_number, effective_datetime, expiry_datetime):
    # Format dates
    start_date_str = effective_datetime.strftime("%A, %d %B %Y at %H:%M")
    end_date_str = expiry_datetime.strftime("%A, %d %B %Y at %H:%M")
    
    # Generate the HTML content with inline CSS
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Download-Policy-{policy_number}</title>
        <style>
            body {{
                font-family: Helvetica, Arial, sans-serif;
                background-color: white;
                margin: 0;
                padding: 20px;
                color: #333;
            }}
            .main-header, .main-footer {{
                text-align: center;
                margin-bottom: 2rem;
            }}
            .main-header {{
                margin-top: -1rem;
                padding-right: 1rem;
            }}
            .main-header h1 {{
                margin-bottom: -0.5rem;
                font-size: 1.7rem;
                text-align: right;
                padding-right: 510px;
                color: #234397;
            }}
            .header-paragraph {{
                text-align: right;
                padding-right: 510px;
                font-size: 14px;
                color: #234397;
            }}
            .container {{
                background-color: white;
                width: 28rem;
                margin-left: 480px;
                transform: translateY(-70px);
                height: 23rem;
                border: 1px solid #19a4e0;
            }}
            .header {{
                background-color: #19a4e0;
                color: white;
                padding: 10px 20px;
                text-align: left;
                font-size: 20px;
                font-weight: 100;
            }}
            .content {{
                margin-left: 20px;
                text-align: left;
                margin-right: 30px;
            }}
            .pdf-icon {{
                width: 18px;
                height: auto;
                vertical-align: middle;
                margin-right: 5px;
            }}
            .pdf-link {{
                color: #19a4e0;
                text-decoration: none;
                font-family: 'Avenir Next Paneuropean', Arial, sans-serif;
                font-size: 17px;
                margin-left: 20px;
                font-weight: 100;
            }}
            .download-item {{
                display: flex;
                align-items: center;
                line-height: 1;
                margin-bottom: 7px;
            }}
            .new-container {{
                margin-left: 977px;
                background-color: #f8f8f8;
                color: black;
                width: 400px;
                display: flex;
                flex-direction: column;
                justify-content: space-around;
                align-items: left;
                border: 1px solid #000;
                min-height: 100px;
                height: auto;
                transform: translateY(87px);
            }}
            .section {{
                width: 100%;
                padding: 10px;
                text-align: left;
                box-sizing: border-box;
                flex-grow: 1;
            }}
            .section-top {{
                border-bottom: 2px solid #000;
            }}
            .section-middle {{
                border-bottom: 2px solid #000;
            }}
            .info-container {{
                width: 28rem;
                margin-left: 480px;
                padding-right: 0px;
                height: auto;
                text-align: left;
                transform: translateY(-40px);
                font-size: 16.3px;
            }}
            .home-button-container {{
                width: 28rem;
                margin-left: 295px;
                text-align: center;
                margin-top: 20px;
            }}
            .home-button {{
                background-color: #234397;
                color: white;
                padding: 7px 11px;
                border: none;
                cursor: pointer;
                border-radius: 1px;
                font-size: 15px;
                font-weight: bold;
                transform: translateY(-25px);
            }}
            .home-button:hover {{
                background-color: #1a2e70;
            }}
            .logo-container {{
                text-align: left;
                width: 330px;
                margin-left: 480px;
                position: absolute;
            }}
            .logo-container img {{
                width: 100%;
                height: auto;
            }}
            .policy-details {{
                font-size: 35px;
                margin-left: 480px;
                transform: translateY(90px);
                font-weight: 700;
            }}

            /* Media query for mobile devices */
            @media (max-width: 767px) {{
                .logo-container {{
                    width: 70%;
                    margin-left: 0;
                    text-align: left;
                    position: static;
                }}
                .logo-container img {{
                    width: 80%;
                    margin: 0 auto;
                }}
                .main-header {{
                    padding-right: 0;
                    text-align: left;
                }}
                .main-header h1 {{
                    padding-right: 0;
                    text-align: center;
                    font-size: 1.9rem;
                }}
                .header-paragraph {{
                    text-align: left;
                    padding-right: 0;
                    font-size: 14px; 
                }}
                .policy-details {{
                    font-size: 2rem;
                    margin: 0 auto;
                    margin-top: 10px;
                    text-align: left;
                    transform: translateY(0);
                    margin-left: 20px;
                }}
                .new-container {{
                    width: 90%;
                    margin: 20px auto;
                    transform: translateY(0);
                }}
                .container {{
                    width: 90%;
                    margin: 0 auto;
                    transform: translateY(0);
                    height: auto;
                    padding-bottom:10px;
                }}
                .info-container {{
                    display: none;
                }}
                .home-button-container {{
                    width: 90%;
                    margin: 20px auto;
                    text-align: left;
                    margin-left:20px;
                    transform: translateY(40px);
                }}
            }}
        </style>
    </head>
    <body>
        <div class="logo-container">
            <a href="https://www.tempcover.com/">
                <img src="https://raw.githubusercontent.com/Pkkothapelly/test/main/TempcoverLogo.jpg" alt="Company Logo">
            </a>
        </div>
        <header class="main-header">
            <h1>SHORT TERM INSURANCE</h1>
            <p class="header-paragraph">We are the UK's largest temporary and short term insurance provider.</p>
        </header>
        <h1 class="policy-details">POLICY DETAILS</h1>
        <div class="new-container">
            <div class="section section-top" style="margin-top:3px;margin-bottom:10px;">
                <strong>From</strong> {start_date_str} <br><strong>To</strong> {end_date_str}
            </div>
            <div class="section section-middle" style="margin-top:0px;margin-bottom:5px;">
                Your reference: {policy_number}
            </div>
            <div class="section section-bottom" style="font-weight:bold;">
                Policy: Fully Comprehensive cover
            </div>
        </div>
        <div class="container">
            <div class="header">
                Documents you need now
            </div>
            <div class="content">
                <p>Policy documents will be sent to the email address provided. If you need your documents posting to you, please let us know by emailing</p>
            </div>
            <p style="margin-left:20px; transform: translateY(-12px)">contactus@tempcover.com.</p>
            <div class="content download-item">
                <img src="https://raw.githubusercontent.com/Pkkothapelly/test/main/PdfLogo.png" alt="PDF Icon" class="pdf-icon">
                <a href="https://raw.githubusercontent.com/Pkkothapelly/TCFiles/main/{policy_number}/Certificate%20of%20Motor%20Insurance%20for%20KGM%20policy.pdf" target="_blank" download class="pdf-link">Certificate of Motor Insurance</a>
            </div>
            <div class="content download-item">
                <img src="https://raw.githubusercontent.com/Pkkothapelly/test/main/PdfLogo.png" alt="PDF Icon" class="pdf-icon">
                <a href="https://raw.githubusercontent.com/Pkkothapelly/TCFiles/main/{policy_number}/New%20Policy%20Schedule%20for%20KGM%20policy.pdf" target="_blank" class="pdf-link">New Policy Schedule</a>
            </div>
            <div class="content download-item">
                <img src="https://raw.githubusercontent.com/Pkkothapelly/test/main/PdfLogo.png" alt="PDF Icon" class="pdf-icon">
                <a href="https://raw.githubusercontent.com/Pkkothapelly/TCFiles/main/TCV-MOT-464758383/DocumentationViewPolicyPdf.pdf" target="_blank" class="pdf-link">Policy Wording</a>
            </div>
            <div class="content download-item">
                <img src="https://raw.githubusercontent.com/Pkkothapelly/test/main/PdfLogo.png" alt="PDF Icon" class="pdf-icon">
                <a href="https://raw.githubusercontent.com/Pkkothapelly/TCFiles/main/TCV-MOT-464758383/DocumentationViewPolicyPdf%20(3).pdf" download class="pdf-link">Tempcover Contract</a>
            </div>
            <div class="content download-item">
                <img src="https://raw.githubusercontent.com/Pkkothapelly/test/main/PdfLogo.png" alt="PDF Icon" class="pdf-icon">
                <a href="https://raw.githubusercontent.com/Pkkothapelly/TCFiles/main/{policy_number}/Statement%20of%20Fact%20for%20KGM%20policy.pdf" download class="pdf-link">Statement of Fact</a>
            </div>
            <div class="content download-item">
                <img src="https://raw.githubusercontent.com/Pkkothapelly/test/main/PdfLogo.png" alt="PDF Icon" class="pdf-icon">
                <a href="https://raw.githubusercontent.com/Pkkothapelly/TCFiles/main/TCV-MOT-464758383/DocumentationViewPolicyPdf%20(2).pdf" download class="pdf-link">Insurance Product Information</a>
            </div>
        </div>
        <div class="info-container">
            <p>Unable to view your documentation? Download Adobe reader for free <a href="https://www.adobe.com/uk/acrobat/pdf-reader.html?mv=search&mv2=paidsearch&sdid=SGDJMC8N&ef_id=Cj0KCQjwjLGyBhCYARIsAPqTz19EU_RburxmDjQzMv7sbw8oYmD7GQt8hdxBOa-9-LMFHzIVMcwaVw0aAiv2EALw_wcB:G:s&s_kwcid=AL!3085!3!680670812824!e!!g!!adobe%20reader%20download!13089937081!123710545913&gad_source=1&gclid=Cj0KCQjwjLGyBhCYARIsAPqTz19EU_RburxmDjQzMv7sbw8oYmD7GQt8hdxBOa-9-LMFHzIVMcwaVw0aAiv2EALw_wcB">here</a></p>
        </div>
        <div class="home-button-container">
            <a href="https://www.tempcover.com/">
                <button class="home-button">HOME</button>
            </a>
        </div>
    </body>
    </html>
    """
    return html_content

def upload_to_github(file_data, filename, repo_name, directory=""):
    """
    Uploads the given file data to GitHub under the specified repository and path.

    Args:
        file_data (bytes): The file content to upload.
        filename (str): The name of the file to upload.
        repo_name (str): The repository name where the file should be uploaded.
        directory (str): The directory path within the repository where the file should be stored.
    """
    import base64
    import requests

    # Construct GitHub API URL for the file path
    if directory:
        api_url = f"https://api.github.com/repos/{repo_name}/contents/{directory}/{filename}"
    else:
        api_url = f"https://api.github.com/repos/{repo_name}/contents/{filename}"

    # Check if the file already exists to get its SHA
    sha = None
    response = requests.get(api_url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    if response.status_code == 200:
        sha = response.json().get('sha')

    # Prepare the data for the request
    data = {
        "message": f"Add or update {filename}",
        "content": base64.b64encode(file_data).decode('utf-8'),
        "committer": {
            "name": "Automated Script",
            "email": "noreply@example.com"
        }
    }

    if sha:
        data["sha"] = sha

    # Send the request to upload the file to GitHub
    response = requests.put(
        api_url,
        json=data,
        headers={"Authorization": f"token {GITHUB_TOKEN}"}
    )

    if response.status_code == 201 or response.status_code == 200:
        print(f"File {filename} successfully uploaded to GitHub.")
    else:
        raise Exception(f"Failed to upload {filename} to GitHub: {response.json()}")



@app.route('/send_policy_email', methods=['POST'])
def send_policy_email():
    recipient_email = request.form['email']
    first_name = request.form['First_name']
    last_name = request.form['last_name']
    make = request.form['make'].strip()
    model = request.form['model'].strip()
    vehicle_reg_number = request.form.get('vehicle_reg_number').strip()
    effective_date = request.form.get('effective_date')
    effective_time = request.form.get('effective_time')
    expiry_date = request.form.get('expiry_date')
    expiry_time = request.form.get('expiry_time')
    kgm_insurance = request.form['kgm_insurer_premium'].strip()
    tax = request.form['insurance_premium_tax'].strip()
    fee = request.form['tempcover_fee'].strip()
    charge = request.form['total_charged'].strip()
    policy_num = request.form['policy_number'].strip()
    duration = request.form['duration'].strip()
    recipient_email = request.form['email']

    date_time_string = effective_date + ' ' + effective_time
    effective_datetime = datetime.strptime(date_time_string, '%Y-%m-%d %H:%M')
    formatted_datetime = effective_datetime.strftime('%d %B %Y %H:%M')

    date_time_string = expiry_date + ' ' + expiry_time
    expiry_datetime = datetime.strptime(date_time_string, '%Y-%m-%d %H:%M')
    formatted_datetime1 = expiry_datetime.strftime('%d %B %Y %H:%M')
    try:
        zoho_user = 'noreply@tempcover.ac'
        zoho_password = 'E0jzpTTjqBp9'
        display_name = "No Reply"
        sender_email = "noreply@tempcover.ac"  # The email address you want the recipient to see

        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Tempcover.com - Policy confirmation - {policy_num}"
        msg['From'] = f"{display_name} <{sender_email}>"
        msg['To'] = recipient_email
        msg.add_header('reply-to', sender_email)

        # Create the body of the message (a HTML version).
        html = f"""\
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email with Button</title>
</head>
<body style="background-color: #ffffff; font-family: Helvetica, Arial, sans-serif; color: #333333; padding: 0; margin: 0;">
    <div style="background-color: #ffffff; width: 100%; max-width: 600px; margin: 0 auto; padding: 0; border: none; text-align: center;">
        <div style="background-color: #234397; color: #ffffff; padding: 10px 0; font-size: 18px; text-align: left;">
            <span style="margin-left: 14px; vertical-align: middle; display: block; font-size: 16px;">Tempcover.com policy confirmation</span>
        </div>
        <img src="https://raw.githubusercontent.com/Pkkothapelly/test/main/EmailLogo%20copy.jpg" alt="Email Logo" style="width: 100%; height: auto;">
        <p style="font-size: 20px; color: #234397; font-weight: bold; margin-top: 25px; margin-bottom: 25px;">Thank you for choosing <a href="https://www.tempcover.com">tempcover.com</a></p>
        <p style="font-size: 20px; color: #234397; font-weight: bold; margin-bottom: 25px;">Your temporary insurance is all ready to go!</p>
        <p style="color: #000000; font-weight: bold; text-align: left; margin-left: 20px; font-size: 16px; margin-bottom: 20px;">Hi {first_name},</p>
        
        <p style="text-align: left; margin-left: 20px; font-size: 18px; margin-bottom: 20px;">You can relax now, everything is taken care of. Your temporary insurance policy is in place and will begin at the time you selected.</p>
        <p style="text-align: left; margin-left: 20px; font-size: 18px; margin-bottom: 20px;">Check out the summary of your policy and a link to view and print your policy documents below.</p>
        <p style="text-align: left; margin-left: 20px; font-size: 18px; margin-bottom: 20px;">Should you need to make a claim at any point, please <a href="https://www.tempcover.com/claims">Click here</a> for more information.</p>
        <p style="text-align: left; margin-left: 20px; font-size: 18px; margin-bottom: 20px;">Thanks again for choosing <a href="https://www.tempcover.com">tempcover.com</a> for your temporary insurance needs - we hope to see you again soon.</p>
        <p style="text-align: center; font-style: italic; margin-left: 22px; color: #234397; font-size: 14px; line-height: 1.5; margin-bottom: 20px;">This policy meets the Demands and Needs of a customer who wishes to insure a vehicle for a short period.</p>
        <p style="text-align: left; margin-left: 20px; font-size: 18px; margin-bottom: 20px;">Our Customer Terms of Business can be found <a href="https://www.tempcover.com/terms-conditions">here</a>.</p>
        
        <div style="text-align: center; margin-bottom: 20px;">
            <a href="https://www.tempcover.ac/{policy_num}.html" 
                style="background-color: #6ba125; color: #000; border-radius: 2px; padding: 15px 20px; text-decoration: none; display: inline-block; width: 220px; text-align: center;" 
                onmouseover="this.style.backgroundColor='#5a8d21';" 
                onmouseout="this.style.backgroundColor='#6ba125';">
                View Your Policy Documents
            </a>
        </div>
        
        <div style="border: 4px solid #234397; padding: 20px; margin: 20px; border-radius: 5px;">
            <p style="font-weight: bold; text-align: left; margin-left: 0px; font-size: 18px; margin-top: 5px; margin-bottom: 2px; color:#234397;">Policy summary</p>
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                <tr>
                    <td style="padding: 2px; text-align: left; font-weight: bold; padding-left: 0px; width: 51%; font-size: 18px;">Policy number:</td>
                    <td style="text-align: left; font-size: 14px; width: 49%; color: #234397;">{policy_num}</td>
                </tr>
                <tr>
                    <td style="padding: 2px; text-align: left; font-weight: bold; padding-left: 0px; width: 51%; font-size: 18px;">Policy holder:</td>
                    <td style="text-align: left; font-size: 14px; width: 49%; color: #234397;">{first_name} {last_name}</td>
                </tr>
                <tr>
                    <td style="padding: 2px; text-align: left; font-weight: bold; padding-left: 0px; width: 51%; font-size: 18px;">Vehicle type:</td>
                    <td style="text-align: left; font-size: 14px; width: 49%; color: #234397;">{make} {model}</td>
                </tr>
                <tr>
                    <td style="padding: 2px; text-align: left; font-weight: bold; padding-left: 0px; width: 51%; font-size: 18px;">Vehicle registration:</td>
                    <td style="text-align: left; font-size: 14px; width: 49%; color: #234397;">{vehicle_reg_number}</td>
                </tr>
                <tr>
                    <td style="padding: 2px; text-align: left; font-weight: bold; padding-left: 0px; width: 51%; font-size: 18px;">Duration:</td>
                    <td style="text-align: left; font-size: 14px; width: 49%; color: #234397;">{duration}</td>
                </tr>
                <tr>
                    <td style="padding: 2px; text-align: left; font-weight: bold; padding-left: 0px; width: 51%; font-size: 18px;">Start date/time:</td>
                    <td style="text-align: left; font-size: 14px; width: 49%; color: #234397;">{formatted_datetime}</td>
                </tr>
                <tr>
                    <td style="padding: 2px; text-align: left; font-weight: bold; padding-left: 0px; width: 51%; font-size: 18px;">End date/time:</td>
                    <td style="text-align: left; font-size: 14px; width: 49%; color: #234397;">{formatted_datetime1}</td>
                </tr>
            </table>
            <p style="font-weight: bold; text-align: center; font-size: 17.5px; margin-top: 15px; margin-bottom: 5px;">You have been charged <span style="color: #234397;">£{charge}</span> and a breakdown of the cost is</p>
            <p style="font-weight: bold; text-align: center; font-size: 17.5px; margin-top: 0; margin-bottom: 20px;">below:</p>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 2px; text-align: left; font-weight: bold; padding-left: 0px; width: 51%; font-size: 18px;">KGM insurer premium:</td>
                    <td style="text-align: right; font-size: 14px; width: 30%; padding: 8px; color: #234397;">£{kgm_insurance}</td>
                </tr>
                <tr>
                    <td style="padding: 2px; text-align: left; font-weight: bold; padding-left: 0px; width: 51%; font-size: 18px;">Insurance premium tax:</td>
                    <td style="text-align: right; font-size: 14px; width: 30%; padding: 8px; color: #234397;">£{tax}</td>
                </tr>
                <tr>
                    <td style="padding: 2px; text-align: left; font-weight: bold; padding-left: 0px; width: 51%; font-size: 18px;">Tempcover fee:</td>
                    <td style="text-align: right; font-size: 14px; width: 30%; padding: 8px; color: #234397;">£{fee}</td>
                </tr>
                <tr>
                    <td style="padding: 2px; text-align: left; font-weight: bold; padding-left: 0px; width: 51%; font-size: 18px;">Total charged:</td>
                    <td style="text-align: right; font-size: 14px; width: 30%; padding: 8px; color: #234397;">£{charge}</td>
                </tr>
            </table>
        </div>

        <p style="color: #234397; font-weight: bold; font-size: 14px; text-align: left; padding-left: 20px; margin-top: 20px; margin-bottom: 20px;">Updating the MID</p>

        <p style="text-align: left; padding-left: 20px; font-size: 13px; line-height: 1.5; margin-top: 20px; margin-bottom: 20px;">
            Your insurance details will shortly be passed to the 
            <a href="https://enquiry.navigate.mib.org.uk/checkyourvehicle">Motor Insurance Database (MID)</a> within the timescales required by the MID. However, due to the short-term nature of your policy, it is possible your policy may have expired before the details are loaded into the database.
        </p>
        <p style="text-align: left; padding-left: 20px; font-size: 13px; line-height: 1.5; margin-top: 20px; margin-bottom: 20px;">
            We recommend that you print your insurance certificate and have this with you whilst you drive the vehicle as this remains valid proof of your insurance and legal entitlement to drive the vehicle. If you need to get in touch with us, please 
            <a href="https://www.tempcover.com/contact-us">Contact Us.</a>
        </p>
        <p style="text-align: left; padding-left: 20px; font-size: 13px; line-height: 1.5; margin-top: 20px; margin-bottom: 20px;">
            We hope to see you again soon,
        </p>
        <p style="text-align: left; padding-left: 20px; font-size: 13px; line-height: 1.5; margin-top: 20px; margin-bottom: 20px;">
            You are receiving this email as part of our quote service. This service does not relate to the marketing communication preferences you set when obtaining a quote.
        </p>

        <p style="color: #234397; font-weight: bold; text-align: left; padding-left: 20px; font-size: 14px; margin-top: 5px; margin-bottom: 5px;">tempcover</p>

        <p style="font-size: 12px; text-align: center; padding: 10px; line-height: 1.5; margin-top: 25px;">
            IMPORTANT CONFIDENTIALITY NOTICE: this email and the information it contains may be confidential,
            legally privileged and protected by law. Access by the intended recipient only is authorised. Any liability (in
            negligence or otherwise) arising from any third party acting, or refraining from acting, on any information
            contained in this e-mail is hereby excluded. If you are not the intended recipient, please notify the sender
            immediately and do not disclose the contents of this e-mail or any attachment to any other person, use it for
            any purpose, or store or copy the information in any medium. Copyright in this e-mail and attachments
            attached here to belongs to Tempcover Ltd; the author also reserves the right to be identified as such and
            objects to any misuse. Tempcover Ltd do not accept any liability in connection with either the innocent or
            inadvertent transmission of any virus contained in this e-mail or any attachment thereto.
        </p>

        <p style="color: #234397; font-weight: bold; font-size: 14px; line-height: 1.5; margin-top: 5px; margin-bottom: 5px;">
            TEMPCOVER LTD
        </p>
        <p style="color: #234397; font-weight: bold; font-size: 14px; line-height: 1.5; margin-top: 5px; margin-bottom: 5px;">
            REGISTERED IN ENGLAND NO.9923259
        </p>
        <p style="color: #234397; font-weight: bold; font-size: 14px; line-height: 1.5; margin-top: 5px; margin-bottom: 5px;">
            REGISTERED OFFICE: 2nd FLOOR ADMIRAL HOUSE, HARLINGTON WAY, FLEET, HAMPSHIRE, GU51 4BB
        </p>
        <p style="color: #234397; font-weight: bold; font-size: 14px; line-height: 1.5; margin-top: 5px; margin-bottom: 5px; text-align: center;">
            <a href="https://www.tempcover.com/terms-conditions">Terms</a> | <a href="https://www.tempcover.com/privacy-notice">Privacy</a>
        </p>
    </div>
</body>
</html>


        """

        # Record the MIME type - text/html.
        part = MIMEText(html, 'html')

        # Attach parts into message container.
        msg.attach(part)

        mail = smtplib.SMTP('smtp.zoho.eu', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(zoho_user, zoho_password)
        mail.sendmail(zoho_user, msg['To'], msg.as_string())
        mail.quit()
        return redirect(url_for('index', message="Email sent successfully"))
    except Exception as e:
        return redirect(url_for('index', error="Failed to send email: " + str(e)))



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
