def admin_email_template(order_data):
  return f"""
  <h1>New Order Received</h1>
  <p>You have received a new order from <b>{order_data['fullName']}</b>.</p>
  <p><b>Email:</b> {order_data['email']}</p>
  <p><b>Phone:</b> {order_data.get('tel', 'N/A')}</p>
  <p><b>Service Type:</b> {order_data['serviceType']}</p>
  <p><b>Work Object Details:</b> {order_data['workObjectDetails']}</p>
  <p><b>Remarks:</b> {order_data.get('remark', 'N/A')}</p>
  """

def user_email_template(order_data):
  return f"""
  <h1>Order Confirmation</h1>
  <p>Dear {order_data['fullName']},</p>
  <p>Thank you for your order! We have received your request and will start processing it shortly.</p>
  <p>Here are the details of your order:</p>
  <ul>
      <li><b>Service Type:</b> {order_data['serviceType']}</li>
      <li><b>Work Object Details:</b> {order_data['workObjectDetails']}</li>
      <li><b>Remarks:</b> {order_data.get('remark', 'N/A')}</li>
  </ul>
  <p>If you have any questions or need further assistance, please feel free to contact us at any time.</p>
  <p>Best regards,</p>
  <p>Power Wash Brothers Team</p>
  """