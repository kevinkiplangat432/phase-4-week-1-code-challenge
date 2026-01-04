import requests
import json

BASE_URL = "http://localhost:5555"

def test_email_endpoints():
    print("Testing Email Functionality")
    print("=" * 50)
    
    #  Test send-test-email endpoint
    print("\n1. Testing POST /send-test-email")
    print("-" * 30)
    
    test_data = {
        "to": "test@example.com"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/send-test-email",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Test email endpoint is working")
            print(f"Response: {response.json()}")
        elif response.status_code == 500:
            print("✗ Email configuration issue detected")
            print(f"Error: {response.json().get('details', 'Unknown error')}")
            print("\nTip: Configure email in .env file or use local SMTP server")
        else:
            print(f"✗ Unexpected status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"✗ Connection error: {e}")
    
    #  Test notify-power-update endpoint
    print("\n2. Testing POST /notify-power-update")
    print("-" * 30)
    
    power_data = {
        "power_id": 1,
        "email": "admin@example.com"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/notify-power-update",
            json=power_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Power notification endpoint is working")
        elif response.status_code == 404:
            print("✓ Endpoint working, but power not found (expected if no data)")
        else:
            print(f"Response: {response.json()}")
            
    except Exception as e:
        print(f"✗ Connection error: {e}")
    
    # Test welcome-hero endpoint
    print("\n3. Testing POST /welcome-hero")
    print("-" * 30)
    
    hero_data = {
        "hero_name": "Test Hero",
        "super_name": "Super Tester",
        "email": "hero@example.com"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/welcome-hero",
            json=hero_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Welcome hero endpoint is working")
        else:
            print(f"Response: {response.json()}")
            
    except Exception as e:
        print(f"✗ Connection error: {e}")
    
    print("\n" + "=" * 50)
    print("Email Testing Complete")
    print("\nNote: If emails aren't sending, check your .env configuration")
    print("For development, you can use a local SMTP server:")

if __name__ == "__main__":
    test_email_endpoints()