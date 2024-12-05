import json
from libs.auth import authenticate

if __name__ == "__main__":

    try:
        print("START")
        data = authenticate(
            {
                "type": "TOKEN",
                "authorizationToken": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlRkYVFKMzk1OHZZQkN5cVVJQVBIOSJ9.eyJpc3MiOiJodHRwczovL2Rldi1xeTVnaGJ6YTdrend4cHVjLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJKRnRlemd0Wnk2d25TTGhlczVGQmtQR3Q0YWZiOUIxbEBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly91bWFhZWFvMzBoLmV4ZWN1dGUtYXBpLmFwLW5vcnRoZWFzdC0xLmFtYXpvbmF3cy5jb20vIiwiaWF0IjoxNzMwMjAyMjgxLCJleHAiOjE3MzAyODg2ODEsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsImF6cCI6IkpGdGV6Z3RaeTZ3blNMaGVzNUZCa1BHdDRhZmI5QjFsIn0.byyqbKiK10W5384hPNWTqG0z7doQU1lwQXH9nxuxDdVMXqm93Bs3uuzS7W-KBDPHaTo8Oafazp2HpDQxyWDNRvk0Y0dhxyvSc80TO9nwfhNP9Oj0RX9ZiVMTODX8z6fNELXkmxKUDp4Ksrt3A-BsFn9xSGS5o7HU2gQmBgsRSJIF07i2p6zlQ3xBHb0dSDkJQcHwMi9p7QuHgFkncpSoztuiMcGDcDcIvXP6uw8dzUmZAZGWaMB9xu0mIrmLifbDdzTgm8DNC-8dQV57vbZxG7mq3jEIri5F_fyAnFMjCQRgOpU-7TIqNAzNfmrZMD1JIMduVsnu7P_pAhiijszSBQ",
                "methodArn": "",
            }
        )

        print(json.dumps(data))

        print("END")

    except Exception as e:
        print(f"Unauthorized {str(e)}")
