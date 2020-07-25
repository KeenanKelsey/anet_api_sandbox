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
    profile.merchantCustomerId = fake.ean8()
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

# if(os.path.basename(__file__) == os.path.basename(sys.argv[0])):
#     create_customer_profile_from_transaction(constants.transactionId)

 
def get_customer_profile(customerProfileId):
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = constants.apiLoginId
    merchantAuth.transactionKey = constants.transactionKey
 
    getCustomerProfile = apicontractsv1.getCustomerProfileRequest()
    getCustomerProfile.merchantAuthentication = merchantAuth
    getCustomerProfile.customerProfileId = customerProfileId
    controller = getCustomerProfileController(getCustomerProfile)
    controller.execute()
 
    response = controller.getresponse()
 
    if (response.messages.resultCode=="Ok"):
        print("Successfully retrieved a customer with profile id %s and customer id %s" % (getCustomerProfile.customerProfileId, response.profile.merchantCustomerId))
        if hasattr(response, 'profile') == True:
            if hasattr(response.profile, 'paymentProfiles') == True:
                for paymentProfile in response.profile.paymentProfiles:
                     print ("paymentProfile in get_customerprofile is:" %paymentProfile)
                     print ("Payment Profile ID %s" % str(paymentProfile.customerPaymentProfileId))
            if hasattr(response.profile, 'shipToList') == True:
                for ship in response.profile.shipToList:
                    print("Shipping Details:")
                    print("First Name %s" % ship.firstName)
                    print("Last Name %s" % ship.lastName)
                    print ("Address %s" % ship.address)
                    print ("Customer Address ID %s" % ship.customerAddressId)
        if hasattr(response, 'subscriptionIds') == True:
            if hasattr(response.subscriptionIds, 'subscriptionId') == True:
                print ("list of subscriptionid:")
                for subscriptionid in (response.subscriptionIds.subscriptionId):
                    print (subscriptionid)
    else:
        print ("response code: %s" % response.messages.resultCode)
        print ("Failed to get customer profile information with id %s" % getCustomerProfile.customerProfileId)
 
    return response
 
if(os.path.basename(__file__) == os.path.basename(sys.argv[0])):
    get_customer_profile(constants.customerProfileId)