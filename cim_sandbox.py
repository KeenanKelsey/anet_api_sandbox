import os, sys
import importlib
from faker import Faker
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *

fake = Faker()
constants = importlib.import_module('constants')

def create_customer_profile_from_transaction(transactionId):
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = constants.apiLoginId
    merchantAuth.transactionKey = constants.transactionKey

    profile = apicontractsv1.customerProfileBaseType()
    profile.merchantCustomerId = "12332"
    profile.description = fake.bs()
    profile.email = fake.email()

    createCustomerProfileFromTransaction = apicontractsv1.createCustomerProfileFromTransactionRequest()
    createCustomerProfileFromTransaction.merchantAuthentication = merchantAuth
    createCustomerProfileFromTransaction.transId = transactionId
    #You can either specify the customer information in form of customerProfileBaseType object
    createCustomerProfileFromTransaction.customer = profile
    #  OR
    # You can just provide the customer Profile ID
    # createCustomerProfileFromTransaction.customerProfileId = "123343"

    controller = createCustomerProfileFromTransactionController(createCustomerProfileFromTransaction)
    controller.execute()

    response = controller.getresponse()

    if (response.messages.resultCode=="Ok"):
        print("Successfully created a customer profile with id: %s from transaction id: %s" % (response.customerProfileId, createCustomerProfileFromTransaction.transId))
    else:
        print("Failed to create customer payment profile from transaction %s" % response.messages.message[0]['text'].text)

    return response

if(os.path.basename(__file__) == os.path.basename(sys.argv[0])):
    create_customer_profile_from_transaction(constants.transactionId)