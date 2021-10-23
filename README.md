
## Features

- Writes a list of log entries from OSB/OSS to the MYSQL Activity Logger Database
- Writes Redactions data to MYSQL Redactions Database

## Local Usage

Clone the repo into your workspace.

```sh
./debug.sh ${MYSQL_HOST} ${MYSQL_USER} ${MYSQL_PASSWORD}
```

Upon successful image build, you can do a POST call to:
```sh
http://localhost:9000/2015-03-31/functions/function/invocations
BODY:
{
    "Records": [
        {
            "messageId": "b2b9af0d-2941-4337-9b93-9245890111c8",
            "receiptHandle": "AQEB60oKBqwRORqjkfarfWTcrxM8/TnTDC/A5VmbaSegAFdm/WL6Nsb72BDed3CG90zLfA7VZYq4hdyo1/grAXQ3i/Auz/FMfYziOdbcDJK7gNvBhumAwMUdRmo1TcH7GGv14hroIg1SBCEkIJMr9WeEZcpZy7tdCxoypf27t2bZArlu1YA/OiRKaFwUYscjCchxjR2grGxE7Tv37ys8MF8Rm29erNlt5qGCeHzSlFkIpljsciHosyEk7F/s3VLJCzzPVjhtZvRXDvevxK+0Ja1+ufteuadeWWUiXwbiDtzeFSGVhyobYUL/+Mjq5Ngkl416zltNTgw3+jT3rwLGbQafbtW3EsTeDV7b9ZwS4vCLjvpeiiXnSAP37MlL23dMHGTO0kr5cNwUqrgcocgYELnNlw==",
            "body": "[{\"user_request_id\":null,\"session_id\":\"a8778f68-4107-46ff-a69f-cb8de69e51c9\",\"parent_uid\":null,\"type\":\"request\",\"data\":[{\"Municipality\":{\"Name\":\"Burlington\",\"StateProvince\":{\"Code\":\"ON\"}},\"PostalCode\":{\"Value\":\"L7M3M7\"},\"Line\":\"3202 Tania Cres\"}],\"data_format\":\"json\",\"activity_code\":\"osb\",\"product_code\":\"OptaAddress\",\"machine_name\":\"a5cdab172dec\",\"billable\":true,\"result_code\":null,\"requestor_id\":null,\"brokerage\":null,\"user_profile\":null,\"remote_ip\":\"127.0.0.1\"},{\"user_request_id\":null,\"session_id\":\"a8778f68-4107-46ff-a69f-cb8de69e51c9\",\"parent_uid\":null,\"type\":\"response\",\"data\":{\"Client\":\"10.33.68.174\",\"ElapsedMilliseconds\":48,\"EndTime\":\"2021-08-09T17:37:41.513821\",\"Failed\":0,\"Name\":\"OptaAddress\",\"Results\":[{\"ElapsedMilliseconds\":48,\"EndTime\":\"2021-08-09T17:37:41.513939\",\"Result\":[{\"AddressTypeCode\":\"STANDARD\",\"ConfidenceScore\":100,\"ID\":\"0d108195c0320800\",\"Municipality\":{\"Name\":\"BURLINGTON\",\"StateProvince\":{\"Code\":\"ON\"}},\"PostalCode\":{\"Value\":\"L7M3M7\"},\"Street\":{\"Name\":\"TANIA\",\"StreetType\":{\"Abbreviation\":{\"en\":\"CRES\"},\"Value\":{\"en\":\"CRES\"}}},\"StreetNumber\":3202,\"StreetNumberInRange\":true}],\"StartTime\":\"2021-08-09T17:37:41.465939\",\"Success\":true}],\"Server\":\"opta-address-5758976bdf-pxggv\",\"SessionId\":\"aefaa6b9-a22b-4ac2-8e67-ad7967175882\",\"StartTime\":\"2021-08-09T17:37:41.465821\",\"StatusCode\":200,\"Succeeded\":1,\"TimedOut\":0,\"Version\":\"1.0\"},\"data_format\":\"json\",\"activity_code\":\"osb\",\"product_code\":\"OptaAddress\",\"machine_name\":\"a5cdab172dec\",\"billable\":true,\"result_code\":null,\"requestor_id\":null,\"brokerage\":null,\"user_profile\":null,\"remote_ip\":\"127.0.0.1\",\"duration_ms\":575},{\"user_request_id\":null,\"session_id\":\"a8778f68-4107-46ff-a69f-cb8de69e51c9\",\"parent_uid\":null,\"type\":\"request\",\"data\":[{\"Address\":{\"ID\":\"0d108195c0320800\",\"Municipality\":{\"StateProvince\":{\"Code\":\"ON\"},\"Name\":\"BURLINGTON\"},\"PostalCode\":{\"Value\":\"L7M3M7\"},\"AddressTypeCode\":\"STANDARD\",\"StreetNumber\":3202,\"ConfidenceScore\":100,\"Street\":{\"Name\":\"TANIA\",\"StreetType\":{\"Value\":{\"en\":\"CRES\"},\"Abbreviation\":{\"en\":\"CRES\"}}},\"StreetNumberInRange\":true},\"Policy\":{\"PolicyNumber\":2002,\"Insured\":{\"Name\":{\"FirstName\":\"Bruce\",\"Surname\":\"Wayne\"},\"DateOfBirth\":\"1980-05-27\",\"Consents\":[{\"ConsentReceived\":true,\"ConsentTypeCode\":\"Insurance\",\"ConsentDate\":\"2020-09-17T20:47:01\"}]},\"EffectiveDate\":\"2020-11-01T06:52:35\",\"PolicyAddress\":{\"ID\":\"0d108195c0320800\",\"Municipality\":{\"StateProvince\":{\"Code\":\"ON\"},\"Name\":\"BURLINGTON\"},\"PostalCode\":{\"Value\":\"L7M3M7\"},\"AddressTypeCode\":\"STANDARD\",\"StreetNumber\":3202,\"ConfidenceScore\":100,\"Street\":{\"Name\":\"TANIA\",\"StreetType\":{\"Value\":{\"en\":\"CRES\"},\"Abbreviation\":{\"en\":\"CRES\"}}},\"StreetNumberInRange\":true},\"MailingAddress\":{\"ID\":\"0d10dfb40003fc000000006cc1b8\",\"AddressTypeCode\":\"STANDARD\"},\"OwnershipTypeCode\":\"Owned\",\"OccupancyTypeCode\":\"Primary\",\"PackageTypeCode\":\"Homeowner\",\"TotalInsuredValue\":222000,\"CoverageAmounts\":{\"BuildingAmount\":20000,\"ContentsAmount\":20000,\"DetachedPrivateStructuresAmount\":22201,\"AdditionalLivingExpensesAmount\":22201},\"Limit\":20000000,\"Deductible\":222011,\"ContactInformation\":{\"Name\":\"Bruce\",\"Email\":\"bruce.wayne@wayneenterprises-inc.com\",\"PhoneNumbers\":[{\"Number\":\"+1-418-5550103\",\"NumberTypeCode\":\"Home\"}],\"ContactTypeCode\":\"PolicyHolder\",\"PreferredContactMethodCode\":\"Email\"}}}],\"data_format\":\"json\",\"activity_code\":\"osb\",\"product_code\":\"InsuranceReferralV2\",\"machine_name\":\"a5cdab172dec\",\"billable\":true,\"result_code\":null,\"requestor_id\":null,\"brokerage\":null,\"user_profile\":null,\"remote_ip\":\"127.0.0.1\"}]",
            "attributes": {
                "ApproximateReceiveCount": "1",
                "SentTimestamp": "1613419808433",
                "SenderId": "AIDA5RYNHW2GNXZ6WWEGB",
                "ApproximateFirstReceiveTimestamp": "1613419808434"
            },
            "messageAttributes": {},
            "md5OfBody": "52588f12fdec4dd4f8485a7a865afaed",
            "eventSource": "aws:sqs",
            "eventSourceARN": "arn:aws:sqs:ca-central-1:931498800780:OptaAddressQueue",
            "awsRegion": "ca-central-1"
        }
    ]
}
```

## Deployment to AWS
For deploying changes from your local...

```sh
./deploy.sh ${image_name} ${aws_account_id} ${my_sql_host} ${my_sql_redactions_host} ${my_sql_redactions_pwd}
## You can add this line to the end of the deploy.sh script to update the code or replace the image_uri to the one generated from the deploy script
aws lambda update-function-code --function-name ${FUNCTION_NAME} --image-uri $IMAGE_URI --publish
```
