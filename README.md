# Automatic EBS Snapshot and Cleanup Using AWS Lambda and Boto3

## **📌 Project Overview**
This project automates the **backup and cleanup** of AWS **EBS (Elastic Block Store) volumes** using **AWS Lambda and Boto3**. The goal is to **create EBS snapshots automatically** and **delete old snapshots (older than 30 days)** to optimize storage costs.

This guide is written for **absolute beginners** who have no prior experience with **AWS** or **Python**.

---

## **💡 What is AWS?**
AWS (**Amazon Web Services**) is a cloud computing platform that provides various services such as storage, databases, and virtual machines. In this project, we will use AWS services to create and manage **EBS snapshots**.

### **🔹 What is an EBS Volume?**
An **EBS (Elastic Block Store) Volume** is like a hard drive for cloud-based servers (EC2 instances). It stores data persistently and can be backed up using **snapshots**.

### **🔹 What is a Snapshot?**
A **snapshot** is a backup copy of an EBS volume at a specific point in time. If something goes wrong, we can restore data from a snapshot.

### **🔹 What is AWS Lambda?**
**AWS Lambda** is a cloud function that runs code automatically without needing to manage servers.

### **🔹 What is Boto3?**
**Boto3** is a Python library that allows us to interact with AWS services using code.

---

## **📌 Step 1: Set Up an AWS Account**
1. **Sign up for AWS** at [aws.amazon.com](https://aws.amazon.com/).  
2. Go to the **AWS Console**.

---

## **📌 Step 2: Create an EBS Volume**
1. Open the **AWS Management Console**.
2. Search for **EC2** and go to the **EC2 Dashboard**.
3. Click on **Volumes** (left menu).
4. Click **Create Volume** and select:
   - **Volume Type**: `gp3` (recommended for general use).
   - **Size**: `8 GiB` (or as per requirement).
   - **Availability Zone**: Choose one where your EC2 instance is located.
   - **Encryption**: Optional but recommended.
5. Click **Create Volume** and **copy the Volume ID** (e.g., `vol-00beb917e98bb8635`).

---

## **📌 Step 3: Create an IAM Role for AWS Lambda**
1. Open **AWS IAM Console** → Click **Roles** → Click **Create Role**.
2. Choose **AWS Service** → Select **Lambda** → Click **Next**.
3. Attach the following policy:
   - `AmazonEC2FullAccess` (for simplicity).  
4. Click **Next** → Enter Role Name: `maheshEBSSnapshotRole` → Click **Create Role**.

---

## **📌 Step 4: Create an AWS Lambda Function**
1. Open **AWS Lambda Console** → Click **Create Function**.
2. Choose **Author from Scratch**.
3. **Function Name**: `maheshEBSSnapshotCleanup`.
4. **Runtime**: `Python 3.x`.
5. **Permissions**: Select **"Use an existing role"** → Choose **`maheshEBSSnapshotRole`**.
6. Click **Create Function**.

---

## **📌 Step 5: Deploy the Python Script**
### **🔹 What Does This Script Do?**
- **Creates an EBS snapshot**.
- **Deletes snapshots older than 30 days**.

### **🔹 Paste This Code in Lambda Editor:**
```python
import boto3
from datetime import datetime, timedelta

# Initialize EC2 client
ec2 = boto3.client("ec2")

# Set retention period
RETENTION_DAYS = 30

def lambda_handler(event, context):
    volume_id = "vol-00beb917e98bb8635"  # Replace with your actual Volume ID

    # Step 1: Create a new EBS Snapshot
    snapshot = ec2.create_snapshot(
        VolumeId=volume_id,
        Description=f"Automated Backup {datetime.now().strftime('%Y-%m-%d')}"
    )
    print(f"Snapshot created: {snapshot['SnapshotId']}")

    # Step 2: List and delete snapshots older than retention period
    snapshots = ec2.describe_snapshots(Filters=[{"Name": "volume-id", "Values": [volume_id]}])
    
    deletion_time = datetime.utcnow() - timedelta(days=RETENTION_DAYS)

    for snap in snapshots["Snapshots"]:
        snapshot_id = snap["SnapshotId"]
        start_time = snap["StartTime"].replace(tzinfo=None)

        if start_time < deletion_time:
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Deleted old snapshot: {snapshot_id}")
```

### **📌 Step 6: Run and Test**
1. Click **Deploy**.
2. Click **Test** → Create a new test event (`EBSBackupTest`).
3. Click **Run**.
4. **Go to EC2 Snapshots** to verify:
   - ✅ A new **snapshot is created**.
   - ✅ Old **snapshots (30+ days)** are deleted.

---

## **📌 Step 7: Automate with CloudWatch (Optional)**
1. Open **Amazon EventBridge** (CloudWatch Events).
2. Click **Rules** → **Create Rule**.
3. Set it to run **daily**:  
   ```
   cron(0 12 * * ? *)
   ```
4. Select **Lambda Function** → Choose **`maheshEBSSnapshotCleanup`**.
5. Click **Create**.

---
