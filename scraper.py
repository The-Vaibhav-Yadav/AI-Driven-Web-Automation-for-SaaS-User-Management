import os
import json
import asyncio
from typing import List
from pydantic import BaseModel
from browser_use.llm import ChatGoogle
from browser_use import Agent, BrowserSession, Controller
from dotenv import load_dotenv

load_dotenv()
email = os.getenv("LOGIN_EMAIL")
passw = os.getenv("PASSWORD")

class Post(BaseModel):
    name: str
    email: str
    department: str
    lastlogin: str

class Posts(BaseModel):
    posts: List[Post] 

controller = Controller(output_model=Posts)

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

initial_actions = [
    {'go_to_url': {'url': 'https://www.dropbox.com/login', 'new_tab': True}}
]

sensitive_data = {
    'https://dropbox.com': {
        'emaildb': {email},
        'passworddb': {passw}
    }
}

async def main():
    """Run the automation and return the result"""
    use_bright_data = False
    browser_session = await create_browser_session(use_bright_data=use_bright_data)
    
    agent = Agent(
        task=f"""
        1. Open Dir2
        2. Open Employee Details.web
        3. Get name, email, department and lastlogin of people working on Project Stronghold as JSON
        """,
        llm=llm,
        initial_actions=initial_actions,
        # sensitive_data=sensitive_data,
        browser_session=browser_session,
        controller=controller
    )
    history = await agent.run()
    result = history.final_result()
    if result:
        with open('extracted_data.json', 'w') as f:
            json.dump(result, f)
        return result


if __name__ == '__main__':
    asyncio.run(main())