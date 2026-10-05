import os

print("Contents of Blogger/:")
if os.path.exists("Blogger"):
    for f in os.listdir("Blogger")[:20]:
        fp = os.path.join("Blogger", f)
        if os.path.isfile(fp):
            sz = os.path.getsize(fp) / 1024 / 1024
            print(f"  {f}: {sz:.2f} MB")
        else:
            print(f"  [DIR] {f}")
else:
    print("  Does not exist")
