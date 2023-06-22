import smtplib
import random
import ssl


def send_otp(otp_,email):
  otp=otp_
  receiver_email = email
  smtp_server = "smtp.gmail.com"
  port = 587  # For starttls
  sender_email = "kunduruabhinayreddy43@gmail.com"
  password = "qmlxwpdbvsdowkaq"

  message = f"Subject: OTP for your account\n\nYour OTP is {otp}."

  context = ssl.create_default_context()

  with smtplib.SMTP(smtp_server, port) as server:
      server.starttls(context=context)
      server.login(sender_email, password)
      server.sendmail(sender_email, receiver_email, message)

  print("OTP sent successfully!")