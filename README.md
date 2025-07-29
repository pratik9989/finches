# Finches Practical task(Prati)

## Setup

### Using GitHub
1. If you have zip file, Extract it and follow next step.If you wynt to use github. Clone the repository and follow next steps.  
2. Create a virtual environment and 
activate it:  
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
4. Run the server:
    ```bash
    uvicorn app:app --reload

## Usage

### Using swagger
 #### Open http://127.0.0.1:8000/docs and check all APIS

### Using Curl
### POST an observation (valid data)
```bash
curl -X POST "http://127.0.0.1:8000/observation" -H "Content-Type: application/json" -d '{
  "observation_id": "obs123",
  "user_id": "user456",
  "text_observation": "A sample observation text.",
  "photo_url": "http://example.com/photo.jpg",
  "location": {
    "latitude": 12.3456,
    "longitude": 65.4321
  }
}'
```
### POST an observation (invalid photo_url - triggers validation error)
```bash
curl -X POST "http://127.0.0.1:8000/observation" -H "Content-Type: application/json" -d '{
  "observation_id": "obs124",
  "user_id": "user456",
  "text_observation": "sample text",
  "photo_url": "badurl",
  "location": {
    "latitude": 12.3456,
    "longitude": 65.4321
  }
}'
```
### GET reports
```bash
curl http://127.0.0.1:8000/reports
```

## Quick Thoughts

- **Cloud Storage Interaction:**  
  In production, the backend would verify cloud storage URLs by validating signed URLs(We already discussed in meeting) or using server-side uploads to ensure security and data integrity.

- **LLM Overload:**  
  To handle LLM rate limits, implement request queuing, exponential backoff retries, and caching of frequent responses.

- **Authentication:**  
  For the authentication, We can use JWT token and encrypt sensitive data using AES encryption.

- **Containerization/Deployment:**  
  Containerize with Docker by creating a Dockerfile and deploy to cloud platforms like GCP Cloud Run with appropriate environment configurations and load balancing.
