#!/usr/bin/env python3
"""
Main file to test deletion-resilient hypermedia pagination
"""

Server = __import__('3-hypermedia_del_pagination').Server

server = Server()

# Force the index map to be built
server.indexed_dataset()

# Test: requesting an invalid index (too high)
try:
    server.get_hyper_index(300000, 100)
except AssertionError:
    print("✅ AssertionError raised when out of range")        

index = 3
page_size = 2

print("\n🟢 Initial indexed dataset size:", len(server._Server__indexed_dataset))

# 1. Request page starting at index 3
res = server.get_hyper_index(index, page_size)
print("\n📄 First request:")
print(res)

# 2. Request next page from next_index
next_index = res.get('next_index')
res2 = server.get_hyper_index(next_index, page_size)
print("\n📄 Second request (next page):")
print(res2)

# 3. Delete the first item retrieved in original page (simulate deletion)
del server._Server__indexed_dataset[res['index']]
print("\n❌ Deleted index", res['index'])

print("🟡 Updated indexed dataset size:", len(server._Server__indexed_dataset))

# 4. Re-request original page index (should now return different first item)
res3 = server.get_hyper_index(index, page_size)
print("\n📄 Re-request after deletion (same index):")
print(res3)

# 5. Re-request next_index page (should return same as res2 if no deletions affected it)
res4 = server.get_hyper_index(next_index, page_size)
print("\n📄 Re-request of next_index page (should be same as before):")
print(res4)

