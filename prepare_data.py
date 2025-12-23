import csv

# Define the file name
CSV_FILENAME = "insurance_test_cases.csv"

# Sample Insurance Test Case Data
# Columns: ID, Title, Module, Pre-conditions, Steps, Expected Result
test_cases = [
    {
        "ID": "TC_POL_001",
        "Title": "Verify successful creation of a Life Insurance Policy",
        "Module": "Policy Management",
        "Pre-conditions": "User is logged in as an Underwriter; Customer profile exists.",
        "Steps": "1. Navigate to 'New Policy' menu.\n2. Select 'Life Insurance' from dropdown.\n3. Enter Coverage Amount: $500,000.\n4. Link to Customer ID 'CUST-102'.\n5. Click 'Calculate Premium'.\n6. Click 'Issue Policy'.",
        "Expected Result": "Policy is generated with status 'Active'; Policy ID is displayed; Premium matches the actuarial table."
    },
    {
        "ID": "TC_CLM_005",
        "Title": "Validate Auto-Claim rejection for expired policy",
        "Module": "Claims",
        "Pre-conditions": "Policy 'POL-999' is in 'Expired' status.",
        "Steps": "1. Log in as a Policy Holder.\n2. Go to 'File a Claim'.\n3. Select Policy 'POL-999'.\n4. Enter incident date (after expiration).\n5. Submit claim.",
        "Expected Result": "System displays error: 'Claim cannot be filed against an expired policy.'; Claim status remains 'Draft'."
    },
    {
        "ID": "TC_PAY_012",
        "Title": "Verify Payment Gateway integration for Credit Card",
        "Module": "Payments",
        "Pre-conditions": "Unpaid invoice exists for Policy 'POL-123'.",
        "Steps": "1. Go to Billing Dashboard.\n2. Select 'Pay Now' for invoice #INV-55.\n3. Choose 'Credit Card' payment method.\n4. Enter valid card details.\n5. Click 'Submit Payment'.",
        "Expected Result": "Transaction is authorized; Invoice status updates to 'Paid'; Confirmation email sent to user."
    },
    {
        "ID": "TC_UI_MOD_001",
        "Title": "Check responsiveness of Claim Dashboard on mobile",
        "Module": "UI/UX",
        "Pre-conditions": "User is accessing application via mobile browser.",
        "Steps": "1. Open 'Claim History' page.\n2. Rotate device from Portrait to Landscape.\n3. Scroll through the table of claims.",
        "Expected Result": "Layout adjusts without horizontal scrolling; All buttons remain clickable and correctly aligned."
    }
]

def generate_csv():
    # Write the data to CSV
    keys = test_cases[0].keys()
    
    with open(CSV_FILENAME, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(test_cases)
        
    print(f"✅ Successfully created '{CSV_FILENAME}' with {len(test_cases)} sample test cases.")

if __name__ == "__main__":
    generate_csv()