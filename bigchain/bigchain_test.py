from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

bdb = BigchainDB(
    'https://test.bigchaindb.com',
    headers={'app_id': 'd5596f54',
             'app_key': '6f108c571fcb25c4d34056bede9d246f'})
alice = generate_keypair()
tx = bdb.transactions.prepare(
    operation='CREATE',
    signers=alice.public_key,
    asset={'data': {'message': 'Hello'}})
signed_tx = bdb.transactions.fulfill(
    tx,
    private_keys=alice.private_key)
print(bdb.transactions.send(signed_tx))