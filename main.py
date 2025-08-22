import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

CONFLUENCE_URL = os.getenv('CONFLUENCE_URL')
USERNAME = os.getenv('USERNAME')
CONFLUENCE_API_TOKEN = os.getenv('CONFLUENCE_API_TOKEN')
CONFLUENCE_SPACE = os.getenv('CONFLUENCE_SPACE')
PAGE_TITLE = os.getenv('PAGE_TITLE')

CONTENT = '''
# What is Accord?
Accord is a framework for online multiplayer game development that provides a set of essential metagame services and takes care of all the communication to help you focus on creating the meta gameplay in your project. With Accord you can build a metagame both around existing client-server solutions, like Unreal Engine or Unity, and on your own.

# Key features
- Microservice architecture
- High performance, scalability, flexibility, pluggability
- Cloud-friendly
- Agnostic to client and server game engines
- Suitable for a wide range of games
- Easy to integrate with the WG infrastructure

# Accord: vision and goals
Our primary goal has always been to design and implement a reusable and customizable metagame development framework that is free from any vendor lock-ins and provides all the basic functionality that the teams need right after the project kickoff. Originally started as an experimental project, Accord has evolved into a technological product used in the company. Following the customer-driven strategy, we're continuously working on the users' feedback and try to tailor Accord to their needs by adding new features and providing specific tools.

# Accord links:
- Full vision: https://confluence.wargaming.net/display/ACCORD/Accord+vision
- Roadmap: https://confluence.wargaming.net/spaces/ACCORD/pages/1890813139/Roadmaps
- Release notes: https://confluence.wargaming.net/display/ACCORD/Release+notes

# Resources
- Project docs: https://confluence.wargaming.net/display/ACCORD/Project
- Technical docs: https://confluence.wargaming.net/display/ACCORD/Documentation
- Customer docs: https://confluence.wargaming.net/display/ACCORD/Customers
- Docs website: https://accord.wargaming.net/
- Gitlab: https://gitlab.rnd.wargaming.net/accord

# Why Accord?
Presentation: https://confluence.wargaming.net/plugins/servlet/pptslide?attachment=Accord_overview.pdf&attachmentId=1970763689&attachmentVer=1&pageId=807179611&slide=0

# Latest releases
- Accord 2024.1: https://confluence.wargaming.net/spaces/ACCORD/pages/2368923012/Accord+2024.1
- Accord 2023.1 https://confluence.wargaming.net/spaces/ACCORD/pages/2145377240/Accord+2023.1
- Accord 2022.1 https://confluence.wargaming.net/spaces/ACCORD/pages/1786671226/Accord+2022.1
- Accord 2021 (annual) https://confluence.wargaming.net/spaces/ACCORD/pages/1692647653/Accord+2021+annual
- Accord 2021.3 https://confluence.wargaming.net/spaces/ACCORD/pages/1638215816/Accord+2021.3
- Accord 2021.2 https://confluence.wargaming.net/spaces/ACCORD/pages/1538682170/Accord+2021.2
- Accord 2021.1 https://confluence.wargaming.net/spaces/ACCORD/pages/1443605862/Accord+2021.1
- Accord 2020 (annual) https://confluence.wargaming.net/spaces/ACCORD/pages/1443606159/Accord+2020+annual
- Accord 2020.3 https://confluence.wargaming.net/spaces/ACCORD/pages/1333006699/Accord+2020.3
- Accord 2020.2 https://confluence.wargaming.net/spaces/ACCORD/pages/1251148370/Accord+2020.2

## Quick links: 
### Project:    
- [Vision](https://confluence.wargaming.net/display/ACCORD/Accord+vision)  
- [Roadmaps](https://confluence.wargaming.net/display/ACCORD/Roadmaps)  
- [Release notes](https://confluence.wargaming.net/display/ACCORD/Release+notes)   
### Docs:    
- [What is Accord?](https://accord.wargaming.net/docs/accord-home/)
- [Technical overview](https://accord.wargaming.net/docs/accord-home/overview/)  
- [Presentation](https://accord.wargaming.net/docs/examples/presentations/#accord)  
- [Getting started](https://accord.wargaming.net/docs/getting-started/)  
- [Accord core](https://accord.wargaming.net/docs/accord-core/)   
## Customer docs:    
- [ColdWar](https://confluence.wargaming.net/display/ACCORD/ColdWar)  
- [Creative Research](https://confluence.wargaming.net/display/ACCORD/Creative+Research) 
- [Warhammer](https://confluence.wargaming.net/spaces/ACCORD/pages/2360872550/Warhammer)

# Contacts
- [Accord MS Teams channel](https://teams.microsoft.com/l/channel/19%3a6f745abaf34b4f0c88f1cff00b1239e6%40thread.skype/General?groupId=fe6f581b-c5ad-463b-b1f7-9d3897a128ee&tenantId=5f98fadd-e7df-4de5-af15-f3da802bab2a)  
- Solution Architect: Pavel Vasiliev    
- Technical/Product Lead: Igor Sadchenko    
- Project Manager: Ivan Ivashkevich
- Head of Game Technology: Viktor Masalov
'''

# Конфиг из env
MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")
BUCKET_NAME = os.environ.get("BUCKET_NAME", "test-bucket")
FILE_NAME = "main.md"

def print_args():
    print(f'=== print confluence args ===')
    print(f'CONFLUENCE_URL: {CONFLUENCE_URL}')
    print(f'USERNAME: {USERNAME}')
    print(f'CONFLUENCE_API_TOKEN: {CONFLUENCE_API_TOKEN}')
    print(f'CONFLUENCE_SPACE: {CONFLUENCE_SPACE}')
    print(f'PAGE_TITLE: {PAGE_TITLE}')
    print(f'=== print storage args ===')
    print(f'MINIO_ENDPOINT: {MINIO_ENDPOINT}')
    print(f'MINIO_ACCESS_KEY: {MINIO_ACCESS_KEY}')
    print(f'MINIO_SECRET_KEY: {MINIO_SECRET_KEY}')
    print(f'BUCKET_NAME: {BUCKET_NAME}')
    print(f'===')

def main():
    print_args()

    s3 = boto3.resource(
        's3',
        endpoint_url=f"http://{MINIO_ENDPOINT}",
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY
    )

    try:
        s3.meta.client.head_bucket(Bucket=BUCKET_NAME)
    except ClientError:
        s3.create_bucket(Bucket=BUCKET_NAME)

    try:
        s3.Object(BUCKET_NAME, FILE_NAME).put(Body=CONTENT)
        print(f"File {FILE_NAME} successfully uploaded to bucket {BUCKET_NAME}")
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print("Error uploading file:", e)

if __name__ == "__main__":
    main()

