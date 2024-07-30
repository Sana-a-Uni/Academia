import frappe
from frappe.auth import LoginManager

def generate_key(user):
    """
    Generate API key and secret for a given user if they don't already exist.

    Args:
        user: The user ID for which to generate the keys.

    Returns:
        dict: A dictionary containing the API key and secret.
    """
    user_details = frappe.get_doc("User", user)
    api_secret = api_key = ''

    if not user_details.api_key and not user_details.api_secret:
        api_secret = frappe.generate_hash(length=15)
        api_key = frappe.generate_hash(length=15)
        user_details.api_key = api_key
        user_details.api_secret = api_secret
        user_details.save(ignore_permissions=True)
    else:
        api_secret = user_details.get_password('api_secret')
        api_key = user_details.get('api_key')

    return {"api_secret": api_secret, "api_key": api_key}

def get_user_details(user):
    """
    Fetch user details for a given user.

    Args:
        user: The user ID for which to fetch the details.

    Returns:
        list: A list of user details dictionaries.
    """
    return frappe.get_all("User", filters={"name": user}, fields=["first_name", "last_name"])

def get_user_role(user):
    """
    Fetch roles for a given user.

    Args:
        user: The user ID for which to fetch the roles.

    Returns:
        list: A list of roles assigned to the user.
    """
    return frappe.get_roles(user)

@frappe.whitelist(allow_guest=True)
def login(username="at@gmail.com", password="atrab7720"):
    """
    Authenticate and log in a user.

    Args:
        username: The username of the user.
        password: The password of the user.

    Returns:
        bool: True if login is successful, False otherwise.
    """
    login_manager = LoginManager()
    login_manager.authenticate(username, password)
    login_manager.post_login()

    if frappe.response['message'] == 'Logged In':
        user = login_manager.user
        frappe.response['key_details'] = generate_key(user)
        frappe.response['user_details'] = get_user_details(user)
        frappe.response['user_role'] = get_user_role(user)

        # Clear session cookies and set new ones
        frappe.local.response.cookies = {
            'session_id': frappe.session.sid,
            'user_id': frappe.session.user
        }

        # Ensure headers are initialized before updating them
        if frappe.local.response.headers is None:
            frappe.local.response.headers = {}

        # Set headers to prevent caching
        frappe.local.response.headers.update({
            'Cache-Control': 'no-store, max-age=0',
            'Pragma': 'no-cache',
            'Expires': 'Thu, 01 Jan 1970 00:00:00 GMT'
        })
        return True
    else:
        return False
    

@frappe.whitelist(allow_guest=True)
def logout():
    """
    Log out the current user by clearing the session and cookies.

    Returns:
        bool: True if logout is successful, False otherwise.
    """
    try:
        frappe.local.login_manager = LoginManager()
        frappe.local.login_manager.logout()
        frappe.db.commit()

        # Clear session cookies
        frappe.local.response.cookies = {
            'session_id': '',
            'user_id': ''
        }

        # Ensure headers are initialized before updating them
        if frappe.local.response.headers is None:
            frappe.local.response.headers = {}

        # Set headers to prevent caching
        frappe.local.response.headers.update({
            'Cache-Control': 'no-store, max-age=0',
            'Pragma': 'no-cache',
            'Expires': 'Thu, 01 Jan 1970 00:00:00 GMT'
        })

        return True
    except Exception as e:
        frappe.log_error(message=str(e), title="Logout Failed")
        return False
