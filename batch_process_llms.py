import pandas as pd
import requests
import json
import time
from tqdm import tqdm

# Path to your synthetic notes file
SYNTHETIC_NOTES_PATH = "/gpfs/data/pcc_lab/kep9496-dir/practice_files/synthetic_notes.csv"  # Adjust if needed
OUTPUT_JSON_PATH = "/gpfs/data/pcc_lab/kep9496-dir/practice_files/llm_results.json"

# API endpoints and configuration
LLAMA_URL = "http://10.189.26.12:30080/model/llama3-3-70b-chat/v1/chat/completions"
DEEPSEEK_URL = "http://10.189.26.12:30080/model/llama3-3-70B-DSR1/v1/chat/completions"

HEADERS = {
    "apiKey": "kep9496",  # your KID
    "accept": "application/json",
    "Content-Type": "application/json"
}

# Function to query Llama model
def query_llama(note_text):
    messages = [
        {"role": "user", "content": f"Does this clinical impression indicate cancer progression. Categorize as progression, regression, or stable: {note_text}"}
    ]
    
    data = {
        "model": "llama3-3-70b-chat", 
        "messages": messages, 
        "max_tokens": 200,
        "temperature": 0.3,
        "top_p": 1,
        "n": 1,
        "stream": False,
        "stop": "string",
        "frequency_penalty": 0.0
    }
    
    max_retries = 3
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            response = requests.post(LLAMA_URL, headers=HEADERS, json=data, timeout=30)
            if response.status_code == 200:
                assistant_response = response.json()["choices"][0]["message"]["content"]
                return assistant_response
            else:
                print(f"Llama API error (attempt {attempt+1}): {response.status_code}")
                time.sleep(retry_delay)
        except Exception as e:
            print(f"Exception during Llama API call (attempt {attempt+1}): {e}")
            time.sleep(retry_delay)
    
    return "ERROR: Failed to get response from Llama model"

# Function to query DeepSeek model
def query_deepseek(note_text):
    messages = [
        {"role": "user", "content": f"Does this clinical impression indicate cancer progression. Categorize as progression, regression, or stable: {note_text}"}
    ]
    
    data = {
        "model": "llama3-3-70B-DSR1", 
        "messages": messages, 
        "max_tokens": 1000,
        "temperature": 0.4,
        "top_p": 1,
        "n": 1,
        "stream": False,
        "stop": "string",
        "frequency_penalty": 0.0
    }
    
    max_retries = 3
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            response = requests.post(DEEPSEEK_URL, headers=HEADERS, json=data, timeout=30)
            if response.status_code == 200:
                assistant_response = response.json()["choices"][0]["message"]["content"]
                cleaned_response = assistant_response.split("</think>\n\n")[-1] if "</think>\n\n" in assistant_response else assistant_response
                return cleaned_response
            else:
                print(f"DeepSeek API error (attempt {attempt+1}): {response.status_code}")
                time.sleep(retry_delay)
        except Exception as e:
            print(f"Exception during DeepSeek API call (attempt {attempt+1}): {e}")
            time.sleep(retry_delay)
    
    return "ERROR: Failed to get response from DeepSeek model"

def main():
    print("Loading synthetic notes data...")
    try:
        # Read the synthetic notes file
        df = pd.read_csv(SYNTHETIC_NOTES_PATH)
        
        # Take the first 200 patients (assuming unique patient IDs)
        patient_ids = df['pat_id'].unique()[:200]
        print(f"Processing {len(patient_ids)} unique patients")
        
        results = []
        
        # Process each patient
        for patient_id in tqdm(patient_ids, desc="Processing patients"):
            # Get the patient's notes (using the most recent note for simplicity)
            patient_notes = df[df['pat_id'] == patient_id].sort_values('note_date', ascending=False)
            
            if len(patient_notes) > 0:
                patient_data = patient_notes.iloc[0]
                note_text = patient_data['note_text']
                
                # Process through both models (with delay to avoid rate limiting)
                print(f"Processing patient ID: {patient_id}")
                llama_result = query_llama(note_text)
                time.sleep(1)  # Small delay between API calls
                deepseek_result = query_deepseek(note_text)
                
                # Store results
                results.append({
                    "pat_id": patient_id,
                    "note_id": patient_data['note_id'],
                    "note_date": patient_data['note_date'],
                    "patient_name": f"{patient_data['firstname']} {patient_data['lastname']}",
                    "llama_assessment": llama_result,
                    "deepseek_assessment": deepseek_result
                })
                
                # Save intermediate results after each patient (in case of interruption)
                with open(OUTPUT_JSON_PATH, 'w') as f:
                    json.dump(results, f, indent=2)
                
                print(f"Completed patient {patient_id}, saved intermediate results")
                
            else:
                print(f"No notes found for patient ID: {patient_id}")
        
        # Final save
        with open(OUTPUT_JSON_PATH, 'w') as f:
            json.dump(results, f, indent=2)
            
        print(f"Processing complete. Results saved to {OUTPUT_JSON_PATH}")
        
    except Exception as e:
        print(f"Error processing data: {e}")

if __name__ == "__main__":
    main()
