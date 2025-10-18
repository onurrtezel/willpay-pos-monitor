"""
UI Automation Test Script
Tests POS UI using pywinauto for Windows UI Automation
"""
import time
import sys
from pywinauto import Application, Desktop
from pywinauto.findwindows import ElementNotFoundError


class POSAutomationTester:
    """Automated testing for POS UI using Windows UI Automation"""
    
    def __init__(self):
        self.app = None
        self.main_window = None
        
    def connect_to_pos(self, timeout=10):
        """Connect to running POS application"""
        print("🔍 Searching for POS application...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Try to connect to the main window
                desktop = Desktop(backend="uia")
                windows = desktop.windows()
                
                for window in windows:
                    if "Granny's Waffle" in window.window_text():
                        self.main_window = window
                        print(f"✅ Connected to: {window.window_text()}")
                        return True
                        
            except Exception as e:
                pass
            
            time.sleep(0.5)
        
        print("❌ Could not find POS application")
        return False
    
    def read_cart_items(self):
        """Read all items from cart using UI Automation"""
        print("\n📋 Reading cart items...")
        cart_items = []
        
        try:
            # Find all elements with receipt_item pattern
            i = 0
            while True:
                try:
                    # Try to find name element
                    name_id = f"receipt_item_{i}_name"
                    price_id = f"receipt_item_{i}_price"
                    quantity_id = f"receipt_item_{i}_quantity"
                    
                    name_elem = self.main_window.child_window(auto_id=name_id, control_type="Text")
                    price_elem = self.main_window.child_window(auto_id=price_id, control_type="Text")
                    quantity_elem = self.main_window.child_window(auto_id=quantity_id, control_type="Text")
                    
                    if name_elem.exists():
                        item = {
                            'index': i,
                            'name': name_elem.window_text(),
                            'price': price_elem.window_text(),
                            'quantity': quantity_elem.window_text()
                        }
                        cart_items.append(item)
                        print(f"  • {item['name']} - {item['price']} {item['quantity']}")
                        i += 1
                    else:
                        break
                        
                except Exception:
                    break
            
            return cart_items
            
        except Exception as e:
            print(f"❌ Error reading cart: {str(e)}")
            return []
    
    def read_total_amount(self):
        """Read total amount from UI"""
        print("\n💰 Reading total amount...")
        
        try:
            total_elem = self.main_window.child_window(auto_id="TotalLabel", control_type="Text")
            
            if total_elem.exists():
                total_text = total_elem.window_text()
                print(f"  Total: {total_text}")
                return total_text
            else:
                print("❌ Total label not found")
                return None
                
        except Exception as e:
            print(f"❌ Error reading total: {str(e)}")
            return None
    
    def click_pay_button(self):
        """Click the payment button"""
        print("\n🖱️ Clicking payment button...")
        
        try:
            pay_button = self.main_window.child_window(auto_id="PayButton", control_type="Button")
            
            if pay_button.exists() and pay_button.is_enabled():
                pay_button.click()
                print("✅ Payment button clicked")
                return True
            else:
                print("❌ Payment button not found or disabled")
                return False
                
        except Exception as e:
            print(f"❌ Error clicking button: {str(e)}")
            return False
    
    def verify_ui_elements(self):
        """Verify all UI Automation elements are accessible"""
        print("\n🔍 Verifying UI Automation elements...")
        
        results = {
            'total_label': False,
            'pay_button': False,
            'cart_items': False
        }
        
        # Check TotalLabel
        try:
            total_elem = self.main_window.child_window(auto_id="TotalLabel")
            results['total_label'] = total_elem.exists()
            print(f"  • TotalLabel: {'✅' if results['total_label'] else '❌'}")
        except:
            print("  • TotalLabel: ❌")
        
        # Check PayButton
        try:
            pay_elem = self.main_window.child_window(auto_id="PayButton")
            results['pay_button'] = pay_elem.exists()
            print(f"  • PayButton: {'✅' if results['pay_button'] else '❌'}")
        except:
            print("  • PayButton: ❌")
        
        # Check cart items
        try:
            item_elem = self.main_window.child_window(auto_id="receipt_item_0_name")
            results['cart_items'] = item_elem.exists()
            print(f"  • Cart Items: {'✅' if results['cart_items'] else '❌'}")
        except:
            print("  • Cart Items: ❌ (No items in cart)")
        
        return results
    
    def print_all_controls(self):
        """Debug: Print all controls in the window"""
        print("\n🔍 Listing all controls...")
        
        try:
            self.main_window.print_control_identifiers()
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    def run_full_test(self):
        """Run complete automation test"""
        print("=" * 60)
        print("🧪 WillPay POS UI Automation Test")
        print("=" * 60)
        
        # Connect to application
        if not self.connect_to_pos():
            print("\n⚠️ Please start the POS application first:")
            print("   python pos_ui.py")
            return False
        
        # Wait for UI to stabilize
        time.sleep(1)
        
        # Verify UI elements
        results = self.verify_ui_elements()
        
        # Read cart items
        cart_items = self.read_cart_items()
        
        # Read total
        total = self.read_total_amount()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 Test Summary")
        print("=" * 60)
        print(f"✅ UI Elements Accessible: {sum(results.values())}/{len(results)}")
        print(f"✅ Cart Items Found: {len(cart_items)}")
        print(f"✅ Total Amount: {total if total else 'N/A'}")
        
        if all(results.values()) or (results['total_label'] and results['pay_button']):
            print("\n✅ UI Automation test PASSED")
            return True
        else:
            print("\n❌ UI Automation test FAILED")
            return False


def simulate_purchase_flow():
    """Simulate a complete purchase flow with automation"""
    print("\n" + "=" * 60)
    print("🤖 Simulating Purchase Flow")
    print("=" * 60)
    
    tester = POSAutomationTester()
    
    # Step 1: Connect
    if not tester.connect_to_pos():
        print("❌ Cannot connect to POS")
        return
    
    print("\n📝 Instructions:")
    print("1. Manually add some products to cart")
    print("2. This script will read the cart and click payment button")
    print("\nPress Enter when ready...")
    input()
    
    # Step 2: Read cart
    time.sleep(0.5)
    cart_items = tester.read_cart_items()
    
    if not cart_items:
        print("⚠️ No items in cart. Please add items first.")
        return
    
    # Step 3: Read total
    total = tester.read_total_amount()
    
    # Step 4: Click payment
    print("\n⏳ Clicking payment button in 3 seconds...")
    time.sleep(3)
    
    if tester.click_pay_button():
        print("\n✅ Payment initiated successfully!")
        print("🎉 QR popup should appear now")
    else:
        print("\n❌ Failed to click payment button")


def main():
    """Main test entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--simulate":
        simulate_purchase_flow()
    else:
        tester = POSAutomationTester()
        tester.run_full_test()


if __name__ == "__main__":
    main()

