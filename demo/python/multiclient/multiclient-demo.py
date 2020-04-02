import securexgboost as xgb
import os

HOME_DIR = os.path.abspath('') + "/../../../"
crypto = xgb.CryptoUtils()

# setting global variable user this will be changed by switch_user() function
current_user = None

# Generate two keys to be used for encryption.

KEY_FILE_1 = "key1.txt"
KEY_FILE_2 = "key2.txt"

# Generate a key you will be using for encryption
crypto.generate_client_key(KEY_FILE_1)
crypto.generate_client_key(KEY_FILE_2)

# Use the key generated above to encrypt our data.
training_data = HOME_DIR + "demo/data/agaricus.txt.train"
enc_training_data = "train.enc"

# Encrypt training data using user 1's key
crypto.encrypt_file(training_data, enc_training_data, KEY_FILE_1)

test_data = HOME_DIR + "demo/data/agaricus.txt.test"
enc_test_data = "test.enc"

# Encrypt test data
crypto.encrypt_file(test_data, enc_test_data, KEY_FILE_1)

# Create an enclave
enclave = xgb.Enclave(HOME_DIR + "build/enclave/xgboost_enclave.signed", log_verbosity = 3)

# Client gets a `report` from the server generated by the enclave
enclave.get_remote_report_with_pubkey()

# Client parses the report, and extracts a public key generated by the enclave
enclave_pem_key, enclave_key_size, remote_report, remote_report_size = enclave.get_report_attrs()

sym_key_1 = None
with open(KEY_FILE_1, "rb") as keyfile:
    sym_key_1 = keyfile.read()

# Encrypt user 1's symmetric key using the enclave's public key
enc_sym_key, enc_sym_key_size = crypto.encrypt_data_with_pk(sym_key_1, len(sym_key_1),
                                                            enclave_pem_key, enclave_key_size)

user_name = "user1"
sig, sig_size = crypto.sign_data("userkeys/private_user_1.pem", enc_sym_key, enc_sym_key_size)

with open("{0}.crt".format(user_name), "r") as cert_file:
    user_certificate = cert_file.read()
# adding the client 1's key with user 1's certificate
crypto.add_client_key_with_certificate(user_certificate,
                                       enc_sym_key, enc_sym_key_size,
                                       sig, sig_size)

## user 2
sym_key_2 = None

with open(KEY_FILE_2, "rb") as keyfile:
    sym_key_2 = keyfile.read()

# Encrypt user 2's symmetric key using the enclave's public key
enc_sym_key, enc_sym_key_size = crypto.encrypt_data_with_pk(sym_key_2, len(sym_key_2),
                                                            enclave_pem_key, enclave_key_size)

user_name = "user2"
sig, sig_size = crypto.sign_data("userkeys/private_user_2.pem", enc_sym_key, enc_sym_key_size)

with open("{0}.crt".format(user_name), "r") as cert_file:
    user_certificate = cert_file.read()

crypto.add_client_key_with_certificate(user_certificate,
                                       enc_sym_key, enc_sym_key_size,
                                       sig, sig_size)

# Load training data encrypted with user 1's key
switch_user("user1")
dtrain = xgb.DMatrix(os.getcwd() + "/" + enc_training_data, encrypted=True)

# Load test data
dtest = xgb.DMatrix(os.getcwd() + "/" + enc_test_data, encrypted=True)

# Set parameters
params = {
        "tree_method": "hist",
        "n_gpus": "0",
        "objective": "binary:logistic",
        "min_child_weight": "1",
        "gamma": "0.1",
        "max_depth": "3",
        "verbosity": "1"
}

# Train
num_rounds = 10
booster = xgb.train(params, dtrain, num_rounds, evals=[(dtrain, "train"), (dtest, "test")])

# Get Encrypted Predictions Using User 1's test data
enc_preds, num_preds = booster.predict(dtest)

# Decrypt Predictions
preds = crypto.decrypt_predictions(sym_key_1, enc_preds, num_preds)
print("user 1's prediction:")
print(preds)

print("user 2's turn")
switch_user("user2")
test_data = HOME_DIR + "demo/data/agaricus.txt.test"
enc_test_data = "test2.enc"

# Encrypt test data with user 2's key
crypto.encrypt_file(test_data, enc_test_data, KEY_FILE_2)
dtest = xgb.DMatrix(os.getcwd() + "/" + enc_test_data, encrypted=True)
enc_preds, num_preds = booster.predict(dtest, username="user2")

preds = crypto.decrypt_predictions(sym_key_2, enc_preds, num_preds)
print("user 2's prediction:")
print(preds)

print("Both users' predictions should be the same! It's the same model predicting on the same test data just encrypted differently")