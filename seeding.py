import uuid
import os
import sys

def generate_uuid(name1, id1, name2, id2):
    """Generate a UUID based on the names and IDs of two students."""
    seed_str = name1 + id1 + name2 + id2
    seed_bytes = seed_str.encode('utf-8')
    seed_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, seed_bytes)
    return seed_uuid

def save_uuid_to_file(uuid, filename):
    """Save the UUID to a file with read-only permissions."""
    with open(filename, 'w') as f:
        f.write(str(uuid))
    # Set file to read-only
    os.chmod(filename, 0o444)

def main():
    if len(sys.argv) != 5:
        print("Usage: python seeding.py <Last Name 1> <ID1> <Last Name 2> <ID2>")
        sys.exit(1)
    name1, id1, name2, id2 = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    seed_uuid = generate_uuid(name1, id1, name2, id2)
    save_uuid_to_file(seed_uuid, "seed_uuid.txt")
    print("Seed UUID generated and saved successfully.")

if __name__ == "__main__":
    main()
