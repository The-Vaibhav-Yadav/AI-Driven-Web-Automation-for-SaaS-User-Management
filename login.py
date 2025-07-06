import asyncio
from browser_use.llm import ChatGoogle
from browser_use import Agent, BrowserSession
from dotenv import load_dotenv
import os

# Read GOOGLE_API_KEY into env
load_dotenv()
email = os.getenv("LOGIN_EMAIL")
passw = os.getenv("PASSWORD")

initial_actions = [
	{'go_to_url': {'url': 'https://www.dropbox.com/login', 'new_tab': True}}
]
sensitive_data={
                'https://dropbox.com': {
            'email': {email},
            'password': {passw}}}

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
            # Bright Data configuration with error handling
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

async def run_automation():
    """Run the automation and return the result"""
    use_bright_data = False 
    browser_session = await create_browser_session(use_bright_data=use_bright_data)
    
    try:
        agent = Agent(
            task="""
            sign in with your email email and password password
            """,
            llm=llm,
            initial_actions=initial_actions,
            sensitive_data=sensitive_data,
            browser_session=browser_session,
            )
        result = await agent.run()
        return result
    except Exception as e:
        print(f"Error running agent: {e}")
        return None
    finally:
        try:
            await browser_session.close()
        except Exception as e:
            print(f"Error closing browser session: {e}")

async def main():
    result = await run_automation()
    print(result)
    return result

if __name__ == '__main__':
    asyncio.run(main())