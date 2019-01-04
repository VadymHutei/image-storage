import os

p = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'storage')
p = os.path.join('/mnt/d/dev/image-storage/app/storage', 'd572a515b8922e037fba839eb2463289')
print(p)
print(os.path.exists(p))