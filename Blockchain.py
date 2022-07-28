from datetime import datetime
from hashlib import sha256


class Block:
    def __init__(self, transactions, previous_hash):
        self.timestamp = datetime.now()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.generate_hash()

    def print_contents(self):
        # prints block contents
        print("timestamp:", self.timestamp)
        print("transactions:", self.transactions)
        print("current hash:", self.generate_hash())
        print("previous hash:", self.previous_hash)

    def generate_hash(self):
        # hash the blocks contents
        block_header = str(self.timestamp) + str(self.transactions) + str(self.previous_hash) + str(self.nonce)
        block_hash = sha256(block_header.encode())
        return block_hash.hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.all_transactions = []
        self.genesis_block()

    def genesis_block(self):
        transactions = {}
        genesis_block = Block(transactions, "0")
        self.chain.append(genesis_block)
        return self.chain

    # print contents of blockchain
    def print_blocks(self):
        for i in range(len(self.chain)):
            current_block = self.chain[i]
            print("Block {} {}".format(i, current_block))
            current_block.print_contents()

    # add block to blockchain `chain`
    def add_block(self, transactions):
        previous_block_hash = self.chain[len(self.chain) - 1].hash
        new_block = Block(transactions, previous_block_hash)
        new_block.generate_hash()
        proof = self.proof_of_work(new_block)
        self.chain.append(new_block)
        return proof, new_block

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.generate_hash():
                print("Blockchain is not valid")
                return False
            if previous.hash != previous.generate_hash():
                print("Blockchain is not valid")
                return False
            return True

    def proof_of_work(self, block, difficulty=2):
        proof = block.generate_hash()
        while proof[:difficulty] != '0' * difficulty:
            block.nonce += 1
            proof = block.generate_hash()
        block.nonce = 0
        return proof


# Hacking
new_transactions = [{'amount': '30', 'sender': 'alice', 'receiver': 'bob'},
                    {'amount': '55', 'sender': 'bob', 'receiver': 'alice'}]

my_blockchain = Blockchain()
my_blockchain.add_block(new_transactions)
my_blockchain.print_blocks()

my_blockchain.chain[1].transactions = "fake_transactions"

my_blockchain.validate_chain()

# Proof-Of_Work

new_transactions = [{'amount': '30', 'sender': 'alice', 'receiver': 'bob'},
                    {'amount': '55', 'sender': 'bob', 'receiver': 'alice'}]

# sets the amount of leading zeros that must be found in the hash produced by the nonce
# difficulty = 2
# nonce = 0

# creating the proof
# proof = sha256((str(nonce) + str(new_transactions)).encode()).hexdigest()

# finding a proof that has 2 leading zeros
# while proof[:2] != '0' * difficulty:
# nonce += 1
# proof = sha256((str(nonce) + str(new_transactions)).encode()).hexdigest()

# printing final proof that was found
# final_proof = proof
# print(final_proof)


block_one_transactions = {"sender":"Alice", "receiver": "Bob", "amount":"50"}
block_two_transactions = {"sender": "Bob", "receiver":"Cole", "amount":"25"}
block_three_transactions = {"sender":"Alice", "receiver":"Cole", "amount":"35"}
fake_transactions = {"sender": "Bob", "receiver":"Cole, Alice", "amount":"25"}

local_blockchain = Blockchain()
# local_blockchain.print_blocks()
local_blockchain.add_block(block_one_transactions)
local_blockchain.add_block(block_two_transactions)
local_blockchain.add_block(block_three_transactions)
# local_blockchain.print_blocks()

local_blockchain.chain[2].transactions = fake_transactions
local_blockchain.validate_chain()

