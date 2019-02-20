### ---------------------------------------------------------------------------
### --- Introduction to AWS Simple Cloud Storage Service (S3)
### ---------------------------------------------------------------------------

# Prerequisites:
# - Installation of `boto3`
# - Creating and adding AWS credentials to `.aws/credentials` file
# - Creating and adding AWS region for computing resources in `.aws/config` file

import boto3
import joblib
import pandas as pd

# Documentation: https://s3fs.readthedocs.io/en/latest/?badge=latest
# Note: s3fs is a wrapper for boto3
import s3fs 

### ---------------------------------------------------------------------------
### --- Part 1: Connect to S3 Bucket on AWS
### ---------------------------------------------------------------------------

# Approach 1: 
s3 = boto3.resource('s3')

# Approach 2:
# - anon=False: use AWS credentials to connect to file system, not as an anonymous user
s3_fs = s3fs.S3FileSystem(anon=False)


# View list of all buckets available on AWS. Note: These are mine -- yours will differ:
for bucket in s3.buckets.all():
    print(bucket.name)


# View list of objects in given bucket:
for file in s3.Bucket('stats404-project').objects.all():
    print(file.key)

### ---------------------------------------------------------------------------
### --- Part 2: Upload CSV File to S3 Bucket
### ---------------------------------------------------------------------------

# --- Step 1: Create a data set to upload -- or use one for your project:
file_name = "https://s3.amazonaws.com/h2o-airlines-unpacked/year1987.csv"
df = pd.read_csv(filepath_or_buffer=file_name,
                 encoding='latin-1',
                 nrows=1000
                )

# --- Step 2: Specify name of bucket to upload to:
bucket_name = "stats404-project"

# --- Step 3: Specify name of file to be created on s3, to store this CSV:
key_name = "airlines_data_1987_1000rows.csv"

# --- Step 4: Upload file to bucket and file name specified: 
with s3_fs.open(f"{bucket_name}/{key_name}","w") as file:
    df.to_csv(file)

# --- Step 5: Check that file got uploaded:
for file in s3.Bucket('stats404-project').objects.all():
    print(file.key)

### ---------------------------------------------------------------------------
### --- Part 3: Upload Model Object to S3 Bucket
### ---------------------------------------------------------------------------

# --- Step 1: Load a previously estimated model object in workspace:
rf_dict = joblib.load("../Class4/rf.joblib") 

# --- Step 2: Keep bucket the same

# --- Step 3: Specify name of file to be created on s3, to store this model object:
key_name = "rf_Fashion_MNIST_500_trees.joblib"

# --- Step 4: Upload file to bucket and file name specified:
with s3_fs.open(f"{bucket_name}/{key_name}","wb") as file:
    joblib.dump(rf_dict[500], file)

# --- Step 5: Check that file got uploaded:
for file in s3.Bucket('stats404-project').objects.all():
    print(file.key)
