"""
WillPay Backend API Test Script
Tests backend endpoints without UI
"""
import requests
import json
import time

# WillPay Backend Configuration  
BACKEND_URL = "http://localhost:8000"  # Localhost
# BACKEND_URL = "http://192.168.1.103:8000"  # Network için

def test_health():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return False

def test_create_receipt():
    """Test creating a new receipt"""
    print("\n📝 Testing receipt creation...")
    
    from datetime import datetime
    
    # WillPay backend format
    receipt_data = {
        "user_id": 1,  # Integer user ID
        "store_name": "Granny's Waffle",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total_amount": 100.0,
        "category": "food",
        "is_favorite": False,
        "notes": "API Test Receipt - POS System",
        "image_url": None,
        "items": [
            {"name": "Çikolatalı Waffle", "price": 35.0, "quantity": 1, "category": "waffle"},
            {"name": "Karışık Smoothie", "price": 25.0, "quantity": 2, "category": "smoothie"},
            {"name": "Türk Kahvesi", "price": 15.0, "quantity": 1, "category": "kahve"}
        ]
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/receipts",
            json=receipt_data,
            timeout=5
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            print("✅ Receipt created successfully")
            
            # Handle both object and array response formats
            if isinstance(result, dict):
                # Backend returns object (current format)
                print(f"   Receipt ID: {result.get('id', 'N/A')}")
                print(f"   Store: {result.get('storeName', 'N/A')}")
                print(f"   Total: {result.get('totalAmount', 'N/A')}₺")
                print(f"   Items: {len(result.get('items', []))} adet")
                return result
            elif isinstance(result, list):
                # Fallback: Backend returns array
                receipt_dict = {
                    'id': result[0],
                    'userId': result[1],
                    'storeName': result[2],
                    'date': result[3],
                    'totalAmount': float(result[4]),
                    'category': result[5],
                    'isFavorite': result[6],
                    'notes': result[7],
                    'imageUrl': result[8],
                    'createdAt': result[9]
                }
                print(f"   Receipt ID: {receipt_dict['id']}")
                print(f"   Store: {receipt_dict['storeName']}")
                print(f"   Total: {receipt_dict['totalAmount']}₺")
                return receipt_dict
            else:
                print(f"   ⚠️ Unexpected format: {type(result)}")
                return result
        else:
            print(f"❌ Receipt creation failed: {response.status_code}")
            print(f"   Error: {response.text[:500]}")
            return None
            
    except Exception as e:
        print(f"❌ Receipt creation error: {str(e)}")
        return None

def test_get_receipt(receipt_id):
    """Test getting receipt by ID"""
    print(f"\n🔍 Testing receipt retrieval (ID: {receipt_id})...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/receipts/{receipt_id}", timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Receipt retrieved successfully")
            print(f"   Store: {result.get('storeName', 'N/A')}")
            print(f"   Total: {result.get('totalAmount', 'N/A')}₺")
            print(f"   Items: {len(result.get('items', []))}")
            return result
        else:
            print(f"❌ Receipt retrieval failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Receipt retrieval error: {str(e)}")
        return None

def test_get_receipt_by_id(receipt_id):
    """Test getting receipt by ID (QR scan simulation)"""
    print(f"\n📱 Testing QR scan (Receipt ID: {receipt_id})...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/receipts/{receipt_id}", timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ QR scan successful")
            print(f"   Receipt ID: {result.get('id', 'N/A')}")
            print(f"   Store: {result.get('storeName', 'N/A')}")
            print(f"   Total: {result.get('totalAmount', 'N/A')}₺")
            
            # Print items
            items = result.get('items', [])
            if items:
                print(f"   Items ({len(items)}):")
                for item in items:
                    print(f"      • {item.get('name')} x{item.get('quantity')} - {item.get('price')}₺")
            
            return result
        else:
            print(f"❌ QR scan failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ QR scan error: {str(e)}")
        return None

def test_notify_receipt(receipt_id):
    """Test sending notification for receipt"""
    print(f"\n🔔 Testing notification (Receipt ID: {receipt_id})...")
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/notify/receipt/{receipt_id}",
            json={"device_token": "test_device_token"},
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Notification sent successfully")
            print(f"   Message: {result['message']}")
            return result
        else:
            print(f"❌ Notification failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Notification error: {str(e)}")
        return None

def run_full_test():
    """Run complete API test suite"""
    print("=" * 60)
    print("🧪 WillPay Backend API Test Suite")
    print("=" * 60)
    
    # Test 1: Health check
    if not test_health():
        print("\n❌ Backend is not running. Please start it with:")
        print("   python backend.py")
        return
    
    # Test 2: Create receipt
    receipt = test_create_receipt()
    if not receipt:
        print("\n❌ Cannot proceed without receipt")
        return
    
    receipt_id = receipt.get('id')
    if not receipt_id:
        print("\n❌ No receipt ID returned")
        return
    
    # Wait a bit
    time.sleep(0.5)
    
    # Test 3: Get receipt by ID (QR simulation)
    test_get_receipt_by_id(receipt_id)
    
    # Test 4: Send notification
    test_notify_receipt(receipt_id)
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    print(f"\n🎯 Test Receipt Details:")
    print(f"   • Receipt ID: {receipt_id}")
    print(f"   • Store: {receipt.get('storeName', 'N/A')}")
    print(f"   • Total: {receipt.get('totalAmount', 'N/A')}₺")
    print(f"   • QR URL (Frontend): http://192.168.1.103:3000/receipt/{receipt_id}")
    print(f"   • API URL (Backend): http://192.168.1.103:8000/receipts/{receipt_id}")
    print(f"\n💡 You can test the QR URL by scanning it with WillPay mobile app")

def create_sample_receipts():
    """Create multiple sample receipts for testing"""
    print("=" * 60)
    print("📦 Creating Sample Receipts")
    print("=" * 60)
    
    from datetime import datetime
    
    samples = [
        {
            "name": "Small Order",
            "items": [
                {"name": "Türk Kahvesi", "price": 15.0, "quantity": 1, "category": "kahve"}
            ],
            "total": 15.0
        },
        {
            "name": "Medium Order",
            "items": [
                {"name": "Çikolatalı Waffle", "price": 35.0, "quantity": 1, "category": "waffle"},
                {"name": "Cappuccino", "price": 20.0, "quantity": 1, "category": "kahve"}
            ],
            "total": 55.0
        },
        {
            "name": "Large Order",
            "items": [
                {"name": "Çikolatalı Waffle", "price": 35.0, "quantity": 2, "category": "waffle"},
                {"name": "Karışık Smoothie", "price": 25.0, "quantity": 3, "category": "smoothie"},
                {"name": "Latte", "price": 22.0, "quantity": 2, "category": "kahve"}
            ],
            "total": 189.0
        }
    ]
    
    for sample in samples:
        print(f"\n📝 Creating: {sample['name']}...")
        receipt_data = {
            "user_id": 1,  # Integer user ID
            "store_name": "Granny's Waffle",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_amount": sample['total'],
            "category": "food",
            "is_favorite": False,
            "notes": f"Sample: {sample['name']}",
            "image_url": None,
            "items": sample['items']
        }
        
        try:
            response = requests.post(
                f"{BACKEND_URL}/receipts",
                json=receipt_data,
                timeout=5
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                
                # Handle response format
                if isinstance(result, dict):
                    receipt_id = result.get('id', 'N/A')
                    total = result.get('totalAmount', 0)
                    print(f"   ✅ Created - ID: {receipt_id}, Total: {total}₺")
                elif isinstance(result, list):
                    receipt_id = result[0]
                    total = float(result[4])
                    print(f"   ✅ Created - ID: {receipt_id}, Total: {total}₺")
                else:
                    print(f"   ⚠️ Unknown format")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                print(f"   Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print("\n✅ Sample receipts created!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--samples":
        create_sample_receipts()
    else:
        run_full_test()

