import os
import json
import asyncio
from typing import List
from pydantic import BaseModel
from browser_use.llm import ChatGoogle
from browser_use import Agent, BrowserSession, Controller
from dotenv import load_dotenv

load_dotenv()

name = "Vaibhav Yadav"
email = "yadavvaibhav0104@gmail.com"
department = "Engineering"
Website = "https://practice.expandtesting.com/register"

async def create_browser_session(use_bright_data=False):
    """Create a browser session with optional Bright Data proxy support"""
    if use_bright_data:
        # Bright Data configuration - check if URL is available
        bright_data_url = os.getenv("BRIGHTDATA_WSS_URL")
        if not bright_data_url:
            print("Warning: BRIGHTDATA_WSS_URL not found in environment variables")
            print("Falling back to local browser...")
            use_bright_data = False
    
    if use_bright_data:
        try:
            browser_session = BrowserSession(
                wss_url=bright_data_url,
                # Additional options for stability
                timeout=30000,
            )
            print("Using Bright Data proxy...")
        except Exception as e:
            print(f"Failed to connect to Bright Data: {e}")
            print("Falling back to local browser...")
            use_bright_data = False
    
    if not use_bright_data:
        # Local browser configuration
        browser_session = BrowserSession(
            executable_path='/opt/google/chrome/google-chrome',
            headless=False,
        )
        print("Using local browser...")
    
    return browser_session

llm = ChatGoogle(model='gemini-2.0-flash-exp')

# initial_actions = [
#     {'go_to_url': {'url': 'https://www.dropbox.com/login', 'new_tab': True}}
# ]

# sensitive_data = {
#     'https://dropbox.com': {
#         'emaildb': {email},
#         'passworddb': {passw}
#     }
# }

async def main():
    """Run the automation and return the result"""
    use_bright_data = False
    browser_session = await create_browser_session(use_bright_data=use_bright_data)
    
    agent = Agent(
        task=f"""
1. Open dropbox
        2. Open Dir2
        3. Open Employee Details.web
        4. Add new Employee information at the bottom of the table below the last name,
            a. Employee information, name {name}, email {email}, department {department} and other details as None
        5. Go to {Website} 
        5. a. Make a account using {name}, if not available make some changes,
           b. Make password 12 characters long using A-Za-z0-9 and special characters,
        6. a. Open https://mail.google.com/
          
    b. Click “Compose” to create a new email.
    c. Draft an email to {email} with the following:
        Subject: “Welcome to the Team!”
        Body:
        text

    Dear {name},

    Welcome to the team! Your account has been created with the following details:
    - Website: {Website}
    - Username: [Generated Username]
    - Temporary Password: [Generated Password]

    Please log in and change your password immediately for security purposes. If you encounter any issues, contact [Support Contact].

    Best regards,
    [Your Company Name]

    c.Send the email.
    d.Verify the email was sent successfully (check the “Sent” folder).
        """,
        llm=llm,
        # initial_actions=initial_actions,
        # sensitive_data=sensitive_data,
        browser_session=browser_session,
        # controller=controller
    )
    history = await agent.run()
    result = history.final_result()
    if result:
        with open('extracted_data.json', 'w') as f:
            json.dump(result, f)
        return result


if __name__ == '__main__':
    asyncio.run(main())