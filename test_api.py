import requests
import json

BASE_URL = "http://localhost:5555"

def test_endpoint(endpoint, method="GET", data=None, expected_status=200):
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "PATCH":
            response = requests.patch(url, json=data, headers={"Content-Type": "application/json"})
        elif method == "POST":
            response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        
        print(f"\nTesting {method} {endpoint}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code != expected_status:
            print(f"FAIL: Expected {expected_status}, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        print("PASS: Status code matches")
        
        # Try to parse JSON
        try:
            result = response.json()
            print(f"Response JSON: {json.dumps(result, indent=2)}")
            return True
        except:
            print("Response is not valid JSON")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"ERROR: Cannot connect to {url}")
        print("Make sure the Flask app is running!")
        return False

def run_all_tests():
    print("=" * 60)
    print("Testing Superheroes API")
    print("=" * 60)
    
    # 1. GET /heroes
    test_endpoint("/heroes")
    
    # 2. GET /heroes/:id (existing)
    test_endpoint("/heroes/1")
    
    # 3. GET /heroes/:id (non-existing)
    test_endpoint("/heroes/999", expected_status=404)
    
    # 4. GET /powers
    test_endpoint("/powers")
    
    # 5. GET /powers/:id (existing)
    test_endpoint("/powers/1")
    
    # 6. GET /powers/:id (non-existing)
    test_endpoint("/powers/999", expected_status=404)
    
    # 7. PATCH /powers/:id (valid)
    test_endpoint("/powers/1", "PATCH", 
                 {"description": "Updated description with more than twenty characters"},
                 expected_status=200)
    
    # 8. PATCH /powers/:id (invalid - too short)
    test_endpoint("/powers/1", "PATCH",
                 {"description": "Too short"},
                 expected_status=400)
    
    # 9. PATCH /powers/:id (non-existing)
    test_endpoint("/powers/999", "PATCH",
                 {"description": "Valid description with enough characters"},
                 expected_status=404)
    
    # 10. POST /hero_powers (valid)
    test_endpoint("/hero_powers", "POST",
                 {"strength": "Average", "power_id": 1, "hero_id": 3},
                 expected_status=201)
    
    # 11. POST /hero_powers (invalid strength)
    test_endpoint("/hero_powers", "POST",
                 {"strength": "Invalid", "power_id": 1, "hero_id": 3},
                 expected_status=400)
    
    # 12. POST /hero_powers (non-existing hero)
    test_endpoint("/hero_powers", "POST",
                 {"strength": "Average", "power_id": 1, "hero_id": 999},
                 expected_status=404)

if __name__ == "__main__":
    # First, make sure app is running
    print("Make sure Flask app is running on port 5555!")
    print("Run: python run.py")
    input("Press Enter when ready...")
    
    run_all_tests()