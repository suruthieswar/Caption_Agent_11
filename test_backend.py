import requests
import io

# Create a dummy image (1x1 pixel)
dummy_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'

files = {'file': ('test.png', dummy_image, 'image/png')}
data = {'vibe': 'Professional & Clean'}

print("Sending request to backend...")
try:
    response = requests.post('http://localhost:8000/generate', files=files, data=data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print("Error:", response.text)
except Exception as e:
    print(f"Failed to connect: {e}")
