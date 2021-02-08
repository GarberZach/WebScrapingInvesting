import boto3
import os
import datetime
import pandas
import csv

from io import StringIO

class AWS_handler():

    def __init__(self):
        pass
    
    def fetch_data(self):
        bucket = 
        aws_key = 
        aws_sKey = 

        s3 = boto3.client('s3', aws_access_key_id = aws_key, aws_secret_access_key = aws_sKey)
        
        list=s3.list_objects(Bucket=bucket)['Contents']
        
        print('list of all files in s3: ')
        for object_in_bucket in list:
            print(object_in_bucket)

        
        object_in_s3 = input("Enter the \"Key\" of object to download: ")

        path = os.path.join(os.getcwd(), "WebScrapingInvesting\\data\\" + object_in_s3)
        
        with open(path, 'a'):
            print('file created in data folder')

        
        
        s3.download_file(bucket, object_in_s3, path)

    def put_data(self, data_frame, ticker):
        bucket = 
        aws_key = 
        aws_sKey = 

        
        path = os.path.join(os.getcwd(), "IB-BAcktrader\\data\\" + ticker + ".csv")
        data_frame.to_csv(path_or_buf= path)
        
        s3 = boto3.resource('s3', aws_access_key_id = aws_key, aws_secret_access_key = aws_sKey)
        
        s3.meta.client.upload_file(path,bucket, ticker + '.csv')