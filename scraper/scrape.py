import requests

list_handle = ["@aprilgrierson2"]
for handle in list_handle:
    print(handle, flush=True)
    response = requests.get(f"https://www.google.com/")
    content = response.content
    print("content", flush=True)
    print(content, flush=True)
    response = requests.get(f"https://www.tiktok.com/{handle}")
    content = response.content
    print("content", flush=True)
    with open("temp.html", "wb") as file:
        file.write(content)
    print(content)

# https://v16-webapp.tiktok.com/ef05918aad2047ae4966f390e75a293a/63cf73a2/video/tos/useast2a/tos-useast2a-pve-0068/cb76b09fea2f4f6784578a3996fa4821