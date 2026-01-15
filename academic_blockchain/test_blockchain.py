from blockchain import Blockchain

bc = Blockchain()

bc.create_block(
    "MHS-001",
    "Budi",
    "Kriptografi",
    "UTS A",
    5,
    "Dr. Lina"
)

bc.create_block(
    "MHS-001",
    "Budi",
    "Kriptografi",
    "UAS A",
    5,
    "Dr. Lina"
)

for block in bc.chain:
    print(block)

print("Blockchain valid?", bc.is_chain_valid())
