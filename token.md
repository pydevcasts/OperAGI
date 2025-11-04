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


	
web	
client_id	"884729939726-6drgqf3bmpjokppkh92l6to4bjksg9q6.apps.googleusercontent.com"
project_id	"operagi-476808"
auth_uri	"https://accounts.google.com/o/oauth2/auth"
token_uri	"https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url	"https://www.googleapis.com/oauth2/v1/certs"
client_secret	"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"
redirect_uris	
0	"http://localhost:3000/api/v1/auth/google/callback/"
1	"http://localhost:8000/accounts/google/login/callback/"
2	"http://127.0.0.1:8000/accounts/google/login/callback/"
3	"http://localhost:8000/api/v1/auth/google/callback/"
4	"https://localhost:8000/api/v1/auth/google/callback/"
5	"http://127.0.0.1:8000/api/v1/auth/google/"
6	"http://127.0.0.1:8000/api/v1/auth/google/callback/"
7	"https://127.0.0.1:8000/api/v1/auth/google/callback/"
javascript_origins	
0	"https://127.0.0.1:3000"
1	"https://localhost:3000"
2	"http://127.0.0.1:3000"
3	"http://localhost:3000"







print("""
curl -X POST \\
  -H "Content-Type: application/json" \\
  -d '{
    "grant_type": "convert_token",
    "client_id": "884729939726-6drgqf3bmpjokppkh92l6to4bjksg9q6.apps.googleusercontent.com",
    "backend": "google-oauth2",
    "token": "ya29.a0ATi6K2tl5sAC3nncV7a5bWpNiWmpHcmtNgQdUdH-zNxTTCqRzxqkcBt3x6dqIVsCBcOqZbnxf5J_H3cIFeMhk49u3n98XIs94tlHcWjEgfm1gYwgdOXFiVrXK2iyAdgUumI37I6bNZnKf3kQjZNfZZRi00fyZquCxsLXF5sOdkNo_5l_c2pLe-CjxLvLUM7TADN0eo8aCgYKAQsSARcSFQHGX2MiFTQG2T_qmBXDfzavj8i7mA0206",
    "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg4NDg5MjEyMmUyOTM5ZmQxZjMxMzc1YjJiMzYzZWM4MTU3MjNiYmIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTMyMDM3OTA1Mzg3Mzg3NDM4MTciLCJlbWFpbCI6InB5ZGV2Y2FzdHNAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJDRVc2clp4a2tGUFFSa05JLVJyMmFnIiwibmFtZSI6InB5dGhvbiBjYXN0cyIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NLcXR2RklLUTU3R1Q5VWdjaGVjaE5uOVZmeE5GYmZ4ci1sNXVveUw5VE5rdGdMLWJZPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6InB5dGhvbiIsImZhbWlseV9uYW1lIjoiY2FzdHMiLCJpYXQiOjE3NjE5MTk0NTQsImV4cCI6MTc2MTkyMzA1NH0.ef4Y5CqW5PHNLmolI7ZP1_Bs-uUvjLayflm2mrDfiNkiUeN8vbpUkl94RbgcE9VlR58rhFBLk2wVU8a_aqBoswjhfstKGJWW1GlHcTktmIdQVV5UL8z54sCsJUwflicaBgpjGZaI7j95b2YC3MztvG5WIy1ddJ9zmKplpSfIB5I19QlYqRAxyf6v6ZkCK_XpQRFXyvJTpG1VJ5wMSxz4i4i4znrrUjEEGPcmW71ZWd7gXMpcKd3FIr1zkgK618p08aw9DjCUl96MCibBIujAidPCHiYrQ2muTxNnqXhPUZCRTfa1gDKADBKqjBs7qfn-raZp64mtO2N64h0Zoj77TQ" \\
  "http://127.0.0.1:8000/auth/convert-token/"
""")











Request URI: 
https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=https://developers.google.com/oauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=https://www.googleapis.com/auth/userinfo.email+https://www.googleapis.com/auth/userinfo.profile&access_type=offline
 











curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/user/auth/google/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg4NDg5MjEyMmUyOTM5ZmQxZjMxMzc1YjJiMzYzZWM4MTU3MjNiYmIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDQ2MTMxNzM5MjAyNzM5NjIwMzEiLCJlbWFpbCI6InNtYXJ0cHlkZXZAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJfOVNXeWpLS19pZkdjX1I1VmVEanBRIiwibmFtZSI6InNtYXJ0cHlkZXYiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jTGYxZHR6UUZ3b2U4UmVmUXN5aFlEODhjZ0FqY0NHMEJ4VTEwWnU5bTlMWEVyLThKRT1zOTYtYyIsImdpdmVuX25hbWUiOiJzbWFydHB5ZGV2IiwiaWF0IjoxNzYyMDM1Nzk5LCJleHAiOjE3NjIwMzkzOTl9.mMi-QlfELEI-PO_7HQWwDNNyfRGQh4DTzgZXUonHqjzBAl7WtGcTrqrrnXzgh0PMfiqLYX_-dDZv5c-vpMb3pdzB4rWVuUGECNqAkDo_c7gBFIOped3Ch-BB2Kjpl9IzphQSyOco2UwnQJqqq2m7VvTz3MsgE25bEsAOlW9rQNu53dNUeczUiFqujWndo8XmECuBOf0ElOMQySdoIqI_CEHLo_JY__YWTfGFmSC7SGzfDnhZuWc9-iNXeWtp4CAvgC3rvDkmOAhk6XmVFyySKJR2xtkpT6hTWymmMhh0hJvLYWvjq9Hnm7ogttqOB6QVzSTlVbUmSCCkYnNsN0Z7JA"
}'




     
https://developers.google.com/oauthplayground/