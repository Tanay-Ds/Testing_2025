import requests
import json
import sys

def run_task():
    print("=========================================")
    print("    STARTING BAJAJ 2026 TASK FLOW        ")
    print("=========================================")
    generate_url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
    payload = {
        "name": "Tanay Dashore",
        "regNo": "0827CD231070",
        "email": "tanaydashore230879@acropolis.in"
    }
    headers = {"Content-Type": "application/json"}
    print(f"Sending POST to generate webhook: {generate_url}...")
    response = requests.post(generate_url, json=payload, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} during webhook generation.")
        print(response.text)
        sys.exit(1)
        
    res_data = response.json()
    webhook_url = res_data.get("webhook")
    access_token = res_data.get("accessToken")
    print(f"Successfully generated webhook!")
    print(f"Webhook URL: {webhook_url}")
    print(f"Access Token: {access_token[:15]}... [TRUNCATED]")

    final_query = """SELECT 
    e1.EMP_ID,
    e1.FIRST_NAME,
    e1.LAST_NAME,
    d.DEPARTMENT_NAME,
    (
        SELECT COUNT(*)
        FROM EMPLOYEE e2
        WHERE e2.DEPARTMENT = e1.DEPARTMENT
          AND e2.DOB > e1.DOB
    ) AS YOUNGER_EMPLOYEES_COUNT
FROM EMPLOYEE e1
JOIN DEPARTMENT d ON e1.DEPARTMENT = d.DEPARTMENT_ID
ORDER BY e1.EMP_ID DESC;"""

    submit_headers = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }
    submit_payload = {"finalQuery": final_query}

    print(f"Submitting final SQL query to webhook URL...")
    submit_response = requests.post(webhook_url, json=submit_payload, headers=submit_headers)
    
    if submit_response.status_code != 200:
        print(f"Error: Received status code {submit_response.status_code} during submission.")
        print(submit_response.text)
        sys.exit(1)
        
    print("=========================================")
    print("    RESPONSE FROM WEBHOOK SUBMISSION:     ")
    print("=========================================")
    print(json.dumps(submit_response.json(), indent=2))
    print("=========================================")

if __name__ == "__main__":
    run_task()
